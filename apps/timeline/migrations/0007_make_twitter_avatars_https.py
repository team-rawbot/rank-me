# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-19 16:56
from __future__ import unicode_literals

from django.db import migrations


def twitter_avatars_to_https(apps, schema_editor):
    Event = apps.get_model('timeline', 'Event')
    player_attrs = ['user', 'player', 'winner', 'loser']

    for event in Event.objects.all():
        for attr in player_attrs:
            if attr in event.details and 'avatar' in event.details[attr]:
                event.details[attr]['avatar'] = event.details[attr]['avatar'].replace('http:', 'https:')
                event.save()


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0006_auto_20160318_2204'),
    ]

    operations = [
        migrations.RunPython(twitter_avatars_to_https),
    ]
