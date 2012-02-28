#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint: disable=C0111

# Copyright (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.

from unittest import TestCase

from mock import Mock

from lizard_measure.suitable_measures import SuitableMeasures


class SimpleSuitableMeasureInfoFactory(object):

    def create(self, esf_pattern, measure):
        return measure


class SimplePatternMeasuresRetriever(object):

    def __init__(self, measures_map):
        self.retrieve = Mock(return_value=measures_map)


class SimplePatternMatcher(object):

    def matches(self, area_pattern, pattern):
        return area_pattern == pattern


class SuitableMeasures_get_TestSuite(TestCase):

    def create_esf_pattern(self, pattern):
        return Mock(pattern=pattern)

    def test_a(self):
        """Test when there are no ESF patterns."""
        area = Mock(pattern='---------', data_set="don't care")
        suitable_measures = \
            SuitableMeasures(SimpleSuitableMeasureInfoFactory(),
                             SimplePatternMeasuresRetriever({}),
                             SimplePatternMatcher())
        self.assertEqual([], suitable_measures.get(area))

    def test_b(self):
        """Test when there is a single ESF pattern that is not suitable."""
        area = Mock(pattern='---------', data_set="don't care")
        suitable_measures = \
            SuitableMeasures(SimpleSuitableMeasureInfoFactory(),
                             SimplePatternMeasuresRetriever({Mock(pattern='XX-------'): ['dummy measure']}),
                             SimplePatternMatcher())
        self.assertEqual([], suitable_measures.get(area))

    def test_c(self):
        """Test when there is a single ESF pattern that is suitable."""
        area = Mock(pattern='XX-------', data_set="don't care")
        suitable_measures = \
            SuitableMeasures(SimpleSuitableMeasureInfoFactory(),
                             SimplePatternMeasuresRetriever({Mock(pattern='XX-------'): ['dummy measure']}),
                             SimplePatternMatcher())
        self.assertEqual(["dummy measure"], suitable_measures.get(area))
