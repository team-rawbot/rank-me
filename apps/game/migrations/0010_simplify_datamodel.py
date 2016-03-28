# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-19 09:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0009_auto_20160317_2159'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='loser_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='games_lost', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='game',
            name='winner_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='games_won', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalscore',
            name='player',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='historical_scores', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='score',
            name='player',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scores', to=settings.AUTH_USER_MODEL),
        ),
    ]