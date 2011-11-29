# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext
# from django.views.decorators.cache import cache_page
import mapnik

from lizard_krw.models import Measure
from lizard_krw.models import MeasureCollection
from lizard_krw.models import WaterBody
from lizard_map import coordinates
from lizard_map.models import Workspace


HOMEPAGE_KEY = 1  # Primary key of the Workspace for rendering the homepage.
CRUMB_HOMEPAGE = {'name': 'home', 'url': '/'}


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
    measure_collection = MeasureCollection.objects.get(
        pk=measure_collection_id)
    if crumbs_prepend:
        crumbs = list(crumbs_prepend)
    else:
        crumbs = [CRUMB_HOMEPAGE]
    crumbs.extend(
        [{'name': measure_collection.waterbody.name,
          'url': measure_collection.waterbody.get_absolute_url()},
         {'name': 'Maatregelen',
          'url': reverse(
                    'lizard_krw.krw_waterbody_measures',
                    kwargs={'waterbody_slug':
                            measure_collection.waterbody.slug})},
         {'name': measure_collection.name,
          'url': reverse(
                    'lizard_krw.measure_collection',
                    kwargs={'measure_collection_id':
                            measure_collection_id})}, ])
    return render_to_response(
        template,
        {'measure_collection': measure_collection,
         'crumbs': crumbs},
        context_instance=RequestContext(request))


def measure_detail(request, measure_id,
                   template='lizard_krw/measure.html'):
    measure = get_object_or_404(Measure, pk=measure_id)

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
         'crumbs': crumbs
         },
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
