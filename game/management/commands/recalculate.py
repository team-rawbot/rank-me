from django.core.management.base import BaseCommand, CommandError

from game.models import Game, Team


class Command(BaseCommand):
    args = "<score> <stdev>"
    help = ("Recalcutes the standings by running all games in the db with the"
            " provided initial score and sigma")

    def handle(self, *args, **options):
        if len(args) != 2:
            raise CommandError("Invalid number of arguments! You should"
                               " provide 2: score and stdev")

        score, stdev = args

        teams = Team.objects.all()
        games = Game.objects.order_by('id')

        teams.update(score=score, stdev=stdev, wins=0, defeats=0)

        for game in games:
            game.update_score()

        self.stdout.write(
            "Recalculated the standings for {nb_games} games with an initial"
            " score of {initial_score} and an initial sigma of"
            " {initial_sigma}".format(
                nb_games=len(games),
                initial_score=score,
                initial_sigma=stdev
            )
        )
