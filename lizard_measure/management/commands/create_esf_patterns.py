#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint: disable=C0111

# Copyright (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.

import logging

from django.core.management.base import BaseCommand

from lizard_area.models import Area

from lizard_measure.models import EsfPattern
from lizard_measure.models import KRWWatertype
from lizard_measure.models import MeasureType
from lizard_measure.models import WaterBody
from lizard_measure.models import WatertypeGroup

logger = logging.getLogger(__name__)

WATERTYPE_GROUP_CODES = ['M', 'R', 'K&O']

PATTERNS = [
    ['M','X','?','?','?','?','?','?','?','?','BR01'],
    ['M','X','?','?','?','?','?','X','?','?','BR04'],
    ['M','X','?','?','?','?','?','-','?','?','IM01'],
    ['M','X','?','?','?','?','X','?','?','?','IM03'],
    ['M','X','?','?','?','?','-','?','?','?','IM04'],
    ['M','X','?','?','?','?','?','?','?','?','IM05'],
    ['M','X','?','?','?','?','?','X','?','?','IM06'],
    ['M','X','?','?','?','?','?','-','?','?','IM08'],
    ['M','X','?','?','?','?','X','?','?','?','IM09'],
    ['M','X','?','?','?','?','-','?','?','?','IN01'],
    ['M','X','?','?','?','?','?','?','?','?','IN02'],
    ['M','X','?','?','?','?','?','X','?','?','IN03'],
    ['M','X','?','?','?','?','?','-','?','?','IN07'],
    ['M','X','?','?','?','?','X','?','?','?','IN08'],
    ['M','X','?','?','?','?','-','?','?','?','IN09'],
    ['M','X','?','?','?','?','?','?','?','?','IN10'],
    ['M','X','?','?','?','?','?','X','?','?','IN12'],
    ['M','X','?','?','?','?','?','-','?','?','IN13'],
    ['M','X','?','?','?','?','X','?','?','?','IN14'],
    ['M','X','?','?','?','?','-','?','?','?','IN16'],
    ['M','X','?','?','?','?','?','?','?','?','IN19'],
    ['M','X','?','?','?','?','?','X','?','?','RO01'],
    ['M','-','X','?','?','?','?','-','?','?','BE01'],
    ['M','-','X','?','?','?','X','?','?','?','BE04'],
    ['M','-','X','?','?','?','-','?','?','?','BR06'],
    ['M','-','X','?','?','?','?','?','?','?','IM02'],
    ['M','-','X','?','?','?','?','X','?','?','IM03'],
    ['M','-','X','?','?','?','?','-','?','?','IM06'],
    ['M','-','X','?','?','?','X','?','?','?','IM09'],
    ['M','-','X','?','?','?','-','?','?','?','IN12'],
    ['M','-','X','?','?','?','?','?','?','?','IN13'],
    ['M','-','X','?','?','?','?','X','?','?','RO03'],
    ['M','-','X','?','?','?','?','-','?','?','RO04'],
    ['M','-','-','?','?','?','X','-','?','?','BE04'],
    ['M','-','-','?','?','?','-','?','?','?','BE01'],
    ['M','-','-','?','?','?','?','?','?','?','BR06'],
    ['M','-','-','?','?','?','?','X','?','?','IM02'],
    ['M','-','-','?','?','?','?','-','?','?','IN04'],
    ['M','-','-','?','?','?','X','-','?','?','IN05'],
    ['M','-','-','?','?','?','-','?','?','?','IN06'],
    ['M','-','-','?','?','?','?','?','?','?','IN07'],
    ['M','-','-','?','?','?','?','X','?','?','IN08'],
    ['M','-','-','?','?','?','?','-','?','?','IN09'],
    ['M','-','-','?','?','?','X','-','?','?','IN10'],
    ['M','-','-','?','?','?','-','?','?','?','IN11'],
    ['M','-','-','?','?','?','?','?','?','?','IN12'],
    ['M','-','-','?','?','?','?','X','?','?','IN13'],
    ['M','-','-','?','?','?','?','-','?','?','IN14'],
    ['M','-','-','?','?','?','X','-','?','?','IN17'],
    ['M','-','-','?','?','?','-','?','?','?','IN18'],
    ['M','-','-','?','?','?','?','?','?','?','RO04'],
    ['M','-','-','?','?','?','?','X','?','?','RO07'],
    ['M','-','-','?','?','?','?','-','?','?','BE02'],
    ['M','-','-','?','?','?','X','-','?','?','BE03'],
    ['M','-','-','?','?','?','-','?','?','?','BE06'],
    ['M','-','-','?','?','X','?','?','?','?','IN15'],
    ['M','-','-','?','?','-','?','X','?','?','IN16'],
    ['M','-','-','-','-','-','X','?','?','?','BE03'],
    ['M','?','?','?','?','?','?','X','?','?','IM03'],
    ['M','?','?','?','?','?','?','X','?','?','IM04'],
    ['M','?','?','?','?','?','?','X','?','?','IM06'],
    ['M','?','?','?','?','?','?','?','X','?','BE05'],
    ['M','?','?','?','?','?','?','?','X','?','BR02'],
    ['M','?','?','?','?','?','?','?','X','?','BR03'],
    ['M','?','?','?','?','?','?','?','X','?','BR04'],
    ['M','?','?','?','?','?','?','?','X','?','BR05'],
    ['M','?','?','?','?','?','?','?','X','?','BR06'],
    ['M','?','?','?','?','?','?','?','X','?','BR07'],
    ['M','?','?','?','?','?','?','?','X','?','BR08'],
    ['M','?','?','?','?','?','?','?','X','?','BR09'],
    ['M','?','?','?','?','?','?','?','X','?','IM02'],
    ['M','?','?','?','?','?','?','?','X','?','IM04'],
    ['M','?','?','?','?','?','?','?','X','?','IM06'],
    ['M','?','?','?','?','?','?','?','X','?','IM07'],
    ['M','?','?','?','?','?','?','?','X','?','IM09'],
    ['M','?','?','?','?','?','?','?','?','X','BE06'],
    ['M','?','?','?','?','?','?','?','?','X','IN07'],
    ['M','?','?','?','?','?','?','?','?','X','IN08'],
    ['M','?','?','?','?','?','?','?','?','X','IN09'],
    ['M','?','?','?','?','?','?','?','?','X','IN10'],
    ]


