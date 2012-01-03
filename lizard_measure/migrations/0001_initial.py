# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'KRWWaterType'
        db.create_table('lizard_measure_krwwatertype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=8)),
        ))
        db.send_create_signal('lizard_measure', ['KRWWaterType'])

        # Adding model 'WaterBodyStatus'
        db.create_table('lizard_measure_waterbodystatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
        ))
        db.send_create_signal('lizard_measure', ['WaterBodyStatus'])

        # Adding model 'Province'
        db.create_table('lizard_measure_province', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('lizard_measure', ['Province'])

        # Adding model 'Municipality'
        db.create_table('lizard_measure_municipality', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('lizard_measure', ['Municipality'])

        # Adding model 'WaterBody'
        db.create_table('lizard_measure_waterbody', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('area', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_area.Area'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('ident', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.WaterBodyStatus'], null=True, blank=True)),
            ('water_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.KRWWaterType'], null=True, blank=True)),
            ('protected_area_reason', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True)),
            ('characteristics', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('current_situation_chemicals', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('control_parameters', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('lizard_measure', ['WaterBody'])

        # Adding M2M table for field province on 'WaterBody'
        db.create_table('lizard_measure_waterbody_province', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('waterbody', models.ForeignKey(orm['lizard_measure.waterbody'], null=False)),
            ('province', models.ForeignKey(orm['lizard_measure.province'], null=False))
        ))
        db.create_unique('lizard_measure_waterbody_province', ['waterbody_id', 'province_id'])

        # Adding M2M table for field municipality on 'WaterBody'
        db.create_table('lizard_measure_waterbody_municipality', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('waterbody', models.ForeignKey(orm['lizard_measure.waterbody'], null=False)),
            ('municipality', models.ForeignKey(orm['lizard_measure.municipality'], null=False))
        ))
        db.create_unique('lizard_measure_waterbody_municipality', ['waterbody_id', 'municipality_id'])

        # Adding model 'MeasureCategory'
        db.create_table('lizard_measure_measurecategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('lizard_measure', ['MeasureCategory'])

        # Adding model 'Unit'
        db.create_table('lizard_measure_unit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('unit', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('valid', self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True)),
        ))
        db.send_create_signal('lizard_measure', ['Unit'])

        # Adding model 'MeasureType'
        db.create_table('lizard_measure_measuretype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=80)),
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

        # Adding model 'Executive'
        db.create_table('lizard_measure_executive', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('lizard_measure', ['Executive'])

        # Adding model 'Organization'
        db.create_table('lizard_measure_organization', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('lizard_measure', ['Organization'])

        # Adding model 'FundingOrganization'
        db.create_table('lizard_measure_fundingorganization', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cost', self.gf('django.db.models.fields.FloatField')()),
            ('percentage', self.gf('django.db.models.fields.FloatField')()),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.Organization'])),
            ('measure', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.Measure'])),
        ))
        db.send_create_signal('lizard_measure', ['FundingOrganization'])

        # Adding model 'MeasureStatus'
        db.create_table('lizard_measure_measurestatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('color', self.gf('lizard_map.models.ColorField')(max_length=8)),
            ('value', self.gf('django.db.models.fields.FloatField')(default=0.0)),
        ))
        db.send_create_signal('lizard_measure', ['MeasureStatus'])

        # Adding model 'MeasureStatusMoment'
        db.create_table('lizard_measure_measurestatusmoment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('measure', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.Measure'])),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.MeasureStatus'])),
            ('datetime', self.gf('django.db.models.fields.DateField')()),
            ('is_planning', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('investment_expenditure', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('exploitation_expenditure', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('lizard_measure', ['MeasureStatusMoment'])

        # Adding model 'MeasurePeriod'
        db.create_table('lizard_measure_measureperiod', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('lizard_measure', ['MeasurePeriod'])

        # Adding model 'Measure'
        db.create_table('lizard_measure_measure', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.Measure'], null=True, blank=True)),
            ('ident', self.gf('django.db.models.fields.CharField')(max_length=64, unique=True, null=True, blank=True)),
            ('is_KRW_measure', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
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
            ('responsible_organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.Organization'])),
            ('executive', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.Executive'])),
            ('total_costs', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('investment_costs', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('exploitation_costs', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('read_only', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_indicator', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
        ))
        db.send_create_signal('lizard_measure', ['Measure'])

        # Adding M2M table for field waterbody on 'Measure'
        db.create_table('lizard_measure_measure_waterbody', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('measure', models.ForeignKey(orm['lizard_measure.measure'], null=False)),
            ('waterbody', models.ForeignKey(orm['lizard_measure.waterbody'], null=False))
        ))
        db.create_unique('lizard_measure_measure_waterbody', ['measure_id', 'waterbody_id'])

        # Adding M2M table for field category on 'Measure'
        db.create_table('lizard_measure_measure_category', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('measure', models.ForeignKey(orm['lizard_measure.measure'], null=False)),
            ('measurecategory', models.ForeignKey(orm['lizard_measure.measurecategory'], null=False))
        ))
        db.create_unique('lizard_measure_measure_category', ['measure_id', 'measurecategory_id'])


    def backwards(self, orm):
        
        # Deleting model 'KRWWaterType'
        db.delete_table('lizard_measure_krwwatertype')

        # Deleting model 'WaterBodyStatus'
        db.delete_table('lizard_measure_waterbodystatus')

        # Deleting model 'Province'
        db.delete_table('lizard_measure_province')

        # Deleting model 'Municipality'
        db.delete_table('lizard_measure_municipality')

        # Deleting model 'WaterBody'
        db.delete_table('lizard_measure_waterbody')

        # Removing M2M table for field province on 'WaterBody'
        db.delete_table('lizard_measure_waterbody_province')

        # Removing M2M table for field municipality on 'WaterBody'
        db.delete_table('lizard_measure_waterbody_municipality')

        # Deleting model 'MeasureCategory'
        db.delete_table('lizard_measure_measurecategory')

        # Deleting model 'Unit'
        db.delete_table('lizard_measure_unit')

        # Deleting model 'MeasureType'
        db.delete_table('lizard_measure_measuretype')

        # Removing M2M table for field units on 'MeasureType'
        db.delete_table('lizard_measure_measuretype_units')

        # Deleting model 'Executive'
        db.delete_table('lizard_measure_executive')

        # Deleting model 'Organization'
        db.delete_table('lizard_measure_organization')

        # Deleting model 'FundingOrganization'
        db.delete_table('lizard_measure_fundingorganization')

        # Deleting model 'MeasureStatus'
        db.delete_table('lizard_measure_measurestatus')

        # Deleting model 'MeasureStatusMoment'
        db.delete_table('lizard_measure_measurestatusmoment')

        # Deleting model 'MeasurePeriod'
        db.delete_table('lizard_measure_measureperiod')

        # Deleting model 'Measure'
        db.delete_table('lizard_measure_measure')

        # Removing M2M table for field waterbody on 'Measure'
        db.delete_table('lizard_measure_measure_waterbody')

        # Removing M2M table for field category on 'Measure'
        db.delete_table('lizard_measure_measure_category')


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
        'lizard_measure.executive': {
            'Meta': {'object_name': 'Executive'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'lizard_measure.fundingorganization': {
            'Meta': {'object_name': 'FundingOrganization'},
            'cost': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'measure': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.Measure']"}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.Organization']"}),
            'percentage': ('django.db.models.fields.FloatField', [], {})
        },
        'lizard_measure.krwwatertype': {
            'Meta': {'object_name': 'KRWWaterType'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'lizard_measure.measure': {
            'Meta': {'object_name': 'Measure'},
            'aggregation_type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lizard_measure.MeasureCategory']", 'symmetrical': 'False'}),
            'datetime_in_source': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'executive': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.Executive']"}),
            'exploitation_costs': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ident': ('django.db.models.fields.CharField', [], {'max_length': '64', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'import_raw': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'import_source': ('django.db.models.fields.CharField', [], {'default': '3', 'max_length': '16'}),
            'investment_costs': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'is_KRW_measure': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_indicator': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'measure_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.MeasureType']"}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.Measure']", 'null': 'True', 'blank': 'True'}),
            'period': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.MeasurePeriod']", 'null': 'True', 'blank': 'True'}),
            'read_only': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'responsible_organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.Organization']"}),
            'status': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lizard_measure.MeasureStatus']", 'through': "orm['lizard_measure.MeasureStatusMoment']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'total_costs': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.Unit']"}),
            'value': ('django.db.models.fields.FloatField', [], {}),
            'waterbody': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lizard_measure.WaterBody']", 'symmetrical': 'False'})
        },
        'lizard_measure.measurecategory': {
            'Meta': {'object_name': 'MeasureCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'lizard_measure.measureperiod': {
            'Meta': {'ordering': "('start_date', 'end_date')", 'object_name': 'MeasurePeriod'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        'lizard_measure.measurestatus': {
            'Meta': {'ordering': "('-value',)", 'object_name': 'MeasureStatus'},
            'color': ('lizard_map.models.ColorField', [], {'max_length': '8'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'value': ('django.db.models.fields.FloatField', [], {'default': '0.0'})
        },
        'lizard_measure.measurestatusmoment': {
            'Meta': {'ordering': "('datetime',)", 'object_name': 'MeasureStatusMoment'},
            'datetime': ('django.db.models.fields.DateField', [], {}),
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
            'code': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'combined_name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.MeasureCategory']", 'null': 'True', 'blank': 'True'}),
            'harmonisation': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'klass': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'subcategory': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'units': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lizard_measure.Unit']", 'symmetrical': 'False'})
        },
        'lizard_measure.municipality': {
            'Meta': {'object_name': 'Municipality'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'lizard_measure.organization': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Organization'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'lizard_measure.province': {
            'Meta': {'object_name': 'Province'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'lizard_measure.unit': {
            'Meta': {'object_name': 'Unit'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'valid': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'})
        },
        'lizard_measure.waterbody': {
            'Meta': {'ordering': "('name',)", 'object_name': 'WaterBody'},
            'area': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_area.Area']", 'null': 'True', 'blank': 'True'}),
            'characteristics': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'control_parameters': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'current_situation_chemicals': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ident': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'municipality': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['lizard_measure.Municipality']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'protected_area_reason': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'province': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['lizard_measure.Province']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.WaterBodyStatus']", 'null': 'True', 'blank': 'True'}),
            'water_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.KRWWaterType']", 'null': 'True', 'blank': 'True'})
        },
        'lizard_measure.waterbodystatus': {
            'Meta': {'object_name': 'WaterBodyStatus'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        }
    }

    complete_apps = ['lizard_measure']
