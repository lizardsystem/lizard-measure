# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

import json
import logging
import datetime
import math

import iso8601

from django.db.models.query_utils import Q
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.http import HttpResponse
from django.template.loader import get_template
from django.views.generic.base import View

from matplotlib.dates import date2num
from matplotlib.lines import Line2D


from lizard_area.models import Area
from lizard_measure.models import Measure, MeasureStatus
from lizard_measure.models import MeasureType
from lizard_measure.models import MeasurePeriod
from lizard_measure.models import MeasureCategory
from lizard_measure.models import Unit
from lizard_measure.models import HorizontalBarGraph
from lizard_measure.models import Score
from lizard_measure.suitable_measures import get_suitable_measures
from lizard_measure.models import SteeringParameterFree
from lizard_measure.models import SteeringParameterPredefinedGraph
from lizard_measure.models import PredefinedGraphSelection
from lizard_measure.models import WatertypeGroup
from lizard_measure.models import EsfPattern
from lizard_security.models import DataSet

from lizard_area.models import Area

from nens_graph.common import DateGridGraph
from nens_graph.common import dates_values_comments
from lizard_map.views import AppView
from lizard_graph.views import TimeSeriesViewMixin
from lizard_fewsnorm.models import GeoLocationCache
from lizard_history.utils import get_history


logger = logging.getLogger(__name__)

# HOMEPAGE_KEY = 1  # Primary key of the Workspace for rendering the homepage.
CRUMB_HOMEPAGE = {'name': 'home', 'url': '/'}

# EKR Colors
COLOR_1 = '#ff0000'
COLOR_2 = '#ffaa00'
COLOR_3 = '#ffff00'
COLOR_4 = '#00ff00'
COLOR_5 = '#0000ff'


# def waterbody_shapefile_search(request):
#     """Return url to redirect to if a waterbody is found.

#     Only works with adapter lizard_shape.
#     """
#     google_x = float(request.GET.get('x'))
#     google_y = float(request.GET.get('y'))

#     # Set up a basic map as only map can search...
#     mapnik_map = mapnik.Map(400, 400)
#     mapnik_map.srs = coordinates.GOOGLE

#     workspace = Workspace.objects.get(name="Homepage")
#     # The following adapter should be available in the fixture.
#     adapter = workspace.workspace_items.all()[0].adapter

#     search_results = adapter.search(google_x, google_y)

#     # Return url of first found object.
#     for search_result in search_results:
#         #name_in_shapefile = search_result['name']
#         id_in_shapefile = search_result['identifier']['id']
#         water_body = WaterBody.objects.get(ident=id_in_shapefile)
#         return HttpResponse(water_body.get_absolute_url())

#     # Nothing found? Return an empty response and the
#     # javascript popup handler
#     # will fire.
#     return HttpResponse('')


def _sorted_measures(area):
    """
    Return list of measures that relate to area. Parent measures ordered
    alphabetically, child measures directly after parent measures,
    and loose child measures (parent not in list) at the end.
    """
    # These must all occur in the list. Also related child measures
    # whose parent are with a different area.
    all_related_measures = Measure.objects.filter(Q(waterbodies__area=area)|Q(areas=area)
        ).distinct()
    all_related_measures_dict = dict([(m.id, m) for m in all_related_measures])

    # get measures without parent: main measures
    parent_measures = all_related_measures.filter(
        parent__isnull=True,
    ).order_by(
        'title',
    )
    result_measures = []
    for p in parent_measures:
        result_measures.append(p)
        child_measures = p.measure_set.all().order_by('title')
        result_measures.extend(child_measures)

        # Keep track of added measures
        if p.id in all_related_measures_dict:
            del all_related_measures_dict[p.id]
        for child_measure in child_measures:
            if child_measure.id in all_related_measures_dict:
                del all_related_measures_dict[child_measure.id]

    # Now all_related_measures_dict contains only the left-over measures
    left_over_measures = all_related_measures_dict.values()
    sorted(left_over_measures, key=lambda m: m.title)
    for measure in left_over_measures:
        measure.parent_other_area = True
        result_measures.append(measure)

    return result_measures

