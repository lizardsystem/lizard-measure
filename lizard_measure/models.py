# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
# -*- coding: utf-8 -*-
import datetime
import logging
from django.core.exceptions import MultipleObjectsReturned

from django.contrib.gis.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from lizard_map.models import ColorField
from lizard_map.utility import short_string

from lizard_geo.models import GeoObject

from lizard_area.models import Area

from lizard_measure.synchronisation import SyncField
from lizard_measure.synchronisation import SyncSource
from lizard_measure.synchronisation import Synchronizer


logger = logging.getLogger(__name__)


class KRWStatus(models.Model):
    """
    Status of KRW Waterbody.

    This model must be synchronized with the Aquo domain table 'KRWStatus'.
    """
    code = models.CharField(
        max_length=32,
        unique=True,
    )
    description = models.CharField(
        verbose_name=_('Description'),
        max_length=256,
        blank=True,
        null=True,
    )
    valid = models.NullBooleanField(
        default=None,
        verbose_name=_('Valid'),
    )

    class Meta:
        verbose_name = _('KRW Status')
        verbose_name_plural = _('KRW Statuses')

    def __unicode__(self):
        return u'%s - %s' % (self.code, self.description)

    @classmethod
    def get_synchronizer(cls):
        """
        Return a configured synchronizer object, tuned for this model.
        """
        fields = [
            SyncField(source='Code', destination='code', match=True),
            SyncField(source='Omschrijving', destination='description'),
        ]

        sources = [SyncSource(
                            model=cls,
                            source_table='KRWStatus',
                            fields=fields,
                        )]

        return Synchronizer(sources=sources)


class KRWWatertype(models.Model):
    """
    Type of KRW Watertype.

    This model must be synchronized with the Aquo domain table 'KRWWatertype'.
    """
    code = models.CharField(
        max_length=32,
        unique=True,
    )
    description = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        verbose_name=_('Description'),
    )
    group = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        verbose_name=_('Group'),
    )
    valid = models.NullBooleanField(
        default=None,
        verbose_name=_('Valid'),
    )

    class Meta:
        verbose_name = _('KRW Watertype')
        verbose_name_plural = _('KRW Watertypes')

    def __unicode__(self):
        return u'%s - %s' % (self.code, self.description)

    @classmethod
    def get_synchronizer(cls):
        """
        Return a configured synchronizer object, tuned for this model.
        """
        fields = [
            SyncField(source='Code', destination='code', match=True),
            SyncField(source='Omschrijving', destination='description'),
            SyncField(source='Groep', destination='group'),
        ]

        sources = [SyncSource(
                            model=cls,
                            source_table='KRWWatertype',
                            fields=fields,
                        )]

        return Synchronizer(sources=sources)


class WaterBody(models.Model):
    """Specific area for which we want to know KRW scores"""

    class Meta:
        verbose_name = _("Waterbody")
        verbose_name_plural = _("Waterbodies")

    area = models.ForeignKey(Area, null=True, blank=True)
    area_ident = models.CharField(
        max_length=32,
        null=True,
        blank=True,
        help_text=_(
            'Area ident for the case the real Area cannot be imported yet'
        ),
    )
    krw_status = models.ForeignKey(KRWStatus, null=True, blank=True)
    krw_watertype = models.ForeignKey(KRWWatertype, null=True, blank=True)

    def __unicode__(self):
        if self.area is None:
            return 'area_ident: %s (No geometry)' % self.area_ident
        else:
            return u'%s' % (self.area.name)


class MeasuringRod(models.Model):
    """
    Presently only a stub to hold MeasuringRod objects.

    This model must be synchronized with the Aquo domain table
    'KRWKwaliteitselement'.
    """

    class Meta:
        verbose_name = _("Maatlat")
        verbose_name_plural = _("Maatlatten")

    id = models.IntegerField(
        primary_key=True
    )

    group = models.CharField(
        max_length=128,
        null=True,
        blank=True,
    )

    measuring_rod = models.CharField(
        max_length=128,
        null=True,
        blank=True,
    )

    sub_measuring_rod = models.CharField(
        max_length=128,
        null=True,
        blank=True,
    )

    unit = models.CharField(
        max_length=128,
        null=True,
        blank=True,
    )

    sign = models.CharField(
        max_length=128,
        null=True,
        blank=True,
    )

    def __unicode__(self):
        return self.measuring_rod


