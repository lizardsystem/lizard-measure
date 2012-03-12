#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

from django.core.management.base import BaseCommand
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import Point
from django.contrib.gis import geos

from lizard_fewsnorm.models import FewsNormSource
from lizard_measure.models import Measure

import math
import random
import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        Add dummy geometries to measures.
        """
        for measure in Measure.objects.all():
            measure.geom = geos.GEOSGeometry(
                geos.Point(
                    5 + random.random(),
                    52 + random.random()
                ),
                srid=4326
            )
            measure.save()
            