class MeasureDetailView(AppView):
    """
    Show measure details
    """
    template_name='lizard_measure/measure.html'

    def measure(self):
        """Return a measure"""
        if not hasattr(self, '_measure'):
            self._measure = Measure.objects.get(
                pk=self.measure_id)
        return self._measure

    def get(self, request, *args, **kwargs):
        self.measure_id = kwargs['measure_id']
        return super(MeasureDetailView, self).get(
            request, *args, **kwargs)


class MeasureHistoryView(MeasureDetailView):
    """
    Show measure history
    """
    template_name='lizard_measure/measure_history.html'

    def history(self):
        """
        Return full history, if possible cached
        """
        if not hasattr(self, '_log_entry'):
            self._history = get_history(
                obj=self.measure(),
            )

        return self._history


class MeasureHistoryDetailView(MeasureDetailView):
    """
    Show measure history details
    """
    template_name='lizard_measure/measure_history_details.html'

    def action(self):
        """
        Return history details dict
        """
        if not hasattr(self, '_action'):
            self._action = get_history(
                log_entry_id=self.log_entry_id,
            )

        return self._action

    def changes(self):
        """
        Return list of changes using verbose names of fields
        """
        result = [(self.measure()._meta.get_field(f).verbose_name, v)
                  for f, v in self.action()['changes'].items()]
        return result


    def get(self, request, *args, **kwargs):
        """
        Pick the log_entry_id from the url
        """
        self.log_entry_id = kwargs['log_entry_id']
        return super(MeasureHistoryDetailView, self).get(
            request, *args, **kwargs)


def measure_detail(request, measure_id,
                   template='lizard_measure/measure.html'):
    measure = get_object_or_404(Measure, pk=measure_id)

    return render_to_response(
        template,
        {'measure': measure},
        context_instance=RequestContext(request))


def krw_waterbody_measures(request, area_ident,
                           template='lizard_measure/waterbody_measures.html'):
    area = get_object_or_404(Area, ident=area_ident)
    
    result_measures = _sorted_measures(area)

    return render_to_response(
        template,
        {'waterbody': area,
         'main_measures': result_measures
         },
        context_instance=RequestContext(request))


def suited_measures(request, area_ident,
                    template='lizard_measure/suited_measures.html'):
    # for testing purposes, we retrieve all measures
    area = get_object_or_404(Area, ident=area_ident)
    suitable_measure_types = get_suitable_measures(area)
    logger.debug("found %d suitable measures", len(suitable_measure_types))
    return render_to_response(
        template,
        {'suitable_measure_types': suitable_measure_types},
        context_instance=RequestContext(request))


def value_to_judgement(value, a=None, b=None, c=None, d=None):
    """
    Simple classifier for judgements.
    """
    if value < a:
        return "slecht"
    if value < b:
        return "ontoereikend"
    if value < c:
        return "matig"
    if value < d:
        return "goed"
    return "zeer goed"


def value_to_html_color(value, a=None, b=None, c=None, d=None):
    """
    Simple classifier for colors. All values will return a color.
    """
    if value < a:
        return COLOR_1
    if value < b:
        return COLOR_2
    if value < c:
        return COLOR_3
    if value < d:
        return COLOR_4
    return COLOR_5


def comment_to_html_color(comment):
    """
    Lookup the EKR color for a fewsnorm comment.

    Defaults to grey.
    """
    return {
        'slecht': COLOR_1,
        'ontoereikend': COLOR_2,
        'matig': COLOR_3,
        'goed': COLOR_4,
        'zeer goed': COLOR_5}.get(comment, '#cccccc')


