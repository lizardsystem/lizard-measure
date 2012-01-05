# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import simplejson
from django.template import defaultfilters
from django.template.defaultfilters import slugify
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.auth.models import User
from lxml import etree

import datetime
import os

from lizard_area.models import Area
from lizard_area.models import DataAdministrator


from lizard_measure.models import Measure
from lizard_measure.models import MeasureCategory
from lizard_measure.models import MeasureType
from lizard_measure.models import MeasurePeriod
from lizard_measure.models import MeasureStatus
from lizard_measure.models import MeasureStatusMoment
from lizard_measure.models import WaterBody
from lizard_measure.models import Organization
from lizard_measure.models import FundingOrganization
from lizard_measure.models import Unit
from lizard_measure.models import OWMStatus
from lizard_measure.models import OWMType

from lizard_geo.models import GeoObjectGroup


def _records(xml_filename):
    """
    Return a record generator

    Each yielded record is a dict with columnnames as keys
    """
    # Parse xml and find records
    print 'Parsing %s' % xml_filename
    tree = etree.parse(xml_filename)
    root = tree.getroot()
    record_elements = root.find('records')

    for record_element in record_elements:
        
        # Create record object
        record = dict([(column.get('name'), column.text)
                       for column in record_element])
        yield record

def _get_or_create(model, get_kwargs, extra_kwargs={}):
    """
    Return object, created_boolean
    """
    try:
        return model.objects.get(**get_kwargs), False
    except model.DoesNotExist:
        create_kwargs = get_kwargs
        create_kwargs.update(extra_kwargs)
        obj = model(**create_kwargs)
        obj.save()
        return obj, True


def _dates_from_xml(description):
    start_year, end_year = [int(y) for y in description.split('-')]
    start_date = datetime.date(year=start_year, month=1, day=1)
    end_date = datetime.date(year=end_year, month=1, day=1)
    return start_date, end_date


def import_waterbodies(filename, user, data_administrator):
    print 'Import waterbodies %s...' % filename
    geo_object_group_name = ('measure::waterbody::%s' %
                             os.path.basename(filename))
    try:
        print 'Finding existing geo object group...'
        geo_object_group = GeoObjectGroup.objects.get(
            name=geo_object_group_name)
        print 'Deleting existing geo object group...'
        geo_object_group.delete()
    except GeoObjectGroup.DoesNotExist:
        pass

    # Create geoobject group
    print 'Creating new geo object group...'
    print geo_object_group_name
    geo_object_group = GeoObjectGroup(
        name=geo_object_group_name[:128],
        slug=slugify(geo_object_group_name)[:50],
        created_by=user)
    geo_object_group.save()

    for record in _records(filename):

        # Create Area
        area = Area(
            # Fields from GeoObject
            ident=record['gafident'],
            geometry=GEOSGeometry(record['wkb_geometry']),
            geo_object_group=geo_object_group,

            # Fields from Communique
            name=record['gafnaam'],
            code=None,
            description=record['gafomsch'],

            # Fields from Area
            parent=None,
            data_administrator=data_administrator,
            area_class = Area.AREA_CLASS_KRW_WATERLICHAAM,
        )
        if not area.description:
            area.description = ''
        area.save()

        # Create WaterBody
        wb = WaterBody(
            area=area,
            name=record['gafnaam'],
            slug=slugify(record['gafnaam']),
            ident=record['gafident'],
            description=record['gafomsch'],
        )
        wb.save()


def import_measures(filename):
    for rec in _records(filename):

        measure_type, measure_type_created = MeasureType.objects.get_or_create(
            code=rec['matcode'],
        )

        unit, unit_created = Unit.objects.get_or_create(
            unit=rec['mateenh'],
        )

#       executive, executive_created = _get_or_create(
#           model=Organization,
#           get_kwargs={'name': rec['uitvoerder']},
#       )

        executive = Organization.objects.get(name=rec['uitvoerder'])


        datetime_in_source = datetime.datetime.strptime(
            rec['datum'],
            '%Y-%m-%d %H:%M:%S.%f',
        )

        import_raw_json = simplejson.dumps(
            rec,
            indent=4,
        )

        if rec['tijdvak'] == 'onbekend':
            period = None
        else:
            period = MeasurePeriod.objects.get(description=rec['tijdvak'])

        measure_kwargs = {
            # KRW matident => Measure.ident
            'ident': rec['matident'],
            'is_KRW_measure': True,
            # XY, geometry?
            'measure_type': measure_type,
            'title': rec['matnaam'],
            'period': period,
            'import_source': Measure.SOURCE_KRW_PORTAAL,
            'datetime_in_source': datetime_in_source,
            'import_raw': import_raw_json,
            'aggregation_type': Measure.AGGREGATION_TYPE_MIN,
            'description': rec['toelichting'],
            'value': rec['matomv'],
            'unit': unit,
            'investment_costs': rec['investkosten'],
            'exploitation_costs': rec['exploitkosten'],
            'initiator': None,
            'executive': executive,
        }

        measure = Measure(**measure_kwargs)
        measure.save()

        # Add some categories
        category_columns = [
            'wb21',
            'thema',
            'n2000',
            'n2000naam',
            'gwb',
            'gwbnaam',
        ]
        for c in category_columns:
            if rec[c] is None:
                continue
            category, category_created = _get_or_create(
                model=MeasureCategory,
                get_kwargs={'name': rec[c]},
            )
            measure.categories.add(category)

        # Add a measurestatusmoment for the status at import
        measure_status, measure_status_created = _get_or_create(
            model=MeasureStatus,
            get_kwargs={'name': rec['maatregelstatus']},
            extra_kwargs={'color': 'gray'},
        )
        measure_status_date = datetime.date(year=2010, month=1, day=1)
        measure_status_moment = MeasureStatusMoment(
            measure=measure,
            status=measure_status,
            date=measure_status_date,
            description='Import KRW portaal',
        )
        measure_status_moment.save()

        # Add fundingorganizations
        for n in ['1', '2', '3']:
            if rec['kostenpercent' + n] == '0':
                continue
            cost_carrier = rec['kostendrager' + n]
            cost_percentage =  float(rec['kostenpercent' + n])
            organization = Organization.objects.get(name=cost_carrier)            
            funding_organization = FundingOrganization(
                percentage=cost_percentage,
                organization=organization,
                measure=measure,
            )
            funding_organization.save()


