# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Measure.measure_collection'
        db.add_column('lizard_krw_measure', 'measure_collection', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lizard_krw.MeasureCollection'], null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Measure.measure_collection'
        db.delete_column('lizard_krw_measure', 'measure_collection_id')


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
            'Meta': {'ordering': "['-min_value']", 'object_name': 'AlphaScore'},
            'color': ('lizard_map.models.ColorField', [], {'default': "'808080'", 'max_length': '8'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_value': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'min_value': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'lizard_krw.area': {
            'Meta': {'object_name': 'Area'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'lizard_krw.department': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Department'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_krw.Organization']", 'null': 'True', 'blank': 'True'})
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
            'Meta': {'ordering': "('start_date', 'waterbody', 'category')", 'object_name': 'GoalScore'},
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
            'exploitation_costs': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identity': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'investment_costs': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'is_indicator': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'measure_collection': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_krw.MeasureCollection']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_krw.Measure']", 'null': 'True', 'blank': 'True'}),
            'period': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_krw.MeasurePeriod']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lizard_krw.MeasureStatus']", 'through': "orm['lizard_krw.MeasureStatusMoment']", 'symmetrical': 'False'}),
            'total_costs': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
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
        'lizard_krw.measurecollection': {
            'Meta': {'object_name': 'MeasureCollection'},
            'area': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['lizard_krw.Area']", 'null': 'True', 'blank': 'True'}),
            'estimated_costs_internal': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'estimated_costs_total': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'need_co_funding': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'responsible_department': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_krw.Department']"}),
            'responsible_organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_krw.Organization']"}),
            'shortname': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'urgency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_krw.Urgency']"}),
            'waterbody': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_krw.WaterBody']"})
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
            'color': ('lizard_map.models.ColorField', [], {'max_length': '8'}),
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
        'lizard_krw.municipality': {
            'Meta': {'object_name': 'Municipality'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'lizard_krw.organization': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Organization'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'lizard_krw.province': {
            'Meta': {'object_name': 'Province'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'lizard_krw.score': {
            'Meta': {'ordering': "('start_date', 'waterbody', 'category')", 'object_name': 'Score'},
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
        'lizard_krw.urgency': {
            'Meta': {'ordering': "('-value',)", 'object_name': 'Urgency'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'lizard_krw.waterbody': {
            'Meta': {'ordering': "('name',)", 'object_name': 'WaterBody'},
            'area': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['lizard_krw.Area']", 'null': 'True', 'blank': 'True'}),
            'characteristics': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'control_parameters': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'current_situation_chemicals': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ident': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'municipality': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['lizard_krw.Municipality']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'protected_area_reason': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'province': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['lizard_krw.Province']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_krw.WaterBodyStatus']", 'null': 'True', 'blank': 'True'}),
            'water_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_krw.KRWWaterType']", 'null': 'True', 'blank': 'True'})
        },
        'lizard_krw.waterbodystatus': {
            'Meta': {'object_name': 'WaterBodyStatus'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'})
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
