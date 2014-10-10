# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('game', '0007_auto_20141010_1444'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='competition',
            options={'ordering': ('name',)},
        ),
        migrations.AddField(
            model_name='club',
            name='creator',
            field=models.ForeignKey(related_name=b'my_clubs', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
