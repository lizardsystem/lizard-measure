#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint: disable=C0111

# Copyright (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.

from unittest import TestCase

from lizard_measure.pattern_matcher import PatternMatcher


class PatternMatcherTestSuite(TestCase):

    def test_a(self):
        """Test the match of a critical ESF to a critical ESF pattern."""
        pattern_matcher = PatternMatcher()
        self.assertTrue(pattern_matcher.matches("X", "X"))

    def test_b(self):
        """Test the match of a critical ESF to a don't care ESF pattern."""
        pattern_matcher = PatternMatcher()
        self.assertTrue(pattern_matcher.matches("X", "?"))

    def test_c(self):
        """Test the mismatch of a critical ESF to a non-critical ESF pattern."""
        pattern_matcher = PatternMatcher()
        self.assertFalse(pattern_matcher.matches("X", "-"))

    def test_d(self):
        """Test the mismatch of a non-critical ESF to a critical ESF pattern."""
        pattern_matcher = PatternMatcher()
        self.assertFalse(pattern_matcher.matches("-", "X"))

    def test_e(self):
        """Test the match of a non-critical ESF to a non-critical ESF pattern."""
        pattern_matcher = PatternMatcher()
        self.assertTrue(pattern_matcher.matches("-", "-"))

    def test_f(self):
        """Test a real-world match."""
        pattern_matcher = PatternMatcher()
        self.assertTrue(pattern_matcher.matches("--X-----X", "--X-----?"))

    def test_g(self):
        """Test a real-world mismatch."""
        pattern_matcher = PatternMatcher()
        self.assertFalse(pattern_matcher.matches("--------X", "--X-----?"))
