# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

from django.test import TestCase
from lizard_measure.models import Measure

import logging
logger = logging.getLogger(__name__)


class ModelTest(TestCase):
    fixtures = ('testdata', )

    def setUp(self):
        pass

    def test_cost_attribute(self):
        m = Measure.objects.get(title='TestMeasure1')
        self.assertEquals(m.total_costs, 500)
