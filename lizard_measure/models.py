# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
import datetime
import logging

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from treebeard.al_tree import AL_Node  # Adjacent list implementation

from lizard_map.models import ColorField
from lizard_map.utility import short_string

from lizard_geo.models import GeoObject

from lizard_area.models import Area


logger = logging.getLogger(__name__)


class KRWWaterType(models.Model):
    """
    TypeKRWTypologie, zie Aquo standaard domein
    """
    class Meta:
        verbose_name = _("KRW water type")
        verbose_name_plural = _("KRW water types")

    name = models.CharField(max_length=80)
    code = models.CharField(max_length=8)

    def __unicode__(self):
        return u'%s - %s' % (self.code, self.name)


class WaterBodyStatus(models.Model):
    """Waterbody status
    """
    class Meta:
        verbose_name = _("Waterbody status")
        verbose_name_plural = _("Waterbody statuses")

    name = models.CharField(max_length=80)

    def __unicode__(self):
        return u'%s' % self.name


class Province(models.Model):
    """Provincie"""
    class Meta:
        verbose_name = _("Province")
        verbose_name_plural = _("Provinces")

    name = models.CharField(max_length=200)

    def __unicode__(self):
        return u'%s' % self.name


class Municipality(models.Model):
    """Gemeente"""
    class Meta:
        verbose_name = _("Municipality")
        verbose_name_plural = _("Municipalities")

    name = models.CharField(max_length=200)

    def __unicode__(self):
        return u'%s' % self.name


class WaterBody(models.Model):
    """Specific area for which we want to know KRW scores"""

    class Meta:
        verbose_name = _("Waterbody")
        verbose_name_plural = _("Waterbodies")
        ordering = ("name",)

    area = models.ForeignKey(Area, null=True, blank=True)

    name = models.CharField(max_length=80)
    slug = models.SlugField(help_text=u"Name used for URL.")
    ident = models.CharField(
        max_length=80,
        help_text=u"The ID corresponding to the shapefile ID.")
    description = models.TextField(null=True, blank=True,
                                   help_text="extra info, not displayed")

    # Infoscreen. All fields are optional.
    status = models.ForeignKey(
        WaterBodyStatus, null=True, blank=True, help_text="status")
    water_type = models.ForeignKey(
        KRWWaterType, null=True, blank=True, help_text="krw water type")

    protected_area_reason = models.TextField(
        null=True, blank=True, help_text="beschermd gebied vanwege")

    code = models.CharField(max_length=80, null=True, blank=True)
    province = models.ManyToManyField(
        Province, null=True, blank=True, help_text="provincie")
    municipality = models.ManyToManyField(
        Municipality, null=True, blank=True, help_text="gemeente")

    characteristics = models.TextField(
        null=True, blank=True, help_text="karakteristiek")
    current_situation_chemicals = models.TextField(
        null=True, blank=True,
        help_text="Normoverschrijding chemie huidige situatie")
    control_parameters = models.TextField(
        null=True, blank=True,
        help_text="stuurparameters")

    def __unicode__(self):
        return u'%s' % (self.name)

    @models.permalink
    def get_absolute_url(self):
        return ('lizard_krw.waterbody',
                (),
                {'area': str(self.slug)})


# Measures
class MeasureCategory(models.Model):
    """Measure Category. i.e. Beheermaatregelen
    """

    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = _("Measure category")
        verbose_name_plural = _("Measure categories")

    def __unicode__(self):
        return u'%s' % (self.name)


class Unit(models.Model):
    """eenheid uit aquo standaard
    http://www.idsw.nl/Aquo/uitwisselmodellen/index.htm?goto=6:192
    """

    unit = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    valid = models.NullBooleanField(default=False)


    class Meta:
        verbose_name = _("Unit")
        verbose_name_plural = _("Units")

    def __unicode__(self):
        return u'%s' % self.unit


