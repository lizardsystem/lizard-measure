#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint: disable=C0111

# Copyright (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.

from unittest import TestCase

from mock import Mock

from lizard_measure.suitable_measures import SuitableMeasures

class SimplePatternMatcher(object):

    def matches(self, area_pattern, pattern):
        return area_pattern == pattern

class SuitableMeasures_get_TestSuite(TestCase):

    def test_a(self):
        """Test when there are no ESF patterns."""
        area = "don't care"
        suitable_measures = SuitableMeasures(SimplePatternMatcher())
        suitable_measures.available_patterns = {}
        self.assertEqual([], suitable_measures.get(area))

    def test_b(self):
        """Test when there is a single ESF pattern that is not suitable."""
        area = Mock(esf_pattern='---------')
        suitable_measures = SuitableMeasures(SimplePatternMatcher())
        suitable_measures.available_patterns = {'XX-------': ['dummy measure']}
        self.assertEqual([], suitable_measures.get(area))

    def test_c(self):
        """Test when there is a single ESF pattern that is suitable."""
        area = Mock(esf_pattern='XX-------')
        suitable_measures = SuitableMeasures(SimplePatternMatcher())
        suitable_measures.available_patterns = {'XX-------': ['dummy measure']}
        self.assertEqual(["dummy measure"], suitable_measures.get(area))
