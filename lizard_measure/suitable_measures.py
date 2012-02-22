#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint: disable=C0111

# Copyright (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.

class SuitableMeasures(object):

    def get(self, area):
        """Return the list of suitable measures for the given area."""
        measures = []
        for pattern in self.available_patterns:
            if area.esf_pattern == pattern:
                measures += self.available_measures[pattern]
        return measures

