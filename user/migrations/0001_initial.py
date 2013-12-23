# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Fill in the destination name with the table name of your model
        db.rename_table('auth_user', 'user_user')
        db.rename_table('auth_user_groups', 'user_user_groups')
        db.rename_table('auth_user_permissions', 'user_user_permissions')
        db.add_column('user_user', 'avatar',
            models.CharField(max_length=255, blank=True))

    def backwards(self, orm):
        db.remove_column('user_user', 'avatar')
        db.rename_table('user_user', 'auth_user')
        db.rename_table('user_user_groups', 'auth_user_groups')
        db.rename_table('user_user_user_permissions', 'auth_user_user_permissions')

    models = {
        
    }

    complete_apps = ['user']
