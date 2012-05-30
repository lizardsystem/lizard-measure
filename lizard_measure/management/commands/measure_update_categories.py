# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
# -*- coding: utf-8 -*-

from lizard_measure.models import MeasureCategory

import logging
import django

logger = logging.getLogger(__name__)


class Command(django.core.management.base.BaseCommand):
    args = ''
    help = 'Import and update from KRW portaal xml files.'

    @django.db.transaction.commit_on_success
    def handle(self, *args, **options):
        logger.info('Invalidating some categories.')
        invalid_categories = [
            'gwb',
            'n2000',
            'KRW',
            'Evenwicht, grondwaterkwantiteit',
            'wb21',
        ]
        MeasureCategory.objects.filter(
            name__in=invalid_categories,
        ).update(valid=False)
        valid_categories = [
            'KRW (in KRW-portaal)',
            'Natura 2000 (in KRW-portaal)',
            'WB21',
            'TOP verdrogingsbestrijding',
            'NBW',
            'Groene Ruggengraat',
            '(P)EHS',
            'WBP (in KRW-portaal)',
            'GRP',
            'SWP',
            'WGP',
            'Zwemwater',
        ]
        logger.info('Creating some categories.')
        for name in valid_categories:
            MeasureCategory.objects.get_or_create(name=name)
        logger.info('Updating new categories.')
        MeasureCategory.objects.filter(
            name__in=valid_categories,
        ).update(valid=True)

