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
        retriever = PatternMeasuresRetriever()
        retriever.retrieve_from_database = \
            Mock(return_value=self.pattern_measures)
        retriever.retrieve_database_key = Mock(return_value=('M', 'HHNK'))
        return retriever

    def test_a(self):
        """Test the right dict is retrieved."""
        retriever = self.setup_retriever()
        self.assertEqual(self.pattern_measures,
            retriever.retrieve(area='area name'))

    def test_b(self):
        """Test the right parameters are passed to the underlying methods."""
        retriever = self.setup_retriever()
        retriever.retrieve(area='area name')
        retriever.retrieve_from_database.assert_called_with('M', 'HHNK')
        retriever.retrieve_database_key.assert_called_with('area name')
