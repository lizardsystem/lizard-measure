# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

import os
from django.test import TestCase
from django.http import QueryDict

from lizard_measure.views import HorizontalBarGraphView

from lizard_measure.views import COLOR_1
from lizard_measure.views import COLOR_2
from lizard_measure.views import COLOR_3
from lizard_measure.views import COLOR_4
from lizard_measure.views import COLOR_5
from lizard_measure.views import value_to_html_color
from lizard_measure.importtool.krw_xml_parser import (
    MeasureXMLParser,
    ScoreXMLParser,
)
from lizard_measure import test_models as testmodels


import logging
logger = logging.getLogger(__name__)


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


class MeasureXMLParserTest(TestCase):

    def setUp(self):
        filepath = os.path.join(
            os.path.dirname(__file__),
            "test_data/test_measure.xml")
        self.parser = MeasureXMLParser(filepath)
        self.measure_objects = self.parser.parse("Waternet")

    def test_parse(self):
        measure_objects = self.parser.parse("HHNK")
        self.assertTrue(len(measure_objects) == 0)
        measure_objects = self.parser.parse("Waternet")
        self.assertTrue(len(measure_objects) == 2)

    def test_identificatie(self):
        matident = self.measure_objects[0].identificatie.matident
        land = self.measure_objects[0].identificatie.land
        waterschapid = self.measure_objects[0].identificatie.waterschapid
        self.assertTrue(matident == "90886")
        self.assertTrue(land == "NL")
        self.assertTrue(waterschapid == "11")

    def test_omschrijving(self):
        omschrijving = self.measure_objects[0].omschrijving
        self.assertTrue(omschrijving == 'Aanleggen natuurvriendelijke oevers')

    def test_waarde(self):
        waarde1 = self.measure_objects[0].waarde
        waarde2 = self.measure_objects[1].waarde
        self.assertTrue(waarde1 == "3")
        self.assertTrue(waarde2 is None)

    def test_typemaatregel(self):
        """Test parsing typemaatregel xml element."""
        code = "IN07"
        measure_type = testmodels.MeasureTypeF.build()
        measure_type.code = code
        type_maatregel = self.measure_objects[0].typeMaatregel.code
        self.assertTrue(type_maatregel == code)
        measure_model_obj = self.measure_objects[0].typeMaatregel.modelObject
        self.assertTrue(measure_model_obj.code == code)

    def test_kostendatatype(self):
        kosten = self.measure_objects[0].maatregelKostenDatatype.kostenGrondverwerving
        self.assertTrue(kosten == 0)

    def test_initielekostendrager(self):
        naam = "Hoogheemraadschap Amstel Gooi en Vecht"
        kostendrager = self.measure_objects[0].initieleKostendrager
        self.assertTrue(kostendrager.naam == naam)

    def test_parse_geldenvoorwaterbeheergebiede(self):
        mat1_gebieden = self.measure_objects[0].geldenVoorWaterbeheerGebied.gebieden
        mat2_gebieden = self.measure_objects[1].geldenVoorWaterbeheerGebied.gebieden
        self.assertTrue(len(mat1_gebieden) == 2)
        self.assertTrue(len(mat2_gebieden) == 1)


class ScoreXMLParserTest(TestCase):

    def setUp(self):
        filepath = os.path.join(
            os.path.dirname(__file__),
            "test_data/test_doelen.xml")
        self.parser = ScoreXMLParser(filepath)
        self.score_objects = self.parser.parse("Waternet")

    def test_parse_vantoepassingopgeoobject(self):
        ident = "NL11_1_1"
        parsed_ident = self.score_objects[0].vanToepassingOpGeoObject
        self.assertTrue(ident == parsed_ident)

    def test_parse_chemischestof(self):
        parameter = "O2"
        omschrijving = "zuurstof"
        parsed_parameter = self.score_objects[0].chemischeStof.parameter
        parsed_omschrijving = self.score_objects[0].chemischeStof.omschrijving
        self.assertTrue(parameter == parsed_parameter)
        self.assertTrue(omschrijving == parsed_omschrijving)

    def test_parse_onderdeelvannormpakket(self):
        onderdeelvannormpakket = '80130'
        parsed_onderdeelvannormpakket = self.score_objects[0].onderdeelvannormpakket
        self.assertTrue(onderdeelvannormpakket == parsed_onderdeelvannormpakket)

    def test_parse_identificatie(self):
        scoreid = '80130'
        parsed_scoreid = self.score_objects[0].identificatie.scoreid
        self.assertTrue(scoreid == parsed_scoreid)