def krw_waterbody_ekr_scores(
    request, area_ident, horizontal_bar_graph_slug='ekr-extended',
    template='lizard_measure/waterbody_ekr_scores.html'):
    """
    Show screen for ekr scores.

    A HorizontalBarGraph with slug 'ekr-extended' must be defined.
    """
    area = get_object_or_404(Area, ident=area_ident)

    location = None
    try:
        location = GeoLocationCache.objects.get(ident=area_ident)
    except GeoLocationCache.DoesNotExist:
        pass

    hor_bar_graph = HorizontalBarGraph.objects.get(
        slug=horizontal_bar_graph_slug)
    graph_items = hor_bar_graph.horizontalbargraphitem_set.all()
    for graph_item in graph_items:
        if not graph_item.location and location:
            graph_item.location = location

    ekr_scores = []
    try:
        ekr_scores = [(graph_item.time_series(with_comments=True),
                       Score.from_graph_item(graph_item),
                       graph_item)
                      for graph_item in graph_items]
    except AttributeError:
        # Occurs when above location =
        # GeoLocationCache... fails... just return nothing.
        pass

    score_tables = []
    for ts, score, graph_item in ekr_scores:
        new_score_table = {
            'title': str(graph_item),
            'score': score,
            'data': []}

        # We assume there is only one.
        len_ts_values = len(ts.values())
        if len_ts_values != 1:
            logger.error('Number of TimeSeries for HorizontalBarGraphItem %s is %d' % (
                    graph_item, len_ts_values))
        if len_ts_values == 0:
            new_score_table['data'] = [{'timestamp': 'Geen tijdreeks beschikbaar', 'value': None}]

        # a, b, c, d = score.borders
        for single_ts in ts.values():
            data_table = []
            for timestamp, (value, flag, comment) in single_ts.get_events():
                # value = math.trunc(10 * value) / 10.0  # Floor at 1 decimal
                data_table.append({'timestamp': timestamp,
                                   'value': value,
                                   'color': comment_to_html_color(comment),
                                   'comment': comment})
            new_score_table['data'] = data_table
            new_score_table['color_target_2015'] = comment_to_html_color(score.target_2015)
            new_score_table['color_target_2027'] = comment_to_html_color(score.target_2027)
        score_tables.append(new_score_table)

    return render_to_response(
        template,
        {'waterbody': area,
         'score_tables': score_tables,
         'COLOR_1': COLOR_1,
         'COLOR_2': COLOR_2,
         'COLOR_3': COLOR_3,
         'COLOR_4': COLOR_4,
         'COLOR_5': COLOR_5,
         },
        context_instance=RequestContext(request))


def _image_measures(graph, measures, start_date, end_date,
                    end_date_realized=None, legend_location=-1,
                    title=None):
    """Function to draw measures

    TODO: when a single measure is drawn, sometimes the whole
    picture is stretched out

    !attn! measure statuses are aggregated from child measures

    """

    def calc_bar_colors(measure, end_date, is_planning):
        """Returns calculated bars. The bars are aggregated from
        measure_status_moments from sub measures.

        ** measure can also be a measure_collection. It uses the
           status_moment function only.
        """
        measure_bar = []
        measure_colors = []
        measure_status_moments = measure.measure_status_moments(
            end_date=end_date, is_planning=is_planning)
        for msm_index, msm in enumerate(measure_status_moments):
            # drawing enddate: "infinity" or next status moment
            if msm_index == len(measure_status_moments) - 1:
                msm_end_date = end_date
            else:
                if is_planning:
                    msm_end_date = measure_status_moments[
                        msm_index + 1].planning_date
                else:
                    msm_end_date = measure_status_moments[
                        msm_index + 1].realisation_date

            if is_planning:
                begin = msm.planning_date
            else:
                begin = msm.realisation_date
            date_length = date2num(msm_end_date) - date2num(begin)

            measure_bar.append((date2num(begin), date_length))
            measure_colors.append(msm.status.color.html)
        return measure_bar, measure_colors

    if end_date_realized is None:
        end_date_realized = min(end_date, datetime.datetime.now().date())
    if title is None:
        title = "maatregel(en)"
    graph.figure.suptitle(title, x=0.5, y=1, horizontalalignment='center', verticalalignment='top')
    for index, measure in enumerate(measures):
        # realized
        measure_bar, measure_colors = calc_bar_colors(
            measure, end_date_realized, False)
        graph.axes.broken_barh(measure_bar,
                               (-index - 0.2, 0.4),
                               facecolors=measure_colors,
                               edgecolors=measure_colors)
        # planning
        measure_bar_p, measure_colors_p = calc_bar_colors(
            measure, end_date, True)
        graph.axes.broken_barh(measure_bar_p,
                               (-index - 0.45, 0.1),
                               facecolors=measure_colors_p,
                               edgecolors=measure_colors_p)

    # Y ticks
    yticklabels = [measure.shortname for measure in measures]
    yticklabels.reverse()
    graph.axes.set_yticks(range(int(-len(measures) + 0.5), 1))
    graph.axes.set_yticklabels(yticklabels)
    graph.axes.set_xlim(date2num((start_date, end_date)))
    graph.axes.set_ylim(-len(measures) + 0.5, 0.5)

    # Legend
    if legend_location >= 0:
        legend_handles, legend_labels = [], []
        for measure_status in MeasureStatus.objects.filter(valid=True):
            legend_handles.append(
                Line2D([], [], color=measure_status.color.html, lw=10))
            legend_labels.append(measure_status.name)
        graph.legend(legend_handles, legend_labels, legend_location=legend_location)


