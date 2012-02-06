# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

import json
import datetime

from django.core.urlresolvers import reverse
from django.db.models.query_utils import Q
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.http import HttpResponse
from django.template.loader import get_template

from matplotlib.dates import date2num
from matplotlib.lines import Line2D

from lizard_map import adapter

# from django.views.decorators.cache import cache_page

from lizard_measure.models import Measure, MeasureStatus
from lizard_measure.models import WaterBody
from lizard_measure.models import MeasureType
from lizard_measure.models import MeasurePeriod
from lizard_measure.models import MeasureCategory
from lizard_measure.models import Unit
from lizard_area.models import Area

from lizard_map.views import AppView

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


def krw_waterbody_measures(request, area_ident,
                           template='lizard_measure/waterbody_measures.html'):
    area = get_object_or_404(Area, ident=area_ident)
    # Obsolete: use MeasureCollections instead
    # get measures without parent: main measures
    main_measures = Measure.objects.filter(Q(waterbodies__area=area)|Q(areas=area))
    print "aantal maatregelen: %i"%main_measures.count()
    return render_to_response(
        template,
        {'waterbody': area,
         'main_measures': main_measures
         },
        context_instance=RequestContext(request))



def _image_measures(graph, measures, start_date, end_date,
                    end_date_realized=None, add_legend=True,
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
                msm_end_date = measure_status_moments[
                    msm_index + 1].datetime

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
        title = "krw maatregel(en)"
    graph.suptitle(title)
    for index, measure in enumerate(measures):
        # realized
        measure_bar, measure_colors = calc_bar_colors(
            measure, end_date_realized, False)
        graph.axes.broken_barh(measure_bar,
                               (-index - 0.3, 0.6),
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
    graph.axes.set_ylim(-len(measures) + 0.5, 0.5)

    # Legend
    if add_legend:
        legend_handles, legend_labels = [], []
        for measure_status in MeasureStatus.objects.all():
            legend_handles.append(
                Line2D([], [], color=measure_status.color.html, lw=10))
            legend_labels.append(measure_status.name)
        graph.legend(legend_handles, legend_labels, ncol=3)



def measure_graph(self, area_ident,
          width=None, height=None,
          layout_extra=None):
    """
    visualizes scores or measures in a graph

    identifier_list: [{'waterbody_slug': ...}, ...]
    start_end_dates: 2-tuple dates

    each row is an area
    """
    area = get_object_or_404(Area, ident=area_ident)
    # Obsolete: use MeasureCollections instead
    # get measures without parent: main measures
    measures = Measure.objects.filter(Q(waterbodies__area=area)|Q(areas=area))

    start_date = datetime.date(2009,1,1)
    end_date = datetime.date(2011,1,1)
    width = self.GET.get('width', 380)
    height = self.GET.get('height', 170)
    layout_extra = None


    #measures = []
    waterbodies = []
    #for identifier in identifier_list:
    #    # it's a measure
    #    measure = Measure.objects.get(pk=identifier['measure_id'])
    #    measures.append(measure

    if width is None:
        width = 380.0
    if height is None:
        height = 170.0

    # Calculate own height, which can be smaller than given.
    #height = min((len(measures) + len(waterbodies)) * 40 + 20 +
    #             len(legend_handles) * 10.0, height)

    graph = adapter.Graph(start_date, end_date, width, height)

    _image_measures(graph, measures, start_date, end_date)

    graph.add_today()
    return graph.http_png()


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
