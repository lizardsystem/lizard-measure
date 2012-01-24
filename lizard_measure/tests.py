# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

from django.test import TestCase

from lizard_measure.models import Measure


class ModelTest(TestCase):
    fixtures = ('testdata', )

    def setUp(self):
        pass

    def test_cost_attribute(self):
        m = Measure.objects.get('TestMeasure1')
        self.assertEquals('m.cost', 500)

        
        

