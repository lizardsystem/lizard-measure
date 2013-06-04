#!/usr/bin/python
# (c) Nelen & Schuurmans. PGL licansed, see LICENSE.txt.

import logging
from lizard_security.models import DataSet
from lizard_area.models import Area
from lizard_measure.models import (
    Measure,
    Organization,
    WaterBody,
    MeasureCategory,
    MeasureType,
)

logger = logging.getLogger(__name__)


WATERBEHEERDER_DATASET = {
    '02': 'Fryslan',
    '04': 'Grootsalland',
    '15': 'Delfland',
    '19': 'wshollandsedelta',
    '33': 'Hunzeenaas',
    '34': 'Noorderzijlvest',
    '57': 'Peelenmaasvallei',
    '11': 'Waternet',
    '12': 'HHNK',
    '13': 'Rijnland'
}


class MatIdentificatie(object):

    def __init__(self, land, waterschapid, matident):
        self.land = land
        self.waterschapid = waterschapid
        self.matident = matident

    @property
    def dataset(self):
        return DataSet.objects.get(
            name=WATERBEHEERDER_DATASET.get(self.waterschapid))


class TypeMaatregel(object):

    def __init__(self, code, naam, title):
        self.code = code
        self.naam = naam
        self.title = title

    @property
    def modelObject(self):
        measure_type, created = MeasureType.objects.get_or_create(
            code=self.code)
        return measure_type


class MaatregelKostenDatatype(object):

    def __init__(self, beginDatum, kostenGrondverwerving):
        self.beginDatum = beginDatum
        self.kostenGrondverwerving = kostenGrondverwerving


class InitieleKostendrager(object):

    def __init__(self, waterschapId, naam):
        self.waterschapid = waterschapId
        self.naam = naam

    @property
    def modelObject(self):
        return Organization.objects.get(description=self.naam)


class GeldenVoorWaterbeheerGebied(object):

    def __init__(self, gebieden):
        self.gebieden = gebieden

    @property
    def modelAreas(self):
        modelGebieden = Area.objects.filter(ident__in=self.gebieden)
        return modelGebieden

    @property
    def modelWaterBodies(self):
        modelWaterlichamen = WaterBody.objects.filter(
            area__ident__in=self.gebieden)
        return modelWaterlichamen


class MeasureObject(object):

    def __init__(self):
        self.identificatie = None
        self.typeMaatregel = None
        self.omschrijving = ""
        self.waarde = ""
        self.maatregelKostenDatatype = None
        self.initieleKostendrager = None
        self.planVerankering = ""
        self.toepasselijkheidMaatregel = ""
        self.geldenVoorWaterbeheerGebied = None
        self.krwcategories = self.categories()
        self.importSource = Measure.SOURCE_KRW_PORTAAL
        self.importRaw = ""
        self.isIndicator = True
        self.isKRWMeasure = True
        self.geometry = None
        self.period = None
        self.datetimeInSource = None
        self.aggregationType = Measure.AGGREGATION_TYPE_MIN
        self.description = ""
        self.investmentCosts = None
        self.exploitationCosts = None
        self.executive = None
        self.valid = True
        self.inSGBP = False
        self.data_set = None

    def measureAsDict(self):
        return {
            'ident': self.identificatie.matident,
            'is_KRW_measure': self.isKRWMeasure,
            'geometry': self.geometry,
            'measure_type': self.typeMaatregel.modelObject,
            'title': self.omschrijving,
            'period': self.period,
            'import_source': self.importSource,
            'datetime_in_source': self.datetimeInSource,
            'aggregation_type': self.aggregationType,
            'description': self.description,
            'value': self.waarde,
            'investment_costs': self.investmentCosts,
            'exploitation_costs': self.exploitationCosts,
            'executive': self.executive,
            'initiator': self.initieleKostendrager.modelObject,
            'valid': self.valid,
            'in_sgbp': self.inSGBP,
            'is_indicator': self.isIndicator,
            'land_costs': self.maatregelKostenDatatype.kostenGrondverwerving,
            'import_raw': self.importRaw,
            'data_set': self.identificatie.dataset
        }

    def categories(self):
        return MeasureCategory.objects.filter(name='KRW')
