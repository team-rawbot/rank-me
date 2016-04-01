from collections import defaultdict, OrderedDict
import datetime
from itertools import groupby
import json
import operator

from django.utils import timezone

from .models import Game, HistoricalScore

from trueskill import Rating, quality_1vs1


def get_head2head(player, competition):
    """
    Compute the amount of wins and defeats against all opponents the player
    played against. The returned value is an OrderedDict since the players
    are ordered by their score.
    """
    head2head = {}
    fairnesses = get_fairness(player, competition)
    games = competition.get_games_played_by(player)

    for game in games:
        opponent = game.get_opponent(player)

        if opponent not in fairnesses:
            continue

        if opponent not in head2head:
            head2head[opponent] = {
                'wins': 0,
                'defeats': 0,
                'games': [],
                'fairness': fairnesses[opponent]['quality']
            }

        stat_to_increase = (
            'wins' if game.winner_id == player.id else 'defeats'
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


def get_fairness(player, competition):
    """
    Compute the probability of draw against all opponents (ie. how fair is the
    game). Return an OrderedDict of players by score.
    """
    qualities = {}

    own_score = competition.get_score(player)
    opponents = competition.players.exclude(pk=player.pk)
    scores = (competition.scores.filter(player__in=opponents)
                                .select_related('player'))
    score_by_opponent = {score.player: score for score in scores}

    for opponent in opponents:
        if opponent not in score_by_opponent:
            continue

        score = score_by_opponent[opponent]

        quality = quality_1vs1(
            Rating(own_score.score, own_score.stdev),
            Rating(score.score, score.stdev)
        )
        qualities[opponent] = {'score': score, 'quality': quality * 100}

    return OrderedDict(
        sorted(
            qualities.items(),
            key=lambda t: t[1]['score'].score,
            reverse=True
        )
    )


def get_last_games_stats(player, competition, games_count):
    """
    Return a dictionary with the latest ``count`` played games and the
    number of wins and defeats.
    """
    games = competition.get_games_played_by(player)[:games_count]
    last_games = {
        'wins': 0,
        'defeats': 0,
        'games': []
    }

    for game in games:
        last_games['wins' if game.winner_id == player.id else 'defeats'] += 1
        last_games['games'].append(game)

    return last_games


def get_longest_streak(player, competition):
    games = competition.get_games_played_by(player)
    # Create a list of booleans indicating won matches
    wins_defeats_list = [game.winner_id == player.id for game in games]

    if True in wins_defeats_list:
        # Sum won matches series and keep the max
        return max([sum(g) for k, g in groupby(wins_defeats_list) if k])
    else:
        return 0


def get_current_streak(player, competition):
    games = competition.get_games_played_by(player)
    streak = 0
    for game in games:
        if game.winner_id == player.id:
            streak += 1
        else:
            break

    return streak


def get_stats_per_week(player, limit_days=140):
    """
    Return games weekly statistics with the current player match number,
    and also as an average for the whole players that have been playing
    that week. ``limit_days`` is the number of days back in time of games taken
    into consideration. This might be rounded up to get to a monday since the
    stats are done on a weekly basis.
    """
    games_per_week = defaultdict(list)
    date_limit = timezone.now() - datetime.timedelta(days=limit_days)
    # We always want to count the week stats starting on monday so we substract
    # enough days to get to the previous monday if necessary
    date_limit -= datetime.timedelta(days=date_limit.weekday())
    for game in Game.objects.filter(date__gte=date_limit):
        week = '%s.%02d' % (game.date.year, game.date.isocalendar()[1])
        games_per_week[week].append(game)

    stats_per_week = {}
    for week, games in games_per_week.items():
        players = set()
        stats_per_week[week] = {
            'total_count': len(games),
            'players_count': 0,
        }

        for game in games:
            players.add(game.winner_id)
            players.add(game.loser_id)

            if player.id in [game.winner_id, game.loser_id]:
                stats_per_week[week]['players_count'] += 1

        stats_per_week[week]['player_count'] = len(players)
        stats_per_week[week]['avg_game_per_player'] = (
            float(stats_per_week[week]['total_count'] * 2) /
            stats_per_week[week]['player_count']
        )

    return sorted(stats_per_week.items())


def get_latest_results_by_player(competition, nb_games, offset=0,
                                 return_json=False):
    """
    Get nb_games latest scores for each player

    :param nb_games:int number of games
    :param return_json:boolean
    :return:dict Dict with key=player and value=list of score objects

    {player_a: [{skill: xx, played: xx, game: game_id}, ...]}
    """
    # add start to nb_games because slicing want the end position
    nb_games += offset
    games = (competition.games
             .order_by('-id')
             .prefetch_related('historical_scores')[offset:nb_games])

    players = competition.get_players()
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
                    if historical_score.player_id == player.id:
                        player_historical_score = historical_score
                        break

                assert player_historical_score is not None

                result['skill'] = player_historical_score.score

                result['win'] = player.id == game.winner_id
                result['played'] = True
            else:
                result['played'] = False
                if len(player_scores) == 0:
                    last_score = competition.get_last_score_for_player(
                        player, game
                    )

                    if not last_score:
                        last_score = HistoricalScore.objects.get_default()

                    result['skill'] = last_score.score
                else:
                    result['skill'] = player_scores[-1]['skill']

            all_skills_by_game[player] = result['skill']

            player_scores.append(result)
            scores_by_player[player] = player_scores

        positions_for_game = sorted(
            all_skills_by_game.items(),
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
