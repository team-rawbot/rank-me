# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-20 08:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0013_auto_20160405_1002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='competition',
            name='sport',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='competitions', to='game.Sport'),
        ),
    ]
