# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url
from django.contrib import admin

from lizard_measure.api.views import RootView
from lizard_measure.api.views import MeasureView
from lizard_measure.api.views import OrganizationView
from lizard_measure.api.views import ScoreView
from lizard_measure.api.views import SteeringParameterFreeView
from lizard_measure.api.views import SteeringParameterPredefinedGraphView
from lizard_measure.api.views import SteerParameterGraphs
from lizard_measure.api.views import EsfPattern
from lizard_measure.api.views import SteerParameterOverview


admin.autodiscover()

NAME_PREFIX = 'lizard_measure_api_'

urlpatterns = patterns(
    '',
    url(r'^$',
        RootView.as_view(),
        name=NAME_PREFIX + 'root'),
    url(r'^measure/$',
        MeasureView.as_view(),
        name=NAME_PREFIX + 'measure'),
    url(r'^organization/$',
        OrganizationView.as_view(),
        name=NAME_PREFIX + 'organization'),
    url(r'^score/$',
        ScoreView.as_view(),
        name=NAME_PREFIX + 'score'),
    url(r'^steer_free/$',
        SteeringParameterFreeView.as_view(),
        name=NAME_PREFIX + 'steering_parameter'),
    url(r'^steer_predefined/$',
        SteeringParameterPredefinedGraphView.as_view(),
        name=NAME_PREFIX + 'steering_parameter_predefined'),
    url(r'^steer_parameter_overview/$',
        SteerParameterOverview.as_view(),
        name=NAME_PREFIX + 'steer_parameter_overview'),


    url(r'^steer_parameter_graphs/$',
        SteerParameterGraphs.as_view(),
        name=NAME_PREFIX + 'steering_parameter_graphs'),
    url(r'^esf_pattern/$',
        EsfPattern.as_view(),
        name=NAME_PREFIX + 'esf_pattern')

    )
