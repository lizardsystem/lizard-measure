# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

import json

from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.http import HttpResponse
from django.template import RequestContext
from django.template import TemplateDoesNotExist
from django.template import Template
from django.template.loader import get_template



# from django.views.decorators.cache import cache_page

from lizard_measure.models import Measure
from lizard_measure.models import WaterBody
from lizard_measure.models import MeasureType
from lizard_measure.models import MeasurePeriod
from lizard_measure.models import MeasureCategory
from lizard_measure.models import Unit

HOMEPAGE_KEY = 1  # Primary key of the Workspace for rendering the homepage.
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
            'measure_types': json.dumps([{'id': r.id, 'name': str(r) } for r in MeasureType.objects.all()]),
            'periods': json.dumps([{'id': r.id, 'name': str(r) } for r in MeasurePeriod.objects.all()]),
            'aggregations': json.dumps([{'id': r[0], 'name': r[1] } for r in Measure.AGGREGATION_TYPE_CHOICES]),
            'categories': json.dumps([{'id': r.id, 'name': str(r) } for r in MeasureCategory.objects.all()]),
            'units': json.dumps([{'id': r.id, 'name': str(r) } for r in Unit.objects.all()])


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
            'measure_types': json.dumps([{'id': r.id, 'name': str(r) } for r in MeasureType.objects.all()]),
            'periods': json.dumps([{'id': r.id, 'name': str(r) } for r in MeasurePeriod.objects.all()]),
            'aggregations': json.dumps([{'id': r[0], 'name': r[1] } for r in Measure.AGGREGATION_TYPE_CHOICES]),
            'categories': json.dumps([{'id': r.id, 'name': str(r) } for r in MeasureCategory.objects.all()]),
            'units': json.dumps([{'id': r.id, 'name': str(r) } for r in Unit.objects.all()])
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
