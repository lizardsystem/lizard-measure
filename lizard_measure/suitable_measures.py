#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint: disable=C0111

# Copyright (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.

class SuitableMeasures(object):

    def __init__(self, pattern_matcher):
        self.pattern_matcher = pattern_matcher

    def get(self, area):
        """Return the list of suitable measures for the given area."""
        suitable_measures = []
        for pattern, measures in self.available_patterns.iteritems():
            if self.pattern_matcher.matches(area.esf_pattern, pattern):
                suitable_measures += measures
        return suitable_measures
