# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('game', '0002_create_default_competition'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='creator',
            field=models.ForeignKey(related_name=b'my_competitions', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='competition',
            name='players',
            field=models.ManyToManyField(related_name=b'competitions', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
