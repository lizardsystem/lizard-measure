# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.management.base import BaseCommand

import os
import logging
from optparse import make_option
from lizard_measure.importtool.krw_xml_parser import MeasureXMLParser
from lizard_measure.models import Measure

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Insert new measure for provided data_set.
    """
    help = ("Example: bin/django import_krw_portaal --action=insert --dataset_name=Waternet")

    option_list = BaseCommand.option_list + (
        make_option('--action',
                    help='update or insert',
                    type='str'),
        make_option('--dataset_name',
                    help='name of dataset_name',
                    type='str'))

    #@transaction.commit_on_success
    def handle(self, *args, **options):
        rel_path = 'import_krw_portaal/import_krw_portaal_new/Maatregelen_v2.xml'
        measure_filepath = os.path.join(settings.BUILDOUT_DIR, rel_path)
        logger.info(
            'Importing KRW portaal xml files from %s.', measure_filepath)
        action = options.get('action')
        dataset_name = options.get('dataset_name')

        if action != "insert" and action != "update":
            logger.error('Unknown action {}, see --help'.format(action))
            return

        if dataset_name is None:
            logger.error('Unknown data_set, see --help')
            return

        parser = MeasureXMLParser(measure_filepath)
        krw_measures = parser.parse(dataset_name)
        if action == "insert":
            self.insert(krw_measures)

    def insert(self, krw_measures):
        """Insert new measures."""
        count = 0
        for krw_measure in krw_measures:
            matident = krw_measure.identificatie.matident
            measure = Measure.objects.filter(ident=matident)
            if measure.exists():
                logger.warning("MATIDENT {} exists.".format(matident))
                continue
            try:
                logger.debug("insert measure {}.".format(matident))
                measure = Measure(**krw_measure.measureAsDict())
                measure.save()
                measure.categories = krw_measure.krwcategories
                measure.areas = krw_measure.geldenVoorWaterbeheerGebied.modelAreas
                measure.waterbodies = krw_measure.geldenVoorWaterbeheerGebied.modelWaterBodies
                measure.save()
                count += 1
            except:
                logger.exception("Cannot insert measure {}.".format(matident))

        logger.info("Parsed measures {}.".format(len(krw_measures)))
        logger.info("Inserted measures {}.".format(count))