class MeasureType(models.Model):
    """
    Measure Type. i.e. BE01 Beheermaatregelen uitvoeren actief
    visstands- of schelpdierstandsbeheer
    """

    code = models.CharField(max_length=80)
    description = models.TextField()

    # Future may require a separate MeasureCodeGroup model for this
    group = models.ForeignKey(MeasureCategory, null=True, blank=True)

    # Other fields from KRW import
    units = models.ManyToManyField(Unit)
    klass = models.CharField(max_length=256, null=True, blank=True)
    subcategory = models.CharField(max_length=256, null=True, blank=True)
    harmonisation = models.CharField(max_length=256, null=True, blank=True)
    combined_name = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        verbose_name = _("Measure type")
        verbose_name_plural = _("Measure types")
        ordering = ('code', )

    def __unicode__(self):
        return u'%s - %s' % (self.code, self.description)


class Executive(models.Model):
    """Uitvoerder_Initiatiefnemer. i.e. Landbouw, Provincie
    """
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = _("Executive")
        verbose_name_plural = _("Executives")

    def __unicode__(self):
        return u'%s' % self.name



class Organization(models.Model):
    """Companies that occur in Measures: Funding Organizations
    """

    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")
        ordering = ('name', )

    def __unicode__(self):
        return u'%s' % self.name


class FundingOrganization(models.Model):
    """
    Links Organizations and measures adding cost info.
    """

    class Meta:
        verbose_name = _("Funding organization")
        verbose_name_plural = _("Funding organizations")

    cost = models.FloatField()  # in euro's
    percentage = models.FloatField()
    organization = models.ForeignKey(Organization)
    # vvv To be removed permanently
    #organization_part = models.ForeignKey(
    #    OrganizationPart, blank=True, null=True)
    measure = models.ForeignKey('Measure')

    def __unicode__(self):
        return u'%s: %s (EUR %f,-)' % (
            self.organization, self.measure, self.cost)


class MeasureStatus(models.Model):
    """
    Status van een (deel)maatregel
    """

    name = models.CharField(max_length=200)
    # Color is matplotlib style, i.e. '0.75', 'red', '#eeff00'.
    color = ColorField(
        max_length=20,
        help_text="Color is rrggbb")
    # Value is 1.0 for up and running, 0 for nothing. Used for ordering.
    value = models.FloatField(default=0.0)

    class Meta:
        verbose_name = _("Measure status")
        verbose_name_plural = _("Measure statuses")
        ordering = ('-value', )

    def __unicode__(self):
        return u'%s' % self.name


class MeasureStatusMoment(models.Model):
    """
    MeasureStatus in time
    """

    measure = models.ForeignKey('Measure')
    status = models.ForeignKey(MeasureStatus)
    datetime = models.DateField()
    is_planning = models.BooleanField(default=False)
    description = models.TextField(
        blank=True, null=True,
        help_text="Beschrijving statusupdate. Aangeraden om dit in te vullen")

    investment_expenditure = models.IntegerField(
        blank=True, null=True,
        help_text="Gemaakte investeringskosten")
    exploitation_expenditure = models.IntegerField(
        blank=True, null=True,
        help_text="Gemaakte exploitatiekosten")

    class Meta:
        verbose_name = _("Measure status moment")
        verbose_name_plural = _("Measure status moments")
        ordering = ("datetime", )

    def __unicode__(self):
        return u'%s %s %s' % (self.measure, self.status, self.datetime)


class MeasurePeriod(models.Model):
    """Period"""

    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ('start_date', 'end_date', )
        verbose_name = _("Measure period")
        verbose_name_plural = _("Measure periods")

    def __unicode__(self):
        return '%d - %d' % (self.start_date.year, self.end_date.year)


