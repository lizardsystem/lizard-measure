from django.contrib import admin

from lizard_measure.models import Area
from lizard_measure.models import Department
from lizard_measure.models import Executive
from lizard_measure.models import FundingOrganization
from lizard_measure.models import KRWWaterType
from lizard_measure.models import Measure
from lizard_measure.models import MeasureCategory
from lizard_measure.models import MeasureCode
from lizard_measure.models import MeasureCollection
from lizard_measure.models import MeasurePeriod
from lizard_measure.models import MeasureStatus
from lizard_measure.models import MeasureStatusMoment
from lizard_measure.models import Municipality
from lizard_measure.models import Organization
from lizard_measure.models import Province
from lizard_measure.models import Unit
from lizard_measure.models import Urgency
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


class MeasureCollectionAdmin(admin.ModelAdmin):
    list_filter = ['waterbody', ]
    list_display = ['__unicode__', 'waterbody', ]
    inlines = [
        MeasureInline,
        ]


class MeasureStatusAdmin(admin.ModelAdmin):
    list_display = ['name', 'value', 'color', ]


admin.site.register(Area)
admin.site.register(Department)
admin.site.register(Executive)
admin.site.register(FundingOrganization)
admin.site.register(KRWWaterType)
admin.site.register(Measure, MeasureAdmin)
admin.site.register(MeasureCategory)
admin.site.register(MeasureCode)
admin.site.register(MeasureCollection, MeasureCollectionAdmin)
admin.site.register(MeasurePeriod)
admin.site.register(MeasureStatus, MeasureStatusAdmin)
admin.site.register(MeasureStatusMoment)
admin.site.register(Municipality)
admin.site.register(Organization)
admin.site.register(Province)
admin.site.register(Unit)
admin.site.register(Urgency)
admin.site.register(WaterBody)
admin.site.register(WaterBodyStatus)
