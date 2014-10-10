# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_auto_20141010_1404'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='competition',
            options={'ordering': ('name',)},
        ),
    ]
