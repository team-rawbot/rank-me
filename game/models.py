import operator
import json
import six

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import Q
from django.template.defaultfilters import slugify
from django.utils import timezone

from trueskill import Rating, rate_1vs1

from . import stats
from .signals import (
    competition_created, game_played, ranking_changed,
    user_joined_competition, user_left_competition
)


class GameManager(models.Manager):
    def get_latest(self, competition=None):
        games = (self.get_queryset()
                 .select_related('winner', 'loser', 'winner__profile',
                                 'loser__profile')
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

        game = self.create(winner=winner, loser=loser)
        game.competitions.add(competition)

        game_played.send(sender=game)
        game.update_score()

        return game

    def delete(self, game, competition):
        history_winner = HistoricalScore.objects.get_last_for_player(
            game.winner,
            game, competition
        )
        history_loser = HistoricalScore.objects.get_last_for_player(
            game.loser,
            game,
            competition
        )

        winner = competition.get_or_create_score(game.winner)
        winner.score = history_winner.score
        winner.stdev = history_winner.stdev
        winner.save()

        loser = competition.get_or_create_score(game.loser)
        loser.score = history_loser.score
        loser.stdev = history_loser.stdev
        loser.save()

        game.delete()
        game.historical_scores.all().delete()


class Game(models.Model):
    winner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='games_won')
    loser = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='games_lost')
    date = models.DateTimeField(default=timezone.now)

    objects = GameManager()

    def clean(self):
        if (self.winner_id is not None and self.loser_id is not None and
                self.winner_id == self.loser_id):
            raise ValidationError(
                "Winner and loser can't be the same person!"
            )

    def __str__(self):
        return u"%s beats %s" % (
            self.winner,
            self.loser
        )

    def update_score(self, notify=True):
        winner = self.winner
        loser = self.loser

        for competition in self.competitions.all():
            if notify:
                old_rankings = Score.objects.get_ranking_by_player(competition)

            winner_score = competition.get_or_create_score(winner)
            loser_score = competition.get_or_create_score(loser)

            winner_new_score, loser_new_score = rate_1vs1(
                Rating(winner_score.score, winner_score.stdev),
                Rating(loser_score.score, loser_score.stdev)
            )

            winner_score.score = winner_new_score.mu
            winner_score.stdev = winner_new_score.sigma
            winner_score.save()

            loser_score.score = loser_new_score.mu
            loser_score.stdev = loser_new_score.sigma
            loser_score.save()

            HistoricalScore.objects.create(
                game=self,
                score=winner_score.score,
                stdev=winner_score.stdev,
                player=winner,
                competition=competition
            )

            HistoricalScore.objects.create(
                game=self,
                score=loser_score.score,
                stdev=loser_score.stdev,
                player=loser,
                competition=competition
            )

            if notify:
                new_rankings = Score.objects.get_ranking_by_player(competition)

                for player in [winner, loser]:
                    if (player not in old_rankings or
                            old_rankings[player] != new_rankings[player]):
                        ranking_changed.send(
                            sender=self,
                            player=player,
                            old_ranking=(old_rankings[player]
                                         if player in old_rankings else None),
                            new_ranking=new_rankings[player],
                            competition=competition
                        )

    def get_opponent(self, player):
        """
        Return the opponent player relative to the given player.
        """
        return self.winner if self.winner_id != player.id else self.loser


class HistoricalScoreManager(models.Manager):
    def get_latest(self, nb_games, competition):
        return (self.get_queryset()
                .select_related('game', 'game__winner', 'game__loser')
                .filter(game__competitions=competition)
                .order_by('-id')[:nb_games])

    def get_latest_results_by_player(self, nb_games, competition,
                                     start=0, return_json=False):
        """
        Get nb_games latest scores for each player

        :param nb_games:int number of games
        :param return_json:boolean
        :return:dict Dict with key=player and value=list of score objects

        {player_a: [{skill: xx, played: xx, game: game_id}, ...]}
        """

        # add start to nb_games because slicing want the end position
        nb_games += int(start)
        games = (Game.objects.filter(competitions=competition)
                 .order_by('-id')
                 .prefetch_related('historical_scores')[start:nb_games])

        players = (get_user_model().objects
                   .filter(
                       Q(games_won__competitions=competition) |
                       Q(games_lost__competitions=competition)
                   )
                   .distinct())
        scores_by_player = {}

        for game in reversed(games):
            all_skills_by_game = {}

            for player in players:
                player_scores = scores_by_player.get(player, [])
                result = {'game': game.id}

                if player.id in [game.winner_id, game.loser_id]:
                    player_historical_score = None
                    # We don't use get() here so we don't hit the database
                    # since historical scores are prefetched
                    for historical_score in game.historical_scores.all():
                        if (historical_score.player_id == player.id
                                and historical_score.competition_id ==
                                competition.id):
                            player_historical_score = historical_score
                            break

                    assert player_historical_score is not None

                    result['skill'] = player_historical_score.score

                    result['win'] = player.id == game.winner_id
                    result['played'] = True
                else:
                    result['played'] = False
                    if len(player_scores) == 0:
                        result['skill'] = self.get_last_score_for_player(
                            player, game, competition
                        )
                    else:
                        result['skill'] = player_scores[-1]['skill']

                all_skills_by_game[player] = result['skill']

                player_scores.append(result)
                scores_by_player[player] = player_scores

            positions_for_game = sorted(
                six.iteritems(all_skills_by_game),
                key=operator.itemgetter(1),
                reverse=True
            )
            for idx, position in enumerate(positions_for_game, start=1):
                scores_by_player[position[0]][-1]['position'] = idx

        if return_json:
            json_result = {}
            for player, results in scores_by_player.items():
                json_result[player.get_full_name()] = results

            return json.dumps(json_result)

        return scores_by_player

    def get_last_score_for_player(self, player, game, competition):
        """
        Returns the latest skill before game :game for player :player

        :param player:Player
        :param game:Game
        :return:float skill
        """
        return self.get_last_for_player(player, game, competition).score

    def get_last_for_player(self, player, game, competition):
        """
        Return the latest historical score before game for a player in the
        competition.

        :param player:Player
        :param game:Game
        :param competition:Competition
        :return:HistoricalScore
        """
        last_score = HistoricalScore.objects.filter(
            game_id__lt=game.id,
            player=player,
            competition=competition
        ).order_by('-id').first()

        if last_score is None:
            last_score = HistoricalScore(
                game=game,
                score=settings.GAME_INITIAL_MU,
                stdev=settings.GAME_INITIAL_SIGMA,
                player=player,
                competition=competition
            )

        return last_score


