# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_hstore.fields


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
                ('details', django_hstore.fields.DictionaryField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('competition', models.ForeignKey(to='game.Competition')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
