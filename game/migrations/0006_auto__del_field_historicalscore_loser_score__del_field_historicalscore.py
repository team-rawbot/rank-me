# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        orm['game.HistoricalScore'].objects.all().delete()

        # Removing unique constraint on 'HistoricalScore', fields ['game']
        db.delete_unique(u'game_historicalscore', ['game_id'])

        # Deleting field 'HistoricalScore.loser_score'
        db.delete_column(u'game_historicalscore', 'loser_score')

        # Deleting field 'HistoricalScore.winner_score'
        db.delete_column(u'game_historicalscore', 'winner_score')

        # Adding field 'HistoricalScore.competition'
        db.add_column(u'game_historicalscore', 'competition',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['game.Competition']),
                      keep_default=False)

        # Adding field 'HistoricalScore.team'
        db.add_column(u'game_historicalscore', 'team',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='historical_scores', to=orm['game.Team']),
                      keep_default=False)

        # Adding field 'HistoricalScore.score'
        db.add_column(u'game_historicalscore', 'score',
                      self.gf('django.db.models.fields.FloatField')(default=25),
                      keep_default=False)


        # Changing field 'HistoricalScore.game'
        db.alter_column(u'game_historicalscore', 'game_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['game.Game']))
        # Deleting field 'Team.wins'
        db.delete_column(u'game_team', 'wins')

        # Deleting field 'Team.score'
        db.delete_column(u'game_team', 'score')

        # Deleting field 'Team.stdev'
        db.delete_column(u'game_team', 'stdev')


    def backwards(self, orm):
        # Adding field 'HistoricalScore.loser_score'
        db.add_column(u'game_historicalscore', 'loser_score',
                      self.gf('django.db.models.fields.FloatField')(default=25),
                      keep_default=False)

        # Adding field 'HistoricalScore.winner_score'
        db.add_column(u'game_historicalscore', 'winner_score',
                      self.gf('django.db.models.fields.FloatField')(default=25),
                      keep_default=False)

        # Deleting field 'HistoricalScore.competition'
        db.delete_column(u'game_historicalscore', 'competition_id')

        # Deleting field 'HistoricalScore.team'
        db.delete_column(u'game_historicalscore', 'team_id')

        # Deleting field 'HistoricalScore.score'
        db.delete_column(u'game_historicalscore', 'score')


        # Changing field 'HistoricalScore.game'
        db.alter_column(u'game_historicalscore', 'game_id', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, to=orm['game.Game']))
        # Adding unique constraint on 'HistoricalScore', fields ['game']
        db.create_unique(u'game_historicalscore', ['game_id'])

        # Adding field 'Team.wins'
        db.add_column(u'game_team', 'wins',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Team.score'
        db.add_column(u'game_team', 'score',
                      self.gf('django.db.models.fields.FloatField')(default=1000),
                      keep_default=False)

        # Adding field 'Team.stdev'
        db.add_column(u'game_team', 'stdev',
                      self.gf('django.db.models.fields.FloatField')(default=333),
                      keep_default=False)


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
        u'auth.user': {
            'Meta': {'object_name': 'User'},
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
            'games': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'competitions'", 'symmetrical': 'False', 'to': u"orm['game.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'game.game': {
            'Meta': {'object_name': 'Game'},
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loser': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'games_lost'", 'to': u"orm['game.Team']"}),
            'winner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'games_won'", 'to': u"orm['game.Team']"})
        },
        u'game.historicalscore': {
            'Meta': {'object_name': 'HistoricalScore'},
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.Competition']"}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'historical_scores'", 'to': u"orm['game.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.FloatField', [], {}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'historical_scores'", 'to': u"orm['game.Team']"})
        },
        u'game.score': {
            'Meta': {'object_name': 'Score'},
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.Competition']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.FloatField', [], {'default': '25'}),
            'stdev': ('django.db.models.fields.FloatField', [], {'default': '8.333'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'scores'", 'to': u"orm['game.Team']"})
        },
        u'game.team': {
            'Meta': {'object_name': 'Team'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'teams'", 'symmetrical': 'False', 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['game']
