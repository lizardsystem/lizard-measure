# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
from django.conf.urls.defaults import include
from django.conf.urls.defaults import patterns
from django.conf import settings
from django.contrib import admin

from lizard_measure.views import MeasureDetailView


API_URL_NAME = 'lizard_measure_api_root'


admin.autodiscover()

urlpatterns = patterns(
    '',
    # # Homepage.
     # # summary view.
    # (r'^summary/(?P<area>[^/]+)/$',
    #  'lizard_measure.views.waterbody_summary',
    #  {},
    #  'lizard_measure.waterbody',
    #  ),
    # # Graphs for the summary view.
    # (r'^summary/(?P<waterbody_slug>.*)/krw_scores/$',
    #  'lizard_measure.views.krw_scores',
    #  {},
    #  "lizard_measure.krw_scores"),
    # (r'^summary/(?P<area>.*)/indicator/graph/(?P<id>.*)/$',
    #  'lizard_measure.views.indicator_graph',
    #  {},
    #  "lizard_measure.indicator_graph"),
    # (r'^summary/(?P<waterbody_slug>.*)/krw_scores/image/$',
    #  'lizard_measure.views.krw_score_graph',
    #  {},
    #  "lizard_measure.krw_score_graph"),

    (r'^summary/(?P<area_ident>.*)/measure_graph/$',
      'lizard_measure.views.measure_graph',
      {},
      "lizard_measure.measure_graph"),
    (r'^summary/(?P<area_ident>.*)/krw_measures/$',
     'lizard_measure.views.krw_waterbody_measures',
     {},
     "lizard_measure.krw_waterbody_measures"),
    (r'^measure/(?P<measure_id>\d+)/$',
     MeasureDetailView.as_view(),
     {},
     "lizard_measure.measure"),

    #edit screens
    (r'^measure_detailedit_portal/$',
    'lizard_measure.views.measure_detailedit_portal',
     {},
     "lizard_measure.measure_detailedit_portal"),
    (r'^measure_groupedit_portal/$',
    'lizard_measure.views.measure_groupedit_portal',
     {},
     "lizard_measure.measure_groupedit_portal"),
    (r'^organization_groupedit_portal/$',
    'lizard_measure.views.organization_groupedit_portal',
     {},
     "lizard_measure.organization_groupedit_portal"),
    (r'^api/',
     include('lizard_measure.api.urls')),

    # (r'^measure/(?P<measure_id>\d+)/graph/$',
    #  'lizard_measure.views.krw_measure_graph',
    #  {},
    #  "lizard_measure.measure_graph"),
    # # Search stuff.
    )


if settings.DEBUG:
    # Add this also to the projects that use this application
    urlpatterns += patterns(
        '',
        (r'^admin/', include(admin.site.urls)),
        (r'', include('staticfiles.urls')),
    )
