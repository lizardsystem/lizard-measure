#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint: disable=C0111

# Copyright (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.

class SuitableMeasures(object):

    def __init__(self, pattern_measures_retriever, pattern_matcher):
        self.pattern_measures_retriever = pattern_measures_retriever
        self.pattern_matcher = pattern_matcher

    def get(self, area):
        """Return the list of suitable measures for the given area."""
        suitable_measures = []
        measures_map = self.pattern_measures_retriever.retrieve(area.data_set)
        for pattern, measures in measures_map.items():
            if self.pattern_matcher.matches(area.esf_pattern, pattern):
                suitable_measures += measures
        return suitable_measures
