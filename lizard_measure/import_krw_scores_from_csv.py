#!/usr/bin/python
# (c) Nelen & Schuurmans. PGL licansed, see LICENSE.txt.

import csv
import logging
import datetime

from lizard_area.models import Area
from lizard_layers.models import AreaValue
from lizard_layers.models import ValueType
from lizard_measure.models import Score
from lizard_measure.models import MeasuringRod

from lizard_area.import_areas_from_krwshapes import (
    WATERBEHEERDER_DATASET,) 


logger = logging.getLogger(__name__)


def get_value_type(measuring_rod):
    valuetype_mapping = {"FYTOPL": "ERK-FYTOPL",
                         "MAFAUNA": "EKR-MAFAUNA",
                         "VIS": "EKR-VIS",
                         "OVWFLORA": "EKR-OVWFLORA"}
    valuetype_name = valuetype_mapping.get(measuring_rod)

    if valuetype_name is None:
        return None

    value_type = ValueType.objects.get(name=valuetype_name)
    return value_type


def import_areavalue(headers, score_row, score):
    """Create a AreaValue objects voor the score."""
    value = score_row[headers.index('TOETSWAARD')]
    judgment = score_row[headers.index('TSTD')]

    value_type = get_value_type(score_row[headers.index('DOMGWCOD')])
    AreaValue(area=score.area,
              value_type=value_type,
              value=value,
              timestamp=datetime.datetime.today(),
              comment=judgment).save()


def import_score(headers, score_row):
    """Create a score."""
    areas = Area.objects.filter(ident=score_row[headers.index('OWMIDENT')])
    areas = areas.filter(data_set__name__in=WATERBEHEERDER_DATASET.values)
    area = None
    if areas.exists():
        area = areas[0]
    measuring_rod_obj = MeasuringRod.objects.get(
        code=score_row[headers.index('DOMGWCOD')])

    score = Score(area=area,
                  area_ident=area.ident,
                  measuring_rod=measuring_rod_obj)
    score.save()
    return score


def import_scores(path_scores_csv):
    """Import krw-scores from csv file."""
    i = 0
    with open(path_scores_csv, 'rb') as f:
        reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
        headers = reader.next()
        for row in reader:
            try:
                score = import_score(headers, row)
                import_areavalue(headers, row, score)
                i = i + 1
            except Exception:
                logger.exception("On import score.")

    logger.debug("The end. Imported {0} score(s)".format(i))
