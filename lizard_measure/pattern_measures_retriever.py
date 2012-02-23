#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint: disable=C0111

# Copyright (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.

from django.db.models import Q

from lizard_measure.models import EsfPattern


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
        return self.retrieve_from_database(watertype_group, area.water_manager)

    def retrieve_watertype_group(self, area):
        """Return the water type group of the given area."""
        assert False

    def retrieve_from_database(self, watertype_group, water_manager):
        pattern_measures = {}
        esf_patterns = self.retrieve_esf_patterns(watertype_group, water_manager)
        for esf_pattern in esf_patterns:
            pattern_measures[esf_pattern.pattern] = esf_pattern.get_measures()
        return pattern_measures

    def retrieve_esf_patterns(self, watertype_group, water_manager):
        """Return the ESF patterns of the specified parameters."""
        query = Q(watertype_group__exact=watertype_group)
        query.add(Q(data_set__exact=None) | Q(data_set=water_manager))
        return EsfPattern.objects.filter(query)




