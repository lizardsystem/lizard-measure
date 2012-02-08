# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import simplejson
from django.template.defaultfilters import slugify

from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import LineString
from django.contrib.gis.geos import MultiLineString
from django.contrib.gis.geos import Polygon
from django.contrib.gis.geos import MultiPolygon
from django.contrib.gis.gdal import SpatialReference
from django.contrib.gis.gdal import CoordTransform

from lizard_map.coordinates import RD
from lizard_map.coordinates import WGS84

from django.contrib.auth.models import User
from lxml import etree

import datetime
import os

from lizard_area.models import Area
from lizard_area.models import Category
from lizard_area.models import DataAdministrator

from lizard_geo.models import GeoObjectGroup

from lizard_security.models import DataSet

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


def _clear_all():
    """
    Clear all objects related to measures.
    """
    KRWStatus.objects.all().delete()
    KRWWatertype.objects.all().delete()
    WaterBody.objects.all().delete()
    Organization.objects.filter(
        source=Organization.SOURCE_KRW_PORTAL,
    ).delete()
    Unit.objects.all().delete()
    MeasuringRod.objects.all().delete()
    Score.objects.all().delete()
    Measure.objects.all().delete()
    MeasureCategory.objects.all().delete()
    MeasureType.objects.all().delete()
    MeasurePeriod.objects.all().delete()
    MeasureStatus.objects.all().delete()
    MeasureStatusMoment.objects.all().delete()
    FundingOrganization.objects.all().delete()


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


