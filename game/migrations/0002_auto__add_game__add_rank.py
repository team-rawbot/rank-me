# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

user_orm_label = '%s.%s' % (User._meta.app_label, User._meta.object_name)
user_model_label = '%s.%s' % (User._meta.app_label, User._meta.module_name)


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Game'
        db.create_table(u'game_game', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('winner',
                self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm[user_orm_label])),
            ('loser',
                self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm[user_orm_label])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 21, 0, 0))),
        ))
        db.send_create_signal(u'game', ['Game'])

        # Adding model 'Rank'
        db.create_table(u'game_rank', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user',
                self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm[user_orm_label])),
            ('rank', self.gf('django.db.models.fields.IntegerField')(default=1000)),
        ))
        db.send_create_signal(u'game', ['Rank'])


    def backwards(self, orm):
        import pdb; pdb.set_trace()
        # Deleting model 'Game'
        db.delete_table(u'game_game')

        # Deleting model 'Rank'
        db.delete_table(u'game_rank')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        user_model_label: {
            'Meta': {
                'object_name': User.__name__,
                'db_table': "'%s'" % User._meta.db_table
            },
            User._meta.pk.attname: (
                'django.db.models.fields.AutoField', [], {
                    'primary_key': 'True',
                    'db_column': "'%s'" % User._meta.pk.column
                }
            ),
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'game.game': {
            'Meta': {'object_name': 'Game'},
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 21, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loser': ('django.db.models.fields.related.ForeignKey', [],
                {'related_name': "'+'", 'to': u"orm[user_orm_label]"}),
            'winner': ('django.db.models.fields.related.ForeignKey', [],
                {'related_name': "'+'", 'to': u"orm[user_orm_label]"})
        },
        u'game.rank': {
            'Meta': {'object_name': 'Rank'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rank': ('django.db.models.fields.IntegerField', [], {'default': '1000'}),
            'user': ('django.db.models.fields.related.ForeignKey', [],
                {'related_name': "'+'", 'to': u"orm[user_orm_label]"})
        }
    }

    complete_apps = ['game']
