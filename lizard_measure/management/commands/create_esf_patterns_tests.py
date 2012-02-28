#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint: disable=C0111

# Copyright (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.

from django.utils.unittest import TestCase

from lizard_measure.models import EsfPattern
from lizard_measure.models import MeasureType
from lizard_measure.models import WatertypeGroup

from lizard_measure.management.commands.create_esf_patterns import EsfPatterns


class EsfPatternsTestSuite(TestCase):

    def tearDown(self):
        EsfPattern.objects.all().delete()
        MeasureType.objects.all().delete()
        WatertypeGroup.objects.all().delete()

    def test_a(self):
        """Test the insertion of a single ESF pattern.

        Both the water type group and measure type already exist.

        """
        esf_patterns = EsfPatterns()

        watertype_group = WatertypeGroup()
        watertype_group.code = 'M'
        watertype_group.save()

        measuretype = MeasureType()
        measuretype.code = 'BR01'
        measuretype.description = 'verminderen emissie nutriënten landbouw'
        measuretype.save()

        esf_patterns.insert([['M','X','?','?','?','?','?','?','?','?','BR01']])

        self.assertEqual(1, EsfPattern.objects.count())

        esf_pattern = EsfPattern.objects.all()[0]
        self.assertEqual(u'X????????', esf_pattern.pattern)
        self.assertEqual(watertype_group, esf_pattern.watertype_group)
        self.assertEqual(measuretype, esf_pattern.measure_types.all()[0])


    def test_b(self):
        """Test the insertion of a two ESF patterns.

        The second ESF pattern is for the same water type group and the same
        pattern as the first type.

        Both the water type group and measure type already exist.

        """
        esf_patterns = EsfPatterns()

        watertype_group = WatertypeGroup()
        watertype_group.code = 'M'
        watertype_group.save()

        measuretype = MeasureType()
        measuretype.code = 'BR01'
        measuretype.description = 'verminderen emissie nutriënten landbouw'
        measuretype.save()
        measuretype = MeasureType()
        measuretype.code = 'IN02'
        measuretype.description = 'aanpassen inlaat / doorspoelen / scheiden water'
        measuretype.save()

        esf_patterns.insert([['M','X','?','?','?','?','?','?','?','?','BR01'],
                             ['M','X','?','?','?','?','?','?','?','?','IN02']])

        self.assertEqual(1, EsfPattern.objects.count())

        esf_pattern = EsfPattern.objects.all()[0]
        self.assertEqual(u'X????????', esf_pattern.pattern)
        self.assertEqual(watertype_group, esf_pattern.watertype_group)

        self.assertEqual(2, esf_pattern.measure_types.count())
        codes = [mt.code for mt in esf_pattern.measure_types.all()]
        codes.sort()
        self.assertEqual([u'BR01', u'IN02'], codes)

    def test_c(self):
        """Test the insertion of a two ESF patterns.

        The second ESF pattern is for a different the same water type group but
        the same pattern as the first type.

        Both the water type group and measure type already exist.

        """
        esf_patterns = EsfPatterns()

        watertype_group = WatertypeGroup()
        watertype_group.code = 'M'
        watertype_group.save()

        watertype_group = WatertypeGroup()
        watertype_group.code = 'B'
        watertype_group.save()

        measuretype = MeasureType()
        measuretype.code = 'BR01'
        measuretype.description = 'verminderen emissie nutriënten landbouw'
        measuretype.save()
        measuretype = MeasureType()
        measuretype.code = 'IN02'
        measuretype.description = 'aanpassen inlaat / doorspoelen / scheiden water'
        measuretype.save()

        esf_patterns.insert([['M','X','?','?','?','?','?','?','?','?','BR01'],
                             ['B','X','?','?','?','?','?','?','?','?','IN02']])

        self.assertEqual(2, EsfPattern.objects.count())


