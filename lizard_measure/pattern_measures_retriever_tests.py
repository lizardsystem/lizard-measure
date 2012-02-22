#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint: disable=C0111

# Copyright (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.

from unittest import TestCase

from mock import Mock

# from lizard_measure.models import EsfPattern
# from lizard_measure.models import Measure
# from lizard_measure.models import MeasureType
from lizard_measure.pattern_measures_retriever import PatternMeasuresRetriever
# from lizard_security.models import DataSet


class PatternMeasuresRetriever_retrieve_TestSuite(TestCase):

    def setup_retriever(self):
        self.pattern_measures = {'string pattern': 'Measure(s)'}
        retriever = PatternMeasuresRetriever()
        retriever.retrieve_from_database = Mock(return_value=self.pattern_measures)
        retriever.retrieve_watertype_group = Mock(return_value ='M')
        retriever.retrieve_water_manager = Mock(return_value = 'HHNK')
        return retriever

    def test_a(self):
        """Test the right dict is retrieved."""
        retriever = self.setup_retriever()
        self.assertEqual(self.pattern_measures, retriever.retrieve(area=None))

    def test_b(self):
        """Test the right parameters are passed."""
        retriever = self.setup_retriever()
        retriever.retrieve(area='area name')
        retriever.retrieve_watertype_group.assert_called_with('area name')
        retriever.retrieve_water_manager.assert_called_with('area name')
        retriever.retrieve_from_database.assert_called_with('M', 'HHNK')
