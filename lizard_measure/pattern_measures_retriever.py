#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint: disable=C0111

# Copyright (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.

from django.db.models import Q

from lizard_measure.models import EsfPattern

class PatternMeasuresRetriever(object):

    def retrieve(self, data_set):
        """Return the dict of ESF pattern to the list of suitable Measures.

        The dict that is returned contains the ESF patterns that are valid for
        the country as a whole as the ones that are only valid for the given data
        set.

        """
        objects = EsfPattern.objects.filter(Q(data_set__exact=None) |  Q(data_set=data_set))
        patterns = [o.pattern for o in objects]
        measures = [0] * len(patterns)
        return dict(zip(patterns, measures))
