from django.contrib import admin

from lizard_measure.models import FundingOrganization
from lizard_measure.models import Measure
from lizard_measure.models import MeasurePeriod
from lizard_measure.models import MeasureCategory
from lizard_measure.models import MeasureType
from lizard_measure.models import MeasureStatus
from lizard_measure.models import MeasureStatusMoment
from lizard_measure.models import Organization
from lizard_measure.models import Unit
from lizard_measure.models import WaterBody
from lizard_measure.models import KRWStatus
from lizard_measure.models import KRWWatertype
from lizard_measure.models import Score
from lizard_measure.models import MeasuringRod



class MeasureStatusMomentInline(admin.TabularInline):
    model = MeasureStatusMoment


class FundingOrganizationInline(admin.TabularInline):
    model = FundingOrganization


class MeasureInline(admin.TabularInline):
    model = Measure


class MeasureAdmin(admin.ModelAdmin):
    list_filter = [
        'waterbodies',
        'areas',
    ]
    readonly_fields = [
        'datetime_in_source',
        'import_raw',
    ]
    inlines = [
        MeasureStatusMomentInline, FundingOrganizationInline,
        ]
    filter_horizontal = [
        'categories',
        'waterbodies',
        'areas',
    ]


class MeasureStatusAdmin(admin.ModelAdmin):
    list_display = ['name', 'value', 'color', ]


class MeasureTypeAdmin(admin.ModelAdmin):
    filter_horizontal = ['units', ]


class ScoreAdmin(admin.ModelAdmin):
    list_display = [
        'measuring_rod',
        'area',
        'limit_bad_insufficient',
        'limit_insufficient_moderate',
    ]


class MeasuringRodAdmin(admin.ModelAdmin):
    list_display = [
        'group',
        'measuring_rod',
        'sub_measuring_rod',
        'unit',
        'sign',
    ]

admin.site.register(FundingOrganization)
admin.site.register(Measure, MeasureAdmin)
admin.site.register(MeasurePeriod)
admin.site.register(MeasureCategory)
admin.site.register(MeasureType, MeasureTypeAdmin)
admin.site.register(MeasureStatus, MeasureStatusAdmin)
admin.site.register(MeasureStatusMoment)
admin.site.register(Organization)
admin.site.register(Unit)
admin.site.register(WaterBody)
admin.site.register(KRWStatus)
admin.site.register(KRWWatertype)
admin.site.register(Score, ScoreAdmin)
admin.site.register(MeasuringRod, MeasuringRodAdmin)
