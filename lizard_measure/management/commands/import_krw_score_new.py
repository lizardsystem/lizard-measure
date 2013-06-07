# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.management.base import BaseCommand

import os
import logging
from optparse import make_option
from lizard_measure.importtool.krw_xml_parser import ScoreXMLParser
from lizard_measure.models import (
    Score,
)

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Insert new measures for provided data_set.
    """
    help = ("Example: bin/django import_krw_score_new --action=insert --dataset_name=Waternet")

    option_list = BaseCommand.option_list + (
        make_option('--action',
                    help='update or insert',
                    type='str'),
        make_option('--dataset_name',
                    help='name of dataset, "Waternet"',
                    type='str'))

    #@transaction.commit_on_success
    def handle(self, *args, **options):
        rel_path = 'import_krw_portaal/import_krw_portaal_new/doelen.xml'
        score_filepath = os.path.join(settings.BUILDOUT_DIR, rel_path)
        logger.info(
            'Importing KRW portaal xml file from %s.', score_filepath)
        action = options.get('action')
        dataset_name = options.get('dataset_name')

        if action != "insert" and action != "update":
            logger.error('Unknown action {}, see --help'.format(action))
            return

        if dataset_name is None:
            logger.error('Unknown data_set, see --help')
            return

        parser = ScoreXMLParser(score_filepath)
        krw_scores = parser.parse(dataset_name)
        if action == "insert":
            self.insert(krw_scores)

    def insert(self, krw_scores):
        """Insert new measures."""
        count = 0
        for krw_score in krw_scores:
            score = Score(**krw_score.scoreAsDict())
            scores = Score.objects.filter(
                **{'measuring_rod': score.measuring_rod,
                   'area': score.area})
            scoreid = krw_score.identificatie.scoreid
            if scores.exists():
                logger.warning("Score id {} exists.".format(scoreid))
                continue
            try:
                logger.debug("insert score {0} for area {1}.".format(
                        krw_score.chemischeStof.parameter, score.area.ident))
                score.save()
                count += 1
            except:
                logger.exception("Cannot insert score {}.".format(scoreid))

        logger.info("Parsed scores {}.".format(len(krw_scores)))
        logger.info("Inserted scores {}.".format(count))
