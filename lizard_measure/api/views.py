import json
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from djangorestframework.views import View
from lizard_area.models import Area

from lizard_measure.models import Organization, Measure, Score, SteeringParameterPredefinedGraph, SteeringParameterFree
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
    field_mapping = {
        'id': 'id',
        'mep': 'mep',
        'gep': 'gep',
        'limit_insufficient_moderate': 'limit_insufficient_moderate',
        'limit_bad_insufficient': 'limit_bad_insufficient',
        'target_2015': 'target_2015',
        'target_2027': 'target_2027',
        'measuring_rod':'measuring_rod__description',
        'area': 'area__name'
    }
    def get_object_for_api(self,
                           score,
                           flat=True,
                           size=BaseApiView.COMPLETE,
                           include_geom=False):
        """
            create object of measure
        """
        model_class = Score
        name_field = 'measuring_rod__description'



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


class SteeringParameterPredefinedGraphView(BaseApiView):
    """
        Show organisations for selection and edit
    """
    model_class = SteeringParameterPredefinedGraph
    name_field = 'name'

    valid_field=None

    field_mapping = {
       'id': 'id',
        'name': 'name',
        'area': 'area__name',
        'order': 'order',
        'for_evaluation': 'for_evaluation',
        'predefined_graph': 'predefined_graph__name',
        'area_of_predefined_graph': 'area_of_predefined_graph__name'
    }

    read_only_fields = [

    ]

    def get_object_for_api(self,
                           sp,
                           flat=True,
                           size=BaseApiView.COMPLETE,
                           include_geom=False):
        """
        create object of measure
        """
        if size == self.ID_NAME:
            output = {
                'id': sp.id,
                'name': sp.name,
            }
        else:
            output = {
                'id': sp.id,
                'name': sp.name,
                'area': self._get_related_object(
                    sp.area,
                    flat=flat
                ),
                'order': sp.order,
                'for_evaluation': sp.for_evaluation,
                'predefined_graph': self._get_related_object(
                    sp.predefined_graph,
                    flat=flat
                ),
                'area_of_predefined_graph': self._get_related_object(
                    sp.area_of_predefined_graph,
                    flat=flat
                )
            }
        return output


class SteeringParameterFreeView(BaseApiView):
    """
        Show organisations for selection and edit
    """
    model_class = SteeringParameterFree
    name_field = 'name'

    valid_field=None

    field_mapping = {
        'id': 'id',
        'name': 'name',
        'area': 'area__name',
        'order': 'order',
        'parameter_code': 'parameter_code',
        'has_target': 'has_target',
        'target_value': 'target_value',
        'for_evaluation': 'for_evaluation',
        'location_modulinstance_string': 'location_modulinstance_string'
    }

    read_only_fields = [

    ]

    def get_object_for_api(self,
                           sp,
                           flat=True,
                           size=BaseApiView.COMPLETE,
                           include_geom=False):
        """
        create object of measure
        """
        if size == self.ID_NAME:
            output = {
                'id': sp.id,
                'name': sp.name,
            }
        else:
            output = {
                'id': sp.id,
                'name': sp.name,
                'area': self._get_related_object(
                    sp.area,
                    flat=flat
                ),
                'order': sp.order,
                'parameter_code': sp.parameter_code,
                'has_target': sp.has_target,
                'target_value': sp.target_value,
                'for_evaluation': sp.for_evaluation,
                'location_modulinstance_string': sp.location_modulinstance_string
            }
        return output




class OrganizationView(BaseApiView):
    """
    Show organisations for selection and edit
    """
    model_class = Organization
    name_field = 'description'

    valid_field='valid'
    valid_value=True

    field_mapping = {
        'id': 'id',
        'code': 'code',
        'description': 'description',
        'group': 'group',
        'source': 'source',
        'read_only': 'source'
    }

    read_only_fields = [
        'code',
        'group',
        'source',
        'read_only'
    ]

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
                'read_only': org.source > 0
            }
        return output

    def create_objects(self, data):
        """
            overwrite of base api to append code
        """
        success, touched_objects =  super(OrganizationView, self).create_objects(data)

        for object in touched_objects:
            object.code = object.id + 1000
            object.save()

        return success, touched_objects


