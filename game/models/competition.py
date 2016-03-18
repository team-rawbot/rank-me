from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from django.template.defaultfilters import slugify
from django.utils import timezone

from .. import signals, stats
from ..exceptions import CannotLeaveCompetitionError
from .score import HistoricalScore, Score


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
            signals.competition_created.send(sender=self)

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
            signals.user_joined_competition.send(sender=self, user=user)

    def remove_user_access(self, user):
        if user.id == self.creator_id:
            raise CannotLeaveCompetitionError()

        self.players.remove(user)
        signals.user_left_competition.send(sender=self, user=user)

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
        return stats.get_head2head(player, self)

    def get_fairness(self, player):
        return stats.get_fairness(player, self)

    def get_last_games_stats(self, player, competition, games_count=10):
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
        return player.games_won.filter(competition=self).count()

    def get_defeats(self, player):
        return player.games_lost.filter(competition=self).count()

    def get_score(self, player):
        return player.scores.get(competition=self)

    def get_players(self):
        return get_user_model().objects.filter(
                  Q(games_won__competition=self) |
                  Q(games_lost__competition=self)).distinct()

    def get_score_board(self):
        return (self.scores.order_by('-score')
                           .select_related('player__profile'))

    def get_ranking_by_player(self):
        score_board = self.get_score_board()

        return dict(zip(
            [score.player for score in score_board],
            range(1, len(score_board) + 1)
        ))

    def get_last_score_for_player(self, player, last_game=None):
        """
        Returns the latest skill before game :game for player :player

        :param player:Player
        :param game:Game
        :return:float skill
        """
        default_score = HistoricalScore.objects.get_default()
        default_score.game = last_game
        default_score.competition = self
        default_score.player = player

        return stats.get_last_score_for_player(player, self, default_score,
                                               last_game)
