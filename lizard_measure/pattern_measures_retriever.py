#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint: disable=C0111

# Copyright (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.


class PatternMeasuresRetriever(object):
    """Defines an interface to retrieve the candidate measures for an area.

    This class also implements the interface.

    """
    def retrieve(self, area):
        """Return the dict of ESF pattern to the list of suitable measures.

        With 'ESF pattern', we mean the string pattern that defines the ESF
        pattern.

        """
        watertype_group, water_manager = self.retrieve_database_key(area)
        return self.retrieve_from_database(watertype_group, water_manager)

    def retrieve_database_key(self, area):
        """Return the (watertype group, water manager) of the given area."""
        return None, area.data_set.name




