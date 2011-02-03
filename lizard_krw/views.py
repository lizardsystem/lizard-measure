# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

import StringIO
import datetime

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.cache import cache_page
from matplotlib.dates import date2num
from matplotlib.lines import Line2D
import Image
import mapnik

from lizard_krw.layers import WorkspaceItemAdapterKrw
from lizard_krw.models import AlphaScore
from lizard_krw.models import GoalScore
from lizard_krw.models import Measure
from lizard_krw.models import MeasureCollection
from lizard_krw.models import MeasureStatus
from lizard_krw.models import SCORE_CATEGORIES
from lizard_krw.models import SCORE_CATEGORY_FAUNA
from lizard_krw.models import SCORE_CATEGORY_FLORA
from lizard_krw.models import SCORE_CATEGORY_FYTO
from lizard_krw.models import SCORE_CATEGORY_VIS
from lizard_krw.models import Score
from lizard_krw.models import SingleIndicator
from lizard_krw.models import WaterBody
from lizard_fewsunblobbed.models import Timeserie
from lizard_map import coordinates
from lizard_map.adapter import Graph
from lizard_map.daterange import DateRangeForm
from lizard_map.daterange import current_start_end_dates
from lizard_map.models import Workspace
from lizard_map.workspace import WorkspaceManager


HOMEPAGE_KEY = 1  # Primary key of the Workspace for rendering the homepage.
CRUMB_HOMEPAGE = {'name': 'home', 'url': '/'}


def indicator_graph(request,
                    area=None,
                    id=None):
    class MockTimeserie(object):
        class MockTimeSerieData(object):
            def all(self):
                return []
        name = 'geen tijdreeks beschikbaar'
        timeseriedata = MockTimeSerieData()

    indicator = get_object_or_404(SingleIndicator, pk=id)
    # Figure size
    width = request.GET.get('width', 1000)
    height = request.GET.get('height', 400)
    start_date, end_date = current_start_end_dates(request)

    krw_graph = Graph(start_date, end_date, width, height)

    # Check if timeserie exists. Else: use mock.
    try:
        timeserie = indicator.timeserie
    except Timeserie.DoesNotExist:
        timeserie = MockTimeserie()

    # Title.
    krw_graph.suptitle(timeserie.name)
    # Two steering lines.
    if indicator.target_value:
        krw_graph.axes.axhline(indicator.target_value,
                               color='green',
                               lw=3,
                               label='Richtwaarde')
    if indicator.boundary_value:
        krw_graph.axes.axhline(indicator.boundary_value,
                               color='red',
                               lw=3,
                               label='Grenswaarde')

    dates = []
    values = []
    for data in timeserie.timeseriedata.all():
        dates.append(data.tsd_time)
        values.append(data.tsd_value)
    krw_graph.axes.plot(dates, values,
                        lw=1,
                        color='blue')
    y_min, y_max = krw_graph.axes.get_ylim()
    if indicator.y_min is not None:
        y_min = indicator.y_min
    if indicator.y_max is not None:
        y_max = indicator.y_max
    krw_graph.axes.set_ylim(y_min, y_max)
    krw_graph.legend()
    krw_graph.legend_space()

    # Show line for today.
    krw_graph.add_today()
    return krw_graph.http_png()


