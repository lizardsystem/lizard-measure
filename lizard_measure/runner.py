# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
# -*- coding: utf-8 -*-

import logging
from django.db import transaction

from lizard_measure.models import Unit
from lizard_measure.models import KRWStatus
from lizard_measure.models import KRWWatertype
from lizard_measure.models import MeasureType
from lizard_measure.models import Organization
from lizard_measure.models import MeasuringRod

@transaction.commit_on_success
def run_sync_aquo(logger=None):
    """Synchronize domaintables to aquo standards."""

    if logger is None:
        logger = logging.getLogger(__name__)
    
    MeasuringRod.get_synchronizer(log=logger).synchronize()
    Unit.get_synchronizer(log=logger).synchronize()
    KRWStatus.get_synchronizer(log=logger).synchronize()
    KRWWatertype.get_synchronizer(log=logger).synchronize()
    MeasureType.get_synchronizer(log=logger).synchronize()
    Organization.get_synchronizer(log=logger).synchronize()
