# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'FundingOrganization'
        db.create_table('lizard_measure_fundingorganization', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('percentage', self.gf('django.db.models.fields.FloatField')()),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.Organization'])),
            ('measure', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.Measure'])),
        ))
        db.send_create_signal('lizard_measure', ['FundingOrganization'])

        # Adding model 'MeasureCategory'
        db.create_table('lizard_measure_measurecategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('valid', self.gf('django.db.models.fields.NullBooleanField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal('lizard_measure', ['MeasureCategory'])

        # Adding model 'KRWWatertype'
        db.create_table('lizard_measure_krwwatertype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
        ))
        db.send_create_signal('lizard_measure', ['KRWWatertype'])

        # Adding model 'Organization'
        db.create_table('lizard_measure_organization', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('organization_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.OrganizationType'], null=True, blank=True)),
            ('source', self.gf('django.db.models.fields.IntegerField')(default=5)),
            ('valid', self.gf('django.db.models.fields.NullBooleanField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal('lizard_measure', ['Organization'])

        # Adding model 'MeasureType'
        db.create_table('lizard_measure_measuretype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=80)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.MeasureCategory'], null=True, blank=True)),
            ('klass', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('subcategory', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('harmonisation', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('combined_name', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
        ))
        db.send_create_signal('lizard_measure', ['MeasureType'])

        # Adding M2M table for field units on 'MeasureType'
        db.create_table('lizard_measure_measuretype_units', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('measuretype', models.ForeignKey(orm['lizard_measure.measuretype'], null=False)),
            ('unit', models.ForeignKey(orm['lizard_measure.unit'], null=False))
        ))
        db.create_unique('lizard_measure_measuretype_units', ['measuretype_id', 'unit_id'])

        # Adding model 'MeasureStatusMoment'
        db.create_table('lizard_measure_measurestatusmoment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('measure', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.Measure'])),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.MeasureStatus'])),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('is_planning', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('investment_expenditure', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('exploitation_expenditure', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('lizard_measure', ['MeasureStatusMoment'])

        # Adding model 'MeasureStatus'
        db.create_table('lizard_measure_measurestatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('color', self.gf('lizard_map.models.ColorField')(max_length=8)),
            ('value', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('valid', self.gf('django.db.models.fields.NullBooleanField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal('lizard_measure', ['MeasureStatus'])

        # Adding model 'KRWStatus'
        db.create_table('lizard_measure_krwstatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
        ))
        db.send_create_signal('lizard_measure', ['KRWStatus'])

        # Adding model 'Score'
        db.create_table('lizard_measure_score', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('measuring_rod', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.MeasuringRod'])),
            ('area', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_area.Area'], null=True, blank=True)),
            ('area_ident', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('mep', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('gep', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('limit_insufficient_moderate', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('limit_bad_insufficient', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('ascending', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('target_2015', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('target_2027', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal('lizard_measure', ['Score'])

        # Adding model 'MeasuringRod'
        db.create_table('lizard_measure_measuringrod', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('group', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('measuring_rod', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('sub_measuring_rod', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('unit', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('sign', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
        ))
        db.send_create_signal('lizard_measure', ['MeasuringRod'])

        # Adding model 'OrganizationType'
        db.create_table('lizard_measure_organizationtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('lizard_measure', ['OrganizationType'])

        # Adding model 'MeasurePeriod'
        db.create_table('lizard_measure_measureperiod', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('valid', self.gf('django.db.models.fields.NullBooleanField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal('lizard_measure', ['MeasurePeriod'])

        # Adding model 'SteeringParameter'
        db.create_table('lizard_measure_steeringparameter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('area', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_area.Area'])),
            ('fews_parameter', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('target_minimum', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('target_maximum', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal('lizard_measure', ['SteeringParameter'])

        # Adding model 'Unit'
        db.create_table('lizard_measure_unit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('unit', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('valid', self.gf('django.db.models.fields.NullBooleanField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal('lizard_measure', ['Unit'])

        # Adding model 'WaterBody'
        db.create_table('lizard_measure_waterbody', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('area', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_area.Area'], null=True, blank=True)),
            ('area_ident', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('krw_status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.KRWStatus'], null=True, blank=True)),
            ('krw_watertype', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.KRWWatertype'], null=True, blank=True)),
        ))
        db.send_create_signal('lizard_measure', ['WaterBody'])

        # Adding model 'Measure'
        db.create_table('lizard_measure_measure', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.Measure'], null=True, blank=True)),
            ('ident', self.gf('django.db.models.fields.CharField')(max_length=64, unique=True, null=True, blank=True)),
            ('is_KRW_measure', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('geometry', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_geo.GeoObject'], null=True, blank=True)),
            ('measure_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.MeasureType'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('period', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.MeasurePeriod'], null=True, blank=True)),
            ('import_source', self.gf('django.db.models.fields.CharField')(default=3, max_length=16)),
            ('datetime_in_source', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('import_raw', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('aggregation_type', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('value', self.gf('django.db.models.fields.FloatField')()),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.Unit'])),
            ('initiator', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='initiator_measure_set', null=True, to=orm['lizard_measure.Organization'])),
            ('executive', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='executive_measure_set', null=True, to=orm['lizard_measure.Organization'])),
            ('responsible_department', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('total_costs', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('investment_costs', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('exploitation_costs', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('read_only', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_indicator', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('lizard_measure', ['Measure'])

        # Adding M2M table for field waterbodies on 'Measure'
        db.create_table('lizard_measure_measure_waterbodies', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('measure', models.ForeignKey(orm['lizard_measure.measure'], null=False)),
            ('waterbody', models.ForeignKey(orm['lizard_measure.waterbody'], null=False))
        ))
        db.create_unique('lizard_measure_measure_waterbodies', ['measure_id', 'waterbody_id'])

        # Adding M2M table for field areas on 'Measure'
        db.create_table('lizard_measure_measure_areas', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('measure', models.ForeignKey(orm['lizard_measure.measure'], null=False)),
            ('area', models.ForeignKey(orm['lizard_area.area'], null=False))
        ))
        db.create_unique('lizard_measure_measure_areas', ['measure_id', 'area_id'])

        # Adding M2M table for field categories on 'Measure'
        db.create_table('lizard_measure_measure_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('measure', models.ForeignKey(orm['lizard_measure.measure'], null=False)),
            ('measurecategory', models.ForeignKey(orm['lizard_measure.measurecategory'], null=False))
        ))
        db.create_unique('lizard_measure_measure_categories', ['measure_id', 'measurecategory_id'])


    def backwards(self, orm):
        
        # Deleting model 'FundingOrganization'
        db.delete_table('lizard_measure_fundingorganization')

        # Deleting model 'MeasureCategory'
        db.delete_table('lizard_measure_measurecategory')

        # Deleting model 'KRWWatertype'
        db.delete_table('lizard_measure_krwwatertype')

        # Deleting model 'Organization'
        db.delete_table('lizard_measure_organization')

        # Deleting model 'MeasureType'
        db.delete_table('lizard_measure_measuretype')

        # Removing M2M table for field units on 'MeasureType'
        db.delete_table('lizard_measure_measuretype_units')

        # Deleting model 'MeasureStatusMoment'
        db.delete_table('lizard_measure_measurestatusmoment')

        # Deleting model 'MeasureStatus'
        db.delete_table('lizard_measure_measurestatus')

        # Deleting model 'KRWStatus'
        db.delete_table('lizard_measure_krwstatus')

        # Deleting model 'Score'
        db.delete_table('lizard_measure_score')

        # Deleting model 'MeasuringRod'
        db.delete_table('lizard_measure_measuringrod')

        # Deleting model 'OrganizationType'
        db.delete_table('lizard_measure_organizationtype')

        # Deleting model 'MeasurePeriod'
        db.delete_table('lizard_measure_measureperiod')

        # Deleting model 'SteeringParameter'
        db.delete_table('lizard_measure_steeringparameter')

        # Deleting model 'Unit'
        db.delete_table('lizard_measure_unit')

        # Deleting model 'WaterBody'
        db.delete_table('lizard_measure_waterbody')

        # Deleting model 'Measure'
        db.delete_table('lizard_measure_measure')

        # Removing M2M table for field waterbodies on 'Measure'
        db.delete_table('lizard_measure_measure_waterbodies')

        # Removing M2M table for field areas on 'Measure'
        db.delete_table('lizard_measure_measure_areas')

        # Removing M2M table for field categories on 'Measure'
        db.delete_table('lizard_measure_measure_categories')


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
        'lizard_area.area': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Area', '_ormbases': ['lizard_area.Communique']},
            'area_class': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'communique_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['lizard_area.Communique']", 'unique': 'True', 'primary_key': 'True'}),
            'data_administrator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_area.DataAdministrator']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_area.Area']", 'null': 'True', 'blank': 'True'})
        },
        'lizard_area.communique': {
            'Meta': {'object_name': 'Communique', '_ormbases': ['lizard_geo.GeoObject']},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'geoobject_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['lizard_geo.GeoObject']", 'unique': 'True', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'lizard_area.dataadministrator': {
            'Meta': {'object_name': 'DataAdministrator'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        'lizard_geo.geoobject': {
            'Meta': {'object_name': 'GeoObject'},
            'geo_object_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_geo.GeoObjectGroup']"}),
            'geometry': ('django.contrib.gis.db.models.fields.GeometryField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ident': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'lizard_geo.geoobjectgroup': {
            'Meta': {'object_name': 'GeoObjectGroup'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'source_log': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'lizard_measure.fundingorganization': {
            'Meta': {'object_name': 'FundingOrganization'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'measure': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.Measure']"}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.Organization']"}),
            'percentage': ('django.db.models.fields.FloatField', [], {})
        },
        'lizard_measure.krwstatus': {
            'Meta': {'object_name': 'KRWStatus'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'lizard_measure.krwwatertype': {
            'Meta': {'object_name': 'KRWWatertype'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'lizard_measure.measure': {
            'Meta': {'object_name': 'Measure'},
            'aggregation_type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'areas': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'area_measure_set'", 'symmetrical': 'False', 'to': "orm['lizard_area.Area']"}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lizard_measure.MeasureCategory']", 'symmetrical': 'False'}),
            'datetime_in_source': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'executive': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'executive_measure_set'", 'null': 'True', 'to': "orm['lizard_measure.Organization']"}),
            'exploitation_costs': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'funding_organizations': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lizard_measure.Organization']", 'through': "orm['lizard_measure.FundingOrganization']", 'symmetrical': 'False'}),
            'geometry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_geo.GeoObject']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ident': ('django.db.models.fields.CharField', [], {'max_length': '64', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'import_raw': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'import_source': ('django.db.models.fields.CharField', [], {'default': '3', 'max_length': '16'}),
            'initiator': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'initiator_measure_set'", 'null': 'True', 'to': "orm['lizard_measure.Organization']"}),
            'investment_costs': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'is_KRW_measure': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_indicator': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'measure_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.MeasureType']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.Measure']", 'null': 'True', 'blank': 'True'}),
            'period': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.MeasurePeriod']", 'null': 'True', 'blank': 'True'}),
            'read_only': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'responsible_department': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'status_moments': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lizard_measure.MeasureStatus']", 'through': "orm['lizard_measure.MeasureStatusMoment']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'total_costs': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.Unit']"}),
            'value': ('django.db.models.fields.FloatField', [], {}),
            'waterbodies': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lizard_measure.WaterBody']", 'symmetrical': 'False'})
        },
        'lizard_measure.measurecategory': {
            'Meta': {'object_name': 'MeasureCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'valid': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        'lizard_measure.measureperiod': {
            'Meta': {'ordering': "('start_date', 'end_date')", 'object_name': 'MeasurePeriod'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'valid': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        'lizard_measure.measurestatus': {
            'Meta': {'ordering': "('-value',)", 'object_name': 'MeasureStatus'},
            'color': ('lizard_map.models.ColorField', [], {'max_length': '8'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'valid': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {'default': '0.0'})
        },
        'lizard_measure.measurestatusmoment': {
            'Meta': {'ordering': "('date',)", 'object_name': 'MeasureStatusMoment'},
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'exploitation_expenditure': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'investment_expenditure': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'is_planning': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'measure': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.Measure']"}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.MeasureStatus']"})
        },
        'lizard_measure.measuretype': {
            'Meta': {'ordering': "('code',)", 'object_name': 'MeasureType'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'combined_name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.MeasureCategory']", 'null': 'True', 'blank': 'True'}),
            'harmonisation': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'klass': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'subcategory': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'units': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lizard_measure.Unit']", 'symmetrical': 'False'})
        },
        'lizard_measure.measuringrod': {
            'Meta': {'object_name': 'MeasuringRod'},
            'group': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'measuring_rod': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'sign': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'sub_measuring_rod': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        'lizard_measure.organization': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Organization'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'organization_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.OrganizationType']", 'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'valid': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        'lizard_measure.organizationtype': {
            'Meta': {'object_name': 'OrganizationType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'lizard_measure.score': {
            'Meta': {'object_name': 'Score'},
            'area': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_area.Area']", 'null': 'True', 'blank': 'True'}),
            'area_ident': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'ascending': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'gep': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'limit_bad_insufficient': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'limit_insufficient_moderate': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'measuring_rod': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.MeasuringRod']"}),
            'mep': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'target_2015': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'target_2027': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'lizard_measure.steeringparameter': {
            'Meta': {'object_name': 'SteeringParameter'},
            'area': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_area.Area']"}),
            'fews_parameter': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'target_maximum': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'target_minimum': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'lizard_measure.unit': {
            'Meta': {'object_name': 'Unit'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'valid': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        'lizard_measure.waterbody': {
            'Meta': {'object_name': 'WaterBody'},
            'area': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_area.Area']", 'null': 'True', 'blank': 'True'}),
            'area_ident': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'krw_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.KRWStatus']", 'null': 'True', 'blank': 'True'}),
            'krw_watertype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.KRWWatertype']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['lizard_measure']
