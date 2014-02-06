from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

from game.models import Game, Team

class Command(BaseCommand):
    args = '<score> <stdev>'
    help = 'Recalcutes the standings by running all games in the db with the provided initial score and sigma'

    def handle(self, *args, **options):

        if len(args) != 2 :
            raise CommandError('Invalid number of arguments! You should provide 2: score and stdev')
            return False

        score = args[0]
        stdev = args[1]

        teams = Team.objects.all()
        games = Game.objects.all()

        teams.update(score=score, stdev=stdev, wins=0, defeats=0)

        for game in games:
            game.update_score()

        self.stdout.write("Recalculated the standings for {} games with an initial score of {} and an initial sigma of {}".format(
            len(games),
            score,
            stdev
            )
        )