class Score(models.Model):
    """
    Scores / GoalScore
    """
    measuring_rod = models.ForeignKey(MeasuringRod)
    area = models.ForeignKey(Area, null=True, blank=True)
    area_ident = models.CharField(
        max_length=32,
        null=True,
        blank=True,
        help_text=_(
            'Area ident for the case the real Area cannot be imported yet'
        ),
    )
    mep = models.FloatField(null=True, blank=True)
    gep = models.FloatField(null=True, blank=True)
    limit_insufficient_moderate = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('Insufficient-moderate limit'),
        help_text=_('limit from insufficient to moderate',)
    )
    limit_bad_insufficient = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('Bad-insufficient limit'),
        help_text=_('limit from bad to insufficient'),
    )

    ascending = models.NullBooleanField(
        help_text=_('True if higher is better'),
    )

    target_2015 = models.FloatField(null=True, blank=True)
    target_2027 = models.FloatField(null=True, blank=True)

    def __unicode__(self):
        if self.area is None:
            area = self.area_ident
        else:
            area = self.area.name
        return '%s - %s: %s' % (
            area,
            self.measuring_rod.measuring_rod,
            self.measuring_rod.sub_measuring_rod,
        )

    class Meta:
        verbose_name = _("Score")
        verbose_name_plural = _("Scores")


class SteeringParameter(models.Model):
    """
    Err...
    """
    area = models.ForeignKey(Area)  # Need to make this generic?
                                    # May also point to WaterBody...

    fews_parameter = models.CharField(max_length=256)
    #fews_timeseries = models.ManyToManyField(TimeSeries)
    target_minimum = models.FloatField(
        blank=True,
        null=True,
    )
    target_maximum = models.FloatField(
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("Steering parameter")
        verbose_name_plural = _("Steering parameters")


# Measures
class MeasureCategory(models.Model):
    """Measure Category. i.e. Beheermaatregelen
    """

    name = models.CharField(max_length=200)
    valid = models.NullBooleanField(
        default=None,
        verbose_name=_('Valid'),
    )

    class Meta:
        verbose_name = _("Measure category")
        verbose_name_plural = _("Measure categories")

    def __unicode__(self):
        return u'%s' % (self.name)


class Unit(models.Model):
    """Units for measures

    This model must be synchronized with the Aquo domain table 'Eenheid'.
    http://www.idsw.nl/Aquo/uitwisselmodellen/index.htm?goto=6:192
    """

    code = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        unique=True,
        verbose_name=_("Code")
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Description")
    )
    dimension = models.CharField(
        max_length=32,
        null=True,
        blank=True,
        verbose_name=_("Dimension")
    )
    conversion_factor = models.FloatField(
        blank=True,
        null=True,
        verbose_name=_("Conversion factor")
    )
    group = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name=_("Group")
    )

    valid = models.NullBooleanField(
        default=None,
        verbose_name=_('Valid'),
    )

    class Meta:
        verbose_name = _("Unit")
        verbose_name_plural = _("Units")

    def __unicode__(self):
        return u'%s' % self.code

    @classmethod
    def get_synchronizer(cls):
        """
        Return a configured synchronizer object, tuned for this model.
        """
        fields = [
            SyncField(source='Code', destination='code', match=True),
            SyncField(source='Omschrijving', destination='description'),
            SyncField(source='Dimensie', destination='dimension'),
            SyncField(source='Omrekenfactor', destination='conversion_factor'),
            SyncField(source='Groep', destination='group'),
        ]

        sources = [SyncSource(
                            model=cls,
                            source_table='Eenheid',
                            fields=fields,
                        )]

        return Synchronizer(sources=sources)


class MeasureType(models.Model):
    """
    Aquo type of measure

    This model must be synchronized with the Aquo domain table
    'KRWMaatregeltype'.
    """

    class Meta:
        verbose_name = _("Measure type")
        verbose_name_plural = _("Measure types")
        ordering = ('code', )

    code = models.CharField(
        max_length=80,
        unique=True,
        verbose_name=_('Code'),
    )
    description = models.TextField(
        verbose_name=_('Description'),
    )
    group = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name=_("Group")
    )

    # Other fields from KRW import
    units = models.ManyToManyField(
        Unit,
        verbose_name=_('Units'),
    )
    klass = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        verbose_name=_('Class'),
    )
    subcategory = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        verbose_name=_('Subcategory'),
    )
    harmonisation = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        verbose_name=_('Harmonisation'),
    )
    combined_name = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        verbose_name=_('Combined Name'),
    )
    valid = models.NullBooleanField(
        default=None,
        verbose_name=_('Valid'),
    )

    def __unicode__(self):
        return u'%s - %s' % (self.code, self.description)

    @classmethod
    def get_synchronizer(cls):
        """
        Return a configured synchronizer object, tuned for this model.
        """
        fields = [
            SyncField(source='Code', destination='code', match=True),
            SyncField(source='Omschrijving', destination='description'),
            SyncField(source='Groep', destination='group'),
        ]

        sources = [SyncSource(
                            model=cls,
                            source_table='KRWMaatregeltype',
                            fields=fields,
                        )]

        return Synchronizer(sources=sources)


