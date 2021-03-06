#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

import os
from django.core.management.base import BaseCommand
from django.conf import settings
from lizard_measure.import_krw_scores_from_csv import import_scores


class Command(BaseCommand):
    """
    Synchronise area's with external WFS.
    """

    help = ("Example: bin/django import_kwr_scores_from_csv")

    def handle(self, *args, **options):
        scores_path = os.path.join(settings.BUILDOUT_DIR,
                                   'import_krw_portaal/overige/Scores_Maatlatten.csv')
        import_scores(scores_path)
