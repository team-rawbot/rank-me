# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-22 15:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0018_fill_icon_for_existing_sports'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='description',
            field=models.CharField(blank=True, max_length=80),
        ),
    ]