class Organization(models.Model):
    """
    Organizations related to measures.

    Used in Measures and FundingOrganizations.

    This model must be synchronized with the Aquo domain tables
    'Waterbeheerder' and 'Meetinstantie'.

    Furthermore, it should contain municipalities, for the time being
    synchronized from
    'www.cbs.nl/nl-NL/menu/methoden/classificaties/
     overzicht/gemeentelijke-indeling/2011/default.htm',
    awaiting an Aquo domain table.

    And there are some other entries as described in
    'http://wikixl.nl/wiki/krwvss/index.php/Beheer_eigen_organisaties',
    loaded from a fixture.
    """

    SOURCE_CHOICES = (
        (1, _("Aquo domain table 'Waterbeheerder'")),
        (2, _("Aquo domain table 'Meetinstantie'")),
        (3, _("CBS Municipality")),
        (4, _("KRW portal")),
        (5, _("Other")),
    )

    SOURCE_AQUO_WATERMANAGER = 1
    SOURCE_AQUO_MEASUREMENT_AUTHORITY = 2
    SOURCE_CBS_MUNICIPALITY = 3
    SOURCE_KRW_PORTAL = 4
    SOURCE_OTHER = 5

    code = models.IntegerField(
        verbose_name=_('Code'),
        null=True,
        blank=True,
    )
    description = models.CharField(
        verbose_name=_('Description'),
        max_length=256,
        blank=True,
        null=True,
    )
    group = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name=_("Group")
    )
    source = models.IntegerField(
        choices=SOURCE_CHOICES,
        default=SOURCE_OTHER,
    )

    valid = models.NullBooleanField(
        default=None,
        verbose_name=_('Valid'),
    )

    class Meta:
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")
        unique_together = ('source', 'code')
        ordering = ('description', )

    def __unicode__(self):
        return u'%s' % self.description

    @classmethod
    def get_synchronizer(cls):
        """
        Return a configured synchronizer object, tuned for this model.
        """
        watermanager_fields = [
            SyncField(source='Code', destination='code', match=True),
            SyncField(source='Omschrijving', destination='description'),
            SyncField(source='Groep', destination='group'),
            SyncField(source=1, destination='source', static=True, match=True),
        ]
        watermanager_source = SyncSource(
            model=cls,
            source_table='Waterbeheerder',
            fields=watermanager_fields,
        )

        measuring_authority_fields = [
            SyncField(source='Code', destination='code', match=True),
            SyncField(source='Omschrijving', destination='description'),
            SyncField(source='Groep', destination='group'),
            SyncField(source=2, destination='source', static=True, match=True),
        ]
        measuring_authority_source = SyncSource(
            model=cls,
            source_table='Meetinstantie',
            fields=measuring_authority_fields,
        )

        return Synchronizer(sources=[watermanager_source,
                                     measuring_authority_source])


class FundingOrganization(models.Model):
    """
    Links Organizations and measures adding cost info.
    """

    class Meta:
        verbose_name = _("Funding organization")
        verbose_name_plural = _("Funding organizations")

    percentage = models.FloatField()
    organization = models.ForeignKey(Organization)
    measure = models.ForeignKey('Measure')

    def __unicode__(self):
        return u'%s: %s (%.0f %%)' % (
            self.organization, self.measure, self.percentage)


