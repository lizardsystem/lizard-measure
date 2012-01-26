from django.core.urlresolvers import reverse
from djangorestframework.views import View

from lizard_measure.models import Organization, Measure, Score
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


class ScoreView(BaseApiView):
    """
    Show organisations for selection and edit
    """
    #todo: add waarde optioneel
    model_class = Score

    def get_object_for_api(self,
                           score,
                           flat=True,
                           size=BaseApiView.COMPLETE,
                           include_geom=False):
        """
            create object of measure
        """
        output = {
            'id': score.id,
            'mep': score.mep,
            'gep': score.gep,
            'limit_insufficient_moderate': score.limit_insufficient_moderate,
            'limit_bad_insufficient': score.limit_bad_insufficient,
            'target_2015': score.target_2015,
            'target_2027': score.target_2027,
            'measuring_rod': self._get_related_object(
                score.measuring_rod,
                flat,
            ),
            'area': self._get_related_object(score.area, flat),
        }
        return output


class OrganizationView(BaseApiView):
    """
    Show organisations for selection and edit
    """
    model_class = Organization

    def get_object_for_api(self,
                           org,
                           flat=True,
                           size=BaseApiView.COMPLETE,
                           include_geom=False):
        """
        create object of measure
        """
        if size == self.ID_NAME:
            output = {
                'id': org.id,
                'name': org.description,
            }
        else:
            output = {
                'id': org.id,
                'code': org.code,
                'description': org.description,
                'group': org.group,
                'source': self._get_choice(
                    Organization._meta.get_field('source'),
                    org.source,
                    flat
                ),
            }
        return output


class MeasureView(BaseApiView):
    """
    Area configuration.
    """
    model_class = Measure

    def get_funding_organisations(self, measure):
        """
            returns funding organisation dict

        """

        return [{'id': obj.organization_id,
                 'percentage': obj.percentage,
                 'name': obj.organization.description}
                for obj in measure.fundingorganization_set.all()]

    def get_object_for_api(self,
                           measure,
                           flat=True,
                           size=BaseApiView.COMPLETE,
                           include_geom=False):
        """
            create object of measure
        """

        output = {}

        if size == self.ID_NAME:
            output = {
                'id': measure.id,
                'name': measure.title,
            }

        if size >= self.SMALL:
            output = {
                'id': measure.id,
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
                'measure_type': self._get_related_object(
                    measure.measure_type,
                    flat
                ),
                'period': self._get_related_object(measure.period, flat),
                'unit': self._get_related_object(measure.unit, flat),
                'categories': self._get_related_objects(
                    measure.categories,
                    flat,
                ),
                'initiator': self._get_related_object(
                    measure.initiator,
                    flat
                ),
                'executive': self._get_related_object(measure.executive, flat),
                'areas': self._get_related_objects(measure.areas, flat),
                'waterbodies': self._get_related_objects(
                    measure.waterbodies,
                    flat,
                ),
                'parent': self._get_related_object(
                    measure.parent,
                    flat
                ),
            }

        if size >= self.MEDIUM:
            output.update({
                'aggregation_type':  self._get_choice(
                    Measure._meta.get_field('aggregation_type'),
                    measure.aggregation_type,
                    flat
                ),
                'funding_organizations': self.get_funding_organisations(
                    measure,
                ),
                'status_moments': measure.get_statusmoments(
                    auto_create_missing_states=True,
                    only_valid=True,
                ),
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
            optional some relations in case the relation is through
            another object
        """

        if model_field.name == 'funding_organizations':
            record.set_fundingorganizations(linked_records)
        if model_field.name == 'status_moments':
            record.set_statusmoments(linked_records)
        else:
            #areas, waterbodies, category
            self.save_single_many2many_relation(record,
                model_field,
                linked_records,
            )
