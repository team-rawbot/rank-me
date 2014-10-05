# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def create_default_competition(apps, schema_editor):
    Competition = apps.get_model("game", "Competition")
    Competition.objects.create(
        name=u"Default competition", slug="default-competition"
    )

class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_competition)
    ]
