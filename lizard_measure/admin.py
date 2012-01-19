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
    filter_horizontal = ['units']
    list_display_links = ['description']
    list_display = [
        'code',
        'description',
        'group',
        'klass',
        'subcategory',
        'harmonisation',
        'combined_name',
        'valid',
    ]


class ScoreAdmin(admin.ModelAdmin):
    list_display = [
        'measuring_rod',
        'area',
        'mep',
        'gep',
        'limit_insufficient_moderate',
        'limit_bad_insufficient',
        'ascending'
    ]


class MeasuringRodAdmin(admin.ModelAdmin):
    list_display = [
        'group',
        'measuring_rod',
        'sub_measuring_rod',
        'unit',
        'sign',
    ]


class UnitAdmin(admin.ModelAdmin):
    list_display_links = ['description']
    list_display = [
        'code',
        'description',
        'dimension',
        'conversion_factor',
        'group',
        'valid',
    ]


class KRWStatusAdmin(admin.ModelAdmin):
    list_display_links = ['description']
    list_display = [
        'code',
        'description',
        'valid',
    ]


class KRWWatertypeAdmin(admin.ModelAdmin):
    list_display_links = ['description']
    list_display = [
        'code',
        'description',
        'group',
        'valid',
    ]


class OrganizationAdmin(admin.ModelAdmin):
    list_display_links = ['description']
    list_display = [
        'code',
        'description',
        'group',
        'source',
        'valid',
    ]


admin.site.register(FundingOrganization)
admin.site.register(Measure, MeasureAdmin)
admin.site.register(MeasurePeriod)
admin.site.register(MeasureCategory)
admin.site.register(MeasureType, MeasureTypeAdmin)
admin.site.register(MeasureStatus, MeasureStatusAdmin)
admin.site.register(MeasureStatusMoment)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(WaterBody)
admin.site.register(KRWStatus, KRWStatusAdmin)
admin.site.register(KRWWatertype, KRWWatertypeAdmin)
admin.site.register(Score, ScoreAdmin)
admin.site.register(MeasuringRod, MeasuringRodAdmin)