class Measure(models.Model):
    """
    KRW maatregel,

    For drawing the measure graph, we only need the fields:
    name, start_date, end_date, status
    """

    AGGREGATION_TYPE_CHOICES = (
        (1, _('Min')),
        (2, _('Max')),
        (3, _('Avg')))

    AGGREGATION_TYPE_MIN = 1
    AGGREGATION_TYPE_MAX = 2
    AGGREGATION_TYPE_AVG = 3

    SOURCE_CHOICES = (
        (1, 'KRW-portaal'),
        (2, 'VSS-2010'),
        (3, 'Handmatig'),
    )

    SOURCE_KRW_PORTAAL = 1
    SOURCE_VSS_2010 = 2
    SOURCE_MANUAL = 3

    parent = models.ForeignKey('self', blank=True, null=True)

    ident = models.CharField(
        max_length=64, unique=True, blank=True, null=True,
    )

    is_KRW_measure = models.NullBooleanField()

    # XY, geometry?

    measure_type = models.ForeignKey(
        MeasureType,
        help_text="SGBP code",
    )

    title = models.CharField(max_length=256, null=True, blank=True)

    # Beleidsdoel?

    period = models.ForeignKey(MeasurePeriod, blank=True, null=True)

    # Fields related to import
    import_source = models.CharField(
        max_length=16, editable=False, default=SOURCE_MANUAL
    )
    datetime_in_source = models.DateTimeField(blank=True, null=True)
    import_raw = models.TextField(blank=True, null=True)

    # aggregation is used to 'summarize' the statuses from child measures
    # and its own status (they are equal in value, normally one would not give
    # status to main measure if it has child measures)
    # affects function current_status_moment
    aggregation_type = models.IntegerField(
        choices=AGGREGATION_TYPE_CHOICES,
        default=AGGREGATION_TYPE_MIN,
    )


    waterbody = models.ManyToManyField(
        WaterBody,
        help_text="Bij welk waterlichaam hoort deze maatregel?",
    )

    description = models.CharField(max_length=512, blank=True, null=True)

    category = models.ManyToManyField(MeasureCategory)

    value = models.FloatField(
        help_text="Omvang van maatregel, inhoud afhankelijk van eenheid")
    unit = models.ForeignKey(
        Unit,
        help_text="Eenheid behorende bij omvang van maatregel")

    responsible_organization = models.ForeignKey(
        Organization,
        help_text="Verantwoordelijke organisatie")

    executive = models.ForeignKey(
        Executive,
        help_text="Initiatiefnemer/uitvoerder")

    total_costs = models.IntegerField(
        null=True, blank=True, help_text="Totale kosten in euro's")
    investment_costs = models.IntegerField(
        null=True, blank=True, help_text="Investeringskosten in euro's")
    exploitation_costs = models.IntegerField(
        null=True, blank=True, help_text="Exploitatiekosten in euro's")


    status = models.ManyToManyField(MeasureStatus,
                                    through='MeasureStatusMoment')

    read_only = models.BooleanField(
        default=False,
        help_text=('Wanneer een maatregel read-only is, is hij geimporteerd '
                   'en dient hij niet met de hand gewijzigd te worden'))

    # Is this different from is_KRW_measure?
    is_indicator = models.BooleanField(default=False)
    owner = models.ForeignKey(User, blank=True, null=True)

    class Meta:
        verbose_name = _("Measure")
        verbose_name_plural = _("Measures")

    def __unicode__(self):
        return u'%s: %s' % (self.waterbody.name, self.name)

    @property
    def shortname(self):
        return short_string(self.name, 17)

    def status_moment_self(self, dt=datetime.datetime.now(),
                           is_planning=False):
        """Returns own status_moment"""
        measure_status_moment_set = self.measurestatusmoment_set.filter(
            is_planning=is_planning,
            datetime__lte=dt).distinct().order_by("-datetime")
        if measure_status_moment_set:
            return measure_status_moment_set[0]
        return None

    def status_moment(self, dt=datetime.datetime.now(), is_planning=False):
        """
        Get status for a given datetime (defaults to today)
        returns MeasureStatusMoment or None.

        If any children: Aggregates from child measures

        """
        # Collect status_moments from children OR self.
        if not self.get_children():
            msm_self = self.status_moment_self(dt=dt, is_planning=is_planning)
            measure_status_moments = [msm_self, ]
        else:
            measure_status_moments = [
                m.status_moment(dt=dt, is_planning=is_planning)
                for m in self.get_children()]

        # Apparently some directly related measures has no status
        if (None in measure_status_moments and
            self.aggregation_type == self.AGGREGATION_TYPE_MIN):

            return None

        # Remove Nones
        measure_status_moments = filter(None, measure_status_moments)

        # No status info at all.
        if not measure_status_moments:
            return None

        #min, max or avg out of measure_status_moments
        if self.aggregation_type == self.AGGREGATION_TYPE_MIN:
            return min(measure_status_moments,
                       key=lambda msm: msm.status.value)
        elif self.aggregation_type == self.AGGREGATION_TYPE_MAX:
            return max(measure_status_moments,
                       key=lambda msm: msm.status.value)
        else:
            # self.aggregation_type == AGGREGATION_TYPE_AVG:
            # TODO: implement
            return min(measure_status_moments,
                       key=lambda msm: msm.status.value)

    def status_moment_planned(self):
        """For use in templates"""
        return self.status_moment(is_planning=True)

    def measure_status_moments(self, end_date=None, is_planning=False,
                               debug=False):
        """If the measure has no children, take own
        measure_status_moments. Else return calculated aggregated list
        of status moments. """
        msm_dates = self.measurestatusmoment_set.filter(
            is_planning=is_planning)
        if end_date is not None:
            msm_dates = msm_dates.filter(datetime__lte=end_date)

        # No children: we're finished.
        if not self.get_children():
            return msm_dates

        # With children:
        # Collect all msms where the date is used to calculate statuses.
        msm_dates = list(msm_dates)
        for measure_child in self.measure_set.all():
            msm_dates_children = measure_child.measure_status_moments(
                is_planning=is_planning, end_date=end_date)
            msm_dates_children = filter(None, msm_dates_children)
            msm_dates.extend(list(msm_dates_children))
        # For each date, calculate status and append to msm.
        msm = []
        for msm_date in msm_dates:
            status_moment = self.status_moment(
                dt=msm_date.datetime, is_planning=is_planning)
            # Remove None's: they can only appear at 'the front' of
            # the timeline and they are irrelevant.
            if status_moment:
                status_moment.datetime = msm_date.datetime
                msm.append(status_moment)

        msm = sorted(msm, key=lambda m: m.datetime)

        return msm

    def image(self, start_date, end_date, width=None, height=None):
        """Return image from adapter for measures.
        """

        # Import here to prevent cyclic imports.
        from lizard_krw.layers import WorkspaceItemAdapterKrw
        adapter = WorkspaceItemAdapterKrw(
            workspace_item=None, layer_arguments={"layer": "measure"})

        return adapter.image([{'measure_id': self.id}],
                             start_date, end_date,
                             width=width, height=height)

    def get_absolute_url(self):
        return reverse('lizard_krw.measure', kwargs={'measure_id': self.pk})

    def value_sum(self):
        """
        Calculates sum of all children, where the unit is the same.
        """

        result = self.value
        descendants = self.get_descendants()
        for descendant in descendants:
            if (descendant.unit ==
                self.unit):
                result += descendant.value
        return result

    def costs_sum(self):
        """
        Calculates sum of all children for total_costs. None=0
        """

        result = 0.0
        children = self.get_children()
        if self.total_costs is not None:
            result += self.total_costs
        for child in children:
            result += child.costs_sum()
        return result

    def investment_costs_sum(self):
        """
        Calculates sum of all children for investment_costs. None=0
        """

        result = 0.0
        children = self.get_children()
        if self.investment_costs is not None:
            result += self.investment_costs
        for child in children:
            result += child.investment_costs_sum()
        return result

    def exploitation_costs_sum(self):
        """
        Calculates sum of all children for exploitation_costs. None=0
        """

        result = 0.0
        children = self.get_children()
        if self.exploitation_costs is not None:
            result += self.exploitation_costs
        for child in children:
            result += child.exploitation_costs_sum()
        return result

    def obligation_end_date_min_max(self):
        minimum = self.obligation_end_date
        maximum = self.obligation_end_date
        descendants = self.get_descendants()
        for descendant in descendants:
            if descendant.oblication_end_date > maximum:
                maximum = descendant.obligation_end_date
            if descendant.oblication_end_date < minimum:
                minimum = descendant.obligation_end_date
        return minimum, maximum

    def obligation_end_date_min(self):
        minimum, maximum = self.obligation_end_date_min_max()
        return minimum

    def obligation_end_date_max(self):
        minimum, maximum = self.obligation_end_date_min_max()
        return maximum

    def funding_organization_cost_sum(self):
        result = 0.0
        for funding_organization in self.fundingorganization_set.all():
            result += funding_organization.cost
        for descendant in self.get_descendants():
            funding_organizations = descendant.fundingorganization_set.all()
            for funding_organization in funding_organizations:
                result += funding_organization.cost
        return result
