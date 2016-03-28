# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0007_auto_20141203_1313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='name',
            field=models.CharField(unique=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='competition',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
