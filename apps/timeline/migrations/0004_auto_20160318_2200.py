# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-18 21:00
from __future__ import unicode_literals

import django.contrib.postgres.fields.hstore
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0003_auto_20141203_1316'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='details_json',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='event',
            name='details',
            field=django.contrib.postgres.fields.hstore.HStoreField(),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.CharField(choices=[('game_played', 'Game played'), ('ranking_changed', 'Ranking changed'), ('competition_created', 'Competition created'), ('user_joined_competition', 'User joined competition'), ('user_left_competition', 'User left competition')], max_length=50),
        ),
    ]