def import_measure_types(filename):
    for rec in _records(filename):
        
        group = MeasureCategory.objects.get_or_create(
            name=rec['hoofdcategorie'],
        )[0]

        measure_type_kwargs = {
            'code': rec['code'],
            'description': rec['samengestelde_naam'],
            'group': group,  # Hoofdcategorie
            'klass': rec['klasse'],
            'subcategory': rec['subcategorie'],
            'harmonisation': rec['harmonisatie'],
            'combined_name': rec['samengestelde_naam'],
        }
        measure_type = MeasureType(**measure_type_kwargs)
        measure_type.save()
        
        # Add the units
        units = rec['eenheid'].split(', ')
        for u_str in units:
            unit_obj = Unit.objects.get_or_create(unit=u_str)[0]
            measure_type.units.add(unit_obj)


def import_KRW_lookup(filename):
    """
    Import various domains into seperate lizard_measure models
    """
    for rec in _records(filename):
        # Insert 'uitvoerders'
        if rec['domein'] == 'uitvoerder':
            organization, organization_created = _get_or_create(
                model=Organization,
                get_kwargs={'name': rec['description']},
            )
        # Insert 'matstatus'
        if rec['domein'] == 'Matstatus':
            measure_status, measure_status_created = _get_or_create(
                model=MeasureStatus,
                get_kwargs={'name': rec['description']},
                extra_kwargs={'color': 'gray'},
            )
        # Insert 'tijdvak'
        if rec['domein'] == 'tijdvak' and not rec['description'] == 'onbekend':
            start_date, end_date = _dates_from_xml(rec['description'])
            measure_period, measure_period_created = _get_or_create(
                model=MeasurePeriod,
                get_kwargs = {'start_date': start_date, 'end_date': end_date},
                extra_kwargs = {'description': rec['description']},
            )
        # Insert 'owmstat'
        if rec['domein'] == 'owmstat':
            owm_stat, owm_stat_created = _get_or_create(
                model=OWMStatus,
                get_kwargs={'code': rec['code']},
                extra_kwargs={'description': rec['description']},
            )
        # Insert 'owmtype'
        if rec['domein'] == 'owmtype':
            owm_type, owm_type_created = _get_or_create(
                model=OWMType,
                get_kwargs={'code': rec['code']},
                extra_kwargs={'description': rec['description']},
            )
        

class Command(BaseCommand):
    args = ''
    help = 'Import KRW portaal xml files'

    @transaction.commit_on_success
    def handle(self, *args, **options):
        if args:
            rel_path = args[0]
        else:
            rel_path = 'import_krw_portaal'
        import_path = os.path.join(settings.BUILDOUT_DIR, rel_path)
        print 'Importing KRW portaal xml files from %s.' % import_path

        user = User.objects.get(pk=1)

        # Rijnland WaterBodies
#       rijnland_administrator = DataAdministrator.objects.get(
#           name='Rijnland',
#       )
#       import_waterbodies(
#           filename=os.path.join(import_path, 'Gaf15.xml'),
#           user=user,
#           data_administrator=rijnland_administrator,
#       )
#       import_waterbodies(
#           filename=os.path.join(import_path, 'gaf45.xml'),
#           user=user,
#           data_administrator=rijnland_administrator,
#       )
        
        # HHNK WaterBodies
#       hhnk_administrator = DataAdministrator.objects.get(
#           name='HHNK',
#       )
#       import_waterbodies(
#           filename=os.path.join(import_path, 'gaf90.xml'),
#           user=user,
#           data_administrator=hhnk_administrator,
#       )

        # Import Lookups
        import_KRW_lookup(os.path.join(import_path, 'KRW_lookup.xml'))
        
        # Maatregeltypes (SGBP)
        import_measure_types(
            filename=os.path.join(
                import_path,
                'maatregelstandaard.xml',
            ),
        )

        # Import measures
        import_measures(os.path.join(import_path, 'maatregelen.xml'))

