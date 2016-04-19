# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0006_auto_20141010_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='players',
            field=models.ManyToManyField(related_name=b'competitions', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
