# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'ExecutivePart'
        db.delete_table('lizard_measure_executivepart')

        # Deleting model 'MeasureCollection'
        db.delete_table('lizard_measure_measurecollection')

        # Removing M2M table for field area on 'MeasureCollection'
        db.delete_table('lizard_measure_measurecollection_area')

        # Deleting model 'Executive'
        db.delete_table('lizard_measure_executive')

        # Deleting model 'Municipality'
        db.delete_table('lizard_measure_municipality')

        # Deleting model 'FundingOrganization'
        db.delete_table('lizard_measure_fundingorganization')

        # Deleting model 'Urgency'
        db.delete_table('lizard_measure_urgency')

        # Deleting model 'KRWWaterType'
        db.delete_table('lizard_measure_krwwatertype')

        # Deleting model 'Organization'
        db.delete_table('lizard_measure_organization')

        # Deleting model 'Department'
        db.delete_table('lizard_measure_department')

        # Deleting model 'MeasureStatusMoment'
        db.delete_table('lizard_measure_measurestatusmoment')

        # Deleting model 'MeasureStatus'
        db.delete_table('lizard_measure_measurestatus')

        # Deleting model 'MeasureCategory'
        db.delete_table('lizard_measure_measurecategory')

        # Deleting model 'MeasureCode'
        db.delete_table('lizard_measure_measurecode')

        # Deleting model 'Province'
        db.delete_table('lizard_measure_province')

        # Deleting model 'Measure'
        db.delete_table('lizard_measure_measure')

        # Deleting model 'OrganizationPart'
        db.delete_table('lizard_measure_organizationpart')

        # Deleting model 'MeasurePeriod'
        db.delete_table('lizard_measure_measureperiod')

        # Deleting model 'WaterBodyStatus'
        db.delete_table('lizard_measure_waterbodystatus')

        # Deleting model 'Unit'
        db.delete_table('lizard_measure_unit')

        # Deleting model 'WaterBody'
        db.delete_table('lizard_measure_waterbody')

        # Removing M2M table for field province on 'WaterBody'
        db.delete_table('lizard_measure_waterbody_province')

        # Removing M2M table for field municipality on 'WaterBody'
        db.delete_table('lizard_measure_waterbody_municipality')

        # Removing M2M table for field area on 'WaterBody'
        db.delete_table('lizard_measure_waterbody_area')

        # Deleting model 'Area'
        db.delete_table('lizard_measure_area')


    def backwards(self, orm):
        
        # Adding model 'ExecutivePart'
        db.create_table('lizard_measure_executivepart', (
            ('executive', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.Executive'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('lizard_measure', ['ExecutivePart'])

        # Adding model 'MeasureCollection'
        db.create_table('lizard_measure_measurecollection', (
            ('need_co_funding', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('waterbody', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.WaterBody'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('responsible_department', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.Department'])),
            ('shortname', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('urgency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.Urgency'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('responsible_organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.Organization'])),
        ))
        db.send_create_signal('lizard_measure', ['MeasureCollection'])

        # Adding M2M table for field area on 'MeasureCollection'
        db.create_table('lizard_measure_measurecollection_area', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('measurecollection', models.ForeignKey(orm['lizard_measure.measurecollection'], null=False)),
            ('area', models.ForeignKey(orm['lizard_measure.area'], null=False))
        ))
        db.create_unique('lizard_measure_measurecollection_area', ['measurecollection_id', 'area_id'])

        # Adding model 'Executive'
        db.create_table('lizard_measure_executive', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('lizard_measure', ['Executive'])

        # Adding model 'Municipality'
        db.create_table('lizard_measure_municipality', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('lizard_measure', ['Municipality'])

        # Adding model 'FundingOrganization'
        db.create_table('lizard_measure_fundingorganization', (
            ('cost', self.gf('django.db.models.fields.FloatField')()),
            ('organization_part', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.OrganizationPart'], null=True, blank=True)),
            ('measure', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.Measure'])),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.Organization'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('lizard_measure', ['FundingOrganization'])

        # Adding model 'Urgency'
        db.create_table('lizard_measure_urgency', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.FloatField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('lizard_measure', ['Urgency'])

        # Adding model 'KRWWaterType'
        db.create_table('lizard_measure_krwwatertype', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
        ))
        db.send_create_signal('lizard_measure', ['KRWWaterType'])

        # Adding model 'Organization'
        db.create_table('lizard_measure_organization', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('lizard_measure', ['Organization'])

        # Adding model 'Department'
        db.create_table('lizard_measure_department', (
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.Organization'], null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('lizard_measure', ['Department'])

        # Adding model 'MeasureStatusMoment'
        db.create_table('lizard_measure_measurestatusmoment', (
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.MeasureStatus'])),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('exploitation_expenditure', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('is_planning', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('investment_expenditure', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('measure', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.Measure'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('lizard_measure', ['MeasureStatusMoment'])

        # Adding model 'MeasureStatus'
        db.create_table('lizard_measure_measurestatus', (
            ('color', self.gf('lizard_map.models.ColorField')(max_length=8)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('lizard_measure', ['MeasureStatus'])

        # Adding model 'MeasureCategory'
        db.create_table('lizard_measure_measurecategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('lizard_measure', ['MeasureCategory'])

        # Adding model 'MeasureCode'
        db.create_table('lizard_measure_measurecode', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('lizard_measure', ['MeasureCode'])

        # Adding model 'Province'
        db.create_table('lizard_measure_province', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('lizard_measure', ['Province'])

        # Adding model 'Measure'
        db.create_table('lizard_measure_measure', (
            ('code', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.MeasureCode'])),
            ('executive', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.Executive'])),
            ('period', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.MeasurePeriod'], null=True, blank=True)),
            ('waterbody', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.WaterBody'])),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('total_costs', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.MeasureCategory'])),
            ('aggregation_type', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('is_indicator', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.Unit'])),
            ('executive_part', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.ExecutivePart'], null=True, blank=True)),
            ('read_only', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('exploitation_costs', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.Measure'], null=True, blank=True)),
            ('measure_collection', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.MeasureCollection'], null=True, blank=True)),
            ('investment_costs', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('identity', self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('value', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('lizard_measure', ['Measure'])

        # Adding model 'OrganizationPart'
        db.create_table('lizard_measure_organizationpart', (
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.Organization'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('lizard_measure', ['OrganizationPart'])

        # Adding model 'MeasurePeriod'
        db.create_table('lizard_measure_measureperiod', (
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('lizard_measure', ['MeasurePeriod'])

        # Adding model 'WaterBodyStatus'
        db.create_table('lizard_measure_waterbodystatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
        ))
        db.send_create_signal('lizard_measure', ['WaterBodyStatus'])

        # Adding model 'Unit'
        db.create_table('lizard_measure_unit', (
            ('sign', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('lizard_measure', ['Unit'])

        # Adding model 'WaterBody'
        db.create_table('lizard_measure_waterbody', (
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.WaterBodyStatus'], null=True, blank=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('protected_area_reason', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('characteristics', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('current_situation_chemicals', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('water_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_measure.KRWWaterType'], null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('control_parameters', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('geoobject_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['lizard_geo.GeoObject'], unique=True, primary_key=True)),
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

        # Adding M2M table for field area on 'WaterBody'
        db.create_table('lizard_measure_waterbody_area', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('waterbody', models.ForeignKey(orm['lizard_measure.waterbody'], null=False)),
            ('area', models.ForeignKey(orm['lizard_measure.area'], null=False))
        ))
        db.create_unique('lizard_measure_waterbody_area', ['waterbody_id', 'area_id'])

        # Adding model 'Area'
        db.create_table('lizard_measure_area', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('lizard_measure', ['Area'])


    models = {
        
    }

    complete_apps = ['lizard_measure']
