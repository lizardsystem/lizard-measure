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

        # Adding model 'Area'
        db.create_table('lizard_measure_area', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('lizard_measure', ['Area'])

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

        # Adding M2M table for field area on 'WaterBody'
        db.create_table('lizard_measure_waterbody_area', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('waterbody', models.ForeignKey(orm['lizard_measure.waterbody'], null=False)),
            ('area', models.ForeignKey(orm['lizard_measure.area'], null=False))
        ))
        db.create_unique('lizard_measure_waterbody_area', ['waterbody_id', 'area_id'])

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

        # Adding model 'MeasureCode'
        db.create_table('lizard_measure_measurecode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('lizard_measure', ['MeasureCode'])

        # Adding model 'Unit'
        db.create_table('lizard_measure_unit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sign', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('lizard_measure', ['Unit'])

        # Adding model 'Executive'
        db.create_table('lizard_measure_executive', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('lizard_measure', ['Executive'])

        # Adding model 'ExecutivePart'
        db.create_table('lizard_measure_executivepart', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('executive', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.Executive'])),
        ))
        db.send_create_signal('lizard_measure', ['ExecutivePart'])

        # Adding model 'Organization'
        db.create_table('lizard_measure_organization', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('lizard_measure', ['Organization'])

        # Adding model 'OrganizationPart'
        db.create_table('lizard_measure_organizationpart', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.Organization'])),
        ))
        db.send_create_signal('lizard_measure', ['OrganizationPart'])

        # Adding model 'Department'
        db.create_table('lizard_measure_department', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.Organization'], null=True, blank=True)),
        ))
        db.send_create_signal('lizard_measure', ['Department'])

        # Adding model 'FundingOrganization'
        db.create_table('lizard_measure_fundingorganization', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cost', self.gf('django.db.models.fields.FloatField')()),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.Organization'])),
            ('organization_part', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.OrganizationPart'], null=True, blank=True)),
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

        # Adding model 'Urgency'
        db.create_table('lizard_measure_urgency', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('value', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('lizard_measure', ['Urgency'])

        # Adding model 'MeasureCollection'
        db.create_table('lizard_measure_measurecollection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('shortname', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('waterbody', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.WaterBody'])),
            ('urgency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.Urgency'])),
            ('responsible_organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.Organization'])),
            ('responsible_department', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.Department'])),
            ('need_co_funding', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('lizard_measure', ['MeasureCollection'])

        # Adding M2M table for field area on 'MeasureCollection'
        db.create_table('lizard_measure_measurecollection_area', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('measurecollection', models.ForeignKey(orm['lizard_measure.measurecollection'], null=False)),
            ('area', models.ForeignKey(orm['lizard_measure.area'], null=False))
        ))
        db.create_unique('lizard_measure_measurecollection_area', ['measurecollection_id', 'area_id'])

        # Adding model 'Measure'
        db.create_table('lizard_measure_measure', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.Measure'], null=True, blank=True)),
            ('measure_collection', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.MeasureCollection'], null=True, blank=True)),
            ('aggregation_type', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('is_indicator', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('waterbody', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.WaterBody'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('identity', self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.MeasureCategory'])),
            ('code', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.MeasureCode'])),
            ('value', self.gf('django.db.models.fields.FloatField')()),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.Unit'])),
            ('executive', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.Executive'])),
            ('executive_part', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.ExecutivePart'], null=True, blank=True)),
            ('total_costs', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('investment_costs', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('exploitation_costs', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('period', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.MeasurePeriod'], null=True, blank=True)),
        ))
        db.send_create_signal('lizard_measure', ['Measure'])


    def backwards(self, orm):
        
        # Deleting model 'KRWWaterType'
        db.delete_table('lizard_measure_krwwatertype')

        # Deleting model 'WaterBodyStatus'
        db.delete_table('lizard_measure_waterbodystatus')

        # Deleting model 'Area'
        db.delete_table('lizard_measure_area')

        # Deleting model 'Province'
        db.delete_table('lizard_measure_province')

        # Deleting model 'Municipality'
        db.delete_table('lizard_measure_municipality')

        # Deleting model 'WaterBody'
        db.delete_table('lizard_measure_waterbody')

        # Removing M2M table for field area on 'WaterBody'
        db.delete_table('lizard_measure_waterbody_area')

        # Removing M2M table for field province on 'WaterBody'
        db.delete_table('lizard_measure_waterbody_province')

        # Removing M2M table for field municipality on 'WaterBody'
        db.delete_table('lizard_measure_waterbody_municipality')

        # Deleting model 'MeasureCategory'
        db.delete_table('lizard_measure_measurecategory')

        # Deleting model 'MeasureCode'
        db.delete_table('lizard_measure_measurecode')

        # Deleting model 'Unit'
        db.delete_table('lizard_measure_unit')

        # Deleting model 'Executive'
        db.delete_table('lizard_measure_executive')

        # Deleting model 'ExecutivePart'
        db.delete_table('lizard_measure_executivepart')

        # Deleting model 'Organization'
        db.delete_table('lizard_measure_organization')

        # Deleting model 'OrganizationPart'
        db.delete_table('lizard_measure_organizationpart')

        # Deleting model 'Department'
        db.delete_table('lizard_measure_department')

        # Deleting model 'FundingOrganization'
        db.delete_table('lizard_measure_fundingorganization')

        # Deleting model 'MeasureStatus'
        db.delete_table('lizard_measure_measurestatus')

        # Deleting model 'MeasureStatusMoment'
        db.delete_table('lizard_measure_measurestatusmoment')

        # Deleting model 'MeasurePeriod'
        db.delete_table('lizard_measure_measureperiod')

        # Deleting model 'Urgency'
        db.delete_table('lizard_measure_urgency')

        # Deleting model 'MeasureCollection'
        db.delete_table('lizard_measure_measurecollection')

        # Removing M2M table for field area on 'MeasureCollection'
        db.delete_table('lizard_measure_measurecollection_area')

        # Deleting model 'Measure'
        db.delete_table('lizard_measure_measure')


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
        'lizard_measure.area': {
            'Meta': {'object_name': 'Area'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'lizard_measure.department': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Department'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.Organization']", 'null': 'True', 'blank': 'True'})
        },
        'lizard_measure.executive': {
            'Meta': {'object_name': 'Executive'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'lizard_measure.executivepart': {
            'Meta': {'object_name': 'ExecutivePart'},
            'executive': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.Executive']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'lizard_measure.fundingorganization': {
            'Meta': {'object_name': 'FundingOrganization'},
            'cost': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'measure': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.Measure']"}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.Organization']"}),
            'organization_part': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.OrganizationPart']", 'null': 'True', 'blank': 'True'})
        },
        'lizard_measure.krwwatertype': {
            'Meta': {'object_name': 'KRWWaterType'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'lizard_measure.measure': {
            'Meta': {'ordering': "('waterbody', 'name')", 'object_name': 'Measure'},
            'aggregation_type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.MeasureCategory']"}),
            'code': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.MeasureCode']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'executive': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.Executive']"}),
            'executive_part': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.ExecutivePart']", 'null': 'True', 'blank': 'True'}),
            'exploitation_costs': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identity': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'investment_costs': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'is_indicator': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'measure_collection': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.MeasureCollection']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.Measure']", 'null': 'True', 'blank': 'True'}),
            'period': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.MeasurePeriod']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lizard_measure.MeasureStatus']", 'through': "orm['lizard_measure.MeasureStatusMoment']", 'symmetrical': 'False'}),
            'total_costs': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.Unit']"}),
            'value': ('django.db.models.fields.FloatField', [], {}),
            'waterbody': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.WaterBody']"})
        },
        'lizard_measure.measurecategory': {
            'Meta': {'object_name': 'MeasureCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'lizard_measure.measurecode': {
            'Meta': {'ordering': "('code',)", 'object_name': 'MeasureCode'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'lizard_measure.measurecollection': {
            'Meta': {'ordering': "('name',)", 'object_name': 'MeasureCollection'},
            'area': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['lizard_measure.Area']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'need_co_funding': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'responsible_department': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.Department']"}),
            'responsible_organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.Organization']"}),
            'shortname': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'urgency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.Urgency']"}),
            'waterbody': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.WaterBody']"})
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
        'lizard_measure.organizationpart': {
            'Meta': {'ordering': "('name',)", 'object_name': 'OrganizationPart'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.Organization']"})
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
            'sign': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'lizard_measure.urgency': {
            'Meta': {'ordering': "('-value',)", 'object_name': 'Urgency'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'lizard_measure.waterbody': {
            'Meta': {'ordering': "('name',)", 'object_name': 'WaterBody'},
            'area': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['lizard_measure.Area']", 'null': 'True', 'blank': 'True'}),
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
