# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['-date']},
        ),
        migrations.AlterField(
            model_name='event',
            name='competition',
            field=models.ForeignKey(to='game.Competition', null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.CharField(max_length=50, choices=[(b'game_played', 'Game played'), (b'ranking_changed', 'Ranking changed')]),
        ),
    ]