class MeasureStatus(models.Model):
    """
    The status of a measure
    """

    name = models.CharField(
        max_length=200,
        verbose_name=_('Status'),
    )
    # Color is matplotlib style, i.e. '0.75', 'red', '#eeff00'.
    color = ColorField(
        max_length=20,
        help_text=_('Color is rrggbb'),
        verbose_name=_('Color'),
    )
    # Value is 1.0 for up and running, 0 for nothing. Used for ordering.
    value = models.FloatField(
        default=0.0,
        verbose_name=_('Numeric value'),
    )
    valid = models.NullBooleanField(
        default=None,
        verbose_name=_('Valid'),
    )

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
    planning_date = models.DateField(null=True, blank=True)
    realisation_date = models.DateField(null=True, blank=True)
    description = models.TextField(
        blank=True, null=True,
        help_text=_('Description of statusupdate. Recommended.')
    )

    investment_expenditure = models.IntegerField(
        blank=True,
        null=True,
        help_text=_("Expenditure for investment"),
    )
    exploitation_expenditure = models.IntegerField(
        blank=True,
        null=True,
        help_text=_("Expenditure for exploitation"),
    )

    class Meta:
        verbose_name = _("Measure status moment")
        verbose_name_plural = _("Measure status moments")
        ordering = ("measure__id", "status__value", )

    def __unicode__(self):
        return u'%s %s: plan: %s real: %s' % (self.measure, self.status, self.planning_date, self.realisation_date)


