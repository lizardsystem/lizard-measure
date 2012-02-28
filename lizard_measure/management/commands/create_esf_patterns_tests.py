#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint: disable=C0111

# Copyright (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.

from UserList import UserList

from django.utils.unittest import TestCase

from lizard_area.models import Area

from lizard_measure.models import EsfPattern
from lizard_measure.models import KRWWatertype
from lizard_measure.models import MeasureType
from lizard_measure.models import WaterBody
from lizard_measure.models import WatertypeGroup

from lizard_measure.management.commands.create_esf_patterns import EsfPatterns
from lizard_measure.management.commands.create_esf_patterns import WatertypeGroups


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


class WatertypeGroupsTestSuite(TestCase):

    def test_a(self):
        """Test a single WatertypeGroup is created."""
        WatertypeGroups().create('M')
        self.assertEqual('M', WatertypeGroup.objects.get(code='M').code)

    def test_b(self):
        """Test a watertype references the new WatertypeGroup."""
        watertype = KRWWatertype()
        watertype.code = 'M1'
        watertype.save()

        WatertypeGroups().create('M')

        watertype = KRWWatertype.objects.get(code='M1')
        self.assertEqual(WatertypeGroup.objects.get(code='M'), watertype.watertype_group)

    def test_c(self):
        """Test a watertype does not reference the new WatertypeGroup."""
        watertype = KRWWatertype()
        watertype.code = 'R1'
        watertype.save()

        WatertypeGroups().create('M')

        watertype = KRWWatertype.objects.get(code='R1')
        self.assertEqual(None, watertype.watertype_group)

    def test_d(self):
        """Test multiple WatertypeGroup(s) are created."""
        WatertypeGroups().create('M', 'R')
        self.assertEqual('M', WatertypeGroup.objects.get(code='M').code)
        self.assertEqual('R', WatertypeGroup.objects.get(code='R').code)

    def test_e(self):
        """Test a single WatertypeGroup with a two-character code is created."""
        WatertypeGroups().create('K&O')
        self.assertEqual('K&O', WatertypeGroup.objects.get(code='K&O').code)

    def test_f(self):
        """Test a watertype references the new WatertypeGroup."""
        watertype = KRWWatertype()
        watertype.code = 'K1'
        watertype.save()

        WatertypeGroups().create('K&O')

        watertype = KRWWatertype.objects.get(code='K1')
        self.assertEqual(WatertypeGroup.objects.get(code='K&O'), watertype.watertype_group)

    def test_g(self):
        """Test a watertype references the new WatertypeGroup."""
        watertype = KRWWatertype()
        watertype.code = 'O1'
        watertype.save()

        WatertypeGroups().create('K&O')

        watertype = KRWWatertype.objects.get(code='O1')
        self.assertEqual(WatertypeGroup.objects.get(code='K&O'), watertype.watertype_group)


class MockQuerySet(UserList):

    def __init__(*args, **kwargs):
        UserList.__init__(*args, **kwargs)

    def count(self):
        return len(self.data)


class AreaWaterBodies(object):

    def __init__(self):
        self.areas = []
        self.water_bodies = []

    def create(self):
        for area in self.areas:
            if area.area_class != Area.AREA_CLASS_KRW_WATERLICHAAM:
                if area.water_bodies.count() == 0:
                    water_body = WaterBody()
                    water_body.area = area
                    self.save_water_body(water_body)

    def save_area(self, area):
        self.areas.append(area)

    def save_water_body(self, water_body):
        self.water_bodies.append(water_body)
        if water_body.area is not None:
            water_body.area.water_bodies.append(water_body)


class AreaWaterBodiesTestSuite(TestCase):

    def test_a(self):
        """Test the creation of a WaterBody for a single aan-/afvoergebied."""
        area_water_bodies = AreaWaterBodies()

        area = Area()
        area.area_class = Area.AREA_CLASS_AAN_AFVOERGEBIED
        area.water_bodies = MockQuerySet()
        area_water_bodies.save_area(area)

        area_water_bodies.create()

        water_body = area_water_bodies.water_bodies[0]
        self.assertEqual(area, water_body.area)

    def test_aa(self):
        """Test the creation of a WaterBody for multiple aan-/afvoergebieden."""
        area_water_bodies = AreaWaterBodies()

        areas = [0] * 2
        areas[0] = Area()
        areas[0].area_class = Area.AREA_CLASS_AAN_AFVOERGEBIED
        areas[0].water_bodies = MockQuerySet()
        area_water_bodies.save_area(areas[0])
        areas[1] = Area()
        areas[1].area_class = Area.AREA_CLASS_AAN_AFVOERGEBIED
        areas[1].water_bodies = MockQuerySet()
        area_water_bodies.save_area(areas[1])

        area_water_bodies.create()

        referenced_areas = set([water_body.area for water_body in area_water_bodies.water_bodies])
        self.assertEqual(set(areas), set(referenced_areas))

    def test_b(self):
        """Test no WaterBody is created for a single aan-/afvoergebied.

        The aan-/afvoergebied already has a WaterBody.

        """
        area_water_bodies = AreaWaterBodies()

        area = Area()
        area.area_class = Area.AREA_CLASS_AAN_AFVOERGEBIED
        area.water_bodies = MockQuerySet()
        area_water_bodies.save_area(area)

        water_body = WaterBody()
        water_body.area = area
        area_water_bodies.save_water_body(water_body)

        area_water_bodies.create()

        self.assertEqual(1, len(area_water_bodies.water_bodies))
        self.assertEqual(water_body, area_water_bodies.water_bodies[0])

    def test_c(self):
        """Test no WaterBody is created for a KRW waterlichaam."""
        area_water_bodies = AreaWaterBodies()

        area = Area()
        area.area_class = Area.AREA_CLASS_KRW_WATERLICHAAM
        area.water_bodies = []
        area_water_bodies.save_area(area)

        area_water_bodies.create()

        self.assertEqual(0, len(area_water_bodies.water_bodies))
