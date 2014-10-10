# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_auto_20141010_1031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='creator',
            field=models.ForeignKey(related_name=b'my_competitions', to=settings.AUTH_USER_MODEL),
        ),
    ]
