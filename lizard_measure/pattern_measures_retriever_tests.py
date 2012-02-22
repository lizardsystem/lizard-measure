#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint: disable=C0111

# Copyright (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.

from unittest import TestCase

from lizard_measure.models import EsfPattern
from lizard_measure.pattern_measures_retriever import PatternMeasuresRetriever


class PatternMeasuresRetriever_retrieve_TestSuite(TestCase):

    def test_a(self):
        """Test the right patterns is retrieved for a single ESF pattern."""
        pattern = EsfPattern()
        pattern.save()
        retriever = PatternMeasuresRetriever()
        pks = [p.pk for p in retriever.retrieve(data_set=None).keys()]
        self.assertEqual([pattern.pk], pks)