class MeasureView(BaseApiView):
    """
    Area configuration.
    """
    model_class = Measure
    name_field = 'title'

    valid_field='valid'
    valid_value=True

    field_mapping = {
        'id': 'id',
        'ident': 'ident',
        'title': 'title',
        'source': 'source',
        'is_KRW_measure': 'is_KRW_measure',
        'is_indicator': 'is_indicator',
        'description': 'description',
        'investment_costs': 'investment_costs',
        'exploitation_costs': 'exploitation_costs',
        'ground_costs': 'ground_costs',
        'total_costs': 'total_costs',
        'responsible_department': 'responsible_department',
        'value': 'value',
        'measure_type': 'measure_type__description',
        'period': 'period__start_date',
        'unit': 'unit__description',
        'initiator': 'initiator__description',
        'executive': 'executive__description',
        'parent': 'parent__title',
        'aggregation_type':  'aggregation_type',
        'read_only': 'read_only',
        'import_raw': 'import_raw',
        'import_source': 'import_source'
    }

    def get_funding_organisations(self, measure):
        """
            returns funding organisation dict

        """

        return [{'id': obj.organization_id,
                 'percentage': obj.percentage,
                 'name': obj.organization.description,
                 'comment': obj.comment}
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
                'import_source': measure.get_import_source_display(),
                'is_KRW_measure': measure.is_KRW_measure,
                'is_indicator': measure.is_indicator,
                'description': measure.description,
                'total_costs': measure.total_costs,
                'investment_costs': measure.investment_costs,
                'exploitation_costs': measure.exploitation_costs,
                'land_costs': measure.land_costs,
                'responsible_department': measure.responsible_department,
                'value': measure.value,
                'in_sgbp': measure.in_sgbp,
                'measure_type': self._get_related_object(
                    measure.measure_type,
                    flat
                ),
                'period': self._get_related_object(measure.period, flat),
                'unit': self._get_related_object(measure.unit, flat),
                'categories': self._get_related_objects(
                    measure.categories,
                    flat
                ),
                'initiator': self._get_related_object(
                    measure.initiator,
                    flat
                ),
                'executive': self._get_related_object(measure.executive, flat),
                'areas': self._get_related_objects(measure.areas, flat),
                'waterbodies': self._get_related_objects(
                    measure.waterbodies,
                    flat
                ),
                'parent': self._get_related_object(
                    measure.parent,
                    flat
                ),
                'target_esf': measure.target_esf_string(),
                'effect_esf': measure.effect_esf_string(),
                'status_planned': measure.status_moment_string(is_planning=True),
                'status_realisation': measure.status_moment_string(is_planning=False),


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
                'esflink_set': measure.get_esflinks(
                    auto_create_missing_states=True
                ),
            })

        if size >= self.COMPLETE:
            output.update({
                'read_only': measure.read_only, #read only
                'import_raw': measure.import_raw, #read only
                'import_source': measure.get_import_source_display(), #read only
            })

        if include_geom:
            output.update({
                'geom': measure.get_geometry_wkt_string(),
            })

        return output

    def update_many2many(self, record, model_field, name, linked_records):
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

        if name == 'funding_organizations':
            record.set_fundingorganizations(linked_records)
        elif name == 'status_moments':
            record.set_statusmoments(linked_records)
        elif name == 'esflink_set':
            record.set_esflinks(linked_records)
        else:
            #areas, waterbodies, category
            self.save_single_many2many_relation(record,
                model_field,
                linked_records,
            )


class SteerParameterGraphs(View):
    """
        Api for toestand and krw-overzicht screen settings
    """
    graph_count = 0
    def _get_graph_id(self):
        self.graph_count += 1
        return 'gr%i'%self.graph_count


    def _get_free_graphsettings(self, graph):
            #todo: locaties goed en doel scores toevoegen
        output = {
            'id': self._get_graph_id,
            'name': graph.name,
            'visible': True,
            'base_url': '/graph/',
            'use_context_location': True,
            'location': None,
            'extra_params': {}
        }
        items = []

        for item in graph.location_modulinstance_string.split(';'):
            part = item.split(',')
            setting = {
                'fews_norm_source_slug': 'waternet', #todo: make dynamic
                'location': part[0],
                'parameter': graph.parameter_code,
                'type': 'line'
            }
            if len(part) > 1:
                setting['moduleinstance'] = part[1]
            if len(part) > 2:
                setting['timestep'] = part[2]
            if len(part) > 3:
                setting['qualifierset'] = part[3]



            items.append(json.dumps(setting))

        if graph.has_target:
            items.append(json.dumps({
                'label': 'Doel',
                'value': graph.target_value,
                'type': 'horizontal-line',
                'layout': {
                    'color': 'black',
                    'line-style': '--'
                }
            }))

        output['extra_params'] = {
            'item': items
        }
        return output


    def _get_predefined_graphsettings(self, graph):

        if graph.area_of_predefined_graph:
            location_ident = graph.area_of_predefined_graph.ident
        else:
            location_ident = None

        return {
            'id': self._get_graph_id,
            'name': graph.name,
            'visible': True,
            'base_url': graph.predefined_graph.url,
            'use_context_location': graph.area_of_predefined_graph == None,
            'location': location_ident,
            'extra_params': {},
        }



    def get(self, request):

        graphs = []
        prefix = ''
        count = 0
        area_ident = request.GET.get('object_id')

        area = get_object_or_404(Area, ident=area_ident)


        for graph in area.steeringparameterfree_set.filter(for_evaluation = False).order_by('order'):
            graphs.append(self._get_free_graphsettings(graph))

        for graph in area.steeringparameterpredefinedgraph_set.filter(for_evaluation = False).order_by('order'):
            graphs.append(self._get_predefined_graphsettings(graph))

        for graph in area.steeringparameterfree_set.filter(for_evaluation = True).order_by('order'):
            graphs.append(self._get_free_graphsettings(graph))

        for graph in area.steeringparameterpredefinedgraph_set.filter(for_evaluation = True).order_by('order'):
            graphs.append(self._get_predefined_graphsettings(graph))

        if area.area_class == Area.AREA_CLASS_KRW_WATERLICHAAM:
            graphs.append({
               'id': prefix + '99',
                'name': 'EKR scores',
                'visible': True,
                'base_url': '/measure/bar/?',
                'use_context_location': True,
                'location': None,
                'predefined_graph': 'ekr',
                'extra_params': {},
                'detail_link': 'ekr-score',
            })

        graphs.append({
            'id': prefix + '100',
            'name': 'maatregelen',
            'visible': True,
            'base_url': '/measure/measure_graph/?filter=focus',
            'use_context_location': True,
            'location': None,
            'predefined_graph': None,
            'extra_params': {},
            'detail_link': 'maatregelen',
        })



        return graphs
