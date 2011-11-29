# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'KRWWaterType'
        db.create_table('lizard_krw_krwwatertype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=8)),
        ))
        db.send_create_signal('lizard_krw', ['KRWWaterType'])

        # Adding model 'WaterBody'
        db.create_table('lizard_krw_waterbody', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('ident', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('water_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_krw.KRWWaterType'])),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('lizard_krw', ['WaterBody'])

        # Adding model 'SingleIndicator'
        db.create_table('lizard_krw_singleindicator', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timeserie_id', self.gf('django.db.models.fields.IntegerField')()),
            ('target_value', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('boundary_value', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('y_min', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('y_max', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('water_body', self.gf('django.db.models.fields.related.ForeignKey')(related_name='indicators', to=orm['lizard_krw.WaterBody'])),
        ))
        db.send_create_signal('lizard_krw', ['SingleIndicator'])

        # Adding model 'Color'
        db.create_table('lizard_krw_color', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('r', self.gf('django.db.models.fields.IntegerField')()),
            ('g', self.gf('django.db.models.fields.IntegerField')()),
            ('b', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('lizard_krw', ['Color'])

        # Adding model 'AlphaScore'
        db.create_table('lizard_krw_alphascore', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('color', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['lizard_krw.Color'])),
        ))
        db.send_create_signal('lizard_krw', ['AlphaScore'])

        # Adding model 'Score'
        db.create_table('lizard_krw_score', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('waterbody', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_krw.WaterBody'])),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('category', self.gf('django.db.models.fields.IntegerField')()),
            ('alpha_score', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_krw.AlphaScore'])),
            ('value', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('lizard_krw', ['Score'])

        # Adding model 'GoalScore'
        db.create_table('lizard_krw_goalscore', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('waterbody', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_krw.WaterBody'])),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('category', self.gf('django.db.models.fields.IntegerField')()),
            ('alpha_score', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['lizard_krw.AlphaScore'])),
            ('value', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('lizard_krw', ['GoalScore'])

        # Adding model 'MeasureCategory'
        db.create_table('lizard_krw_measurecategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('lizard_krw', ['MeasureCategory'])

        # Adding model 'MeasureCode'
        db.create_table('lizard_krw_measurecode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('lizard_krw', ['MeasureCode'])

        # Adding model 'Unit'
        db.create_table('lizard_krw_unit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sign', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('lizard_krw', ['Unit'])

        # Adding model 'Executive'
        db.create_table('lizard_krw_executive', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('lizard_krw', ['Executive'])

        # Adding model 'Organization'
        db.create_table('lizard_krw_organization', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('lizard_krw', ['Organization'])

        # Adding model 'FundingOrganization'
        db.create_table('lizard_krw_fundingorganization', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cost', self.gf('django.db.models.fields.FloatField')()),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_krw.Organization'])),
            ('measure', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_krw.Measure'])),
        ))
        db.send_create_signal('lizard_krw', ['FundingOrganization'])

        # Adding model 'MeasureStatus'
        db.create_table('lizard_krw_measurestatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('color', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('value', self.gf('django.db.models.fields.FloatField')(default=0.0)),
        ))
        db.send_create_signal('lizard_krw', ['MeasureStatus'])

        # Adding model 'MeasureStatusMoment'
        db.create_table('lizard_krw_measurestatusmoment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('measure', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_krw.Measure'])),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_krw.MeasureStatus'])),
            ('datetime', self.gf('django.db.models.fields.DateField')()),
            ('is_planning', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('lizard_krw', ['MeasureStatusMoment'])

        # Adding model 'MeasurePeriod'
        db.create_table('lizard_krw_measureperiod', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('lizard_krw', ['MeasurePeriod'])

        # Adding model 'Measure'
        db.create_table('lizard_krw_measure', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_krw.Measure'], null=True, blank=True)),
            ('aggregation_type', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('is_indicator', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('waterbody', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_krw.WaterBody'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('identity', self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_krw.MeasureCategory'])),
            ('code', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_krw.MeasureCode'])),
            ('value', self.gf('django.db.models.fields.FloatField')()),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_krw.Unit'])),
            ('executive', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_krw.Executive'])),
            ('total_costs', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('investment_costs', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('exploitation_costs', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('period', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_krw.MeasurePeriod'], null=True, blank=True)),
        ))
        db.send_create_signal('lizard_krw', ['Measure'])

        # Adding model 'XMLImportMeetobject'
        db.create_table('lizard_krw_xmlimportmeetobject', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('lizard_krw', ['XMLImportMeetobject'])

        # Adding M2M table for field waterbodies on 'XMLImportMeetobject'
        db.create_table('lizard_krw_xmlimportmeetobject_waterbodies', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('xmlimportmeetobject', models.ForeignKey(orm['lizard_krw.xmlimportmeetobject'], null=False)),
            ('waterbody', models.ForeignKey(orm['lizard_krw.waterbody'], null=False))
        ))
        db.create_unique('lizard_krw_xmlimportmeetobject_waterbodies', ['xmlimportmeetobject_id', 'waterbody_id'])

        # Adding model 'XMLImport'
        db.create_table('lizard_krw_xmlimport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('xml_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('import_category', self.gf('django.db.models.fields.IntegerField')()),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
        ))
        db.send_create_signal('lizard_krw', ['XMLImport'])


    def backwards(self, orm):
        
        # Deleting model 'KRWWaterType'
        db.delete_table('lizard_krw_krwwatertype')

        # Deleting model 'WaterBody'
        db.delete_table('lizard_krw_waterbody')

        # Deleting model 'SingleIndicator'
        db.delete_table('lizard_krw_singleindicator')

        # Deleting model 'Color'
        db.delete_table('lizard_krw_color')

        # Deleting model 'AlphaScore'
        db.delete_table('lizard_krw_alphascore')

        # Deleting model 'Score'
        db.delete_table('lizard_krw_score')

        # Deleting model 'GoalScore'
        db.delete_table('lizard_krw_goalscore')

        # Deleting model 'MeasureCategory'
        db.delete_table('lizard_krw_measurecategory')

        # Deleting model 'MeasureCode'
        db.delete_table('lizard_krw_measurecode')

        # Deleting model 'Unit'
        db.delete_table('lizard_krw_unit')

        # Deleting model 'Executive'
        db.delete_table('lizard_krw_executive')

        # Deleting model 'Organization'
        db.delete_table('lizard_krw_organization')

        # Deleting model 'FundingOrganization'
        db.delete_table('lizard_krw_fundingorganization')

        # Deleting model 'MeasureStatus'
        db.delete_table('lizard_krw_measurestatus')

        # Deleting model 'MeasureStatusMoment'
        db.delete_table('lizard_krw_measurestatusmoment')

        # Deleting model 'MeasurePeriod'
        db.delete_table('lizard_krw_measureperiod')

        # Deleting model 'Measure'
        db.delete_table('lizard_krw_measure')

        # Deleting model 'XMLImportMeetobject'
        db.delete_table('lizard_krw_xmlimportmeetobject')

        # Removing M2M table for field waterbodies on 'XMLImportMeetobject'
        db.delete_table('lizard_krw_xmlimportmeetobject_waterbodies')

        # Deleting model 'XMLImport'
        db.delete_table('lizard_krw_xmlimport')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'lizard_krw.alphascore': {
            'Meta': {'object_name': 'AlphaScore'},
            'color': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['lizard_krw.Color']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'lizard_krw.color': {
            'Meta': {'object_name': 'Color'},
            'b': ('django.db.models.fields.IntegerField', [], {}),
            'g': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'r': ('django.db.models.fields.IntegerField', [], {})
        },
        'lizard_krw.executive': {
            'Meta': {'object_name': 'Executive'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'lizard_krw.fundingorganization': {
            'Meta': {'object_name': 'FundingOrganization'},
            'cost': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'measure': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_krw.Measure']"}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_krw.Organization']"})
        },
        'lizard_krw.goalscore': {
            'Meta': {'ordering': "('start_date', 'waterbody', 'category', 'alpha_score')", 'object_name': 'GoalScore'},
            'alpha_score': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['lizard_krw.AlphaScore']"}),
            'category': ('django.db.models.fields.IntegerField', [], {}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'value': ('django.db.models.fields.FloatField', [], {}),
            'waterbody': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_krw.WaterBody']"})
        },
        'lizard_krw.krwwatertype': {
            'Meta': {'object_name': 'KRWWaterType'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'lizard_krw.measure': {
            'Meta': {'ordering': "('waterbody', 'name')", 'object_name': 'Measure'},
            'aggregation_type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_krw.MeasureCategory']"}),
            'code': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_krw.MeasureCode']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'executive': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_krw.Executive']"}),
            'exploitation_costs': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identity': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'investment_costs': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'is_indicator': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_krw.Measure']", 'null': 'True', 'blank': 'True'}),
            'period': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_krw.MeasurePeriod']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lizard_krw.MeasureStatus']", 'through': "orm['lizard_krw.MeasureStatusMoment']", 'symmetrical': 'False'}),
            'total_costs': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_krw.Unit']"}),
            'value': ('django.db.models.fields.FloatField', [], {}),
            'waterbody': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_krw.WaterBody']"})
        },
        'lizard_krw.measurecategory': {
            'Meta': {'object_name': 'MeasureCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'lizard_krw.measurecode': {
            'Meta': {'ordering': "('code',)", 'object_name': 'MeasureCode'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'lizard_krw.measureperiod': {
            'Meta': {'ordering': "('start_date', 'end_date')", 'object_name': 'MeasurePeriod'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        'lizard_krw.measurestatus': {
            'Meta': {'ordering': "('-value',)", 'object_name': 'MeasureStatus'},
            'color': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'value': ('django.db.models.fields.FloatField', [], {'default': '0.0'})
        },
        'lizard_krw.measurestatusmoment': {
            'Meta': {'ordering': "('datetime',)", 'object_name': 'MeasureStatusMoment'},
            'datetime': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_planning': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'measure': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_krw.Measure']"}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_krw.MeasureStatus']"})
        },
        'lizard_krw.organization': {
            'Meta': {'object_name': 'Organization'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'lizard_krw.score': {
            'Meta': {'ordering': "('start_date', 'waterbody', 'category', 'alpha_score')", 'object_name': 'Score'},
            'alpha_score': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_krw.AlphaScore']"}),
            'category': ('django.db.models.fields.IntegerField', [], {}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'value': ('django.db.models.fields.FloatField', [], {}),
            'waterbody': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_krw.WaterBody']"})
        },
        'lizard_krw.singleindicator': {
            'Meta': {'object_name': 'SingleIndicator'},
            'boundary_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'target_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'timeserie_id': ('django.db.models.fields.IntegerField', [], {}),
            'water_body': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'indicators'", 'to': "orm['lizard_krw.WaterBody']"}),
            'y_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'y_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'lizard_krw.unit': {
            'Meta': {'object_name': 'Unit'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sign': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'lizard_krw.waterbody': {
            'Meta': {'ordering': "('name',)", 'object_name': 'WaterBody'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ident': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'water_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_krw.KRWWaterType']"})
        },
        'lizard_krw.xmlimport': {
            'Meta': {'object_name': 'XMLImport'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'import_category': ('django.db.models.fields.IntegerField', [], {}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'xml_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        'lizard_krw.xmlimportmeetobject': {
            'Meta': {'object_name': 'XMLImportMeetobject'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'waterbodies': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lizard_krw.WaterBody']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['lizard_krw']