def krw_score_graph(request, waterbody_slug):
    """
    Draws a krw score chart
    """

    waterbody = get_object_or_404(WaterBody, slug=waterbody_slug)

    start_date, end_date = current_start_end_dates(request)
    # we fit 50 scores in the graph
    score_width = (date2num(end_date) - date2num(start_date)) / 50
    width = request.GET.get('width', 1000)
    height = request.GET.get('height', 400)
    krw_graph = Graph(start_date, end_date, width, height)

    # add specific graphics to krw_graph
    scores = Score.objects.filter(start_date__gte=start_date,
                                  start_date__lte=end_date,
                                  waterbody=waterbody)

    display_score = {
        SCORE_CATEGORY_FYTO: [],
        SCORE_CATEGORY_FLORA: [],
        SCORE_CATEGORY_FAUNA: [],
        SCORE_CATEGORY_VIS: [],
        }  # Dict of lists
    display_colors = {
        SCORE_CATEGORY_FYTO: [],
        SCORE_CATEGORY_FLORA: [],
        SCORE_CATEGORY_FAUNA: [],
        SCORE_CATEGORY_VIS: [],
        }  # Dict of lists
    for score in scores:
        category = score.category
        alpha_score = score.alpha_score
        display_score[category].append(
            (date2num(score.start_date), score_width))
        display_colors[category].append(
            alpha_score.color.html)

    display_positions = {
        SCORE_CATEGORY_FYTO: (27, 6),
        SCORE_CATEGORY_FLORA: (17, 6),
        SCORE_CATEGORY_FAUNA: (7, 6),
        SCORE_CATEGORY_VIS: (-3, 6),
        }
    categories = [SCORE_CATEGORY_FYTO, SCORE_CATEGORY_FLORA,
                  SCORE_CATEGORY_FAUNA, SCORE_CATEGORY_VIS]
    for category in categories:
        krw_graph.axes.broken_barh(display_score[category],
                                   display_positions[category],
                                   facecolors=display_colors[category],
                                   edgecolors='grey')

    # Y ticks.
    krw_graph.axes.set_yticks([0, 10, 20, 30])
    krw_graph.axes.set_yticklabels([
            SCORE_CATEGORIES[SCORE_CATEGORY_VIS],
            SCORE_CATEGORIES[SCORE_CATEGORY_FAUNA],
            SCORE_CATEGORIES[SCORE_CATEGORY_FLORA],
            SCORE_CATEGORIES[SCORE_CATEGORY_FYTO]])

    krw_graph.axes.set_ylim(-5, 35)

    # Legend
    legend_handles = []
    legend_labels = []
    for alpha_score in AlphaScore.objects.all():
        legend_handles.append(
            Line2D([], [], color=alpha_score.color.html, lw=10))
        legend_labels.append(alpha_score.name)
    krw_graph.legend(legend_handles, legend_labels)
    krw_graph.legend_space()

    # Future
    subplot_numbers = [312, 313]

    goalscores = GoalScore.objects.filter(waterbody=waterbody)
    # Collect goal score dates
    goalscore_dates = {}
    for goalscore in goalscores:
        goalscore_dates[goalscore.start_date] = None
    goalscore_dates_sorted = goalscore_dates.keys()
    goalscore_dates_sorted.sort()

    for goalscore_date_index, goalscore_date in enumerate(
        goalscore_dates_sorted):

        axes_future = krw_graph.figure.add_subplot(
            subplot_numbers[goalscore_date_index])
        axes_future.set_yticks([0, 10, 20, 30])
        axes_future.set_yticklabels(['', '', '', ''])
        axes_future.set_xticks([0.5, ])
        goalscores = GoalScore.objects.filter(waterbody=waterbody,
                                              start_date=goalscore_date)
        axes_future.set_xticklabels([str(goalscores[0].start_date.year), ])
        for goalscore in goalscores:  # Should be 4.
            axes_future.broken_barh(
                [(0, 1)],
                display_positions[goalscore.category],
                facecolors=goalscore.alpha_score.color.html,
                edgecolors='grey')
        axes_future.set_ylim(-5, 35)
        axes_future.set_position((
                (1 - krw_graph.legend_width + 0.015 +
                 goalscore_date_index * 0.03),
                krw_graph.bottom_axis_location,
                0.015,
                1 - 2 * krw_graph.bottom_axis_location))
        axes_future.axvline(date2num(end_date), color='blue', lw=1, ls='--')
        axes_future.set_xlim((0, 1))

    # finish up
    krw_graph.add_today()

    return krw_graph.http_png()


def krw_measure_graph(request, waterbody_slug=None):
    """
    Draw krw measure graphs.

    uses datetime.datetime.now() for current time

    uses _image_measures draw function from WorkspaceItemAdapterKrw
    """
    if waterbody_slug is None:
        waterbody_slug = request.GET.get("waterbody")
    waterbody = get_object_or_404(WaterBody, slug=waterbody_slug)

    measure_collections = MeasureCollection.objects.filter(
        waterbody=waterbody)
    measures = Measure.objects.filter(is_indicator=True, waterbody=waterbody)

    start_date, end_date = current_start_end_dates(request)
    # one cannot realize things in the future, so do not visualize
    end_date_realized = min(end_date, datetime.datetime.now().date())
    width = request.GET.get('width', 1000)
    height = request.GET.get('height', 400)
    krw_graph = Graph(start_date, end_date, width, height)

    krw_graph.axes.set_ylim(0, len(measures))

    # Draw krw measure collections
    WorkspaceItemAdapterKrw._image_measures(
        krw_graph, measure_collections,
        start_date, end_date, end_date_realized,
        add_legend=False)

    # Legend
    measure_statuses = MeasureStatus.objects.all()
    handles = [Line2D([], [], color=s.color.html, lw=10)
               for s in measure_statuses]
    labels = [status.name for status in measure_statuses]
    krw_graph.legend(handles, labels)
    krw_graph.legend_space()

    krw_graph.add_today()

    return krw_graph.http_png()


