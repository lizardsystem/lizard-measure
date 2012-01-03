from django.contrib import admin

from lizard_measure.models import Executive
from lizard_measure.models import FundingOrganization
from lizard_measure.models import KRWWaterType
from lizard_measure.models import Measure
from lizard_measure.models import MeasureCategory
from lizard_measure.models import MeasureType
from lizard_measure.models import MeasureStatus
from lizard_measure.models import MeasureStatusMoment
from lizard_measure.models import Municipality
from lizard_measure.models import Organization
from lizard_measure.models import Province
from lizard_measure.models import Unit
from lizard_measure.models import WaterBody
from lizard_measure.models import WaterBodyStatus


class MeasureStatusMomentInline(admin.TabularInline):
    model = MeasureStatusMoment


class FundingOrganizationInline(admin.TabularInline):
    model = FundingOrganization


class MeasureInline(admin.TabularInline):
    model = Measure


class MeasureAdmin(admin.ModelAdmin):
    list_filter = ['waterbody', ]
    inlines = [
        MeasureStatusMomentInline, FundingOrganizationInline,
        ]


class MeasureStatusAdmin(admin.ModelAdmin):
    list_display = ['name', 'value', 'color', ]


admin.site.register(FundingOrganization)
admin.site.register(KRWWaterType)
admin.site.register(Measure, MeasureAdmin)
admin.site.register(MeasureCategory)
admin.site.register(MeasureType)
admin.site.register(MeasureStatus, MeasureStatusAdmin)
admin.site.register(MeasureStatusMoment)
admin.site.register(Municipality)
admin.site.register(Organization)
admin.site.register(Province)
admin.site.register(Unit)
admin.site.register(WaterBody)
admin.site.register(WaterBodyStatus)
