# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
# -*- coding: utf-8 -*-

# Import Scores from KRW portaal files.
import os
from lxml import etree
import logging

from django.db import transaction
from django.conf import settings
from django.core.management.base import BaseCommand

from lizard_measure.models import Score
from lizard_measure.models import MeasuringRod
from lizard_measure.models import Area

logger = logging.getLogger(__name__)


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


def _records(xml_filename):
    """
    Return a record generator

    Each yielded record is a dict with columnnames as keys
    """
    # Parse xml and find records
    logger.debug('Parsing %s' % xml_filename)
    tree = etree.parse(xml_filename)
    root = tree.getroot()
    record_elements = root.find('records')
    for record_element in record_elements:

        # Create record object
        record = dict([(column.get('name'), column.text)
                       for column in record_element])
        yield record


def import_scores(filename):
    """
    Import model Score from a file.
    """
    no_updated = 0
    no_created = 0
    records = _records(filename)
    logger.debug('Importing scores %s...' % filename)
    for rec in records:

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

        ascending = _ascending_or_none(limit_bad_insufficient, limit_insufficient_moderate)

        target_2015 = rec['doel2015']
        target_2027 = rec['doel2027']

        #  Note that I assume that area and measuring_rod together
        #  uniquely define the score.
        score_params = {
            'area': area,
            'mep': mep,
            'gep': gep,
            'limit_insufficient_moderate': limit_insufficient_moderate,
            'limit_bad_insufficient': limit_bad_insufficient,
            'ascending': ascending,
            'target_2015': target_2015,
            'target_2027': target_2027,
            }
        score, score_created = Score.objects.get_or_create(
            measuring_rod=measuring_rod,
            area_ident=area_ident,
            defaults=score_params,
        )
        if score_created:
            logger.debug('Score created: %s' % score)
            no_created += 1
        else:
            no_updated += 1
            for k, v in score_params.items():
                score.__setattr__(k, v)
            score.save()
    logger.info("# scores created: %d" % no_created)
    logger.info("# scores updated: %d" % no_updated)


class Command(BaseCommand):
    args = ''
    help = 'Import and update Scores from KRW portaal xml files.'

    @transaction.commit_on_success
    def handle(self, *args, **options):

        # Assume import path
        import_path = os.path.join(settings.BUILDOUT_DIR, 'import_krw_portaal')

        # Import scores
        score_sources = [
            'doelenhhnk.xml',
            'doelenrijnland.xml',
            'doelenwaternet.xml',
        ]

        for xml_file in score_sources:
            import_scores(
                filename=os.path.join(import_path, xml_file),
            )

