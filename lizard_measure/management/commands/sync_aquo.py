# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.db import transaction

from lizard_measure.models import Unit
from lizard_measure.models import KRWStatus
from lizard_measure.models import KRWWatertype
from lizard_measure.models import MeasureType
from lizard_measure.models import Organization
from lizard_measure.models import MeasuringRod
from lizard_measure.runner import run_sync_aquo


class Command(BaseCommand):
    args = ''
    help = 'Synchronize domaintables to aquo standards'

    @transaction.commit_on_success
    def handle(self, *args, **options):
        run_sync_aquo()
