# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
from django.conf.urls.defaults import include
from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url
from django.conf import settings
from django.contrib import admin

from lizard_measure.views import (
    MeasureDetailView,
    MeasureHistoryView,
    MeasureHistoryDetailView,
    MeasureArchiveView,
    HorizontalBarGraphView,
)

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

    (r'^measure_graph/(?P<area_ident>.*)/focus/$',
      'lizard_measure.views.measure_graph',
      {'filter': 'focus'},
      "lizard_measure.measure_graph"),

    (r'^measure_graph/(?P<area_ident>.*)/measure/$',
      'lizard_measure.views.measure_graph',
      {'filter': 'measure'},
      "lizard_measure.measure_graph"),
    (r'^measure_graph/(?P<area_ident>.*)/$',
      'lizard_measure.views.measure_graph',
      {'filter': 'all'},
      "lizard_measure.measure_graph"),
    (r'^measure_graph/$',
      'lizard_measure.views.measure_graph_api',
      {},
      "lizard_measure.measure_graph_api"),
    (r'^summary/(?P<area_ident>.*)/krw_measures/$',
     'lizard_measure.views.krw_waterbody_measures',
     {},
     "lizard_measure.krw_waterbody_measures"),
    (r'^summary/(?P<area_ident>.*)/suited_measures/$',
     'lizard_measure.views.suited_measures',
     {},
     "lizard_measure.suited_measures"),
    (r'^summary/(?P<area_ident>.*)/tables/(?P<horizontal_bar_graph_slug>.*)/$',
     'lizard_measure.views.krw_waterbody_ekr_scores',
     {},
     "lizard_measure.krw_waterbody_ekr_scores"),
    (r'^measure/(?P<measure_id>\d+)/$',
     MeasureDetailView.as_view(),
     {},
     "lizard_measure.measure"),
    (r'^history/(?P<measure_id>\d+)/$',
     MeasureHistoryView.as_view(),
     {},
     "lizard_measure.history"),
    (r'^history_details/(?P<measure_id>\d+)/(?P<log_entry_id>\d+)/$',
     MeasureHistoryDetailView.as_view(),
     {},
     "lizard_measure.history_details"),
    (r'^archive/(?P<measure_id>\d+)/(?P<log_entry_id>\d+)/$',
     MeasureArchiveView.as_view(),
     {},
     "lizard_measure.archive"),
    (r'^api/',
     include('lizard_measure.api.urls')),
    #edit screens measures
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

    #edit screens steering parameters
    (r'^steering_parameter_form/$',
    'lizard_measure.views.steering_parameter_form',
     {},
     "lizard_measure.steering_parameter_form"),

    (r'^steering_parameter_overview/$',
     'lizard_measure.views.steerparameter_overview',
         {},
     "lizard_measure.steerparameter_overview"),



    (r'^esf_pattern_form/$',
     'lizard_measure.views.esfpattern_detailedit_portal',
     {},
     "lizard_measure.esfpattern_detailedit_portal"),

    # (r'^measure/(?P<measure_id>\d+)/graph/$',
    #  'lizard_measure.views.krw_measure_graph',
    #  {},
    #  "lizard_measure.measure_graph"),
    # # Search stuff.
    # url(r'^homepage_area_search/',
    #     'lizard_measure.views.waterbody_shapefile_search',
    #     name="lizard_measure_homepage_area_search"),
    # # Map clicking, workspaces
    # (r'^map/', include('lizard_map.urls')),
    # # Fake help page.
    # url(r'^$',
    #     'lizard_measure.views.select_area',
    #     name="help"
    #     ),
    url(r'^bar/$',
        HorizontalBarGraphView.as_view(),
        name="lizard_graph_horizontal_bar_graph_view"),
    )


if settings.DEBUG:
    # Add this also to the projects that use this application
    urlpatterns += patterns(
        '',
        (r'^admin/', include(admin.site.urls)),
        (r'', include('staticfiles.urls')),
    )
