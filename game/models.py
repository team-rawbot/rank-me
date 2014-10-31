import redis
from collections import defaultdict, OrderedDict
from itertools import groupby

from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import Prefetch, Q
from django.template.defaultfilters import slugify
from django.utils import timezone
from game.rating import rating

from .signals import game_played, team_ranking_changed


class TeamManager(models.Manager):
    def get_or_create_from_players(self, player_ids):
        """
        Return the team associated to the given players, creating it first if
        it doesn't exist.

        Args:
            player_ids: a tuple of user ids, or a single user id.
        """
        if not isinstance(player_ids, tuple):
            player_ids = (player_ids,)

        # We need to get only the teams that have the exact number of player
        # ids, otherwise we would also get teams that have the given players
        # plus additional ones
        team = self.annotate(c=models.Count('users')).filter(c=len(player_ids))

        # Chain filter over all player ids
        for player_id in player_ids:
            team = team.filter(users=player_id)

        if not team:
            created = True
            team = self.create()

            for player_id in player_ids:
                team.users.add(player_id)
        else:
            created = False
            team = team.get()

        return (team, created)


class Team(models.Model):
    users = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   related_name='teams')

    objects = TeamManager()

    def __unicode__(self):
        return self.get_name()

    def get_name(self):
        return u" / ".join([user.first_name.title() for user in self.users.all()])

    def get_competitions(self):
        return Competition.objects.filter(score__team=self)

    def get_games(self, competition):
        """
        Fetch the list of games played by the team, filtered by competition.
        """
        User = get_user_model()
        users_with_profile_qs = User.objects.select_related('profile')

        games = Game.objects.filter(
            Q(winner_id=self.id) | Q(loser_id=self.id)
        ).filter(competitions=competition).order_by('-date').select_related(
            'winner', 'loser'
        ).prefetch_related(
            Prefetch('winner__users', queryset=users_with_profile_qs),
            Prefetch('loser__users', queryset=users_with_profile_qs),
        )

        return games

    def get_head2head(self, competition):
        """
        Compute the amount of wins and defeats against all opponents the team
        played against. The returned value is an OrderedDict since the teams
        are ordered by their score.
        """
        head2head = {}
        fairnesses = self.get_fairness(competition)

        games = self.get_games(competition)

        for game in games:
            opponent = game.get_opponent(self)

            if opponent not in head2head:
                head2head[opponent] = {
                    'wins': 0,
                    'defeats': 0,
                    'games': [],
                    'fairness': fairnesses[opponent]['quality']
                }

            stat_to_increase = (
                'wins' if game.winner_id == self.id else 'defeats'
            )
            head2head[opponent][stat_to_increase] += 1
            head2head[opponent]['games'].append(game)

        return OrderedDict(
            sorted(
                head2head.items(),
                key=lambda t: t[0].scores.get(competition=competition).score,
                reverse=True
            )
        )

    def get_fairness(self, competition):
        """
        Compute the probability of draw against all opponents (ie. how fair is the game).
        Returns an OrderedDict of teams by score
        """
        qualities = {}

        own_score = self.get_score(competition)
        teams = competition.teams.all()

        for team in teams:
            if team == self:
                continue
            score = team.get_score(competition)
            quality = rating.quality(own_score, score)
            qualities[team] = {'score': score, 'quality': quality * 100}

        return OrderedDict(
            sorted(
                qualities.items(),
                key=lambda t: t[1]['score'].score,
                reverse=True
            )
        )


    def get_recent_stats(self, competition, count=10):
        """
        Return a dictionary with the latest ``count`` played games and the
        number of wins and defeats.
        """
        games = self.get_games(competition)[:count]
        last_games = {
            'wins': 0,
            'defeats': 0,
            'games': []
        }

        for game in games:
            last_games['wins' if game.winner_id == self.id else 'defeats'] += 1
            last_games['games'].append(game)

        return last_games

    def get_longest_streak(self, competition):
        games = self.get_games(competition)
        # Create a list of booleans indicating won matches
        wins_defeats_list = [game.winner_id == self.id for game in games]

        if True in wins_defeats_list:
            # Sum won matches series and keep the max
            return max([sum(g) for k, g in groupby(wins_defeats_list) if k])
        else:
            return 0

    def get_current_streak(self, competition):
        games = self.get_games(competition)
        streak = 0
        for game in games:
            if game.winner_id == self.id:
                streak += 1
            else:
                break
        return streak

    def get_or_create_score(self, competition):
        try:
            score = Score.objects.get(
                team=self,
                competition=competition
            )
        except Score.DoesNotExist:
            score = Score.objects.create(
                team=self,
                competition=competition,
                score=settings.GAME_INITIAL_MU,
                stdev=settings.GAME_INITIAL_SIGMA
            )

        return score

    def get_wins(self, competition):
        return self.games_won.filter(competitions=competition).count()

    def get_defeats(self, competition):
        return self.games_lost.filter(competitions=competition).count()

    def get_score(self, competition):
        return self.scores.get(competition=competition)

    def get_stats_per_week(self):
        """
        Return games weekly statistics with the current team match number, and
        also as an average for the whole teams that have been playing that
        week.
        """
        games_per_week = defaultdict(list)
        for game in Game.objects.all():
            week = '%s.%02d' % (game.date.year, game.date.isocalendar()[1])
            games_per_week[week].append(game)

        stats_per_week = {}
        for week, games in games_per_week.items():
            players = set()
            stats_per_week[week] = {
                'total_count': len(games),
                'team_count': 0,
            }

            for game in games:
                players.add(game.winner_id)
                players.add(game.loser_id)

                if self.id in [game.winner_id, game.loser_id]:
                    stats_per_week[week]['team_count'] += 1

            stats_per_week[week]['player_count'] = len(players)
            stats_per_week[week]['avg_game_per_team'] = (
                float(stats_per_week[week]['total_count'] * 2)
                / stats_per_week[week]['player_count']
            )

        return sorted(stats_per_week.items())