def single_measure_graph(request, measure_id, width=None, height=None):
    """
    Graph for single measure, not using workspace technology
    """
    measure = get_object_or_404(Measure, pk=measure_id)
    if width is None:
        width = 650.0
    start_date, end_date = current_start_end_dates(request)
    return measure.image(start_date, end_date, width=width, height=height)


# TODO: cache should be different for IE...
@cache_page(24 * 60 * 60)
def tiny_map(request, waterbody_slug=None, shape_id=None,
             bbox=(523838.00391791, 6818214.5267836,
                   575010.91942212, 6869720.7532931)):
    """Return PNG of area map. Code based on lizard_map.views:wms"""
    width = 300
    height = 140

    # Map settings
    mapnik_map = mapnik.Map(width, height)
    mapnik_map.srs = coordinates.GOOGLE
    mapnik_map.background = mapnik.Color('transparent')

    layer_arguments = {
        'layer': 'background',
        'waterbody_slug': waterbody_slug}
    if shape_id is not None:
        layer_arguments.update({'shape_id': shape_id})
    workspace_item_adapter = WorkspaceItemAdapterKrw(
        None,
        layer_arguments=layer_arguments)
    layers, styles = workspace_item_adapter.layer()
    for layer in layers:
        mapnik_map.layers.append(layer)
    for name in styles:
        mapnik_map.append_style(name, styles[name])

    #Zoom and create image
    mapnik_map.zoom_to_box(mapnik.Envelope(*bbox))
    # m.zoom_to_box(layer.envelope())
    img = mapnik.Image(width, height)
    mapnik.render(mapnik_map, img)
    http_user_agent = request.META.get('HTTP_USER_AGENT', '')
    rgba_image = Image.fromstring('RGBA', (width, height), img.tostring())
    buf = StringIO.StringIO()
    if 'MSIE 6.0' in http_user_agent:
        imgPIL = rgba_image.convert('P')
        imgPIL.save(buf, 'png', transparency=0)
    else:
        rgba_image.save(buf, 'png')
    buf.seek(0)
    response = HttpResponse(buf.read())
    response['Content-type'] = 'image/png'
    return response


def waterbody_summary(request,
                      area=None,
                      template='lizard_krw/water_body_summary.html'):
    water_body = get_object_or_404(WaterBody, slug=area)
    indicators = water_body.indicators.all()
    shown_indicators = [indicator for indicator in
                        indicators[:2]]
    unused_indicators = [indicator for indicator in
                         indicators[2:]]
    date_range_form = DateRangeForm(
        current_start_end_dates(request, for_form=True))
    crumbs = [CRUMB_HOMEPAGE,
              {'name': water_body.name,
               'url': water_body.get_absolute_url()},]

    return render_to_response(
        template,
        {'water_body': water_body,
         'indicators': indicators,
         'shown_indicators': shown_indicators,
         'unused_indicators': unused_indicators,
         'date_range_form': date_range_form,
         'crumbs': crumbs},
        context_instance=RequestContext(request))


def select_area(request, template='lizard_krw/select_area.html',
                homepage_key=HOMEPAGE_KEY):
    water_bodies = WaterBody.objects.all()
    special_homepage_workspace = get_object_or_404(
        Workspace, pk=homepage_key)

    crumbs = [CRUMB_HOMEPAGE]

    return render_to_response(
        template,
        {'water_bodies': water_bodies,
         'workspaces': {'user': [special_homepage_workspace]},
         'javascript_hover_handler': 'popup_hover_handler',
         'javascript_click_handler': 'homepage_area_click_handler',
         'crumbs': crumbs},
        context_instance=RequestContext(request))


def krw_browser(request, template='lizard_krw/krw-browser.html',
                crumbs_prepend=None):
    """Show krw browser.

    Automatically makes new workspace if not yet available

    """
    workspace_manager = WorkspaceManager(request)
    workspaces = workspace_manager.load_or_create()
    date_range_form = DateRangeForm(
        current_start_end_dates(request, for_form=True))

    if crumbs_prepend is not None:
        crumbs = crumbs_prepend
    else:
        crumbs = [{'name': 'home', 'url': '/'}]
    crumbs.append({'name': 'krw gegevens',
                   'title': 'krw gegevens',
                   'url': reverse('krw-browser')})

    return render_to_response(
        template,
        {'date_range_form': date_range_form,
         'workspaces': workspaces,
         'javascript_hover_handler': 'popup_hover_handler',
         'javascript_click_handler': 'popup_click_handler',
         'crumbs': crumbs},
        context_instance=RequestContext(request))


