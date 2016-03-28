# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_date', models.DateTimeField(null=True, blank=True)),
                ('slug', models.SlugField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.FloatField(verbose_name=b'Current team score')),
                ('stdev', models.FloatField(default=8.333, verbose_name=b'Current team standard deviation')),
                ('competition', models.ForeignKey(to='game.Competition')),
                ('game', models.ForeignKey(related_name=b'historical_scores', to='game.Game')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.FloatField(default=25, verbose_name=b'skills')),
                ('stdev', models.FloatField(default=8.333, verbose_name=b'standard deviation')),
                ('competition', models.ForeignKey(to='game.Competition')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('users', models.ManyToManyField(related_name=b'teams', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='score',
            name='team',
            field=models.ForeignKey(related_name=b'scores', to='game.Team'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='score',
            unique_together=set([('competition', 'team')]),
        ),
        migrations.AddField(
            model_name='historicalscore',
            name='team',
            field=models.ForeignKey(related_name=b'historical_scores', to='game.Team'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='historicalscore',
            unique_together=set([('team', 'game', 'competition')]),
        ),
        migrations.AddField(
            model_name='game',
            name='loser',
            field=models.ForeignKey(related_name=b'games_lost', to='game.Team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='winner',
            field=models.ForeignKey(related_name=b'games_won', to='game.Team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='competition',
            name='games',
            field=models.ManyToManyField(related_name=b'competitions', to='game.Game'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='competition',
            name='teams',
            field=models.ManyToManyField(to='game.Team', through='game.Score'),
            preserve_default=True,
        ),
    ]
