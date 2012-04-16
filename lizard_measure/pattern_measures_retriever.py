#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint: disable=C0111

# Copyright (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.

import logging

from django.core.exceptions import ObjectDoesNotExist

from django.db.models import Q

from mock import Mock

from lizard_measure.management.commands.update_db_for_suitable_measures import WatertypeGroups
from lizard_measure.models import EsfPattern
from lizard_measure.models import WaterBody

logger = logging.getLogger(__name__)


class PatternMeasuresRetriever(object):
    """Defines an interface to retrieve the candidate esf patterns.

    This class also implements the interface.

    """
    def retrieve(self, area):
        """Return dict of ESF string pattern to list of suitable measures.

        This dict depends on the water type group of the given area and its
        water manager.

        """
        watertype_group = self.retrieve_watertype_group(area)
        return self.retrieve_esf_patterns(watertype_group, area.data_set.name)

    def retrieve_watertype_group(self, area):
        """Return the water type group of the given area.

        This method returns the default WatertypeGroup when no WaterBody exists
        for the given area or when no water type is specified for the
        WaterBody.

        """
        watertype_group = None
        try:
            waterbody = WaterBody.objects.get(area=area)
            if waterbody.krw_watertype is not None:
                watertype_group = waterbody.krw_watertype.watertype_group
        except ObjectDoesNotExist:
            pass
        if watertype_group is None:
            watertype_group = WatertypeGroups.get_default()
        return watertype_group

    def retrieve_esf_patterns(self, watertype_group, water_manager):
        """Return the ESF patterns of the specified parameters."""
        query = Q(watertype_group__exact=watertype_group) & \
            (Q(data_set__exact=None) | Q(data_set__name=water_manager))
        return EsfPattern.objects.filter(query)
