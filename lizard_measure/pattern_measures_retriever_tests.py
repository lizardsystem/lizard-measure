#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint: disable=C0111

# Copyright (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.

from unittest import TestCase

from mock import Mock

from lizard_measure.pattern_measures_retriever import PatternMeasuresRetriever


class PatternMeasuresRetrieverTestSuite(TestCase):

    def setup_retriever(self):
        self.pattern_measures = {'string pattern': 'Measure(s)'} # pylint: disable=C0301, W0201
        self.area = Mock(water_manager='HHNK')  # pylint: disable=W0201
        retriever = PatternMeasuresRetriever()
        retriever.retrieve_from_database = Mock(return_value=self.pattern_measures)
        retriever.retrieve_watertype_group = Mock(return_value='M')
        return retriever

    def test_a(self):
        """Test the right dict is retrieved."""
        retriever = self.setup_retriever()
        self.assertEqual(self.pattern_measures, retriever.retrieve(self.area))

    def test_b(self):
        """Test the right parameters are passed to the underlying methods."""
        retriever = self.setup_retriever()
        retriever.retrieve(self.area)
        retriever.retrieve_from_database.assert_called_with('M', 'HHNK')
        retriever.retrieve_watertype_group.assert_called_with(self.area)


class PatternMeasuresRetriever_retrieve_from_database_TestSuite(TestCase):

    def test_a(self):
        """Test an empty dict is returned when there are no ESF patterns."""
        retriever = PatternMeasuresRetriever()
        retriever.retrieve_esf_patterns = Mock(return_value=[])
        pattern_measures = retriever.retrieve_from_database('M', 'HHNK')
        self.assertEqual(0, len(pattern_measures))

    def create_esf_pattern(self, pattern, measures):
        return Mock(pattern=pattern, get_measures = Mock(return_value=measures))

    def test_b(self):
        """Test the right dict is returned when there is a single ESF pattern"""
        retriever = PatternMeasuresRetriever()
        esf_patterns = [0]
        esf_patterns[0] = self.create_esf_pattern(pattern='XX-------', measures=['dummy measure'])
        retriever.retrieve_esf_patterns = Mock(return_value=esf_patterns)

        pattern_measures = retriever.retrieve_from_database('M', 'HHNK')
        expected_pattern_measures = { 'XX-------': ['dummy measure'] }
        self.assertEqual(expected_pattern_measures, pattern_measures)

    def test_c(self):
        """Test the right dict is returned when there are multiple ESF patterns"""
        retriever = PatternMeasuresRetriever()
        esf_patterns = [0] * 2
        esf_patterns[0] = self.create_esf_pattern(pattern='XX-------', measures=['dummy measure'])
        esf_patterns[1] = self.create_esf_pattern(pattern='----?----', measures=['another dummy measure'])
        retriever.retrieve_esf_patterns = Mock(return_value=esf_patterns)

        pattern_measures = retriever.retrieve_from_database('M', 'HHNK')
        expected_pattern_measures = {
            'XX-------': ['dummy measure'],
            '----?----': ['another dummy measure']
            }
        self.assertEqual(expected_pattern_measures, pattern_measures)
