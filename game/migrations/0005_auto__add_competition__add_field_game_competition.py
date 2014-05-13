# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Competition'
        db.create_table(u'game_competition', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'game', ['Competition'])

        # Adding M2M table for field games on 'Competition'
        m2m_table_name = db.shorten_name(u'game_competition_games')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('competition', models.ForeignKey(orm[u'game.competition'], null=False)),
            ('game', models.ForeignKey(orm[u'game.game'], null=False))
        ))
        db.create_unique(m2m_table_name, ['competition_id', 'game_id'])

        # Adding field 'Game.competition'
        db.add_column(u'game_game', 'competition',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['game.Competition']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Competition'
        db.delete_table(u'game_competition')

        # Removing M2M table for field games on 'Competition'
        db.delete_table(db.shorten_name(u'game_competition_games'))

        # Deleting field 'Game.competition'
        db.delete_column(u'game_game', 'competition_id')


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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'game.competition': {
            'Meta': {'object_name': 'Competition'},
            'games': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'games'", 'symmetrical': 'False', 'to': u"orm['game.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'game.game': {
            'Meta': {'object_name': 'Game'},
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.Competition']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loser': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'games_lost'", 'to': u"orm['game.Team']"}),
            'winner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'games_won'", 'to': u"orm['game.Team']"})
        },
        u'game.historicalscore': {
            'Meta': {'object_name': 'HistoricalScore'},
            'game': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'historical_score'", 'unique': 'True', 'to': u"orm['game.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loser_score': ('django.db.models.fields.FloatField', [], {}),
            'winner_score': ('django.db.models.fields.FloatField', [], {})
        },
        u'game.team': {
            'Meta': {'object_name': 'Team'},
            'defeats': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.FloatField', [], {'default': '25'}),
            'stdev': ('django.db.models.fields.FloatField', [], {'default': '8.333'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'teams'", 'symmetrical': 'False', 'to': u"orm['user.User']"}),
            'wins': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'user.user': {
            'Meta': {'object_name': 'User'},
            'avatar': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['game']