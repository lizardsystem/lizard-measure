# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.db import transaction

from lizard_measure.models import Unit

class Command(BaseCommand):
    args = ''
    help = 'Synchronize domaintables to aquo standards'

    @transaction.commit_on_success
    def handle(self, *args, **options):
        Unit.synchronize(invalidate=True)
