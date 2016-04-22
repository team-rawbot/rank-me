from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from django.template.defaultfilters import slugify
from django.utils import timezone

from .. import signals
from ..exceptions import CannotLeaveCompetitionError
from .game import Game
from .score import Score


class CompetitionManager(models.Manager):
    def get_visible_for_user(self, user):
        """
        Return all competitions the given user has access to.
        """
        return self.filter(
            Q(players=user.id) | Q(creator_id=user.id)
        ).distinct()


class OngoingCompetitionManager(CompetitionManager):
    def get_queryset(self):
        return super().get_queryset().filter(
            Q(end_date__gt=timezone.now()) | Q(end_date__isnull=True),
            start_date__lte=timezone.now(),
        )


class PastCompetitionManager(CompetitionManager):
    def get_queryset(self):
        return super().get_queryset().filter(end_date__lte=timezone.now())


class UpcomingCompetitionManager(CompetitionManager):
    def get_queryset(self):
        return super().get_queryset().filter(start_date__gt=timezone.now())


class Sport(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=255)
    icon = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Competition(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    slug = models.SlugField(unique=True)
    players = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                     related_name='competitions',
                                     blank=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='my_competitions')
    sport = models.ForeignKey('Sport',
                              related_name='competitions')

    objects = CompetitionManager()
    ongoing_objects = OngoingCompetitionManager()
    past_objects = PastCompetitionManager()
    upcoming_objects = UpcomingCompetitionManager()

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
            signals.competition_created.send(sender=self)

    def add_game(self, winner, loser):
        """
        Announce a new game in the competition with the given winner and loser.
        """
        return Game.objects.announce(winner, loser, self)

    def user_has_read_access(self, user):
        return self.user_has_write_access()

    def user_has_write_access(self, user):
        return (self.players.filter(id=user.id).count() == 1 or
                self.creator_id == user.id)

    def user_is_admin(self, user):
        return self.creator_id == user.id

    def user_can_leave(self, user):
        return self.creator_id != user.id

    def is_over(self):
        """
        Return True if the competition end date is reached.
        """
        return self.end_date is not None and self.end_date <= timezone.now()

    def is_started(self):
        """
        Return True if the competition start date has passed.
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
            signals.user_joined_competition.send(sender=self, user=user)

    def remove_user_access(self, user):
        if user.id == self.creator_id:
            raise CannotLeaveCompetitionError()

        self.players.remove(user)
        signals.user_left_competition.send(sender=self, user=user)

    def get_games_played_by(self, player):
        """
        Fetch the list of games played by the user in the competition.
        """
        games = (self.games
                     .order_by('-date')
                     .select_related('winner', 'winner__profile', 'loser',
                                     'loser__profile')
                     .filter(Q(winner_id=player.id) | Q(loser_id=player.id)))

        return games

    def get_or_create_score(self, player):
        try:
            score = self.get_score(player)
        except Score.DoesNotExist:
            score = Score.objects.create(
                player=player,
                competition=self,
                score=settings.GAME_INITIAL_MU,
                stdev=settings.GAME_INITIAL_SIGMA
            )

        return score

    def get_wins(self, player):
        """
        Return the number of games won by the player in the competition.
        """
        return player.games_won.filter(competition=self).count()

    def get_defeats(self, player):
        """
        Return the number of games lost by the player in the competition.
        """
        return player.games_lost.filter(competition=self).count()

    def get_score(self, player):
        """
        Return the score of the user in the competition.
        """
        return player.scores.get(competition=self)

    def get_players(self):
        """
        Return a list of players who have played at least 1 game in the
        competition.
        """
        return get_user_model().objects.filter(
                  Q(games_won__competition=self) |
                  Q(games_lost__competition=self)).distinct()

    def get_score_board(self):
        """
        Return sorted scores (highest to lowest) from players in the
        competition.
        """
        return (self.scores.order_by('-score')
                           .select_related('player__profile'))

    def get_ranking_by_player(self):
        """
        Return a dict {player: position} for every player in the ranking.
        """
        score_board = self.get_score_board()

        return dict(zip(
            [score.player for score in score_board],
            range(1, len(score_board) + 1)
        ))

    def get_last_score_for_player(self, player, last_game=None):
        """
        Returns the latest HistoricalScore before ``last_game`` for the given
        ``player``.
        """
        last_score = (player.historical_scores
                            .filter(game__competition=self)
                            .order_by('-id'))

        if last_game:
            last_score = last_score.filter(game_id__lt=last_game.id)

        return last_score.first()

    def get_latest_games(self, n=20):
        """
        Return the latest ``n`` games in the competition.
        """
        return self.games.get_latest(n)
