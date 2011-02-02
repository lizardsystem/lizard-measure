# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns(
    '',
    # Homepage.
    url(r'^$',
        'lizard_krw.views.select_area',
        name="lizard_krw.select_area"
        ),
    # summary view.
    (r'^summary/(?P<area>[^/]+)/$',
     'lizard_krw.views.waterbody_summary',
     {},
     'lizard_krw.waterbody',
     ),
    # KRW browser.
    url(r'^krw-browser/$',
        'lizard_krw.views.krw_browser',
        name="lizard_krw.krw_browser"
        ),
    # Graphs for the summary view.
    (r'^summary/(?P<waterbody_slug>.*)/krw_scores/$',
     'lizard_krw.views.krw_scores',
     {},
     "lizard_krw.krw_scores"),
    (r'^summary/(?P<area>.*)/indicator/graph/(?P<id>.*)/$',
     'lizard_krw.views.indicator_graph',
     {},
     "lizard_krw.indicator_graph"),
    (r'^summary/(?P<waterbody_slug>.*)/krw_scores/image/$',
     'lizard_krw.views.krw_score_graph',
     {},
     "lizard_krw.krw_score_graph"),
    (r'^summary/(?P<waterbody_slug>.*)/krw_measure_graph/$',
     'lizard_krw.views.krw_measure_graph',
     {},
     "lizard_krw.krw_measure_graph"),
    (r'^summary/(?P<waterbody_slug>.*)/krw_measures/$',
     'lizard_krw.views.krw_waterbody_measures',
     {},
     "lizard_krw.krw_waterbody_measures"),
    # Map for summary view
    (r'^summary/(?P<waterbody_slug>.*)/tiny_map/$',
     'lizard_krw.views.tiny_map',
     {},
     "lizard_krw.tiny_map"),
    # Measure collection
    (r'^measure_collection/(?P<measure_collection_id>\d+)/$',
     'lizard_krw.views.measure_collection',
     {},
     "lizard_krw.measure_collection"),
    # KRW measure info
    (r'^measure/(?P<measure_id>\d+)/$',
     'lizard_krw.views.measure_detail',
     {},
     "lizard_krw.measure"),
    (r'^measure/(?P<measure_id>\d+)/graph/$',
     'lizard_krw.views.single_measure_graph',
     {},
     "lizard_krw.measure_graph"),
    # Search stuff.
    url(r'^homepage_area_search/',
        'lizard_krw.views.waterbody_shapefile_search',
        name="lizard_krw_homepage_area_search"),
    # Map clicking, workspaces
    (r'^map/', include('lizard_map.urls')),
    # Fake help page.
    url(r'^$',
        'lizard_krw.views.select_area',
        name="help"
        ),
    )


if settings.DEBUG:
    # Add this also to the projects that use this application
    urlpatterns += patterns(
        '',
        (r'^admin/', include(admin.site.urls)),
        (r'', include('staticfiles.urls')),
    )
