# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.db import transaction

from lizard_measure.models import Unit
from lizard_measure.models import KRWStatus
from lizard_measure.models import KRWWatertype
from lizard_measure.models import MeasureType

class Command(BaseCommand):
    args = ''
    help = 'Synchronize domaintables to aquo standards'

    @transaction.commit_on_success
    def handle(self, *args, **options):
        Unit.get_synchronizer().synchronize()
        #KRWStatus.synchronize()
        #KRWWatertype.synchronize()
        #MeasureType.synchronize()



