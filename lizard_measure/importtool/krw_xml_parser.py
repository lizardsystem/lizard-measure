#!/usr/bin/python
# (c) Nelen & Schuurmans. PGL licansed, see LICENSE.txt.

import logging

from lxml import objectify

from lizard_measure.importtool.measurefile import (
    MatIdentificatie,
    TypeMaatregel,
    WATERBEHEERDER_DATASET,
    MeasureObject,
    MaatregelKostenDatatype,
    InitieleKostendrager,
    GeldenVoorWaterbeheerGebied,
)

from lizard_measure.importtool.scorefile import (
    ScoreObject,
    ChemischeStof,
    ScoreIdentificatie,
)

logger = logging.getLogger(__name__)


class XMLParser(object):

    def __init__(self, filepath):
        self.filepath = filepath
        with open(filepath) as xmlfile:
            self.root = objectify.fromstring(xmlfile.read())


class ScoreXMLParser(XMLParser):
    """Parse doelen.xml from krw-portal."""

    def __init__(self, filepath):
        XMLParser.__init__(self, filepath)
        self.toetsnorm_tags = self.root.featureMembers.getchildren()

    def parse(self, dataset_name):
        score_objects = []
        for toetsnorm_tag in self.toetsnorm_tags:
            identificatie = self.parse_identificatie(toetsnorm_tag)
            if dataset_name != WATERBEHEERDER_DATASET.get(
                identificatie.waterschapid):
                continue
            score_object = ScoreObject()
            score_object.identificatie = identificatie
            score_object.vanToepassingOpGeoObject = self.parse_vantoepassingopgeoobject(
                toetsnorm_tag)
            score_object.chemischeStof = self.parse_chemischestof(toetsnorm_tag) 
            score_object.onderdeelvannormpakket = self.parse_onderdeelvannormpakket(
                toetsnorm_tag)
            score_objects.append(score_object)           
        return score_objects

    def parse_identificatie(self, toetsnorm_tag):
        """Return ScoreIdentificatie object.
        ScoreIdentificatie(land, waterschapid, scoreid)"""
        values = toetsnorm_tag.identificatie.text.split('.')
        identificatie = ScoreIdentificatie(
            values[0], values[2], values[3][3:])
        return identificatie

    def parse_vantoepassingopgeoobject(self, toetsnorm_tag):
        """Return ident of geo object as string."""
        value = toetsnorm_tag.vanToepassingOpGeoObject.attrib.get(
            '{http://www.w3.org/1999/xlink}href')
        return value

    def parse_chemischestof(self, toetsnorm_tag):
        """Return instance of ChemischeStof(parameter, omschrijving) class."""
        value = toetsnorm_tag.kwaliteitsElementOfParameter.ParameterTyperingDataType.parameterGrootheid.ParameterGrootheidDataType.parameter.StofDataType.chemischeStof.text
        values = value.split(';')
        return ChemischeStof(values[0], values[1])

    def parse_onderdeelvannormpakket(self, toetsnorm_tag):
        """Return id of parent score."""
        value = toetsnorm_tag.onderdeelVanNormpakket.attrib.get(
            '{http://www.w3.org/1999/xlink}href')
        return value


class MeasureXMLParser(XMLParser):
    """Parse Maatregelen.xml from krw-portal."""

    def __init__(self, filepath):
        XMLParser.__init__(self, filepath)
        self.measure_tags = self.root.featureMembers.getchildren()

    def parse(self, dataset_name):
        """Return list of MeasureObjects."""
        measure_objects = []
        for measure_tag in self.measure_tags:
            identificatie = self.parse_identificatie(measure_tag)
            if dataset_name != WATERBEHEERDER_DATASET.get(
                identificatie.waterschapid):
                continue
            measure_object = MeasureObject()
            measure_object.identificatie = identificatie
            measure_object.typeMaatregel = self.parse_typemaatregel(
                measure_tag)
            measure_object.omschrijving = self.parse_omschrijving(measure_tag)
            measure_object.waarde = self.parse_waarde(measure_tag)
            measure_object.maatregelKostenDatatype = self.parse_kostendatatype(
                measure_tag)
            measure_object.initieleKostendrager = self.parse_initielekostendrager(
                measure_tag)
            measure_object.geldenVoorWaterbeheerGebied = self.parse_geldenvoorwaterbeheergebieden(measure_tag)
            measure_object.importRaw = objectify.dump(measure_tag)

            measure_objects.append(measure_object)

        return measure_objects

    def parse_omschrijving(self, measure_tag):
        try:
            return measure_tag.omschrijving.text
        except AttributeError:
            logger.exception("Attr. omschrijving not exists for {}.".format(
                    measure_tag.identificatie.text))
            return ""

    def parse_waarde(self, measure_tag):
        try:
            return measure_tag.waarde.text
        except AttributeError:
            logger.warning("Attr. waarde not exists for {}.".format(
                    measure_tag.identificatie.text))

    def parse_identificatie(self, measure_tag):
        """Return MatIdentificatie object.
        MatIdentificatie(land, waterschapid, matident)"""
        values = measure_tag.identificatie.text.split('.')
        identificatie = MatIdentificatie(
            values[0], values[2], values[3][3:])
        return identificatie

    def parse_typemaatregel(self, measure_tag):
        """Returns typeMaatregel object.
       TypeMaatregel(code, naam, title)"""
        values = measure_tag.typeMaatregel.text.split(';')
        return TypeMaatregel(values[0], values[1], values[2])

    def parse_kostendatatype(self, measure_tag):
        """Return MaatregelKostenDatatype object."""
        dt = '1-1-1970'
        kosten = 0
        try:
            dt = measure_tag.kostenMaatregel.MaatregelKostenDatatype.beginDatum.text
            kosten = measure_tag.kostenMaatregel.MaatregelKostenDatatype.kostenGrondverwerving.text
        except AttributeError:
            logger.exception(measure_tag.identificatie.text)

        try:
            if float(kosten) < 0:
                kosten = 0
        except:
            logger.exception()
        return MaatregelKostenDatatype(dt, kosten)

    def parse_initielekostendrager(self, measure_tag):
        """Return InitieleKostenDrager object.
        InitieleKostendrager(waterschapId, naam)"""
        values = measure_tag.initieleKostendrager.text.split(';')
        kostendrager = InitieleKostendrager(values[0], values[1])
        return kostendrager

    def parse_geldenvoorwaterbeheergebieden(self, measure_tag):
        """Return GeldenVoorWaterbeheerGebied object."""
        value = measure_tag.geldenVoorWaterbeheerGebied.attrib.get(
            '{http://www.w3.org/1999/xlink}href')
        values = value.replace(' ', '').split(',')
        return GeldenVoorWaterbeheerGebied(values)
