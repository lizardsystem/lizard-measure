# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ESFPattern'
        db.create_table('lizard_measure_esfpattern', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('watertype_group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', null=True, to=orm['lizard_measure.WatertypeGroup'])),
            ('data_set', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', null=True, to=orm['lizard_security.DataSet'])),
        ))
        db.send_create_signal('lizard_measure', ['ESFPattern'])

        # Adding M2M table for field measure_types on 'ESFPattern'
        db.create_table('lizard_measure_esfpattern_measure_types', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('esfpattern', models.ForeignKey(orm['lizard_measure.esfpattern'], null=False)),
            ('measuretype', models.ForeignKey(orm['lizard_measure.measuretype'], null=False))
        ))
        db.create_unique('lizard_measure_esfpattern_measure_types', ['esfpattern_id', 'measuretype_id'])

        # Adding model 'WatertypeGroup'
        db.create_table('lizard_measure_watertypegroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
        ))
        db.send_create_signal('lizard_measure', ['WatertypeGroup'])

        # Adding field 'KRWWatertype.watertype_group'
        db.add_column('lizard_measure_krwwatertype', 'watertype_group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='watertypes', null=True, to=orm['lizard_measure.WatertypeGroup']), keep_default=False)


    def backwards(self, orm):
        
        # Deleting model 'ESFPattern'
        db.delete_table('lizard_measure_esfpattern')

        # Removing M2M table for field measure_types on 'ESFPattern'
        db.delete_table('lizard_measure_esfpattern_measure_types')

        # Deleting model 'WatertypeGroup'
        db.delete_table('lizard_measure_watertypegroup')

        # Deleting field 'KRWWatertype.watertype_group'
        db.delete_column('lizard_measure_krwwatertype', 'watertype_group_id')


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
            'area_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'communique_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['lizard_area.Communique']", 'unique': 'True', 'primary_key': 'True'}),
            'data_administrator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_area.DataAdministrator']", 'null': 'True', 'blank': 'True'}),
            'data_set': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_security.DataSet']", 'null': 'True', 'blank': 'True'}),
            'dt_created': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 2, 21, 15, 44, 12, 613020)'}),
            'dt_latestchanged': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'dt_latestsynchronized': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_area.Area']", 'null': 'True', 'blank': 'True'})
        },
        'lizard_area.communique': {
            'Meta': {'object_name': 'Communique', '_ormbases': ['lizard_geo.GeoObject']},
            'areasort': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'areasort_krw': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'dt_latestchanged_krw': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'edited_at': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'edited_by': ('django.db.models.fields.TextField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'geoobject_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['lizard_geo.GeoObject']", 'unique': 'True', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'surface': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '1', 'blank': 'True'}),
            'watertype_krw': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'lizard_area.dataadministrator': {
            'Meta': {'object_name': 'DataAdministrator'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        'lizard_fewsnorm.fewsnormsource': {
            'Meta': {'object_name': 'FewsNormSource'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'database_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'database_schema_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        'lizard_fewsnorm.geolocationcache': {
            'Meta': {'ordering': "('ident', 'name')", 'object_name': 'GeoLocationCache', '_ormbases': ['lizard_geo.GeoObject']},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'data_set': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_security.DataSet']", 'null': 'True', 'blank': 'True'}),
            'fews_norm_source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_fewsnorm.FewsNormSource']"}),
            'geoobject_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['lizard_geo.GeoObject']", 'unique': 'True', 'primary_key': 'True'}),
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'module': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['lizard_fewsnorm.ModuleCache']", 'null': 'True', 'through': "orm['lizard_fewsnorm.TimeSeriesCache']", 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'parameter': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['lizard_fewsnorm.ParameterCache']", 'null': 'True', 'through': "orm['lizard_fewsnorm.TimeSeriesCache']", 'blank': 'True'}),
            'shortname': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'timestep': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['lizard_fewsnorm.TimeStepCache']", 'null': 'True', 'through': "orm['lizard_fewsnorm.TimeSeriesCache']", 'blank': 'True'}),
            'tooltip': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'lizard_fewsnorm.modulecache': {
            'Meta': {'ordering': "('ident',)", 'object_name': 'ModuleCache'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ident': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'lizard_fewsnorm.parametercache': {
            'Meta': {'ordering': "('ident',)", 'object_name': 'ParameterCache'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ident': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'lizard_fewsnorm.qualifiersetcache': {
            'Meta': {'ordering': "('ident',)", 'object_name': 'QualifierSetCache'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ident': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'lizard_fewsnorm.timeseriescache': {
            'Meta': {'object_name': 'TimeSeriesCache'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'geolocationcache': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_fewsnorm.GeoLocationCache']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modulecache': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_fewsnorm.ModuleCache']"}),
            'parametercache': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_fewsnorm.ParameterCache']"}),
            'qualifiersetcache': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_fewsnorm.QualifierSetCache']", 'null': 'True', 'blank': 'True'}),
            'timestepcache': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_fewsnorm.TimeStepCache']"})
        },
        'lizard_fewsnorm.timestepcache': {
            'Meta': {'ordering': "('ident',)", 'object_name': 'TimeStepCache'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ident': ('django.db.models.fields.CharField', [], {'max_length': '64'})
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
        'lizard_measure.esflink': {
            'Meta': {'unique_together': "(('measure', 'esf'),)", 'object_name': 'EsfLink'},
            'esf': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_target_esf': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'measure': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.Measure']"}),
            'negative': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'positive': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'})
        },
        'lizard_measure.esfpattern': {
            'Meta': {'object_name': 'ESFPattern'},
            'data_set': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['lizard_security.DataSet']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'measure_types': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'+'", 'null': 'True', 'to': "orm['lizard_measure.MeasureType']"}),
            'watertype_group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['lizard_measure.WatertypeGroup']"})
        },
        'lizard_measure.fundingorganization': {
            'Meta': {'object_name': 'FundingOrganization'},
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'measure': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.Measure']"}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.Organization']"}),
            'percentage': ('django.db.models.fields.FloatField', [], {})
        },
        'lizard_measure.horizontalbargraph': {
            'Meta': {'object_name': 'HorizontalBarGraph'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'x_label': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'y_label': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'})
        },
        'lizard_measure.horizontalbargraphitem': {
            'Meta': {'ordering': "('-index',)", 'object_name': 'HorizontalBarGraphItem'},
            'horizontal_bar_graph': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.HorizontalBarGraph']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_fewsnorm.GeoLocationCache']", 'null': 'True', 'blank': 'True'}),
            'measuring_rod': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.MeasuringRod']", 'null': 'True', 'blank': 'True'}),
            'module': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_fewsnorm.ModuleCache']", 'null': 'True', 'blank': 'True'}),
            'parameter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_fewsnorm.ParameterCache']", 'null': 'True', 'blank': 'True'}),
            'qualifierset': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_fewsnorm.QualifierSetCache']", 'null': 'True', 'blank': 'True'}),
            'time_step': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_fewsnorm.TimeStepCache']", 'null': 'True', 'blank': 'True'})
        },
        'lizard_measure.krwstatus': {
            'Meta': {'object_name': 'KRWStatus'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'valid': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        'lizard_measure.krwwatertype': {
            'Meta': {'object_name': 'KRWWatertype'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'valid': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'watertype_group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'watertypes'", 'null': 'True', 'to': "orm['lizard_measure.WatertypeGroup']"})
        },
        'lizard_measure.measure': {
            'Meta': {'ordering': "('id',)", 'object_name': 'Measure'},
            'aggregation_type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'areas': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'area_measure_set'", 'blank': 'True', 'to': "orm['lizard_area.Area']"}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lizard_measure.MeasureCategory']", 'symmetrical': 'False', 'blank': 'True'}),
            'data_set': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_security.DataSet']", 'null': 'True', 'blank': 'True'}),
            'datetime_in_source': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'executive': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'executive_measure_set'", 'null': 'True', 'to': "orm['lizard_measure.Organization']"}),
            'exploitation_costs': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'funding_organizations': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lizard_measure.Organization']", 'through': "orm['lizard_measure.FundingOrganization']", 'symmetrical': 'False'}),
            'geom': ('django.contrib.gis.db.models.fields.GeometryField', [], {'null': 'True', 'blank': 'True'}),
            'geometry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_geo.GeoObject']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ident': ('django.db.models.fields.CharField', [], {'max_length': '64', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'import_raw': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'import_source': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            'in_sgbp': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'initiator': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'initiator_measure_set'", 'null': 'True', 'to': "orm['lizard_measure.Organization']"}),
            'investment_costs': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'is_KRW_measure': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_indicator': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'land_costs': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'measure_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.MeasureType']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.Measure']", 'null': 'True', 'blank': 'True'}),
            'period': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.MeasurePeriod']", 'null': 'True', 'blank': 'True'}),
            'read_only': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'responsible_department': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'status_moments': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lizard_measure.MeasureStatus']", 'through': "orm['lizard_measure.MeasureStatusMoment']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'total_costs': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.Unit']"}),
            'valid': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {}),
            'waterbodies': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lizard_measure.WaterBody']", 'symmetrical': 'False', 'blank': 'True'})
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
            'valid': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'lizard_measure.measurestatus': {
            'Meta': {'ordering': "('-value',)", 'object_name': 'MeasureStatus'},
            'color': ('lizard_map.models.ColorField', [], {'max_length': '8'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'valid': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {'default': '0.0'})
        },
        'lizard_measure.measurestatusmoment': {
            'Meta': {'ordering': "('measure__id', 'status__value')", 'object_name': 'MeasureStatusMoment'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'exploitation_expenditure': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'investment_expenditure': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'measure': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.Measure']"}),
            'planning_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'realisation_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.MeasureStatus']"})
        },
        'lizard_measure.measuretype': {
            'Meta': {'ordering': "('code',)", 'object_name': 'MeasureType'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'combined_name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'group': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'harmonisation': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'klass': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'subcategory': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'units': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lizard_measure.Unit']", 'symmetrical': 'False', 'blank': 'True'}),
            'valid': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        'lizard_measure.measuringrod': {
            'Meta': {'object_name': 'MeasuringRod'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '32', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'measuring_rod': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'measuring_rod_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.MeasuringRod']", 'null': 'True', 'blank': 'True'}),
            'sign': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'sub_measuring_rod': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'valid': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        'lizard_measure.organization': {
            'Meta': {'ordering': "('description',)", 'unique_together': "(('source', 'code'),)", 'object_name': 'Organization'},
            'code': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.CharField', [], {'default': "'Lokaal'", 'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'valid': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
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
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'conversion_factor': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'dimension': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'valid': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        'lizard_measure.waterbody': {
            'Meta': {'object_name': 'WaterBody'},
            'area': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_area.Area']", 'null': 'True', 'blank': 'True'}),
            'area_ident': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'krw_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.KRWStatus']", 'null': 'True', 'blank': 'True'}),
            'krw_watertype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lizard_measure.KRWWatertype']", 'null': 'True', 'blank': 'True'})
        },
        'lizard_measure.watertypegroup': {
            'Meta': {'object_name': 'WatertypeGroup'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'lizard_security.dataset': {
            'Meta': {'ordering': "['name']", 'object_name': 'DataSet'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'})
        }
    }

    complete_apps = ['lizard_measure']