class ScoreManager(models.Manager):
    def get_score_board(self, competition):
        return (self.get_queryset().filter(competition=competition)
                .order_by('-score').select_related('player__profile'))

    def get_ranking_by_player(self, competition):
        score_board = self.get_score_board(competition)

        return dict(zip(
            [score.player for score in score_board],
            range(1, len(score_board) + 1)
        ))


class Score(models.Model):
    competition = models.ForeignKey('Competition', related_name='scores')
    player = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='scores')
    score = models.FloatField('skills', default=settings.GAME_INITIAL_MU)
    stdev = models.FloatField('standard deviation',
                              default=settings.GAME_INITIAL_SIGMA)

    objects = ScoreManager()

    class Meta:
        unique_together = (
            ('competition', 'player'),
        )

    def __str__(self):
        return '[%s] %s: mu = %s, s = %s' % (self.competition.name,
                                             self.player.get_full_name(),
                                             self.score, self.stdev)


class HistoricalScore(models.Model):
    game = models.ForeignKey(Game, related_name='historical_scores')
    competition = models.ForeignKey('Competition')
    player = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='historical_scores')
    score = models.FloatField('Current player score')
    stdev = models.FloatField('Current player standard deviation',
                              default=settings.GAME_INITIAL_SIGMA)

    objects = HistoricalScoreManager()

    class Meta:
        unique_together = (
            ('player', 'game', 'competition'),
        )


class CompetitionManager(models.Manager):
    def get_visible_for_user(self, user):
        return self.filter(
            Q(players=user.id) | Q(creator_id=user.id)
        ).distinct()


class Competition(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    games = models.ManyToManyField(Game, related_name='competitions')
    slug = models.SlugField(unique=True)
    players = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                     related_name='competitions',
                                     blank=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='my_competitions')

    objects = CompetitionManager()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        new_competition = self.id is None

        super(Competition, self).save(*args, **kwargs)

        # Make sure we send the signal after calling the parent save method, so
        # that the competition now has an id
        if new_competition:
            competition_created.send(sender=self)

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

    def add_user_access(self, user):
        if user not in self.players.all() and user.id != self.creator_id:
            self.players.add(user)
            user_joined_competition.send(sender=self, user=user)

    def remove_user_access(self, user):
        if user.id == self.creator_id:
            raise CannotLeaveCompetitionError()

        self.players.remove(user)
        user_left_competition.send(sender=self, user=user)

    def get_games_played_by(self, player):
        """
        Fetch the list of games played by the user, filtered by competition.
        """
        games = (self.games
                     .order_by('-date')
                     .select_related('winner', 'loser')
                     .filter(Q(winner_id=player.id) | Q(loser_id=player.id)))

        return games

    def get_head2head(self, player):
        """
        Compute the amount of wins and defeats against all opponents the player
        played against. The returned value is an OrderedDict since the players
        are ordered by their score.
        """
        return stats.get_head2head(player, self)

    def get_fairness(self, player):
        """
        Compute the probability of draw against all opponents
        (ie. how fair is the game).
        Returns an OrderedDict of players by score
        """
        return stats.get_fairness(player, self)

    def get_last_games_stats(self, player, competition, games_count=10):
        """
        Return a dictionary with the latest ``count`` played games and the
        number of wins and defeats.
        """
        return stats.get_last_games_stats(player, self, games_count)

    def get_longest_streak(self, player):
        return stats.get_longest_streak(player, self)

    def get_current_streak(self, player):
        return stats.get_current_streak(player, self)

    def get_or_create_score(self, player):
        try:
            score = Score.objects.get(
                player=player,
                competition=self
            )
        except Score.DoesNotExist:
            score = Score.objects.create(
                player=player,
                competition=self,
                score=settings.GAME_INITIAL_MU,
                stdev=settings.GAME_INITIAL_SIGMA
            )

        return score

    def get_wins(self, player):
        return player.games_won.filter(competitions=self).count()

    def get_defeats(self, player):
        return player.games_lost.filter(competitions=self).count()

    def get_score(self, player):
        return player.scores.get(competition=self)


class InactiveCompetitionError(Exception):
    pass


class CannotLeaveCompetitionError(Exception):
    pass
