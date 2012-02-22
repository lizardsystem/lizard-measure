#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint: disable=C0111

# Copyright (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.


class PatternMeasuresRetriever(object):
    """Defines an interface to retrieve the candidate measures for an area.

    This class also implements the interface.

    """
    def retrieve(self, area):
        """Return the dict of ESF pattern to list of suitable measures.

        Which ESF patterns apply to the current area depends on the water type of
        the area and on the water manager of the area.

        """
        watertype_group = self.retrieve_watertype_group(area)
        water_manager = self.retrieve_water_manager(area)
        return self.retrieve_from_database(watertype_group, water_manager)

    def retrieve_watertype_group(self, area):
        pass

    def retrieve_water_manager(self, area):
        return area.data_set.name



