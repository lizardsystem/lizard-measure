# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.template import defaultfilters
from django.template.defaultfilters import slugify
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.auth.models import User
from lxml import etree
import os

from lizard_area.models import Area
from lizard_area.models import DataAdministrator


from lizard_measure.models import Measure
from lizard_measure.models import MeasureCategory
from lizard_measure.models import MeasureType
from lizard_measure.models import Executive
from lizard_measure.models import MeasurePeriod
from lizard_measure.models import MeasureStatus
from lizard_measure.models import WaterBody
from lizard_measure.models import Unit

from lizard_geo.models import GeoObjectGroup


def _records(xml_filename):
    """
    Return a record generator

    Each yielded record is a dict with columnnames as keys
    """
    # Parse xml and find records
    tree = etree.parse(xml_filename)
    root = tree.getroot()
    record_elements = root.find('records')

    for record_element in record_elements:
        
        # Create record object
        record = dict([(column.get('name'), column.text)
                       for column in record_element])
        yield record

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


def import_maatregelen(filename):
    print 'Import maatregelen %s...' % filename
    for record in _records(filename):

        # KRW matident => Measure.ident
        measure = Measure()
        measure.ident = record['matident']

        measure.is_KRW_measure = True

        import_source = Measure.SOURCE_KRW_PORTAAL

        # XY, geometry?

        



        





        # gafident has 'NL' added to it.
        # Sometimes multiple occurences are present.
        waterbody = WaterBody.objects.filter(
            ident=record['gafident'][2:])[0]
        category = MeasureCategory.objects.all()[0]  # Don't know...
        code, code_created = MeasureCode.objects.get_or_create(
            code=record['matcode'])
        if code_created:
            print 'Warning: code %s created, check manually' % code
        unit, unit_created = Unit.objects.get_or_create(
            sign=record['mateenh'])
        if unit_created:
            print 'Warning: unit %s created, check manually' % unit
        executive, executive_created = Executive.objects.get_or_create(
            name=record['uitvoerder'])
        if executive_created:
            print 'Warning: executive %s created, check manually' % executive
        measure.waterbody = waterbody
        measure.name = record['matnaam'][:200]
        measure.description = (record['toelichting'][:200]
                               if record['toelichting'] else '')
        measure.category = category
        measure.code = code
        measure.value = record['matomv']  # Floatfield??
        measure.unit = unit
        measure.executive = executive
        measure.save()


def import_measure_codes(filename):
    for r in _records(filename):
        
        group = MeasureCategory.objects.get_or_create(
            name=r['hoofdcategorie'],
        )[0]

        measure_type_kwargs = {
            'code': r['code'],
            'description': r['samengestelde_naam'],
            'group': group,  # Hoofdcategorie
            'klass': r['klasse'],
            'subcategory': r['subcategorie'],
            'harmonisation': r['harmonisatie'],
            'combined_name': r['samengestelde_naam'],
        }
        measure_type = MeasureType(*measure_type_kwargs)
        #measure_type.save()
        
        # Add the units
        units = r['eenheid'].split(', ')
        for u_str in units:
            unit_obj = Unit.objects.get_or_create(unit=u_str)[0]
            measure_type.units.add(unit_obj)


class Command(BaseCommand):
    args = ''
    help = 'Import KRW portaal xml files'

    @transaction.commit_on_success
    def handle(self, *args, **options):
        print 'Import KRW portaal'
        if args:
            rel_path = args[0]
        else:
            rel_path = 'import_krw_portaal'
        import_path = os.path.join(settings.BUILDOUT_DIR, rel_path)
        print import_path

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
        
        # Maatregelcodes (SGBP)
        import_measure_codes(
            filename=os.path.join(
                import_path,
                'maatregelstandaard.xml',
            ),
        )

        # Import measures
#       import_maatregelen(os.path.join(import_path, 'maatregelen.xml'))