def waterbody_shapefile_search(request):
    """Return url to redirect to if a waterbody is found.

    Only works with adapter lizard_shape.
    """
    google_x = float(request.GET.get('x'))
    google_y = float(request.GET.get('y'))

    # Set up a basic map as only map can search...
    mapnik_map = mapnik.Map(400, 400)
    mapnik_map.srs = coordinates.GOOGLE

    workspace = Workspace.objects.get(name="Homepage")
    # The following adapter should be available in the fixture.
    adapter = workspace.workspace_items.all()[0].adapter

    search_results = adapter.search(google_x, google_y)

    # Return url of first found object.
    for search_result in search_results:
        #name_in_shapefile = search_result['name']
        id_in_shapefile = search_result['identifier']['id']
        water_body = WaterBody.objects.get(ident=id_in_shapefile)
        return HttpResponse(water_body.get_absolute_url())

    # Nothing found? Return an empty response and the javascript popup handler
    # will fire.
    return HttpResponse('')


def measure_collection(request, measure_collection_id,
                       template='lizard_krw/measure_collection.html',
                       crumbs_prepend=None):
    return render_to_response(
        template,
        {},
        context_instance=RequestContext(request))


def measure_detail(request, measure_id,
                   template='lizard_krw/measure.html'):
    measure = get_object_or_404(Measure, pk=measure_id)

    date_range_form = DateRangeForm(
        current_start_end_dates(request, for_form=True))

    crumbs = [CRUMB_HOMEPAGE,
              {'name': measure.waterbody.name,
               'url': measure.waterbody.get_absolute_url()},
              {'name': 'Maatregelen',
               'url': reverse(
                'lizard_krw.krw_waterbody_measures',
                kwargs={'waterbody_slug': measure.waterbody.slug})},
              {'name': measure.name,
               'url': measure.get_absolute_url()}]

    return render_to_response(
        template,
        {'measure': measure,
         'date_range_form': date_range_form,
         'crumbs': crumbs
         },
        context_instance=RequestContext(request))


def krw_waterbody_measures(request, waterbody_slug,
                           template='lizard_krw/waterbody_measures.html'):
    waterbody = get_object_or_404(WaterBody, slug=waterbody_slug)
    date_range_form = DateRangeForm(
        current_start_end_dates(request, for_form=True))
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
                kwargs={'waterbody_slug': waterbody.slug})},]

    return render_to_response(
        template,
        {'waterbody': waterbody,
         'date_range_form': date_range_form,
         'main_measures': main_measures,
         'measure_collections': measure_collections,
         'crumbs': crumbs
         },
        context_instance=RequestContext(request))


def krw_scores(request, waterbody_slug,
               template='lizard_krw/krw_scores.html'):
    """
    Displays big table with krw scores for a specific waterbody.
    """
    waterbody = WaterBody.objects.get(slug=waterbody_slug)
    scores = Score.objects.filter(waterbody=waterbody)
    goalscores = GoalScore.objects.filter(waterbody=waterbody)

    scores_list = []  # Must contain list of {scores, name, goalscore}

    for category in [SCORE_CATEGORY_FYTO, SCORE_CATEGORY_FLORA,
                     SCORE_CATEGORY_FAUNA, SCORE_CATEGORY_VIS]:
        scores = scores.filter(category=category)
        goalscores = goalscores.filter(category=category)
        category_name = SCORE_CATEGORIES[category]
        scores_list.append({'scores': scores,
                           'goalscores': goalscores,
                           'name': category_name})

    crumbs = [
        CRUMB_HOMEPAGE,
        {'name': waterbody.name,
         'url': waterbody.get_absolute_url()},
        {'name': 'Scores',
         'url': reverse('lizard_krw.krw_scores', kwargs={
                    'waterbody_slug': waterbody.slug})}]

    return render_to_response(
        template,
        {'scores': scores,
         'scores_list': scores_list,
         'waterbody': waterbody,
         'crumbs': crumbs,
            },
        context_instance=RequestContext(request))
