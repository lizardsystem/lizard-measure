from django.contrib import admin

from lizard_krw.models import AlphaScore
from lizard_krw.models import Area
from lizard_krw.models import AreaPlan
from lizard_krw.models import CatchmentAreaPlan
from lizard_krw.models import Color
from lizard_krw.models import Department
from lizard_krw.models import FundingCategory
from lizard_krw.models import FundingOrganization
from lizard_krw.models import GoalScore
from lizard_krw.models import Measure
from lizard_krw.models import MeasureCategory
from lizard_krw.models import MeasureStatus
from lizard_krw.models import MeasureStatusMoment
from lizard_krw.models import MeasureType
from lizard_krw.models import Organization
from lizard_krw.models import Score
from lizard_krw.models import SingleIndicator
from lizard_krw.models import Unit
from lizard_krw.models import WaterBody
from lizard_krw.models import XMLImport
from lizard_krw.models import XMLImportMeetobject


class SingleIndicatorInline(admin.TabularInline):
    model = SingleIndicator


class MeasureStatusMomentInline(admin.TabularInline):
    model = MeasureStatusMoment


class FundingOrganizationInline(admin.TabularInline):
    model = FundingOrganization


class WaterBodyAdmin(admin.ModelAdmin):
    inlines = [
        SingleIndicatorInline,
        ]


class ScoreAdmin(admin.ModelAdmin):
    list_filter = ['waterbody', ]


class MeasureAdmin(admin.ModelAdmin):
    list_filter = ['waterbody', ]
    inlines = [
        MeasureStatusMomentInline, FundingOrganizationInline,
        ]


admin.site.register(AlphaScore)
admin.site.register(Area)
admin.site.register(AreaPlan)
admin.site.register(CatchmentAreaPlan)
admin.site.register(Color)
admin.site.register(Department)
admin.site.register(FundingCategory)
admin.site.register(FundingOrganization)
admin.site.register(GoalScore, ScoreAdmin)
admin.site.register(Measure, MeasureAdmin)
admin.site.register(MeasureCategory)
admin.site.register(MeasureStatus)
admin.site.register(MeasureStatusMoment)
admin.site.register(MeasureType)
admin.site.register(Organization)
admin.site.register(Score, ScoreAdmin)
admin.site.register(SingleIndicator)
admin.site.register(Unit)
admin.site.register(WaterBody, WaterBodyAdmin)
admin.site.register(XMLImport)
admin.site.register(XMLImportMeetobject)
