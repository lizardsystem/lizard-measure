from djangorestframework.resources import ModelResource

from lizard_measure.models import Measure


class MeasureResource(ModelResource):
    """
    Measure
    """
    model = Measure
