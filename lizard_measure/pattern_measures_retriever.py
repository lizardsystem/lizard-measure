#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint: disable=C0111

# Copyright (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.

import logging

from django.core.exceptions import ObjectDoesNotExist

from django.db.models import Q

from mock import Mock

from lizard_measure.models import EsfPattern
from lizard_measure.models import WaterBody

logger = logging.getLogger(__name__)


class PatternMeasuresRetriever(object):
    """Defines an interface to retrieve the candidate measures for an area.

    This class also implements the interface.

    """
    def retrieve(self, area):
        """Return dict of ESF string pattern to list of suitable measures.

        This dict depends on the water type group of the given area and its
        water manager.

        """
        watertype_group = self.retrieve_watertype_group(area)
        if watertype_group is None:
            logger.debug('unable to retrieve a watertype group for the given area')
        else:
            logger.debug('retrieved watertype group %s', watertype_group.code)
        return self.retrieve_from_database(watertype_group, area.water_manager)

    def retrieve_watertype_group(self, area):
        """Return the water type group of the given area.

        This method returns None when a WaterBody does not exist for the given
        area or when the water type is not specified for the WaterBody.

        """
        try:
            waterbody = WaterBody.objects.get(area=area)
            if waterbody.krw_watertype is None:
                watertype = Mock(watertype_group=None)
        except ObjectDoesNotExist:
            watertype = Mock(watertype_group=None)
        return watertype.watertype_group

    def retrieve_from_database(self, watertype_group, water_manager):
        pattern_measures = {}
        esf_patterns = self.retrieve_esf_patterns(watertype_group, water_manager)
        logger.debug("retrieved %d ESF patterns", len(esf_patterns))
        for esf_pattern in esf_patterns:
            pattern_measures[esf_pattern.pattern] = esf_pattern.get_measures()
        return pattern_measures

    def retrieve_esf_patterns(self, watertype_group, water_manager):
        """Return the ESF patterns of the specified parameters."""
        query = Q(watertype_group__exact=watertype_group) & \
            (Q(data_set__exact=None) | Q(data_set__name=water_manager))
        return EsfPattern.objects.filter(query)
