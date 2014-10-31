from django.conf import settings
from django.core.management.base import BaseCommand

from game.models import Game, HistoricalScore, Score


class Command(BaseCommand):
    args = "<score> <stdev>"
    help = ("Recalcutes the standings by running all games in the db with the"
            " provided initial score and sigma")

    def handle(self, *args, **options):
        try:
            score = args[0]
        except IndexError:
            score = settings.GAME_INITIAL_MU

        try:
            stdev = args[1]
        except IndexError:
            stdev = settings.GAME_INITIAL_SIGMA

        scores = Score.objects.all()
        games = Game.objects.prefetch_related('competitions').order_by('id')

        # remove all HistoricalScores
        HistoricalScore.clear()

        scores.update(score=score, stdev=stdev)

        for game in games:
            game.update_score(notify=False)

        self.stdout.write(
            "Recalculated the standings for {nb_games} games with an initial"
            " score of {initial_score} and an initial sigma of"
            " {initial_sigma}".format(
                nb_games=len(games),
                initial_score=score,
                initial_sigma=stdev
            )
        )
