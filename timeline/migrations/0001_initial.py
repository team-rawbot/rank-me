# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.postgres.fields import HStoreField
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_auto_20141010_1404'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('event_type', models.CharField(max_length=50)),
                ('details', HStoreField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('competition', models.ForeignKey(to='game.Competition')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