def measure_graph_api(request):
    """
        wrapper around measure_graph which get arguments from parameters instead of url


    """
    area_ident = request.GET.get('location', None)
    filter = request.GET.get('filter', 'all')

    return measure_graph(request, area_ident, filter)


def measure_graph(request, area_ident, filter='all'):
    """
    visualizes scores or measures in a graph

    identifier_list: [{'waterbody_slug': ...}, ...]
    start_end_dates: 2-tuple dates

    each row is an area
    """

    if filter == 'measure':
        measures = Measure.objects.filter(
            Q(pk=area_ident)|Q(parent__id=area_ident)).order_by('title')
    else:
        area = get_object_or_404(Area, ident=area_ident)

        if filter == 'focus':
            measures = [m for m in _sorted_measures(area) 
                        if m.is_indicator == True]
        else:
            measures = _sorted_measures(area)


    start_date = iso8601.parse_date(request.GET.get('dt_start', '2008-1-1T00:00:00')).date()
    end_date = iso8601.parse_date(request.GET.get('dt_end', '2013-1-1T00:00:00')).date()
    width = int(request.GET.get('width', 380))
    height = int(request.GET.get('height', 170))
    legend_location = int(request.GET.get('legend_location', -1))

    graph = DateGridGraph(width=width, height=height)

    _image_measures(graph, measures, start_date, end_date, legend_location=legend_location)

    graph.set_margins()
    return graph.png_response(
        response=HttpResponse(content_type='image/png'))


def measure_detailedit_portal(request):
    """
    Return JSON for request.
    """
    c = RequestContext(request)

    measure_id = request.GET.get('measure_id', None)

    init_parent = request.GET.get('parent_id', None)
    area_id = request.GET.get('area_id', None)

    if init_parent:
        init_parent = Measure.objects.get(pk=init_parent)

    init_area = None
    init_waterbody = None

    if area_id:
        area =  Area.objects.get(ident=area_id)

        if area.area_class == Area.AREA_CLASS_AAN_AFVOERGEBIED:
            init_area = area
        else:
            init_waterbody = area

    try:
        measure = Measure.objects.get(pk=measure_id)
    except Measure.DoesNotExist:
        measure = None

    if request.user.is_authenticated():

        t = get_template('portals/maatregelen_form.js')
        c = RequestContext(request, {
            'measure': measure,
            'measure_types': json.dumps(
                [{'id': r.id, 'name': str(r)}
                 for r in MeasureType.objects.all()]
            ),
            'periods': json.dumps(
                [{'id': r.id, 'name': str(r)}
                 for r in MeasurePeriod.objects.all()]
            ),
            'aggregations': json.dumps(
                [{'id': r[0], 'name': r[1]}
                 for r in Measure.AGGREGATION_TYPE_CHOICES]
            ),
            'categories': json.dumps(
                [{'id': r.id, 'name': str(r)}
                 for r in MeasureCategory.objects.all()]
            ),
            'units': json.dumps(
                [{'id': r.id, 'name': str(r)}
                 for r in Unit.objects.all()]
            ),
            'init_parent': init_parent,
            'init_area': init_area,
            'init_waterbody': init_waterbody,
        })

    else:
        t = get_template('portals/geen_toegang.js')

    return HttpResponse(t.render(c),  mimetype="text/plain")


