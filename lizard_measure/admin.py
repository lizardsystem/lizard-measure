from django.contrib import admin

from lizard_measure.models import FundingOrganization
from lizard_measure.models import KRWWaterType
from lizard_measure.models import Measure
from lizard_measure.models import MeasurePeriod
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
from lizard_measure.models import OWMStatus
from lizard_measure.models import OWMType


class MeasureStatusMomentInline(admin.TabularInline):
    model = MeasureStatusMoment


class FundingOrganizationInline(admin.TabularInline):
    model = FundingOrganization


class MeasureInline(admin.TabularInline):
    model = Measure


class MeasureAdmin(admin.ModelAdmin):
    list_filter = ['waterbody', ]
    readonly_fields = [
        'datetime_in_source',
        'import_raw',
    ]
    inlines = [
        MeasureStatusMomentInline, FundingOrganizationInline,
        ]
    filter_horizontal = ['categories', ]


class MeasureStatusAdmin(admin.ModelAdmin):
    list_display = ['name', 'value', 'color', ]


class MeasureTypeAdmin(admin.ModelAdmin):
    filter_horizontal = ['units', ]


admin.site.register(FundingOrganization)
admin.site.register(KRWWaterType)
admin.site.register(Measure, MeasureAdmin)
admin.site.register(MeasurePeriod)
admin.site.register(MeasureCategory)
admin.site.register(MeasureType, MeasureTypeAdmin)
admin.site.register(MeasureStatus, MeasureStatusAdmin)
admin.site.register(MeasureStatusMoment)
admin.site.register(Municipality)
admin.site.register(Organization)
admin.site.register(Province)
admin.site.register(Unit)
admin.site.register(WaterBody)
admin.site.register(WaterBodyStatus)
admin.site.register(OWMStatus)
admin.site.register(OWMType)