class GameManager(models.Manager):
    def get_latest(self, competition=None):
        User = get_user_model()
        users_with_profile_qs = User.objects.select_related('profile')

        games = (self.get_queryset()
                 .select_related('winner', 'loser', 'winner__users__profile',
                 'loser__users__profile')
                 .prefetch_related(
                     Prefetch('winner__users', queryset=users_with_profile_qs),
                     Prefetch('loser__users', queryset=users_with_profile_qs)
                 )
                 .order_by('-date'))

        if competition is not None:
            games = games.filter(competitions=competition)

        games = games[:20]

        return games

    @transaction.atomic
    def announce(self, winner, loser, competition):
        """
        Announce the results of a new game.

        Args:
            winner: the user id (or tuple of user ids) of the users who won the
            game.
            loser: the user id (or tuple of user ids) of the users who lost the
            game.
        """
        if not competition.is_active():
            raise InactiveCompetitionError()

        winner, created = Team.objects.get_or_create_from_players(winner)
        loser, created = Team.objects.get_or_create_from_players(loser)

        game = self.create(winner=winner, loser=loser)
        game.competitions.add(competition)

        game_played.send(sender=game)
        game.update_score()

        return game

    def delete(self, game, competition):
        history_winner, history_loser = HistoricalScore.delete_for_game_and_competition(game, competition)

        Score.objects.filter()
        winner = game.winner.get_or_create_score(competition)
        winner.score = history_winner.score
        winner.stdev = history_winner.stdev
        winner.save()

        loser = game.loser.get_or_create_score(competition)
        loser.score = history_loser.score
        loser.stdev = history_loser.stdev
        loser.save()

        game.delete()
        game.historical_scores.all().delete()


class Game(models.Model):
    winner = models.ForeignKey(Team, related_name='games_won')
    loser = models.ForeignKey(Team, related_name='games_lost')
    date = models.DateTimeField(default=timezone.now)

    objects = GameManager()

    def clean(self):
        if (self.winner_id is not None and self.loser_id is not None and
                self.winner_id == self.loser_id):
            raise ValidationError(
                "Winner and loser can't be the same team!"
            )

    def __unicode__(self):
        return u"%s beats %s" % (
            self.winner,
            self.loser
        )

    def update_score(self, notify=True):
        winner = self.winner
        loser = self.loser

        for competition in self.competitions.all():
            if notify:
                old_rankings = Score.objects.get_ranking_by_team(competition)

            winner_score = winner.get_or_create_score(competition)
            loser_score = loser.get_or_create_score(competition)

            winner_new_score, loser_new_score = rating.rate(winner_score, loser_score)

            winner_score.score = winner_new_score.mu
            winner_score.stdev = winner_new_score.sigma
            winner_score.save()

            loser_score.score = loser_new_score.mu
            loser_score.stdev = loser_new_score.sigma
            loser_score.save()

            new_rankings = Score.objects.get_ranking_by_team(competition)

            HistoricalScore.save(
                game=self,
                competition=competition,
                winner_score=winner_score,
                loser_score=loser_score,
                rankings=new_rankings,
            )


            if notify:
                for team in [winner, loser]:
                    if (team not in old_rankings or
                            old_rankings[team] != new_rankings[team]):
                        team_ranking_changed.send(
                            sender=self,
                            team=team,
                            old_ranking=(old_rankings[team]
                                         if team in old_rankings else None),
                            new_ranking=new_rankings[team],
                            competition=competition
                        )

    def get_opponent(self, team):
        """
        Return the opponent team relative to the given team.
        """
        return self.winner if self.winner_id != team.id else self.loser


