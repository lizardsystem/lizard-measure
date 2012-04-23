#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint: disable=C0111

# Copyright (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.

import logging

from lizard_esf.models import get_data_main_esf
from lizard_measure.pattern_matcher import PatternMatcher
from lizard_measure.pattern_measures_retriever import PatternMeasuresRetriever

logger = logging.getLogger(__name__)


class SuitableMeasureInfo(object):

    def __init__(self, measure, is_country_wide):
        self.measure = measure
        self.is_country_wide = is_country_wide


class SuitableMeasureInfoFactory(object):

    def create(self, esf_pattern, measures):
        return [SuitableMeasureInfo(m, esf_pattern.data_set is None) for m in measures]


class SuitableMeasures(object):
    """Implements the retrieval of the suitable measures of an area."""

    matching_measure_types = []

    def __init__(self, suitable_measure_info_factory, pattern_measures_retriever,
        pattern_matcher):
        self.suitable_measure_info_factory = suitable_measure_info_factory
        self.pattern_measures_retriever = pattern_measures_retriever
        self.pattern_matcher = pattern_matcher

    def get(self, area):
        """Return the list of suitable measures for the given area."""
        matching_measure_types = {}
        matching_esf_patterns = []
        area_pattern = self._get_area_pattern(area)
        esf_patterns = self.pattern_measures_retriever.retrieve(area)
        for esf_pattern in esf_patterns:
            if self.pattern_matcher.matches(area_pattern, esf_pattern.pattern):
                for measure_type in esf_pattern.measure_types.all():
                    if not measure_type.id in matching_measure_types:
                        matching_measure_types[measure_type.id] = {
                            'code': measure_type.code,
                            'name': measure_type.description,
                            'landelijk': 0,
                            'regional': 0,
                        }
                        if esf_pattern.data_set is None:
                            matching_measure_types[measure_type.id]['landelijk'] += 1
                        else:
                            matching_measure_types[measure_type.id]['regional'] += 1

        #sort
        matching_measure_types = sorted(matching_measure_types.values(), key=lambda k: k['code'])

        result = []
        for measure_type in matching_measure_types:
            measure_type['matches'] = ''
            if measure_type['landelijk'] > 0:
                measure_type['matches'] += 'landelijk (%i) '% measure_type['landelijk']

            if measure_type['regional'] > 0:
                measure_type['matches'] += 'lokaal (%i)'% measure_type['regional']

            result.append(measure_type)

        return result

    def _get_area_pattern(self, area):
        """Return the string that specifies the critical ESFs of the given area."""
        result = ''
        esf_data = get_data_main_esf(area)
        for e in esf_data:
            if e['judgement'] == 'critical':
                result += 'X'
            else:
                result += '-'

        return result


def get_suitable_measures(area):
    """Return the list of suitable measures for the given area."""
    measures = SuitableMeasures(SuitableMeasureInfoFactory(),
                                PatternMeasuresRetriever(),
                                PatternMatcher())
    return measures.get(area)
