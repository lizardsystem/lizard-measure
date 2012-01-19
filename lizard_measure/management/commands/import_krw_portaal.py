# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import simplejson
# from django.contrib.gis.geos import GEOSGeometry
from django.contrib.auth.models import User
from lxml import etree

import datetime
import os

from lizard_area.models import Area
from lizard_area.models import DataAdministrator


from lizard_measure.models import KRWStatus
from lizard_measure.models import KRWWatertype
from lizard_measure.models import WaterBody
from lizard_measure.models import Organization
from lizard_measure.models import Unit
from lizard_measure.models import MeasuringRod
from lizard_measure.models import Score
from lizard_measure.models import Measure
from lizard_measure.models import MeasureCategory
from lizard_measure.models import MeasureType
from lizard_measure.models import MeasurePeriod
from lizard_measure.models import MeasureStatus
from lizard_measure.models import MeasureStatusMoment
from lizard_measure.models import FundingOrganization


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
    Return object, created_boolean.

    TODO: Get rid of this method, since django's get_or_create
    does just the same. You need to specify the 'extra_kwargs'
    as a keyword argument 'defaults'...
    """
    try:
        return model.objects.get(**get_kwargs), False
    except model.DoesNotExist:
        create_kwargs = get_kwargs
        create_kwargs.update(extra_kwargs)
        obj = model(**create_kwargs)
        obj.save()
        return obj, True


def _to_float_or_none(xml_str):
    """
    Return float from str, replacing ',' by '.'.

    Return None if xml_str is None or unintelligible.
    """
    if xml_str is None:
        return None
    else:
        try:
            return float(xml_str.replace(',', '.'))
        except ValueError:
            return None


def _ascending_or_none(first, second):
    """
    Return first < second, or None if one or both arguments is None
    """
    if first is None or second is None:
        return None
    return first < second


def _area_or_none(area_ident):
    """
    Return Area object or None if it is not present.
    """
    try:
        return Area.objects.get(ident=area_ident)
    except Area.DoesNotExist:
        return None


def _dates_from_xml(description):
    start_year, end_year = [int(y) for y in description.split('-')]
    start_date = datetime.date(year=start_year, month=1, day=1)
    end_date = datetime.date(year=end_year, month=1, day=1)
    return start_date, end_date


def import_KRW_lookup(filename):
    """
    Import various domains into seperate lizard_measure models
    """
    for rec in _records(filename):
        # Insert 'uitvoerders'
        if rec['domein'] == 'uitvoerder':
            organization, organization_created = _get_or_create(
                model=Organization,
                get_kwargs={'description': rec['description']},
                extra_kwargs={
                    'source': Organization.SOURCE_KRW_PORTAL,
                }
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
                get_kwargs={'start_date': start_date, 'end_date': end_date},
                extra_kwargs={'description': rec['description']},
            )
        # Insert 'owmstat'
        if rec['domein'] == 'owmstat':
            owm_stat, owm_stat_created = _get_or_create(
                model=KRWStatus,
                get_kwargs={'code': rec['code']},
                extra_kwargs={'description': rec['description']},
            )
        # Insert 'owmtype'
        if rec['domein'] == 'owmtype':
            owm_type, owm_type_created = _get_or_create(
                model=KRWWatertype,
                get_kwargs={'code': rec['code']},
                extra_kwargs={'description': rec['description']},
            )


def import_measure_types(filename):
    for rec in _records(filename):

        group = MeasureCategory.objects.get_or_create(
            name=rec['hoofdcategorie'],
        )[0]

        extra_kwargs = {
            'description': rec['samengestelde_naam'],
            'group': group,  # Hoofdcategorie
            'klass': rec['klasse'],
            'subcategory': rec['subcategorie'],
            'harmonisation': rec['harmonisatie'],
            'combined_name': rec['samengestelde_naam'],
        }

        measure_type, measure_type_created = _get_or_create(
            model=MeasureType,
            get_kwargs={'code': rec['code']},
            extra_kwargs=extra_kwargs,
        )

        # Add the units
        units = rec['eenheid'].split(', ')
        for u_str in units:
            unit_obj = Unit.objects.get_or_create(code=u_str)[0]
            measure_type.units.add(unit_obj)


def import_waterbodies(filename, user, data_administrator):
#   geo_object_group_name = ('measure::waterbody::%s' %
#                            os.path.basename(filename))
#   try:
#       print 'Finding existing geo object group...'
#       geo_object_group = GeoObjectGroup.objects.get(
#           name=geo_object_group_name)
#       print 'Deleting existing geo object group...'
#       geo_object_group.delete()
#   except GeoObjectGroup.DoesNotExist:
#       pass

    # Create geoobject group
#   geo_object_group = GeoObjectGroup(
#       name=geo_object_group_name,
#       slug=slugify(os.path.basename(filename).split('.')[-2]),
#       created_by=user,
#   )
#   geo_object_group.save()

    for rec in _records(filename):

        # Get or create Area
#       ident = rec['owmident'].strip()
#       geometry = GEOSGeometry('POINT(0 0)')  # Dummy geometry

#       # Fields from Communique
#       name = rec['owmnaam'].strip()
#       code = None
#       description = ''  # Check this one. I thought there was a description.

#       # Fields from Area
#       parent = None
#       data_administrator=data_administrator
#       area_class = Area.AREA_CLASS_KRW_WATERLICHAAM,
#       area, area_created = _get_or_create(
#           model=Area,
#           get_kwargs={'ident': ident},
#           extra_kwargs={
#               'geometry': geometry,
#               'geo_object_group': geo_object_group,
#               'name': name,
#               'code': code,
#               'description': description,
#               'parent': parent,
#               'data_administrator': data_administrator,
#               'area_class': Area.AREA_CLASS_KRW_WATERLICHAAM,
#           },
#       )

        # Try to get Area
        area_ident = rec['owmident'].strip()
        area = _area_or_none(area_ident)

        # Create WaterBody
        krw_status = KRWStatus.objects.get(code=rec['owmstat'].strip())
        krw_watertype = KRWWatertype.objects.get(code=rec['owmtype'].strip())
        waterbody, waterbody_created = _get_or_create(
            model=WaterBody,
            get_kwargs={'area_ident': area_ident},
            extra_kwargs={
                'area': area,
                'krw_status': krw_status,
                'krw_watertype': krw_watertype,
            },
        )


def import_measuring_rods(filename):
    for rec in _records(filename):
        # Only import EKR-scores
        if not (rec['eenheid'] == 'EKR' and rec['deelmaatlat'] == 'Totaal'):
            continue

        measuring_rod, measuring_rod_created = _get_or_create(
            model=MeasuringRod,
            get_kwargs={'id': rec['id']},
            extra_kwargs={
                'group': rec['groep'],
                'measuring_rod': rec['maatlat'],
                'sub_measuring_rod': rec['deelmaatlat'],
                'unit': rec['eenheid'],
                'sign': rec['teken'],
            }
        )


def import_scores(filename):
    for rec in _records(filename):

        # Only import if MeasuringRod is imported
        if not MeasuringRod.objects.filter(id=rec['maatlat']).exists():
            continue

        # Try to get Area
        area_ident = rec['owmident'].strip()
        area = _area_or_none(area_ident)

        measuring_rod = MeasuringRod.objects.get(id=rec['maatlat'])
        mep = _to_float_or_none(rec['mep'])
        gep = _to_float_or_none(rec['gep'])
        limit_bad_insufficient = _to_float_or_none(rec['ontoereikend'])
        limit_insufficient_moderate = _to_float_or_none(rec['matig'])

        ascending = _ascending_or_none(
            limit_bad_insufficient,
            limit_insufficient_moderate,
        )

        target_2015 = _to_float_or_none(rec['doel2015'])
        target_2027 = _to_float_or_none(rec['doel2027'])

        #  Note that I assume that area and measuring_rod together
        #  uniquely define the score.
        score, score_created = _get_or_create(
            model=Score,
            get_kwargs={
                'measuring_rod': measuring_rod,
                'area_ident': area_ident,
            },
            extra_kwargs={
                'area': area,
                'mep': mep,
                'gep': gep,
                'limit_insufficient_moderate': limit_insufficient_moderate,
                'limit_bad_insufficient': limit_bad_insufficient,
                'ascending': ascending,
                'target_2015': target_2015,
                'target_2027': target_2027,
            },
        )


def import_measures(filename):
    for rec in _records(filename):

        measure_type, measure_type_created = MeasureType.objects.get_or_create(
            code=rec['matcode'],
        )

        unit, unit_created = Unit.objects.get_or_create(
            code=rec['mateenh'],
        )

        # vvv Decided from examination of screenshots from KRW portal
        initiator = Organization.objects.get(description=rec['uitvoerder'])

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
            'geometry': None,
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
            'executive': None,
            'initiator': initiator,

        }

        measure = Measure(**measure_kwargs)
        measure.save()

        # Add waterbodies
        # They can be None, or single, or comma separated
        if rec['locatie'] is None:
            locations = []
        else:
            locations = rec['locatie'].split(', ')
        for area_ident in locations:
            if area_ident.startswith('NL'):
                corrected_area_ident = area_ident
            else:
                corrected_area_ident = 'NL' + area_ident
            waterbody = WaterBody.objects.get(
                area_ident=corrected_area_ident,
            )
            waterbody.save()
            measure.waterbodies.add(waterbody)

        # Add some categories
        boolean_categories = [
            'wb21',
            'n2000',
            'gwb',
        ]
        for c in boolean_categories:
            if rec[c] == 1:
                category, category_created = _get_or_create(
                    model=MeasureCategory,
                    get_kwargs={'naam': c},
                )
                measure.categories.add(category)
        if rec['thema'] is not None:
            category, category_created = _get_or_create(
                model=MeasureCategory,
                get_kwargs={'name': rec['thema']},
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
            cost_percentage = _to_float_or_none(rec['kostenpercent' + n])
            organization = Organization.objects.get(description=cost_carrier)
            funding_organization = FundingOrganization(
                percentage=cost_percentage,
                organization=organization,
                measure=measure,
            )
            funding_organization.save()


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

        # Import Lookups
        import_KRW_lookup(os.path.join(import_path, 'KRW_lookup.xml'))

        # Maatregeltypes (SGBP)
        import_measure_types(
            filename=os.path.join(
                import_path,
                'maatregelstandaard.xml',
            ),
        )

        # Waterbodies
        owm_sources = [
            ('HHNK', 'owmhhnk.xml'),
            ('Waternet', 'OWMwaternet.xml'),
            ('Rijnland', 'owmrijnland.xml'),
        ]

        for admin_name, xml_file in owm_sources:
            administrator = DataAdministrator.objects.get(name=admin_name)
            import_waterbodies(
                filename=os.path.join(import_path, xml_file),
                user=user,
                data_administrator=administrator,
            )

        # Import MeasuringRods
        import_measuring_rods(os.path.join(import_path, 'maatlatten.xml'))

        # Import scores
        Score.objects.all().delete()
        score_sources = [
            'doelenhhnk.xml',
            'doelenrijnland.xml',
            'doelenwaternet.xml',
        ]

        for xml_file in score_sources:
            import_scores(
                filename=os.path.join(import_path, xml_file),
            )

        # Import measures
        import_measures(os.path.join(import_path, 'maatregelen.xml'))
