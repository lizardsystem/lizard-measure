# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

from djangorestframework.views import InstanceModelView
from djangorestframework.views import ListOrCreateModelView

from lizard_measure.api.resources import MeasureResource
from lizard_measure.api.views import RootView


admin.autodiscover()

NAME_PREFIX = 'lizard_measure_api_'

urlpatterns = patterns(
    '',
    url(r'^$',
        RootView.as_view(),
        name=NAME_PREFIX + 'root'),
    url(r'^measure/$',
        ListOrCreateModelView.as_view(resource=MeasureResource),
        name=NAME_PREFIX + 'measure_list'),
    url(r'^measure/(?P<id>\d+)/$',
        InstanceModelView.as_view(resource=MeasureResource),
        name=NAME_PREFIX + 'measure_detail'),
    )
