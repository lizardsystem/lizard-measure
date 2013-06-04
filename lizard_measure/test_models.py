"""Tests for lizard_measure/models.py."""

from __future__ import unicode_literals

import factory

from django.test import TestCase
from lizard_measure import models as measuremodels


class MeasureTypeF(factory.Factory):
    FACTORY_FOR = measuremodels.MeasureType
    id = 1
    code = "BE01"
    description = "uitvoeren actief visstandsof schelpdierstandsbeheer"


class MeasurePeriodF(factory.Factory):
    FACTORY_FOR = measuremodels.MeasurePeriod


class OrganizationF(factory.Factory):
    FACTORY_FOR = measuremodels.Organization
    description = "Hoogheemraadschap Amstel Gooi en Vecht"


class TestMeasureTypeF(TestCase):
    """Tests for MeasureTypeF."""

    def test_has_unicode(self):
        measure_type = MeasureTypeF.build()
        uni = measure_type.__unicode__()

        self.assertTrue(uni)
        self.assertTrue(isinstance(uni, unicode))


class TesOrganizationFt(TestCase):
    """Tests for OrganizationF."""

    def test_has_unicode(self):
        organization = OrganizationF.build()
        uni = organization.__unicode__()

        self.assertTrue(uni)
        self.assertTrue(isinstance(uni, unicode))
