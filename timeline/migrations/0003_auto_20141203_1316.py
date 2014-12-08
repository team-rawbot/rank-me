# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0002_auto_20141203_0918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.CharField(max_length=50, choices=[(b'game_played', 'Game played'), (b'ranking_changed', 'Ranking changed'), (b'competition_created', 'Competition created'), (b'user_joined_competition', 'User joined competition')]),
        ),
    ]
