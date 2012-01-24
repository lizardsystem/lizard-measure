from django.contrib.gis.geos.io import WKTReader
from django.core.urlresolvers import reverse
from django.db.models.fields import FieldDoesNotExist
from djangorestframework.views import View
import json
from django.contrib.gis.db import models
from lizard_measure.models import Organization, Measure

from lizard_api.base import BaseApiView

import logging
logger = logging.getLogger(__name__)



class RootView(View):
    """
    Startpoint.
    """
    def get(self, request):
        return {
            "measure": reverse("lizard_measure_api_measure"),
            }


class OrganizationView(BaseApiView):
    """
    Show organisations for selection and edit
    """
    model_class = Organization

    def get_object_for_api(self, org, flat=True, size=BaseApiView.COMPLETE, include_geom=False):
        """
            create object of measure
        """
        output = {
            'id':org.id,
            'code': org.code,
            'name': org.description,
            'description': org.description,
            'group': org.group,
            'source': self._get_choice(Organization._meta.get_field('source'), org.source, flat),
        }
        return output

    
class MeasureView(BaseApiView):
    """
    Area configuration.
    """
    model_class = Measure
    valid_field = 'deleted'
    valid_value = False

    def get_funding_organisations(self, measure):
        """
            returns funding organisation dict

        """

        return [{'id': obj.organization_id, 'percentage': obj.percentage, 'name': obj.organization.description}
                        for obj in measure.fundingorganization_set.all()]

    def get_object_for_api(self, measure, flat=True, size=BaseApiView.COMPLETE, include_geom=False):
        """
            create object of measure
        """
        output = {
            'id':measure.id,
            'ident': measure.ident,
            'title': measure.title,
            'is_KRW_measure': measure.is_KRW_measure,
            'is_indicator': measure.is_indicator,
            'description': measure.description,
            'total_costs': measure.total_costs,
            'investment_costs': measure.investment_costs,
            'exploitation_costs': measure.exploitation_costs,
            'responsible_department': measure.responsible_department,
            'value': measure.value,
            'measure_type': self._get_related_object(measure.measure_type, flat),
            'period': self._get_related_object(measure.period, flat),
            'unit': self._get_related_object(measure.unit, flat),
            'categories': self._get_related_objects(measure.categories, flat),
            'initiator': self._get_related_object(measure.initiator, flat),
            'executive': self._get_related_object(measure.executive, flat),
            'areas': self._get_related_objects(measure.areas, flat),
            'waterbodies': self._get_related_objects(measure.waterbodies, flat),
        }

        if size >= self.MEDIUM:
            output.update({
                'aggregation_type':  self._get_choice(Measure._meta.get_field('aggregation_type'), measure.aggregation_type, flat),
                'funding_organizations': self.get_funding_organisations(measure),
                'status_moments': measure.get_statusmoments(auto_create_missing_states=True, only_valid=True),
            })

        if size >= self.COMPLETE:
            output.update({
                'read_only': measure.read_only,
                'import_raw': measure.import_raw,
                'import_source': measure.import_source,
            })

        if include_geom:
            output.update({
                'geom': measure.get_geometry_wkt_string(),
            })

        return output


    def update_many2many(self, record, model_field, linked_records):
        """
            update specific part of manyToMany relations.
            input:
                - record: measure
                - model_field. many2many field object
                - linked_records. list with dictionaries with:
                    id: id of related objects
                    optional some relations in case the relation is through another object

        """

        if model_field.name == 'funding_organizations':
            record.set_fundingorganizations(linked_records)
        if model_field.name == 'status_moments':
            record.set_statusmoments(linked_records)
        else:
            #areas, waterbodies, category
            self._save_single_many2many_relation(record, model_field, linked_records)