class ScoreManager(models.Manager):
    def get_score_board(self, competition):
        User = get_user_model()

        return (self.get_queryset().filter(competition=competition)
                .order_by('-score').prefetch_related(
                    Prefetch('team__users',
                             queryset=User.objects.select_related('profile')))
               )

    def get_ranking_by_team(self, competition):
        score_board = self.get_score_board(competition)

        return dict(zip(
            [score.team for score in score_board],
            range(1, len(score_board) + 1)
        ))


class Score(models.Model):
    competition = models.ForeignKey('Competition')
    team = models.ForeignKey(Team, related_name='scores')
    score = models.FloatField('skills', default=settings.GAME_INITIAL_MU)
    stdev = models.FloatField('standard deviation',
                              default=settings.GAME_INITIAL_SIGMA)

    objects = ScoreManager()

    class Meta:
        unique_together = (
            ('competition', 'team'),
        )

    def __unicode__(self):
        return '[%s] %s: mu = %s, s = %s' % (self.competition.name,
                                             self.team.get_name(), self.score,
                                             self.stdev)


class HistoricalScore(object):
    game_id = None
    competition_id = None
    team = None
    score = None
    stdev = None
    position = None

    def __init__(self, game_id, competition_id, team, score, stdev, position):
        self.game_id = game_id
        self.competition_id = competition_id
        self.team = team
        self.score = score
        self.stdev = stdev
        self.position = position

    def serialize(self):
        from api.serializers import HistoricalScoreSerializer
        from rest_framework.renderers import JSONRenderer
        return JSONRenderer().render(HistoricalScoreSerializer(instance=self).data)

    def persist(self):
        print "SAVE !"
        redis.StrictRedis().rpush("historical_%s_%s" % (self.competition_id, self.team), self.serialize())

    @staticmethod
    def clear():
        redis.StrictRedis().flushall()

    @staticmethod
    def save(game, competition, winner_score, loser_score, rankings):
        winner = HistoricalScore(
            game.pk, competition.pk, winner_score.team.get_name(),
            winner_score.score, winner_score.stdev, rankings[winner_score.team]
        )
        winner.persist()

        loser = HistoricalScore(
            game.pk, competition.pk, loser_score.team.get_name(),
            loser_score.score, loser_score.stdev, rankings[loser_score.team]
        )
        loser.persist()

        extra = ""
        for team in rankings:
            if team != winner_score.team and team != loser_score.team:
                extra += ', "%s": {"game_id": %s, "team": "%s", "position": %s, "score": %s}' % \
                         (team.get_name(), game.pk, team.get_name(), rankings[team], 10)

        redis.StrictRedis().rpush("games_%s" % competition.pk,
            '{"winner": %s, "loser": %s %s}' % (winner.serialize(), loser.serialize(), extra)
        )

    @staticmethod
    def delete_for_game_and_competition(team, competition):
        return HistoricalScore(), HistoricalScore

    @staticmethod
    def get_latest_results_by_team(competition, start=0, number=50):
        start = int(start)
        number = int(number)
        scores = redis.StrictRedis().lrange("games_%s" % competition.pk, -number - start, -1 - start)
        return '{"games" : [%s]}' % ', '.join(scores)


class CompetitionManager(models.Manager):
    def get_visible_for_user(self, user):
        return self.filter(Q(players=user.id) | Q(creator_id=user.id)).distinct()


class Competition(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    teams = models.ManyToManyField(Team, through=Score)
    games = models.ManyToManyField(Game, related_name='competitions')
    slug = models.SlugField()
    players = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                     related_name='competitions')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='my_competitions')

    objects = CompetitionManager()

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super(Competition, self).save(*args, **kwargs)

    def user_has_read_access(self, user):
        return self.user_has_write_access()

    def user_has_write_access(self, user):
        return (self.players.filter(id=user.id).count() == 1 or
                self.creator_id == user.id)

    def user_is_admin(self, user):
        return self.creator_id == user.id

    def is_over(self):
        """
        Return if the competition end date is reached.
        """
        return self.end_date is not None and self.end_date < timezone.now()

    def is_started(self):
        """
        Return if the competition start date has passed.
        """

        return self.start_date <= timezone.now()

    def is_active(self):
        """
        Return True if the competition has started and is not over yet.
        """
        return self.is_started() and not self.is_over()


class InactiveCompetitionError(Exception):
    pass
