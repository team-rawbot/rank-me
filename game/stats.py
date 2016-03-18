from collections import defaultdict, OrderedDict
from itertools import groupby

from django.core.exceptions import ObjectDoesNotExist

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
    Compute the probability of draw against all opponents
    (ie. how fair is the game).
    Returns an OrderedDict of players by score
    """
    qualities = {}

    own_score = competition.get_score(player)
    opponents = competition.players.exclude(pk=player.pk)

    for opponent in opponents:
        try:
            score = competition.get_score(opponent)
        except ObjectDoesNotExist:
            continue

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


def get_stats_per_week(player, games):
    """
    Return games weekly statistics with the current player match number,
    and also as an average for the whole players that have been playing
    that week.
    """
    games_per_week = defaultdict(list)
    for game in games:
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