def _combine(geometries):
    """
    Try to combine geometries with least computing power necessary.

    If there are both lines and polygons, all lines are first buffered
    one by one into polygons, and then added to a MultiPolygon together
    with the other polygons.

    If there are only polygons, they are combined in a single
    multipolygon.

    If there are only lines, they are combined in a single multilinestring
    """
    if len(geometries) == 1:
        return geometries[0]

    lines = [g for g in geometries
             if isinstance(g, (LineString))]
    multilines = [g for g in geometries
             if isinstance(g, (MultiLineString))]
    polygons = [g for g in geometries
                if isinstance(g, (Polygon))]
    multipolygons = [g for g in geometries
                if isinstance(g, (MultiPolygon))]

    if polygons or multipolygons:
        if lines or multilines:
            # All kinds of stuff present
            lines.extend([l for ml in multilines for l in ml])
            print 'buffering lines'
            for l in lines:
                polygons.append(l.buffer(0.0001, 2))
        result = MultiPolygon(polygons)
        for mp in multipolygons:
            result.extend(mp)
    else:
        # Only lines or multilines
        result = MultiLineString(lines)
        for ml in multilines:
            result.extend(ml)

    return result


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
        if rec['domein'] == 'matstatus':
            measure_status, measure_status_created = _get_or_create(
                model=MeasureStatus,
                get_kwargs={'name': rec['description']},
                extra_kwargs={
                    'color': 'gray',
                    'valid': True,
                },
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

#       group = MeasureCategory.objects.get_or_create(
#           name=rec['hoofdcategorie'],
#       )[0]

        extra_kwargs = {
            'description': rec['samengestelde_naam'],
            'group': rec['hoofdcategorie'],
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


def import_waterbodies(wb_import_settings):
    """
    Create geoobjects and waterbodies.
    """
    owmsources = wb_import_settings['owm_sources']

    # Reset geo object groups
    geogroups = {}
    category = Category.objects.get(slug='krw-waterlichamen')

    for s in wb_import_settings['owm_sources']:
        # Determine geoobject group name
        geo_object_group_name = ('measure::waterbody::%s' %
                                 os.path.basename(s['file']))

        # Remove geoobject group by name if it exists
        try:
            print 'Finding existing geoobject group named %s' % (
                geo_object_group_name,
            )
            geo_object_group = GeoObjectGroup.objects.get(
                name=geo_object_group_name)
            print 'Deleting existing geoobject group named %s' % (
                geo_object_group_name,
            )
            geo_object_group.delete()
        except GeoObjectGroup.DoesNotExist:
            pass

        # Create new geoobject group with that name
        geo_object_group = GeoObjectGroup(
            name=geo_object_group_name,
            slug=slugify(os.path.basename(s['file']).split('.')[-2]),
            created_by=s['user'],
        )
        geo_object_group.save()

        # Add this geoobject group to lizard_area category of waterbodies
        category.geo_object_groups.add(geo_object_group)

        # Keep a dict of geo_object_groups for later assignment
        geogroups[s['data_administrator'].name] = geo_object_group

    # Make a mapping of owmidents to sets of owaidents
    # There are multiple owaidents per owmident
    owa_idents = {}
    for rec in _records(wb_import_settings['link_file']):
        owm = rec['owmident']
        owa = rec['owaident']
        if owm not in owa_idents:
            owa_idents[owm] = []
        owa_idents[owm].append(owa)

    # Loop geofile, create geometry object for each geometry
    owa_geometry = {}
    spatialreference_wgs84 = SpatialReference(WGS84)
    spatialreference_rd = SpatialReference(RD)
    coordtransform = CoordTransform(
        spatialreference_rd,
        spatialreference_wgs84,
    )
    for f in wb_import_settings['geometry_files']:
        for rec in _records(f):
            geometry = GEOSGeometry(
                rec['wkb_geometry'],
                srid=28992,
            )
            geometry.transform(coordtransform)
            owa_geometry[rec['owaident']] = geometry

    # Go through the owm files, to get or create the corresponding areas
    for s in owmsources:
        for rec in _records(s['file']):
            owm_ident = rec['owmident'].strip()
            # Get or create area
            try:
                area = Area.objects.get(ident=owm_ident)
            except Area.DoesNotExist:
                owa_geometries = [owa_geometry[owa_ident]
                                  for owa_ident in owa_idents[owm_ident]]
                area = Area(
                    # Fields from GeoObject
                    ident=owm_ident,
                    geometry=_combine(owa_geometries),
                    geo_object_group=geogroups[s['data_administrator'].name],
                    # Fields from Area
                    area_class=Area.AREA_CLASS_KRW_WATERLICHAAM,
                    data_administrator=s['data_administrator'],
                    parent=None,
                    # Fields from Communique
                    name=rec['owmnaam'].strip(),
                    code=None,
                    description='',
                )
            # Set data_set on area in any case, existing or imported here.
            area.data_set = s['data_set']
            area.save()

            # Create WaterBody
            krw_status = KRWStatus.objects.get(code=rec['owmstat'].strip())
            krw_watertype = KRWWatertype.objects.get(
                code=rec['owmtype'].strip()
            )
            waterbody, waterbody_created = _get_or_create(
                model=WaterBody,
                get_kwargs={'area_ident': area.ident},
                extra_kwargs={
                    'area': area,
                    'krw_status': krw_status,
                    'krw_watertype': krw_watertype,
                },
            )


def import_measuring_rods(filename):
    for rec in _records(filename):
        # Only import EKR-scores
        if rec['eenheid'] != 'EKR':
            continue

        measuring_rod, measuring_rod_created = _get_or_create(
            model=MeasuringRod,
            get_kwargs={'measuring_rod_id': rec['id']},
            extra_kwargs={
                'code': rec['domgwcod'],
                'group': rec['groep'],
                'measuring_rod': rec['maatlat'],
                'sub_measuring_rod': rec['deelmaatlat'],
                'unit': rec['eenheid'],
                'sign': rec['teken'],
            }
        )
    # Assign parents, where necessary:
    for mr in MeasuringRod.objects.all():
        if not mr.sub_measuring_rod == 'Totaal':
            mr.parent = MeasuringRod.objects.get(
                measuring_rod=mr.measuring_rod,
                sub_measuring_rod='Totaal',
            )
            mr.save()


def import_scores(filename):
    for rec in _records(filename):

        # Only import if MeasuringRod is imported
        if not MeasuringRod.objects.filter(
            measuring_rod_id=rec['maatlat'],
        ).exists():
            continue

        # Try to get Area
        area_ident = rec['owmident'].strip()
        area = Area.objects.get(ident=area_ident)

        measuring_rod = MeasuringRod.objects.get(
            measuring_rod_id=rec['maatlat'],
        )
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
            'valid': True,
            'in_sgbp': rec['par_sgbp'],

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

        data_set_set = set([w.area.data_set
                            for w in measure.waterbodies.all()])
        if None in data_set_set:
            data_set_set.remove(None)
        if len(data_set_set) == 1:
            # If dataset is unambiguously defined by the associated area's,
            # Use it for the measure, too.
            measure.data_set = data_set_set.pop()
            measure.save()

        # Add some categories
        krw_category, created = MeasureCategory.objects.get_or_create(
            name='KRW',
        )
        measure.categories.add(krw_category)
        boolean_categories = [
            'wb21',
            'n2000',
            'gwb',
        ]
        for c in boolean_categories:
            if rec[c] == '1':
                category, category_created = _get_or_create(
                    model=MeasureCategory,
                    get_kwargs={'name': c},
                )
                measure.categories.add(category)
        if rec['thema'] is not None:
            category, category_created = _get_or_create(
                model=MeasureCategory,
                get_kwargs={'name': rec['thema']},
            )
            measure.categories.add(category)

        # Add a measurestatusmoment for the status at import
        measure_status = MeasureStatus.objects.get(
            name=rec['maatregelstatus'],
        )
        measure_status_date = datetime.date(year=2010, month=1, day=1)
        measure_status_moment = MeasureStatusMoment(
            measure=measure,
            status=measure_status,
            planning_date=measure_status_date,
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

        print 'Deleting all measure-related objects.'
        _clear_all()

        print 'Importing KRW portaal xml files from %s.' % import_path

        user = User.objects.get(pk=1)

        # Import Lookups
        import_KRW_lookup(os.path.join(import_path, 'KRW_lookup.xml'))

        # Waterbodies
        owm_sources = [
            ('HHNK', 'owmhhnk.xml'),
            ('Waternet', 'OWMwaternet.xml'),
            ('Rijnland', 'owmrijnland.xml'),
        ]

        wb_import_settings = {
            'geometry_files': [
                os.path.join(import_path, 'owageovlakken.xml'),
                os.path.join(import_path, 'owageolijnen.xml'),
            ],
            'link_file': os.path.join(import_path, 'owa.xml'),
            'owm_sources': [],
        }

        for data_administrator_name, xml_file in owm_sources:
            data_administrator = DataAdministrator.objects.get(
                name=data_administrator_name,
            )
            data_set = DataSet.objects.get(
                name=data_administrator_name,
            )
            wb_import_settings['owm_sources'].append({
                'data_administrator': data_administrator,
                'data_set': data_set,
                'user': user,
                'file': os.path.join(import_path, xml_file),
            })

        import_waterbodies(wb_import_settings=wb_import_settings)

        # Maatregeltypes (SGBP)
        import_measure_types(
            filename=os.path.join(
                import_path,
                'maatregelstandaard.xml',
            ),
        )

        # Import MeasuringRods
        import_measuring_rods(
            # Using corrected maatlatten, see readme.RST in xmldir.
            os.path.join(import_path, 'maatlatten_corrected.xml'),
        )

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