def measure_groupedit_portal(request):
    """
    Return JSON for request.
    """
    c = RequestContext(request)

    if request.user.is_authenticated():

        t = get_template('portals/maatregelen-beheer.js')
        c = RequestContext(request, {
            'measure_types': json.dumps(
                [{'id': r.id, 'name': str(r)}
                 for r in MeasureType.objects.all()],
            ),
            'periods': json.dumps(
                [{'id': r.id, 'name': str(r)}
                 for r in MeasurePeriod.objects.all()],
            ),
            'aggregations': json.dumps(
                [{'id': r[0], 'name': r[1]}
                 for r in Measure.AGGREGATION_TYPE_CHOICES],
            ),
            'categories': json.dumps(
                [{'id': r.id, 'name': str(r)}
                 for r in MeasureCategory.objects.all()],
            ),
            'units': json.dumps(
                [{'id': r.id, 'name': str(r)}
                 for r in Unit.objects.all()],
            ),
        })

    else:
        t = get_template('portals/geen_toegang.js')

    return HttpResponse(t.render(c),  mimetype="text/plain")


def organization_groupedit_portal(request):
    """
    Return JSON for request.
    """
    c = RequestContext(request)

    if request.user.is_authenticated():

        t = get_template('portals/organisatie-beheer.js')
        c = RequestContext(request, {
        })

    else:
        t = get_template('portals/geen_toegang.js')

    return HttpResponse(t.render(c),  mimetype="text/plain")


def steering_parameter_form(request):
    """
        Return JSON with editor for steering parameters .
    """
    c = RequestContext(request)

    object_id = request.GET.get('object_id', None)

    area = get_object_or_404(Area,ident=object_id)


    if request.user.is_authenticated():

        t = get_template('portals/stuurparameter_form.js')

        if area.area_class == Area.AREA_CLASS_KRW_WATERLICHAAM:
            predefined_graphs = PredefinedGraphSelection.objects.filter(
                Q(for_area_type=Area.AREA_CLASS_KRW_WATERLICHAAM)|Q(for_area_type=None))

            related_areas = Area.objects.filter(Q(arealink_a__area_b=area)|Q(arealink_b__area_a=area)).distinct()
        elif  area.area_class == Area.AREA_CLASS_AAN_AFVOERGEBIED:
            predefined_graphs = PredefinedGraphSelection.objects.filter(
                Q(for_area_type=Area.AREA_CLASS_AAN_AFVOERGEBIED)|Q(for_area_type=None))

            related_areas = Area.objects.filter(Q(arealink_a__area_b=area)|Q(arealink_b__area_a=area)).distinct()

        c = RequestContext(request, {
            'area': area,
            'predefined_graphs': json.dumps(
                [{'id': r.id, 'name': r.name}
                 for r in predefined_graphs]),
            'related_areas': json.dumps(
                [{'id': r.id, 'name': r.name}
                 for r in related_areas]),
        })

    else:
        t = get_template('portals/geen_toegang.js')

    return HttpResponse(t.render(c),  mimetype="text/plain")


def esfpattern_detailedit_portal(request):
    """
    Return JSON for request.
    """
    c = RequestContext(request)

    pattern_id = request.GET.get('esfpattern_id', None)

    try:
        pattern = EsfPattern.objects.get(pk=pattern_id)
    except EsfPattern.DoesNotExist:
        pattern = None

    if request.user.is_authenticated():

        data_sets = [{'id': r.id, 'name': str(r)} for r in DataSet.objects.filter(
            pk__in=list(request.allowed_data_set_ids))]

        if request.user.is_superuser:
            data_sets = [{'id': r.id, 'name': str(r)} for r in DataSet.objects.all()]

            data_sets.append({'id':None, 'name': 'landelijk'})

        t = get_template('portals/esfpattern_form.js')
        c = RequestContext(request, {
            'pattern': pattern,
            'measure_types': json.dumps(
                [{'id': r.id, 'name': str(r)}
                for r in MeasureType.objects.all()]
            ),
            'watertype_group': json.dumps(
                [{'id': r.id, 'name': str(r)}
                for r in WatertypeGroup.objects.all()]
            ),
            'data_sets': json.dumps(data_sets
            ),
            })

    else:
        t = get_template('portals/geen_toegang.js')

    return HttpResponse(t.render(c),  mimetype="text/plain")


