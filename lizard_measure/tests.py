# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

from django.test import TestCase
from django.http import QueryDict
from lizard_measure.models import Measure

from lizard_measure.views import HorizontalBarGraphView

from lizard_measure.views import COLOR_1
from lizard_measure.views import COLOR_2
from lizard_measure.views import COLOR_3
from lizard_measure.views import COLOR_4
from lizard_measure.views import COLOR_5
from lizard_measure.views import value_to_html_color

import logging
logger = logging.getLogger(__name__)


class ModelTest(TestCase):
    fixtures = ('testdata', )

    def setUp(self):
        pass

    def test_cost_attribute(self):
        m = Measure.objects.get(title='TestMeasure1')
        self.assertEquals(m.total_costs, 500)


class HorizontalBarGraphViewTest(TestCase):
    def graph_items_from_request(self, get):
        class MockRequest(object):
            def __init__(self, get):
                self.GET = QueryDict(get)
        request = MockRequest(get)
        graph_view = HorizontalBarGraphView()
        graph_view.request = request
        return graph_view._graph_items_from_request()

    def test_empty(self):
        graph_item_dict = {}
        graph_items, graph_settings = self.graph_items_from_request(
            graph_item_dict)
        self.assertTrue(graph_settings.has_key('width'))
        self.assertTrue(graph_settings.has_key('height'))

    def test_width_height(self):
        graph_item_dict = 'width=123&height=345'
        graph_items, graph_settings = self.graph_items_from_request(
            graph_item_dict)
        self.assertEquals(int(graph_settings['width']), 123)
        self.assertEquals(int(graph_settings['height']), 345)


class ValueToHtmlColorTest(TestCase):
    # COLOR_1 | a | COLOR_2 | b | COLOR_3 | c | COLOR_4 | d | COLOR_5
    def test_a(self):
        self.assertEquals(
            value_to_html_color(.1, a=.2, b=.4, c=.6, d=.8),
            COLOR_1)
        self.assertEquals(
            value_to_html_color(.3, a=.2, b=.4, c=.6, d=.8),
            COLOR_2)
        self.assertEquals(
            value_to_html_color(.5, a=.2, b=.4, c=.6, d=.8),
            COLOR_3)
        self.assertEquals(
            value_to_html_color(.7, a=.2, b=.4, c=.6, d=.8),
            COLOR_4)
        self.assertEquals(
            value_to_html_color(.9, a=.2, b=.4, c=.6, d=.8),
            COLOR_5)

    def test_b(self):
        self.assertEquals(
            value_to_html_color(.1, c=.6),
            COLOR_3)
        self.assertEquals(
            value_to_html_color(.7, c=.6),
            COLOR_5)  # Is this the desired behaviour?