class WatertypeGroups(object):
    """Implements the functionality to insert WatertypeGroup(s)."""

    def create(self, *codes):
        """Create a WatertypeGroup for each given code.

        This method also creates the reference from each KRWWatertype to each
        new WatertypeGroup.

        Parameter:
          *codes* list of codes where each code specifies the
             code of a WatertypeGroup

        """
        for code in codes:
            watertype_group, _= WatertypeGroup.objects.get_or_create(code=code)
            for watertype in KRWWatertype.objects.all():
                if len(watertype.code) > 0 and watertype.code[0] in code:
                    watertype.watertype_group = watertype_group
                    watertype.save()


class EsfPatterns(object):
    """Implements the functionality to insert EsfPattern(s)."""

    def insert(self, patterns):
        """Insert the specified ESF patterns in the database.

        Parameter:
          *patterns* list of patterns, where each pattern is
             specified by a list of 10 strings.

        Let p be a pattern in *patterns*, then

          - p[0] specifies the code of the WatertypeGroup,
          - p[i], where 0 < i < 10, is a string that specifies whether ESF i
            should be critical (value 'X'), not critical (value '-') or does
            not care (value '?'), and
          - p[10] specifies the code of the MeasureType.

        """
        for pattern in patterns:
            watertype_group_code = pattern[0]
            string_pattern = ''.join(pattern[1:10])

            esf_pattern, created = \
                EsfPattern.objects.get_or_create(watertype_group__code=watertype_group_code,
                                                 pattern=string_pattern)

            watertype_group = WatertypeGroup.objects.get(code=watertype_group_code)
            esf_pattern.watertype_group = watertype_group

            # Before we can use the many-to-many relationship of the ESF
            # pattern, the pattern must have a primary key. So we save the
            # pattern to generate that key.
            esf_pattern.save()

            measure_type = MeasureType.objects.get(code=pattern[10])
            esf_pattern.measure_types.add(measure_type)

            esf_pattern.save()


class AreaWaterBodies(object):
    """Provides the functionality to create a WaterBody for each aan-/afvoergebied.

    Parameter:
      *db*
        interface to the database to ease unit testing

    """
    def __init__(self, database):
        self.db = database

    def create(self):
        """Create and save a WaterBody for each aan-afvoergebied."""
        for area in self.db.areas:
            if area.area_class != Area.AREA_CLASS_KRW_WATERLICHAAM:
                if area.water_bodies.count() == 0:
                    water_body = self.db.WaterBody()
                    water_body.area = area
                    water_body.save()


class Database(object):
    """Provides a wrapper around the Django database."""

    @property
    def areas(self):
        return Area.objects.all()

    def WaterBody(self):
        return WaterBody()


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        logger.info('Create a WaterBody for each aan-/afvoergebied.')
        AreaWaterBodies(Database()).create()
        logger.info('Create each WatertypeGroup %s and connect each '
                    'KRWWatertype', ', '.join(WATERTYPE_GROUP_CODES))
        WatertypeGroups().create(*WATERTYPE_GROUP_CODES)
        logger.info('Create each EsfPattern')
        EsfPatterns().insert(PATTERNS)
        logger.info('Done.')
