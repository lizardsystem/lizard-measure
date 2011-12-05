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

from lizard_measure.models import Measure
from lizard_measure.models import MeasureCategory
from lizard_measure.models import MeasureCode
from lizard_measure.models import Executive
from lizard_measure.models import MeasurePeriod
from lizard_measure.models import MeasureStatus
from lizard_measure.models import WaterBody

from lizard_geo.models import GeoObjectGroup


def import_waterbodies(filename, user):
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

    print 'Creating new geo object group...'
    print geo_object_group_name
    geo_object_group = GeoObjectGroup(
        name=geo_object_group_name[:128],
        slug=slugify(geo_object_group_name)[:50],
        created_by=user)
    geo_object_group.save()

    tree = etree.parse(filename)
    root = tree.getroot()
    records = root.find('records')
    for record in records:
        record_data = {}
        for column in record:
            record_data[column.get('name')] = column.text
        wb = WaterBody(
            ident=record_data['gafident'],
            geo_object_group=geo_object_group,
            geometry=GEOSGeometry(record_data['wkb_geometry']),
            name=record_data['gafnaam'],
            slug=slugify(record_data['gafnaam']),
            description=record_data['gafomsch'])
        wb.save()


def import_maatregelen(filename):
    print 'Import maatregelen %s...' % filename
    tree = etree.parse(filename)
    root = tree.getroot()
    header = root.find('header')
    records = root.find('records')
    for record in records:
        record_data = {}
        for column in record:
            record_data[column.get('name')] = column.text
        try:
            measure = Measure.objects.get(identity=record_data['matident'])
        except Measure.DoesNotExist:
            measure = Measure(identity=record_data['matident'])
        waterbody = WaterBody.objects.get(ident=record_data['gafident'])
        category = Category.objects.all()[0]  # Don't know...
        code, code_created = MeasureCode.objects.get_or_create(
            code=record_data['matcode'])
        if code_created:
            print 'Warning: code %s created, check manually' % code
        unit, unit_created = Unit.objects.get_or_create(
            sign=record_data['mateenh'])
        if unit_created:
            print 'Warning: unit %s created, check manually' % unit
        executive, executive_created = Executive.objects.get_or_create(
            name=record_data['uitvoerder'])
        if executive_created:
            print 'Warning: executive %s created, check manually' % executive
        measure.waterbody = waterbody
        measure.name = record_data['matnaam']
        measure.description = record_data['toelichting']
        measure.category = category
        measure.code = code
        measure.value = record_data['matomv']
        measure.unit = unit
        measure.executive = executive
        measure.save()


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

        import_waterbodies(os.path.join(import_path, 'Gaf15.xml'), user)
        import_waterbodies(os.path.join(import_path, 'gaf45.xml'), user)
        import_waterbodies(os.path.join(import_path, 'gaf90.xml'), user)
        import_maatregelen(os.path.join(import_path, 'maatregelen.xml'))
