#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint: disable=C0111

# Copyright (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.

from unittest import TestCase

from lizard_measure.models import EsfPattern
from lizard_measure.models import Measure
from lizard_measure.models import MeasureType
from lizard_measure.pattern_measures_retriever import PatternMeasuresRetriever
# from lizard_security.models import DataSet


class PatternMeasuresRetriever_retrieve_TestSuite(TestCase):

    def test_a(self):
        """Test the right pattern is retrieved for a single ESF pattern."""
        pattern = EsfPattern()
        pattern.pattern = 'XX------'
        pattern.save()
        retriever = PatternMeasuresRetriever()
        measures_map = retriever.retrieve(data_set=None)
        self.assertEqual(1, len(measures_map))
        self.assertEqual(u'XX------', measures_map.keys()[0])

