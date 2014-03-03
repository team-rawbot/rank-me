import json

from django.template.defaulttags import register

from game.models import HistoricalScore


@register.inclusion_tag('historical_scores.html', takes_context=True)
def historical_scores(context, *args, **kwargs):
    try:
        nb_games = kwargs['nb_games']
    except KeyError as e:
        nb_games = 50

    scores_by_team = HistoricalScore.objects.get_latest_results_by_team(nb_games)

    context.dicts[0]['scores_by_team'] = scores_by_team
    context.dicts[0]['scores_by_team_json'] = parse_to_json(scores_by_team)
    context.dicts[0]['nb_games'] = nb_games

    return context


def parse_to_json(scores_by_team):
    json_result = {}
    for team, results in scores_by_team.items():
        json_result[team.get_name()] = results

    return json.dumps(json_result)
