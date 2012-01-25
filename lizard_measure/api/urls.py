# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url
from django.contrib import admin

from lizard_measure.api.views import RootView
from lizard_measure.api.views import MeasureView
from lizard_measure.api.views import OrganizationView
from lizard_measure.api.views import ScoreView

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
    )



