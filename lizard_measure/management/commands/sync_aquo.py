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


class Command(BaseCommand):
    args = ''
    help = 'Synchronize domaintables to aquo standards'

    @transaction.commit_on_success
    def handle(self, *args, **options):
        MeasuringRod.get_synchronizer().synchronize()
        Unit.get_synchronizer().synchronize()
        KRWStatus.get_synchronizer().synchronize()
        KRWWatertype.get_synchronizer().synchronize()
        MeasureType.get_synchronizer().synchronize()
        Organization.get_synchronizer().synchronize()
