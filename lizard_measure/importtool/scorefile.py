#!/usr/bin/python
# (c) Nelen & Schuurmans. PGL licansed, see LICENSE.txt.

import logging
from lizard_area.models import Area
from lizard_measure.models import (
    MeasuringRod,
)

logger = logging.getLogger(__name__)


class ScoreIdentificatie(object):

    def __init__(self, land, waterschapid, scoreid):
        self.land = land
        self.waterschapid = waterschapid
        self.scoreid = scoreid


class ChemischeStof(object):

    def __init__(self, parameter, omschrijving):
        self.parameter = parameter
        self.omschrijving = omschrijving


class ScoreObject(object):

    def __init__(self):
        self.vanToepassingOpGeoObject = None
        self.chemischeStof = None
        self.identificatie = None
        self.onderdeelvannormpakket = None

    def scoreAsDict(self):
        area = self.get_area()
        area_ident = None
        if area is not None:
            area_ident = area.ident
        return {
            'measuring_rod': self.get_measuring_rod(),
            'area': area,
            'area_ident': area.ident,
        }

    def get_parent_measuring_rod(self):
        """Return measuring_rod models object or None."""
        measuring_rods = MeasuringRod.objects.filter(
            measuring_rod_id=self.onderdeelvannormpakket)
        if measuring_rods.exists():
            return measuring_rods[0]
        return None

    def get_measuring_rod(self):
        """Get or create measuring_rod model object."""
        measuring_rod, created = MeasuringRod.objects.get_or_create(
            code=self.chemischeStof.parameter,
            description =self.chemischeStof.omschrijving,
            valid=True,
            parent=self.get_parent_measuring_rod())
        return measuring_rod

    def get_area(self):
        try:
            area = Area.objects.get(ident=self.vanToepassingOpGeoObject)
            return area
        except Area.DoesNotExist:
            logging.exception(
                "Cannot find area '{}'.".format(self.vanToepassingOpGeoObject))
            return None
    
            
        
        
