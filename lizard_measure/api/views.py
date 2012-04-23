import json

from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from djangorestframework.views import View
from lizard_area.models import Area
from lizard_security.models import DataSet

from lizard_measure.models import Organization, Measure, Score, SteeringParameterPredefinedGraph, \
    SteeringParameterFree, EsfPattern
from lizard_measure.models import PredefinedGraphSelection
from lizard_measure.models import WaterBody
from lizard_api.base import BaseApiView

from lizard_layers.models import AreaValue

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


class AreaFiltered(object):
    """
    Filter objects using areas where you have the permission.

    Usage: put in front of BaseApiView class definition

    i.e. class ScoreView(AreaFiltered, BaseApiView):
    """

    # Force get_filtered_model instead of model.objects.all()
    use_filtered_model = True

    def get_filtered_model(self, request):
        """
        Return score objects that you may see
        """
        # Automagically filtered using lizard-security
        available_areas = Area.objects.all()
        return self.model_class.objects.filter(area__in=available_areas)


class ScoreView(AreaFiltered, BaseApiView):
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
        'area': 'area__name',
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

        try:
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
                'latest_value': None,
                'latest_comment': None,
                'latest_timestamp': None,
                }
            # Try to add most recent values
            try:
                # print 'yeah values'
                area_value = AreaValue.objects.get(
                    area=score.area,
                    value_type__parametertype__measuring_rod_code=score.measuring_rod.code)
                output['latest_value'] = area_value.value
                output['latest_comment'] = area_value.comment
                output['latest_timestamp'] = area_value.timestamp
            except AreaValue.DoesNotExist:
                pass
            except AreaValue.MultipleObjectsReturned:
                logger.warning('Multiple AreaValues found area:%s measuring_rod_code:%s' % (
                        score.area, score.measuring_rod.code))
        except:
            output = None

        return output

    def get(self, request):
        output_dict = BaseApiView.get(self, request)
        output_dict['data'] = [o for o in output_dict['data'] if o is not None]
        return output_dict


class SteeringParameterPredefinedGraphView(AreaFiltered, BaseApiView):
    """
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


class SteeringParameterFreeView(AreaFiltered, BaseApiView):
    """
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


class WaterBodyView(AreaFiltered, BaseApiView):
    """
    Water bodies that you can see
    """
    model_class = WaterBody
    name_field = 'area__name'

    valid_field=None

    field_mapping = {
        'id': 'id',
        'name': 'area__name',
    }

    read_only_fields = [
    ]

    def get_object_for_api(self,
                           obj,
                           flat=True,
                           size=BaseApiView.COMPLETE,
                           include_geom=False):
        """
        Create dict from object.
        """
        if size == self.ID_NAME:
            output = {
                'id': obj.id,
                'name': obj.area.name,
            }
        else:
            output = {
                'id': obj.id,
                'name': obj.area.name,
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

    def update_one2many(self, record, key, linked_records):

        if key == 'esflink_set':
            record.set_esflinks(linked_records)

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
        elif model_field.name == 'status_moments':
            # Fields: realisation_date, planning_date, id, name.
            # dates in YYYY-MM-DD format.
            # id is StatusMoment id.
            record.set_statusmoments(linked_records)
        else:
            #areas, waterbodies, category
            self.save_single_many2many_relation(record,
                model_field,
                linked_records,
            )


class SteerParameterOverview(View):

    def get(self, request):

        areas = Area.objects.all()
        #.select_related('steeringparameterpredefinedgraph_set') select related does not work
        # because of one2one relation, see https://code.djangoproject.com/ticket/13839

        predefined_graphs = PredefinedGraphSelection.objects.all().values('name')

        parameters = SteeringParameterFree.objects.filter(area__in=areas).values('parameter_code')


        data = []

        for area in areas:
            item = {
                'code': area.ident,
                'name': area.name
            }
            for steerp in area.steeringparameterpredefinedgraph_set.all():
                item['st_'+ steerp.predefined_graph.name] = 'X'

            for param in area.steeringparameterfree_set.values('parameter_code'):
                item['stf_' + param['parameter_code'].replace('.', '_')]  = 'X'

            data.append(item)

        return {'data': data, 'count': areas.count()}


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
            #'extra_params': {},
            'legend_location': 7,  # Legend on right side
        }
        items = []

        for item in graph.location_modulinstance_string.split(';'):
            part = item.split(',')
            setting = {
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
                },
            }))

        output['extra_params'] = {
            'item': items,
            'unit-as-y-label': True,
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
               'legend_location': 7,  # Legend on right side
            })

        if area.area_class == Area.AREA_CLASS_KRW_WATERLICHAAM:
            detail_link = 'maatregelen_krw'
        else:
            detail_link = 'maatregelen'

        graphs.append({
            'id': prefix + '100',
            'name': 'maatregelen',
            'visible': True,
            'base_url': '/measure/measure_graph/?filter=focus',
            'use_context_location': True,
            'location': None,
            'predefined_graph': None,
            'extra_params': {},
            'detail_link': detail_link,
            'legend_location': 7,  # Legend on right side
        })

        return graphs


class EsfPatternView(BaseApiView):


    model_class = EsfPattern
    name_field = 'pattern'

    #valid_field='valid'
    #valid_value=True

    field_mapping = {
        'id': 'id',
        'pattern': 'pattern',
        'watertype_group': 'watertype_group__code',
        'data_set': 'data_set',
        'read_only': 'data_set'  # for sort on read_only, use data_set (None == read_only)
    }

    read_only_fields = [
        'read_only',
        ]


    def get_data_set_description(self, data_set):
        """
        return dictiopnary with id, name. for None, the label 'landelijk' is used

        """
        if data_set is None:
            return {'id': None, 'name': 'landelijk'}
        else:
            return {'id': data_set.id, 'name': data_set.__unicode__()}


    def get_object_for_api(self,
                           pattern,
                           flat=True,
                           size=BaseApiView.COMPLETE,
                           include_geom=False):
        """
            create object of pattern
        """
        #todo: improve read_only, so superuser can also edit 'landelijke' records

        output = {}

        if size == self.ID_NAME:
            output = {
                'id': pattern.id,
                'name': pattern.pattern,
                }

        if size >= self.SMALL:
            output = {
                'id': pattern.id,
                'pattern': pattern.pattern,
                'watertype_group': self._get_related_object(pattern.watertype_group, flat),
                'data_set': self.get_data_set_description(pattern.data_set),
                'read_only': pattern.data_set == None,
                'measure_types': self._get_related_objects(pattern.measure_types, flat)
            }

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

        if True:
            #measure types
            self.save_single_many2many_relation(
                record,
                model_field,
                linked_records,
            )

    def create_objects(self, data, request):
        """
            overwrite of base api to modify data_set
        """
        for rec in data:
            if rec['data_set'][0]['id'] == None:
                del rec['data_set']

        success, touched_objects =  super(EsfPatternView, self).create_objects(data)

        return success, touched_objects
