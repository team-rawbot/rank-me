# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def set_default_creator(apps, schema_editor):
    Competition = apps.get_model("game", "Competition")
    User = apps.get_model("auth", "User")
    default_user = User.objects.order_by("pk").first()
    for competition in Competition.objects.filter(creator=None):
        competition.creator = default_user
        competition.save()


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_auto_20141010_1031'),
    ]

    operations = [
        migrations.RunPython(set_default_creator)
    ]
