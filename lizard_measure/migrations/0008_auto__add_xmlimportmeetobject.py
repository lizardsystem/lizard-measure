# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'XMLImportMeetobject'
        db.create_table('lizard_measure_xmlimportmeetobject', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('lizard_measure', ['XMLImportMeetobject'])

        # Adding M2M table for field waterbodies on 'XMLImportMeetobject'
        db.create_table('lizard_measure_xmlimportmeetobject_waterbodies', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('xmlimportmeetobject', models.ForeignKey(orm['lizard_measure.xmlimportmeetobject'], null=False)),
            ('waterbody', models.ForeignKey(orm['lizard_measure.waterbody'], null=False))
        ))
        db.create_unique('lizard_measure_xmlimportmeetobject_waterbodies', ['xmlimportmeetobject_id', 'waterbody_id'])


    def backwards(self, orm):
        
        # Deleting model 'XMLImportMeetobject'
        db.delete_table('lizard_measure_xmlimportmeetobject')

        # Removing M2M table for field waterbodies on 'XMLImportMeetobject'
        db.delete_table('lizard_measure_xmlimportmeetobject_waterbodies')


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
        'lizard_measure.alphascore': {
            'Meta': {'ordering': "['-min_value']", 'object_name': 'AlphaScore'},
            'color': ('lizard_map.models.ColorField', [], {'default': "'808080'", 'max_length': '8'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_value': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'min_value': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
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
        'lizard_measure.goalscore': {
            'Meta': {'ordering': "('start_date', 'waterbody', 'category')", 'object_name': 'GoalScore'},
            'category': ('django.db.models.fields.IntegerField', [], {}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'value': ('django.db.models.fields.FloatField', [], {}),
            'waterbody': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.WaterBody']"})
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
            'read_only': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
        'lizard_measure.score': {
            'Meta': {'ordering': "('start_date', 'waterbody', 'category')", 'object_name': 'Score'},
            'category': ('django.db.models.fields.IntegerField', [], {}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'value': ('django.db.models.fields.FloatField', [], {}),
            'waterbody': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.WaterBody']"})
        },
        'lizard_measure.singleindicator': {
            'Meta': {'object_name': 'SingleIndicator'},
            'boundary_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'target_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'timeserie_id': ('django.db.models.fields.IntegerField', [], {}),
            'water_body': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'indicators'", 'to': "orm['lizard_measure.WaterBody']"}),
            'y_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'y_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
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
            'Meta': {'ordering': "('name',)", 'object_name': 'WaterBody', '_ormbases': ['lizard_geo.GeoObject']},
            'area': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['lizard_measure.Area']", 'null': 'True', 'blank': 'True'}),
            'characteristics': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'control_parameters': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'current_situation_chemicals': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'geoobject_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['lizard_geo.GeoObject']", 'unique': 'True', 'primary_key': 'True'}),
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
        },
        'lizard_measure.xmlimportmeetobject': {
            'Meta': {'object_name': 'XMLImportMeetobject'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'waterbodies': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lizard_measure.WaterBody']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['lizard_measure']
