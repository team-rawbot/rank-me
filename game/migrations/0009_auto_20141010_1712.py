# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0008_auto_20141010_1705'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='competition',
            options={'ordering': ('name',)},
        ),
        migrations.AddField(
            model_name='club',
            name='logo',
            field=models.ImageField(null=True, upload_to=b'', blank=True),
            preserve_default=True,
        ),
    ]
