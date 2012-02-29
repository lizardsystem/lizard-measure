#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint: disable=C0111

# Copyright (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.

from UserList import UserList

from django.utils.unittest import TestCase

from mock import Mock

from lizard_area.models import Area
from lizard_measure.models import EsfPattern
from lizard_measure.models import KRWWatertype
from lizard_measure.models import MeasureType
from lizard_measure.models import WaterBody
from lizard_measure.models import WatertypeGroup
from lizard_measure.management.commands.update_db_for_suitable_measures import AreaWaterBodies
from lizard_measure.management.commands.update_db_for_suitable_measures import EsfPatterns
from lizard_measure.management.commands.update_db_for_suitable_measures import WatertypeGroups


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

class MockDatabase(object):

    def __init__(self):
        self.areas = []
        self.water_bodies = []

    def Area(self):
        area = Mock(spec=Area)
        area.water_bodies = MockQuerySet()
        area.save = lambda a=area: self.areas.append(a)
        return area

    def WaterBody(self):
        water_body = Mock(spec=WaterBody)
        water_body.save = lambda w=water_body: self.save_water_body(w)
        return water_body

    def save_water_body(self, water_body):
        self.water_bodies.append(water_body)
        if water_body.area is not None:
            water_body.area.water_bodies.append(water_body)


class AreaWaterBodiesTestSuite(TestCase):

    def setUp(self):
        self.db = MockDatabase()

    def test_a(self):
        """Test the creation of a WaterBody for a single aan-/afvoergebied."""
        area = self.db.Area()
        area.area_class = Area.AREA_CLASS_AAN_AFVOERGEBIED
        area.save()
        AreaWaterBodies(self.db).create()
        water_body = self.db.water_bodies[0]
        self.assertEqual(area, water_body.area)

    def test_b(self):
        """Test the creation of a WaterBody for multiple aan-/afvoergebieden."""
        areas = [0] * 2
        areas[0] = self.db.Area()
        areas[0].area_class = Area.AREA_CLASS_AAN_AFVOERGEBIED
        areas[0].save()
        areas[1] = self.db.Area()
        areas[1].area_class = Area.AREA_CLASS_AAN_AFVOERGEBIED
        areas[1].save()
        AreaWaterBodies(self.db).create()
        referenced_areas = set([w.area for w in self.db.water_bodies])
        self.assertEqual(set(areas), set(referenced_areas))

    def test_c(self):
        """Test no WaterBody is created for a single aan-/afvoergebied.

        The aan-/afvoergebied already has a WaterBody.

        """
        area = self.db.Area()
        area.area_class = Area.AREA_CLASS_AAN_AFVOERGEBIED
        area.save()
        water_body = self.db.WaterBody()
        water_body.area = area
        water_body.save()
        AreaWaterBodies(self.db).create()
        self.assertEqual(1, len(self.db.water_bodies))
        self.assertEqual(water_body, self.db.water_bodies[0])

    def test_d(self):
        """Test no WaterBody is created for a KRW waterlichaam."""
        area = self.db.Area()
        area.area_class = Area.AREA_CLASS_KRW_WATERLICHAAM
        area.save()
        AreaWaterBodies(self.db).create()
        self.assertEqual(0, len(self.db.water_bodies))