class MeasurePeriod(models.Model):
    """Period"""

    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(null=True, blank=True)
    valid = models.NullBooleanField(
        default=None,
        verbose_name=_('Valid'),
    )

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
        max_length=64,
        unique=True,
        blank=True,
        null=True,
        verbose_name=_('Unique code'),
    )

    deleted = models.BooleanField(
        default=False
    )

    is_KRW_measure = models.NullBooleanField(
        verbose_name=_('Is a KRW measure'),
    )

    geometry = models.ForeignKey(
        GeoObject,
        null=True,
        blank=True,
    )

    geom = models.GeometryField(
        null=True,
        blank=True,
    )

    measure_type = models.ForeignKey(
        MeasureType,
        help_text="SGBP code",
        verbose_name='Maatregeltype',
    )

    title = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        verbose_name='Titel',
    )

    # Beleidsdoel?

    period = models.ForeignKey(
        MeasurePeriod,
        blank=True,
        null=True,
        verbose_name='Tijdvak',
    )

    # Fields related to import
    import_source = models.IntegerField(
        editable=False,
        choices=SOURCE_CHOICES,
        default=SOURCE_MANUAL,
        verbose_name=_('Source of imported data'),
    )

    datetime_in_source = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_('Original date of imported data'),
    )
    import_raw = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Full raw imported data'),
    )

    # aggregation is used to 'summarize' the statuses from child measures
    # and its own status (they are equal in value, normally one would not give
    # status to main measure if it has child measures)
    # affects function current_status_moment
    aggregation_type = models.IntegerField(
        choices=AGGREGATION_TYPE_CHOICES,
        default=AGGREGATION_TYPE_MIN,
    )

    waterbodies = models.ManyToManyField(
        WaterBody,
        help_text=_('Which waterbodies does this measure belong to?'),
        verbose_name=_('Waterbody'),
    )

    areas = models.ManyToManyField(
        Area,
        related_name='area_measure_set',
        help_text=_('Which areas does this measure belong to?'),
        verbose_name=_('Area'),
    )

    description = models.CharField(
        max_length=512,
        blank=True,
        null=True,
        verbose_name=_('Description'),
    )

    categories = models.ManyToManyField(
        MeasureCategory,
        verbose_name=_('Categories'),
    )

    value = models.FloatField(
        help_text="Omvang van maatregel, inhoud afhankelijk van eenheid",
        verbose_name='Omvang van maatregel.',
    )
    unit = models.ForeignKey(
        Unit,
        help_text="Eenheid behorende bij omvang van maatregel",
        verbose_name='Eenheid',
    )

    initiator = models.ForeignKey(
        Organization,
        null=True,
        blank=True,
        verbose_name=_('Initiator of this measure'),
        related_name='initiator_measure_set',
    )

    executive = models.ForeignKey(
        Organization,
        null=True,
        blank=True,
        verbose_name=_('Executive of this measure'),
        related_name='executive_measure_set',
    )

    responsible_department = models.CharField(
        max_length=256,
        verbose_name='Verantwoordelijke afdeling',
        help_text='Verantwoordelijke afdeling binnen initiatiefnemer',
    )

    total_costs = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Totale kosten',
        help_text="Totale kosten in euro's"
    )
    investment_costs = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Investeringskosten',
        help_text="Investeringskosten in euro's"
    )
    exploitation_costs = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Exploitatiekosten',
        help_text="Exploitatiekosten in euro's"
    )

    funding_organizations = models.ManyToManyField(
        Organization,
        through='FundingOrganization',
        verbose_name='Financieringsorganisaties',
    )

    status_moments = models.ManyToManyField(
        MeasureStatus,
        through='MeasureStatusMoment',
        verbose_name='Statusmomenten',
    )

    read_only = models.BooleanField(
        default=False,
        help_text=('Wanneer een maatregel read-only is, is hij geimporteerd '
                   'en dient hij niet met de hand gewijzigd te worden'))

    # Is this different from is_KRW_measure?
    is_indicator = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Measure")
        verbose_name_plural = _("Measures")
        ordering = ('id', )

    def __unicode__(self):
        return self.title

    @property
    def shortname(self):
        return short_string(self.name, 17)

    def get_geometry_wkt_string(self):
        """
            returns geometry in the well known text format
        """
        if self.geom is None:
            return ''
        else:
            return self.geom.wkt


    def create_empty_statusmoments(self):
        """
            create status moments for measure


        """
        not_yet_created = MeasureStatus.objects.exclude(measurestatusmoment__measure=self, valid=True)
        for status in not_yet_created:
            self.measurestatusmoment_set.create(status=status)


    def set_statusmoments(self, statusmoments):
        """
            updates the many2many relation with the MeasureStatusMoments
            input:
                id = StatusMoment.id
                name = StatusMoment.name
                planning_date = MeasureStatusMoment.date for records with MeasureStatusMoment.isPlanning == True
                realisation_date = MeasureStatusMoment.date for records with MeasureStatusMoment.isPlanning == False
        """
        for moment in statusmoments:

            try:
                msm, new = self.measurestatusmoment_set.get_or_create(status=MeasureStatus.objects.get(pk=moment['id']))
            except MultipleObjectsReturned:
                #remove all other
                first = True

                for msm in self.measurestatusmoment_set.filter(status=MeasureStatus.objects.get(pk=moment['id'])):
                    if first:
                        first = False
                    else:
                        msm.delete()

                msm, newDimim = self.measurestatusmoment_set.get_or_create(status=MeasureStatus.objects.get(pk=moment['id']))

            if moment['realisation_date'] is None or moment['realisation_date'] == '':
                msm.realisation_date = None
            else:
                msm.realisation_date = moment['realisation_date'].split('T')[0]

            if moment['planning_date'] is None or moment['planning_date'] == '':
                msm.planning_date = None
            else:
                msm.planning_date = moment['planning_date'].split('T')[0]

            msm.save()



    def get_statusmoments(self, auto_create_missing_states=False, only_valid=True):
        """
            updates the many2many relation with the MeasureStatusMoments
            return :
                ordered list with statusmomnts with:
                id = statusMoment.id
                name = statusMoment.name
                planning_date = statusMoment.date for records with statusMoment.isPlanning == True
                realisation_datestatusMoment for records with statusMoment.isPlanning == False
        """
        output = []

        if auto_create_missing_states:
            self.create_empty_statusmoments()

        measure_status_moments = self.measurestatusmoment_set.filter(status__valid=only_valid).order_by('status__value')

        for measure_status_moment in measure_status_moments:
            output.append({
                'id': measure_status_moment.status_id,
                'name': measure_status_moment.status.name,
                'planning_date': measure_status_moment.planning_date,
                'realisation_date': measure_status_moment.realisation_date
            })

        return output


    def set_fundingorganizations(self, organizations):
        """
            updates the many2many relation with the funding organizations
            input:
                organizations is a list with dictionaries with:
                            id = organization.id
                            percentage = percentage
        """
        #todo: everything in one transaction
        existing_links = dict([(obj.id, obj) for obj in self.fundingorganization_set.all()])

        for organization in organizations:

            if existing_links.has_key(organization['id']):
                #update record
                funding_org = existing_links[organization['id']]
                funding_org.percentage = organization['percentage']
                funding_org.save()
                del existing_links[organization['id']]
            else:
                #create new
                obj = self.fundingorganization_set.create(
                    organization=Organization.objects.get(pk=organization['id']),
                    percentage=organization['percentage'])
                #obj.save()


        #remove existing links, that are not anymore
        for funding_org in existing_links.itervalues():
            funding_org.delete()


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
