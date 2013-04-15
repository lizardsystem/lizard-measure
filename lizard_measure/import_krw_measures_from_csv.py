#!/usr/bin/python
# (c) Nelen & Schuurmans. PGL licansed, see LICENSE.txt.

import csv
import logging
import simplejson

from lizard_area.import_areas_from_krwshapes import (
    WATERBEHEERDER_DATASET,)

from lizard_measure.models import (
    Measure,
    Organization,
    WaterBody,
    MeasureCategory,
    MeasureType,
    MeasurePeriod,
)


logger = logging.getLogger(__name__)


def import_measure(headers, measure_row):
    """Create a score."""
    print measure_row[headers.index('Tijdvak')]

    measure_type, measure_type_created = MeasureType.objects.get_or_create(
        code=measure_row[headers.index('MATCODE')])
    if measure_row[headers.index('Tijdvak')].replace(' ', '') == '':
        period = None
    else:
        period = MeasurePeriod.objects.get(
            description=measure_row[headers.index('Tijdvak')])

    import_raw_json = simplejson.dumps(measure_row, indent=4)

    initiator = Organization.objects.get(
        description=measure_row[headers.index('Initiatiefnemer')])

    measure_kwargs = {
        # KRW matident => Measure.ident
        'ident': measure_row[headers.index('MATIDENT')],
        'is_KRW_measure': True,
        'geometry': None,
        'measure_type': measure_type,
        'title': measure_row[headers.index('Maatregelnaam')],
        'period': period,
        'import_source': Measure.SOURCE_KRW_PORTAAL,
        'datetime_in_source': None,
        'import_raw': import_raw_json,
        'aggregation_type': Measure.AGGREGATION_TYPE_MIN,
        'description': "",
        'value': measure_row[headers.index('Omvang')],
        'investment_costs': None,
        'exploitation_costs': None,
        'executive': None,
        'initiator': initiator,
        'valid': True,
        'in_sgbp': measure_row[headers.index('Rapporteren')] == 'SGBP',
        'is_indicator': True}

    measure = Measure(**measure_kwargs)
    measure.save()

    return measure


def retrieve_locations(headers, measure_row):
    """Retrieve locations from row."""
    locations_str = measure_row[headers.index('Locatie')]
    if locations_str is None:
        return
    return locations_str.replace(' ', '').split(',')


def expected_data_set(headers, measure_row):
    """Return true if location(s) belong(s) to organization
    from the list."""
    locations = retrieve_locations(headers, measure_row)
    for location in locations:
        code = location[:4]
        if code not in WATERBEHEERDER_DATASET.keys():
            return False
    return True


def paire_to_waterbodies_or_remove(measure, headers, measure_row):
    """Paire waterbody(ies) with the measure.
    Remove not paired measure in case to hold it clean."""
    paired = False
    locations = retrieve_locations(headers, measure_row)
    for location in locations:
        waterbodies = WaterBody.objects.filter(area__ident=location)
        if waterbodies.exists():
            measure.waterbodies.add(waterbodies[0])
            paired = True

    if paired:
        measure.save()
    else:
        Measure.objects.get(ident=measure.ident).delete()


def measure_exists(headers, measure_row):
    """Check measure."""
    measures = Measure.objects.filter(
        ident=measure_row[headers.index('MATIDENT')])
    return measures.exists()


def set_data_set(measure, headers, measure_row):
    data_set_set = set([w.area.data_set
                        for w in measure.waterbodies.all()])
    if None in data_set_set:
        data_set_set.remove(None)
    if len(data_set_set) == 1:
        # If dataset is unambiguously defined by the associated area's,
        # Use it for the measure, too.
        measure.data_set = data_set_set.pop()
        measure.save()


def set_krwcategory(measure):
    krw_category, created = MeasureCategory.objects.get_or_create(
        name='KRW')
    measure.categories.add(krw_category)
    measure.save()


def import_measures(path_measures_csv):
    """Import krw-mesure from csv file."""
    i = 0
    with open(path_measures_csv, 'rb') as f:
        reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
        headers = reader.next()
        for row in reader:
            try:
                if measure_exists(headers, row):
                    continue
                if not expected_data_set(headers, row):
                    continue
                # crerate measure
                measure = import_measure(headers, row)
                # paire with waterbodies or remove the measure
                paire_to_waterbodies_or_remove(measure, headers, row)
                # set data_set of location to measure
                if not Measure.objects.filter(pk=measure.id).exists():
                    continue
                set_data_set(measure, headers, row)
                # set krwcategory
                set_krwcategory(measure)
                i = i + 1
                logger.debug("Added {0} for {1}".format(measure.ident,
                                                        measure.data_set.name))
            except Exception:
                logger.exception('')

    logger.debug("The end. Imported {0} measure(s)".format(i))
