#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint: disable=C0111

# Copyright (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.

from lizard_measure.pattern_matcher import PatternMatcher
from lizard_measure.pattern_measures_retriever import PatternMeasuresRetriever


class SuitableMeasures(object):
    """Implements the retrieval of the suitable measures of an area."""

    def __init__(self, pattern_measures_retriever, pattern_matcher):
        self.pattern_measures_retriever = pattern_measures_retriever
        self.pattern_matcher = pattern_matcher

    def get(self, area):
        """Return the list of suitable measures for the given area."""
        suitable_measures = []
        measures_dict = self.pattern_measures_retriever.retrieve(area)
        for pattern, measures in measures_dict.items():
            if self.pattern_matcher.matches(area.esf_pattern, pattern):
                suitable_measures += measures
        return suitable_measures


def get_suitable_measures(area):
    """Return the list of suitable measures for the given area."""
    measures = SuitableMeasures(PatternMeasuresRetriever(), PatternMatcher())
    return measures.get(area)
