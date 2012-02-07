# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

import json
import logging
from sets import Set

from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.http import HttpResponse
from django.template.loader import get_template
from django.views.generic.base import View

# from django.views.decorators.cache import cache_page

from lizard_measure.models import Measure
from lizard_measure.models import WaterBody
from lizard_measure.models import MeasureType
from lizard_measure.models import MeasurePeriod
from lizard_measure.models import MeasureCategory
from lizard_measure.models import Unit

from nens_graph.common import DateGridGraph
from nens_graph.common import dates_values
from matplotlib.dates import date2num
from lizard_map.views import AppView
from lizard_graph.views import TimeSeriesViewMixin
from lizard_measure.models import HorizontalBarGraph
#from lizard_graph.models import HorizontalBarGraphItem
from lizard_fewsnorm.models import GeoLocationCache


logger = logging.getLogger(__name__)

# HOMEPAGE_KEY = 1  # Primary key of the Workspace for rendering the homepage.
CRUMB_HOMEPAGE = {'name': 'home', 'url': '/'}


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


def measure_detail(request, measure_id,
                   template='lizard_measure/measure.html'):
    measure = get_object_or_404(Measure, pk=measure_id)

    return render_to_response(
        template,
        {'measure': measure},
        context_instance=RequestContext(request))


def krw_waterbody_measures(request, waterbody_slug,
                           template='lizard_krw/waterbody_measures.html'):
    waterbody = get_object_or_404(WaterBody, slug=waterbody_slug)
    # Obsolete: use MeasureCollections instead
    # get measures without parent: main measures
    main_measures = waterbody.measure_set.filter(parent=None)
    measure_collections = waterbody.measurecollection_set.all()

    crumbs = [CRUMB_HOMEPAGE,
              {'name': waterbody.name,
               'url': waterbody.get_absolute_url()},
              {'name': 'Maatregelen',
               'url': reverse(
                'lizard_krw.krw_waterbody_measures',
                kwargs={'waterbody_slug': waterbody.slug})}, ]

    return render_to_response(
        template,
        {'waterbody': waterbody,
         'main_measures': main_measures,
         'measure_collections': measure_collections,
         'crumbs': crumbs
         },
        context_instance=RequestContext(request))


def measure_detailedit_portal(request):
    """
    Return JSON for request.
    """
    c = RequestContext(request)

    measure_id = request.GET.get('measure_id', None)

    if request.user.is_authenticated():

        t = get_template('portals/maatregelen_form.js')
        c = RequestContext(request, {
            'measure': Measure.objects.get(pk=measure_id),
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


################ EKR GRAPHS

COLOR_1 = '#ff0000'
COLOR_2 = '#ffaa00'
COLOR_3 = '#ffff00'
COLOR_4 = '#00ff00'
COLOR_5 = '#0000ff'

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
        collected_goal_timestamps = Set()

        for index, graph_item in enumerate(graph_items):
            yticklabels.append(graph_item.label)
            if not graph_item.location:
                graph_item.location = graph_settings['location']
            # We want to draw a shadow past the end of the last
            # event. That's why we ignore dt_start.
            ts = graph_item.time_series(dt_end=dt_end)
            if len(ts) != 1:
                logger.warn('Warning: drawing %d timeseries on a single bar '
                            'HorizontalBarView', len(ts))
            # We assume there is only one timeseries.
            for (loc, par), single_ts in ts.items():
                dates, values, flag_dates, flag_values = dates_values(
                    single_ts)
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

                a, b, c, d = .2, .4, .6, .8
                block_colors = [value_to_html_color(value, a=a, b=b, c=c, d=d)
                                for value in values]

                # Block shadow
                graph.axes.broken_barh(
                    block_dates_shadow, (index - 0.2, 0.4),
                    facecolors=block_colors, edgecolors=block_colors,
                    alpha=0.2)
                # The 'real' block
                graph.axes.broken_barh(
                    block_dates, (index - 0.4, 0.8),
                    facecolors=block_colors, edgecolors='grey')

            for goal in graph_item.goals.all():
                collected_goal_timestamps.update([goal.timestamp, ])

        # For each unique bar goal timestamp, generate a mini
        # graph. The graphs are ordered by timestamp.
        goal_timestamps = list(collected_goal_timestamps)
        goal_timestamps.sort()
        subplot_numbers = [312, 313]
        for index, goal_timestamp in enumerate(goal_timestamps[:2]):
            axes_goal = graph.figure.add_subplot(subplot_numbers[index])
            axes_goal.set_yticks(range(len(yticklabels)))
            axes_goal.set_yticklabels('')
            axes_goal.set_xticks([0, ])
            axes_goal.set_xticklabels([goal_timestamp.year, ])
            for graph_item_index, graph_item in enumerate(graph_items):
                # 0 or 1 items
                goals = graph_item.goals.filter(timestamp=goal_timestamp)
                for goal in goals:
                    axes_goal.broken_barh(
                        [(-0.5, 1)], (graph_item_index - 0.4, 0.8),
                        facecolors=value_to_html_color(goal.value),
                        edgecolors='grey')
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
