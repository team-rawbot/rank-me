from collections import OrderedDict
import operator

from django.template.defaulttags import register
from django.db.models import Q

from game.models import HistoricalScore, Team


@register.inclusion_tag('historical_scores.html', takes_context=True)
def historical_scores(context, *args, **kwargs):
    try:
        nb_games = kwargs['nb_games']
    except KeyError as e:
        nb_games = 50

    scores_by_team = OrderedDict()
    team_position_evolution = OrderedDict()

    teams = Team.objects.all().select_related('winner', 'loser')
    scores = HistoricalScore.objects.select_related('game', 'game__winner', 'game__loser').order_by('-id')[:nb_games]
    scores = sorted(scores, key=lambda score: score.id)
    for score in scores:
        game_scores_by_team = {}
        for team in teams:
            team_scores = scores_by_team.get(team, [])

            if team.id == score.game.winner_id:
                skill = score.winner_score
            elif team.id == score.game.loser_id:
                skill = score.loser_score
            else:
                if len(team_scores) == 0:
                    skill = get_last_score_for_team(team, scores[0].id)
                else:
                    skill = team_scores[-1]

            game_scores_by_team[team] = skill

            team_scores.append(skill)
            scores_by_team[team] = team_scores

        positions_for_game = sorted(game_scores_by_team.iteritems(), key=operator.itemgetter(1), reverse=True)
        for idx, position in enumerate(positions_for_game, start=1):
            team_positions = team_position_evolution.get(position[0], [])
            team_positions.append(idx)
            team_position_evolution[position[0]] = team_positions

    context.dicts[0]['scores_by_team'] = scores_by_team
    context.dicts[0]['team_position_evolution'] = team_position_evolution
    context.dicts[0]['nb_games'] = nb_games

    return context


def get_last_score_for_team(team, historical_score_id):
    last_score = HistoricalScore.objects.filter(Q(game__winner=team) | Q(game__loser=team)).filter(id__lte=historical_score_id).select_related('game__winner', 'game__loser', 'game').order_by('-id').first()
    return last_score.winner_score if last_score.game.winner == team else last_score.loser_score
