from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

from game.models import Game, Team
from trueskill import Rating, rate_1vs1

class Command(BaseCommand):
	args = '<score> <stdev>'
	help = 'Recalcutes the standings by running all games in the db with the provided initial score and sigma'
	option_list = BaseCommand.option_list + (
		make_option('-a', '--algo',
			action='store',
			dest='algorithm',
			default='trueskill',
			help='choose the algorithm used to recalculate. default is trueSkill'),
		)

	def handle(self, *args, **options):

		if len(args) != 2 :
			raise CommandError('Invalid number of arguments! You should provide 2: score and stdev')
			return False

		score = args[0]
		stdev = args[1]

		algorithm = options.algorithm

		teams = Team.objects.all()
		games = Game.objects.all()

		teams.update(score=score, stdev=stdev)

		for game in games:
			
			winner = game.winner
			loser = game.loser

			winner_new_score, loser_new_score = rate_1vs1(
				Rating(winner.score, winner.stdev),
				Rating(loser.score, loser.stdev)
			)
			
			winner.score = winner_new_score.mu
			winner.stdev = winner_new_score.sigma
			winner.save()
			
			loser.score = loser_new_score.mu
			loser.stdev = loser_new_score.sigma
			loser.save()

		self.stdout.write("Recalculated the standings for {} games with an initial score of {} and an initial sigma of {}".format(
			len(games),
			score,
			stdev
			)
		)