def steerparameter_overview(request):
    """
    Return JSON for request.
    """
    c = RequestContext(request)

    areas = Area.objects.all()

    predefined_graphs = PredefinedGraphSelection.objects.all().values_list('name', flat=True)
    #predefined_graphs = ['testa', 'testb']

    parameters = SteeringParameterFree.objects.filter(area__in=areas).distinct().values_list('parameter_code', flat=True)

    parameters = [{'org': par, 'no_point': par.replace('.','_')} for par in parameters]
    #parameters = ['test','test2']
    if request.user.is_authenticated():

        t = get_template('portals/stuurparameter-overzicht.js')
        c = RequestContext(request, {
            'predefined_graphs': predefined_graphs,
            'parameters': parameters
            })

    else:
        t = get_template('portals/geen_toegang.js')

    return HttpResponse(t.render(c),  mimetype="text/plain")









################ EKR GRAPHS


class HorizontalBarGraphView(View, TimeSeriesViewMixin):
    """
    Display horizontal bars
    """

    def _graph_items_from_request(self):
        """
        Return graph_items and graph_settings

        graph_items must be a list with for each item a function
        time_series.  This function accepts keyword arguments dt_start
        and dt_end and returns a list of timeseries.
        """
        get = self.request.GET
        graph_settings = {
            'width': 1200,
            'height': 500,
            'location': None
            }

        location = get.get('location', None)
        if location is not None:
            try:
                location = GeoLocationCache.objects.filter(ident=location)[0]
            except IndexError:
                logger.exception(
                    ("Tried to fetch a non existing "
                     "GeoLocationCache %s, created dummy one") %
                    location)
                location = GeoLocationCache(ident=location)
        graph_settings['location'] = location

        graph_items = []
        # Using the shortcut graph=<graph-slug>
        hor_graph_slug = get.get('graph', None)
        if hor_graph_slug is not None:
            # Add all graph items of graph to result
            try:
                hor_graph = HorizontalBarGraph.objects.get(
                    slug=hor_graph_slug)
                graph_items.extend(hor_graph.horizontalbargraphitem_set.all())
            except HorizontalBarGraph.DoesNotExist:
                logger.exception("Tried to fetch a non-existing hor.bar."
                                 "graph %s" % hor_graph_slug)

        # Graph settings can be overruled
        graph_parameters = ['width', 'height']
        for graph_parameter in graph_parameters:
            if graph_parameter in get:
                graph_settings[graph_parameter] = get[graph_parameter]

        return graph_items, graph_settings

    def get(self, request, *args, **kwargs):
        """
        Draw the EKR graph
        """

        dt_start, dt_end = self._dt_from_request()
        graph_items, graph_settings = self._graph_items_from_request()
        graph = DateGridGraph(
            width=int(graph_settings['width']),
            height=int(graph_settings['height']))

        # # Legend. Must do this before using graph location calculations
        # legend_handles = [
        #     Line2D([], [], color=value_to_html_color(0.8), lw=10),
        #     Line2D([], [], color=value_to_html_color(0.6), lw=10),
        #     Line2D([], [], color=value_to_html_color(0.4), lw=10),
        #     Line2D([], [], color=value_to_html_color(0.2), lw=10),
        #     Line2D([], [], color=value_to_html_color(0.0), lw=10),
        #     ]
        # legend_labels = [
        #     'Zeer goed', 'Goed', 'Matig', 'Ontoereikend', 'Slecht']
        # graph.legend(legend_handles, legend_labels, legend_location=6)

        yticklabels = []
        block_width = (date2num(dt_end) - date2num(dt_start)) / 50

        for index, graph_item in enumerate(graph_items):
            if not graph_item.location:
                graph_item.location = graph_settings['location']

            # Find the corresponding Score.
            score = Score.from_graph_item(graph_item)
            if score.id is None:
                graph_item.label = '(%s)' % graph_item.label

            yticklabels.append(graph_item.label)

            # We want to draw a shadow past the end of the last
            # event. That's why we ignore dt_start.
            try:
                ts = graph_item.time_series(dt_end=dt_end, with_comments=True)
            except:
                logger.exception(
                    'HorizontalBarView crashed on graph_item.time_series of %s' %
                    graph_item)
                ts = {}
            if len(ts) != 1:
                logger.warn('Warning: drawing %d timeseries on a single bar '
                            'HorizontalBarView', len(ts))
            # We assume there is only one timeseries.
            for (loc, par), single_ts in ts.items():
                dates, values, comments, flag_dates, flag_values, flag_comments = (
                    dates_values_comments(single_ts))
                if not dates:
                    logger.warning('Tried to draw empty timeseries %s %s',
                                   loc, par)
                    continue
                block_dates = []
                block_dates_shadow = []
                for date_index in range(len(dates) - 1):
                    dist_to_next = (date2num(dates[date_index + 1]) -
                                    date2num(dates[date_index]))
                    this_block_width = min(block_width, dist_to_next)

                    block_dates.append(
                        (date2num(dates[date_index]), this_block_width))
                    block_dates_shadow.append(
                        (date2num(dates[date_index]), dist_to_next))

                block_dates.append(
                    (date2num(dates[-1]), block_width))
                # Ignoring tzinfo, otherwise we can't compare.
                last_date = max(dt_start.replace(tzinfo=None), dates[-1])
                block_dates_shadow.append(
                    (date2num(last_date),
                     (date2num(dt_end) - date2num(dt_start))))

                a, b, c, d = score.borders
                block_colors = [comment_to_html_color(comment)
                                for comment in comments]

                # Block shadow
                graph.axes.broken_barh(
                    block_dates_shadow, (index - 0.2, 0.4),
                    facecolors=block_colors, edgecolors=block_colors,
                    alpha=0.2)
                # The 'real' block
                graph.axes.broken_barh(
                    block_dates, (index - 0.4, 0.8),
                    facecolors=block_colors, edgecolors='grey')

            # for goal in graph_item.goals.all():
            #     collected_goal_timestamps.update([goal.timestamp, ])

        # For each unique bar goal timestamp, generate a mini
        # graph. The graphs are ordered by timestamp.
        goal_timestamps = [
            datetime.datetime(2015, 1, 1, 0, 0),
            datetime.datetime(2027, 1, 1, 0, 0),
            ]
        subplot_numbers = [312, 313]
        for index, goal_timestamp in enumerate(goal_timestamps):
            axes_goal = graph.figure.add_subplot(subplot_numbers[index])
            axes_goal.set_yticks(range(len(yticklabels)))
            axes_goal.set_yticklabels('')
            axes_goal.set_xticks([0, ])
            axes_goal.set_xticklabels([goal_timestamp.year, ])
            for graph_item_index, graph_item in enumerate(graph_items):
                # TODO: make more efficient; score is retrieved twice
                # in this function.

                score = Score.from_graph_item(graph_item)
                #print 'score: %s' % score
                #print 'doel scores: %s' % str(score.targets)
                #a, b, c, d = score.borders
                goal = score.targets[index]
                if goal is not None:
                    axes_goal.broken_barh(
                        [(-0.5, 1)], (graph_item_index - 0.4, 0.8),
                        facecolors=comment_to_html_color(goal),
                        edgecolors='grey')
                # # 0 or 1 items
                # goals = graph_item.goals.filter(timestamp=goal_timestamp)
                # for goal in goals:
                #     axes_goal.broken_barh(
                #         [(-0.5, 1)], (graph_item_index - 0.4, 0.8),
                #         facecolors=value_to_html_color(goal.value),
                #         edgecolors='grey')
            axes_goal.set_xlim((-0.5, 0.5))
            axes_goal.set_ylim(-0.5, len(yticklabels) - 0.5)

            # Coordinates are related to the graph size - not graph 311
            bar_width_px = 12
            axes_x = float(graph.width -
                           (graph.MARGIN_RIGHT + graph.margin_right_extra) +
                           bar_width_px +
                           2 * bar_width_px * index
                           ) / graph.width
            axes_y = float(graph.MARGIN_BOTTOM +
                      graph.margin_bottom_extra) / graph.height
            axes_width = float(bar_width_px) / graph.width
            axes_height = float(graph.graph_height()) / graph.height
            axes_goal.set_position((axes_x, axes_y,
                                    axes_width, axes_height))

        graph.axes.set_yticks(range(len(yticklabels)))
        graph.axes.set_yticklabels(yticklabels)
        graph.axes.set_xlim(date2num((dt_start, dt_end)))
        graph.axes.set_ylim(-0.5, len(yticklabels) - 0.5)

        # Set the margins, including legend.
        graph.set_margins()

        return graph.png_response(
            response=HttpResponse(content_type='image/png'))
