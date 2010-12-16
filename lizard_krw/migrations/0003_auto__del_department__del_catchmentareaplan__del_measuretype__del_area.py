# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Department'
        db.delete_table('lizard_krw_department')

        # Deleting model 'CatchmentAreaPlan'
        db.delete_table('lizard_krw_catchmentareaplan')

        # Deleting model 'MeasureType'
        db.delete_table('lizard_krw_measuretype')

        # Deleting model 'AreaPlan'
        db.delete_table('lizard_krw_areaplan')

        # Deleting model 'Area'
        db.delete_table('lizard_krw_area')

        # Deleting model 'FundingCategory'
        db.delete_table('lizard_krw_fundingcategory')

        # Adding model 'MeasureCode'
        db.create_table('lizard_krw_measurecode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('lizard_krw', ['MeasureCode'])

        # Adding model 'Executive'
        db.create_table('lizard_krw_executive', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('lizard_krw', ['Executive'])

        # Adding model 'MeasurePeriod'
        db.create_table('lizard_krw_measureperiod', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('lizard_krw', ['MeasurePeriod'])

        # Deleting field 'FundingOrganization.price'
        db.delete_column('lizard_krw_fundingorganization', 'price')

        # Deleting field 'FundingOrganization.funding_category'
        db.delete_column('lizard_krw_fundingorganization', 'funding_category_id')

        # Adding field 'FundingOrganization.cost'
        db.add_column('lizard_krw_fundingorganization', 'cost', self.gf('django.db.models.fields.FloatField')(default=0), keep_default=False)

        # Deleting field 'Measure.area'
        db.delete_column('lizard_krw_measure', 'area_id')

        # Deleting field 'Measure.catchment_area_plan_value'
        db.delete_column('lizard_krw_measure', 'catchment_area_plan_value')

        # Deleting field 'Measure.type'
        db.delete_column('lizard_krw_measure', 'type_id')

        # Deleting field 'Measure.responsible_organization'
        db.delete_column('lizard_krw_measure', 'responsible_organization_id')

        # Deleting field 'Measure.price'
        db.delete_column('lizard_krw_measure', 'price')

        # Deleting field 'Measure.need_co_funding'
        db.delete_column('lizard_krw_measure', 'need_co_funding')

        # Deleting field 'Measure.area_plan'
        db.delete_column('lizard_krw_measure', 'area_plan_id')

        # Deleting field 'Measure.obligation_end_date'
        db.delete_column('lizard_krw_measure', 'obligation_end_date')

        # Deleting field 'Measure.responsible_department'
        db.delete_column('lizard_krw_measure', 'responsible_department_id')

        # Deleting field 'Measure.catchment_area_plan_unit'
        db.delete_column('lizard_krw_measure', 'catchment_area_plan_unit_id')

        # Deleting field 'Measure.catchment_area_plan'
        db.delete_column('lizard_krw_measure', 'catchment_area_plan_id')

        # Adding field 'Measure.identity'
        db.add_column('lizard_krw_measure', 'identity', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'Measure.category'
        db.add_column('lizard_krw_measure', 'category', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['lizard_krw.MeasureCategory']), keep_default=False)

        # Adding field 'Measure.value'
        db.add_column('lizard_krw_measure', 'value', self.gf('django.db.models.fields.FloatField')(default=0), keep_default=False)

        # Adding field 'Measure.unit'
        db.add_column('lizard_krw_measure', 'unit', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['lizard_krw.Unit']), keep_default=False)

        # Adding field 'Measure.executive'
        db.add_column('lizard_krw_measure', 'executive', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['lizard_krw.Executive']), keep_default=False)

        # Adding field 'Measure.total_costs'
        db.add_column('lizard_krw_measure', 'total_costs', self.gf('django.db.models.fields.FloatField')(null=True, blank=True), keep_default=False)

        # Adding field 'Measure.investment_costs'
        db.add_column('lizard_krw_measure', 'investment_costs', self.gf('django.db.models.fields.FloatField')(null=True, blank=True), keep_default=False)

        # Adding field 'Measure.exploitation_costs'
        db.add_column('lizard_krw_measure', 'exploitation_costs', self.gf('django.db.models.fields.FloatField')(null=True, blank=True), keep_default=False)

        # Renaming column for 'Measure.code' to match new field type.
        db.rename_column('lizard_krw_measure', 'code', 'code_id')
        # Changing field 'Measure.code'
        db.alter_column('lizard_krw_measure', 'code_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_krw.MeasureCode']))

        # Adding index on 'Measure', fields ['code']
        db.create_index('lizard_krw_measure', ['code_id'])


    def backwards(self, orm):
        
        # Removing index on 'Measure', fields ['code']
        db.delete_index('lizard_krw_measure', ['code_id'])

        # Adding model 'Department'
        db.create_table('lizard_krw_department', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('lizard_krw', ['Department'])

        # Adding model 'CatchmentAreaPlan'
        db.create_table('lizard_krw_catchmentareaplan', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('lizard_krw', ['CatchmentAreaPlan'])

        # Adding model 'MeasureType'
        db.create_table('lizard_krw_measuretype', (
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_krw.MeasureCategory'])),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('lizard_krw', ['MeasureType'])

        # Adding model 'AreaPlan'
        db.create_table('lizard_krw_areaplan', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('lizard_krw', ['AreaPlan'])

        # Adding model 'Area'
        db.create_table('lizard_krw_area', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('lizard_krw', ['Area'])

        # Adding model 'FundingCategory'
        db.create_table('lizard_krw_fundingcategory', (
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_krw.Organization'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('lizard_krw', ['FundingCategory'])

        # Deleting model 'MeasureCode'
        db.delete_table('lizard_krw_measurecode')

        # Deleting model 'Executive'
        db.delete_table('lizard_krw_executive')

        # Deleting model 'MeasurePeriod'
        db.delete_table('lizard_krw_measureperiod')

        # User chose to not deal with backwards NULL issues for 'FundingOrganization.price'
        raise RuntimeError("Cannot reverse this migration. 'FundingOrganization.price' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'FundingOrganization.funding_category'
        raise RuntimeError("Cannot reverse this migration. 'FundingOrganization.funding_category' and its values cannot be restored.")

        # Deleting field 'FundingOrganization.cost'
        db.delete_column('lizard_krw_fundingorganization', 'cost')

        # User chose to not deal with backwards NULL issues for 'Measure.area'
        raise RuntimeError("Cannot reverse this migration. 'Measure.area' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Measure.catchment_area_plan_value'
        raise RuntimeError("Cannot reverse this migration. 'Measure.catchment_area_plan_value' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Measure.type'
        raise RuntimeError("Cannot reverse this migration. 'Measure.type' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Measure.responsible_organization'
        raise RuntimeError("Cannot reverse this migration. 'Measure.responsible_organization' and its values cannot be restored.")

        # Adding field 'Measure.price'
        db.add_column('lizard_krw_measure', 'price', self.gf('django.db.models.fields.FloatField')(null=True, blank=True), keep_default=False)

        # Adding field 'Measure.need_co_funding'
        db.add_column('lizard_krw_measure', 'need_co_funding', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # User chose to not deal with backwards NULL issues for 'Measure.area_plan'
        raise RuntimeError("Cannot reverse this migration. 'Measure.area_plan' and its values cannot be restored.")

        # Adding field 'Measure.obligation_end_date'
        db.add_column('lizard_krw_measure', 'obligation_end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True), keep_default=False)

        # User chose to not deal with backwards NULL issues for 'Measure.responsible_department'
        raise RuntimeError("Cannot reverse this migration. 'Measure.responsible_department' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Measure.catchment_area_plan_unit'
        raise RuntimeError("Cannot reverse this migration. 'Measure.catchment_area_plan_unit' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Measure.catchment_area_plan'
        raise RuntimeError("Cannot reverse this migration. 'Measure.catchment_area_plan' and its values cannot be restored.")

        # Deleting field 'Measure.identity'
        db.delete_column('lizard_krw_measure', 'identity')

        # Deleting field 'Measure.category'
        db.delete_column('lizard_krw_measure', 'category_id')

        # Deleting field 'Measure.value'
        db.delete_column('lizard_krw_measure', 'value')

        # Deleting field 'Measure.unit'
        db.delete_column('lizard_krw_measure', 'unit_id')

        # Deleting field 'Measure.executive'
        db.delete_column('lizard_krw_measure', 'executive_id')

        # Deleting field 'Measure.total_costs'
        db.delete_column('lizard_krw_measure', 'total_costs')

        # Deleting field 'Measure.investment_costs'
        db.delete_column('lizard_krw_measure', 'investment_costs')

        # Deleting field 'Measure.exploitation_costs'
        db.delete_column('lizard_krw_measure', 'exploitation_costs')

        # Renaming column for 'Measure.code' to match new field type.
        db.rename_column('lizard_krw_measure', 'code_id', 'code')
        # Changing field 'Measure.code'
        db.alter_column('lizard_krw_measure', 'code', self.gf('django.db.models.fields.CharField')(max_length=80))


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
        'lizard_krw.measure': {
            'Meta': {'object_name': 'Measure'},
            'aggregation_type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_krw.MeasureCategory']"}),
            'code': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_krw.MeasureCode']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'executive': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_krw.Executive']"}),
            'exploitation_costs': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identity': ('django.db.models.fields.IntegerField', [], {}),
            'investment_costs': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'is_indicator': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_krw.Measure']", 'null': 'True', 'blank': 'True'}),
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
            'Meta': {'object_name': 'MeasureCode'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'lizard_krw.measureperiod': {
            'Meta': {'object_name': 'MeasurePeriod'},
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
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
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
