#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint: disable=C0111

# Copyright (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.


class PatternMatcher(object):

    def matches(self, area_pattern, pattern):
        """Return True iff the given area pattern matches the ESF pattern."""
        match = True
        for index, area_char in enumerate(area_pattern):
            match = area_char == pattern[index] or pattern[index] == '?'
            if not match:
                break
        return match
