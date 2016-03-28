# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-19 09:26
from __future__ import unicode_literals

from django.db import migrations


def game_teams_to_users(apps, schema_editor):
    Game = apps.get_model('game', 'Game')

    for game in Game.objects.all():
        game.winner_user_id = game.winner.users.first().pk
        game.loser_user_id = game.loser.users.first().pk
        game.save()


def score_teams_to_users(apps, schema_editor):
    Score = apps.get_model('game', 'Score')

    for score in Score.objects.all():
        score.player_id = score.team.users.first().pk
        score.save()


def historical_score_teams_to_users(apps, schema_editor):
    HistoricalScore = apps.get_model('game', 'HistoricalScore')

    for hs in HistoricalScore.objects.all():
        hs.player_id = hs.team.users.first().pk
        hs.save()


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0010_simplify_datamodel'),
    ]

    operations = [
        migrations.RunPython(game_teams_to_users),
        migrations.RunPython(score_teams_to_users),
        migrations.RunPython(historical_score_teams_to_users),
    ]