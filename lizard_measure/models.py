# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
# -*- coding: utf-8 -*-
import datetime
import dateutil
import logging
from django.core.exceptions import MultipleObjectsReturned

from django.contrib.gis.db import models
from django.core.urlresolvers import reverse
from django.db.models.query_utils import Q
from django.utils.translation import ugettext as _

from lizard_map.models import ColorField
from lizard_map.utility import short_string

from lizard_geo.models import GeoObject

from lizard_area.models import Area

from lizard_security.manager import FilteredGeoManager
from lizard_security.models import DataSet

from lizard_measure.synchronisation import SyncField
from lizard_measure.synchronisation import SyncSource
from lizard_measure.synchronisation import Synchronizer

from lizard_graph.models import GraphItemMixin


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


class WatertypeGroup(models.Model):

    class Meta:
        verbose_name = _('Watertype group')
        verbose_name_plural = _('Watertype groups')

    code = models.CharField(max_length=32, unique=True,
        verbose_name=_('Code'),
        help_text=_('Unique code to identify the watertype group'))
    description = models.CharField(max_length=256, blank=True, null=True,
        verbose_name=_('Description'))

    def __unicode__(self):
        return self.code


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

    watertype_group = models.ForeignKey(WatertypeGroup, verbose_name=_('Watertype group'),
        null=True, blank=True, related_name='watertypes')

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
        ordering = ('area', )

    area = models.ForeignKey(Area, null=True, blank=True,
        related_name='water_bodies')
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
            return u'%s (%s)' % (self.area.name, self.area.ident)


class MeasuringRodManager(models.Manager):
    def get_by_natural_key(self, code, measuring_rod, sub_measuring_rod):
        return self.get(
            code=code, measuring_rod=measuring_rod,
            sub_measuring_rod=sub_measuring_rod)


class MeasuringRod(models.Model):
    """
    Presently only a stub to hold MeasuringRod objects.

    This model must be synchronized with the Aquo domain table
    'KRWKwaliteitselement'.

    Note: when using natural keys, "code" is sufficient.
    """
    objects = MeasuringRodManager()

    class Meta:
        verbose_name = _("Measuring rod")
        verbose_name_plural = _("Measuring rods")

    measuring_rod_id = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_('Measuring rod id'),
    )

    parent = models.ForeignKey('self', blank=True, null=True)

    code = models.CharField(
        max_length=32,
        null=True,
        blank=True,
        unique=True,
        verbose_name=_("Code")
    )

    description = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        verbose_name=_('Description'),
    )

    group = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name=_('Group'),
    )

    measuring_rod = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name=_('Measuring rod'),
    )

    sub_measuring_rod = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name=_('Sub measuring rod'),
    )

    unit = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name=_('Unit'),
    )

    sign = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name=_('Sign'),
    )

    valid = models.NullBooleanField(
        default=None,
        verbose_name=_('Valid'),
    )

    def __unicode__(self):
        return u'%s - %s' % (self.code, self.measuring_rod)

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
                            source_table='KRWKwaliteitselement',
                            fields=fields,
                        )]

        return Synchronizer(sources=sources)

    def natural_key(self):
        return (self.code, self.measuring_rod, self.sub_measuring_rod, )


class Score(models.Model):
    """
    Scores / GoalScore

    Define area, borders, targets.
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

    target_2015 = models.CharField(max_length=40, null=True, blank=True)
    target_2027 = models.CharField(max_length=40, null=True, blank=True)

    def __unicode__(self):
        if self.area is None:
            area = self.area_ident
        else:
            area = self.area.name
        try:
            return '%s - %s: %s' % (
                area,
                self.measuring_rod.measuring_rod,
                self.measuring_rod.sub_measuring_rod,
                )
        except:
            return '%s' % area

    class Meta:
        verbose_name = _("Score")
        verbose_name_plural = _("Scores")

    @property
    def targets(self):
        return (self.target_2015, self.target_2027)

    @property
    def borders(self):
        """OLD, TO BE DELETED"""
        return (self.limit_bad_insufficient,
                self.limit_insufficient_moderate,
                self.gep,
                self.mep)

    # def _zone_from_limits(self, value, borders):
    #     """
    #     Return zero based zone index.

    #     Value and borders assumed to be between 0 and 1. Return lowest
    #     value if borders coincide.
    #     """
    #     # Determine in which zone
    #     lower_limits = [0] + list(borders)
    #     upper_limits = list(borders) + [1.001]  # Include values of 1!
    #     result = [l <= value < u for l, u in zip(lower_limits, upper_limits)]
    #     try:
    #         return result.index(True)
    #     except ValueError:
    #         # No True in list
    #         return None

    def judgement(self, value, target):
        """
        Return judgment for this score for value.

        value = alphanumeric: slecht, ontoereikend, ...
        target = alphanumeric: slecht, ontoereikend, ...

        Value is same as target: Goal reached (1)
        Value is higher than target: Goal more than achieved (2)
        Value is lower than target: Goal not reached (-1)
        Value is more than one zone lower than target: Goal still not reached (-2)
        (-2)

        Used in lizard-layers when calculating AreaValues for EKR-DOELSCORE

        See also GS060
        """
        def numeric(v):
            """Easy to calculate number of steps difference
            """
            return {'slecht': 1,
                    'ontoereikend': 2,
                    'matig': 3,
                    'goed': 4,
                    'zeer goed': 5}.get(v, None)

        # target_zone = self._zone_from_limits(
        #     value=target,
        #     borders=self.borders
        # )
        # value_zone = self._zone_from_limits(
        #     value=value,
        #     borders=self.borders,
        # )

        # if value_zone is None or target_zone is None:
        #     return None

        #zonedif = value_zone - target_zone
        try:
            zonedif = numeric(target) - numeric(value)
        except:
            logger.debug(
                'target or value not in slecht, ontoereikend, ...:target, value = "%s", "%s"' % (
                    target, value))
            return None

        if zonedif > 0:
            return 2
        if zonedif == 0:
            return 1
        if zonedif == -1:
            return -1
        if zonedif < -1:
            return -2

    @classmethod
    def from_graph_item(cls, graph_item):
        """
        Return a score from graph_item.

        When a corresponding Score cannot be found, return empty
        memory score.
        """
        try:
            # TODO: test with correct database
            score = cls.objects.get(
                area__ident=graph_item.location.ident,
                measuring_rod=graph_item.measuring_rod)
        except Score.DoesNotExist:
            score = cls()
            # These are dummy values.
            score.mep = 0.8
            score.gep = 0.6
            score.limit_insufficient_moderate = 0.4
            score.limit_bad_insufficient = 0.2
            logger.warn('Score.from_graph_item: Score could '
                        'not be found using %s, %s' %
                        (graph_item.location.ident,
                         graph_item.measuring_rod))
        return score


class PredefinedGraphSelection(models.Model):
    """
        List of graphs which can be selected
    """
    name = models.CharField(max_length=256,
                        help_text='naam voor selectie')

    code = models.CharField(max_length=256,
                        help_text='code zoals gedefinieerd bij de pre-defined graphs')

    url = models.CharField(max_length=256,
                        help_text='basis url of grafiek')

    for_area_type = models.IntegerField(null=True, blank=True,
                        choices=Area.AREA_CLASS_CHOICES,
                        help_text='voor de gebieden groep waarvoor de grafiek gekozen kan worden. null is voor alle')

    valid = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

class SteeringParameterPredefinedGraph(models.Model):
    """
        predefined graphs
    """

    name = models.CharField(max_length=256,
                        help_text='alleen gebruikt voor weergave')

    area = models.ForeignKey(Area,
                        help_text='Gebied waarbij stuurparameter hoort')

    order = models.IntegerField(default=0,
                        help_text='volgorde van grafieken (binnen zelfde type)')

    for_evaluation = models.BooleanField(
                        default= False,
                        help_text='Evaluatie stuurparameter, anders Toestand')

    predefined_graph = models.ForeignKey(PredefinedGraphSelection)

    area_of_predefined_graph = models.ForeignKey(Area,
                        null=True, blank=True,
                        related_name='+',
                        help_text='locatie van pre-defined graph anders dan eigen gebied')

    class Meta:
        verbose_name = _("Steering parameter predefined graph ")
        verbose_name_plural = _("Steering parameters predefined graph")

class SteeringParameterFree(models.Model):
    """
        selection of parameter and locations for a steerparameter graph
    """
    name = models.CharField(max_length=256,
                    help_text='alleen gebruikt voor weergave')

    area = models.ForeignKey(Area)

    order = models.IntegerField(default=0,
                        help_text='volgorde van grafieken (binnen zelfde type)')

    for_evaluation = models.BooleanField(
                        default= False,
                        help_text='Evaluatie stuurparameter, anders Toestand')

    parameter_code = models.CharField(max_length=256)

    has_target = models.BooleanField(
        default=False
    )
    target_value = models.FloatField(
        blank=True,
        null=True,
    )
    location_modulinstance_string = models.TextField(
        help_text = 'text string met "location_ident,moduleinstance_code,timestep_id,identifier_id".\
                    Als een deel wordt weggelaten, dan wordt indien de verwijzing naar meerdere is\
                    een willekeurige genomen. Meerdere locaties opdelen met een ";"'
    )

    class Meta:
        verbose_name = _("Steering parameter free selection")
        verbose_name_plural = _("Steering parameters free selection")


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
        return u'%s' % self.name


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
        blank=True,
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
        (0, _("Manual")),
        (1, _("Aquo domain table 'Waterbeheerder'")),
        (2, _("Aquo domain table 'Meetinstantie'")),
        (3, _("CBS Municipality")),
        (4, _("KRW portal")),
        (5, _("Other")),
    )

    SOURCE_MANUAL = 0
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
        default='Lokaal',
        verbose_name=_("Group")
    )
    source = models.IntegerField(
        choices=SOURCE_CHOICES,
        default=SOURCE_MANUAL,
    )

    valid = models.BooleanField(
        default=True,
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
    comment = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('Comment'),
    )
    organization = models.ForeignKey(Organization)
    measure = models.ForeignKey('Measure')

    @property
    def cost(self):
        if self.percentage is None or self.measure.total_costs is None:
            return None
        return self.measure.total_costs * self.percentage / 100

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
    valid = models.BooleanField(
        default=True,
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
        return u'%s %s: plan: %s real: %s' % (self.measure,
                                              self.status,
                                              self.planning_date,
                                              self.realisation_date)


class MeasurePeriod(models.Model):
    """Period"""

    start_date = models.DateField(
        default=datetime.date(year=2016, month=1, day=1),
        null=True,
        blank=True,
    )
    end_date = models.DateField(
        default=datetime.date(year=2027, month=1, day=1),
        null=True,
        blank=True,
    )
    description = models.TextField(
        null=True,
        blank=True,
    )
    valid = models.BooleanField(
        default=True,
        verbose_name=_('Valid'),
    )

    class Meta:
        ordering = ('start_date', 'end_date', )
        verbose_name = _("Measure period")
        verbose_name_plural = _("Measure periods")

    def __unicode__(self):
        return self.description


class EsfLink(models.Model):
    """
    ESF related to measure.
    """
    ESF_CHOICES = [(n, n) for n in range(1, 10)]

    measure = models.ForeignKey('Measure')
    esf = models.IntegerField(
        choices=ESF_CHOICES,
        blank=True,
        null=True,
        verbose_name=_('Ecological Key Factor'),
    )
    is_target_esf = models.NullBooleanField(
        default=False,
        verbose_name=_('Target'),
    )
    positive = models.NullBooleanField(
        default=False,
        verbose_name=_('Positive'),
    )
    negative = models.NullBooleanField(
        default=False,
        verbose_name=_('Negative'),
    )

    class Meta:
        verbose_name = _("Ecological Key Factor")
        verbose_name_plural = _("Ecological Key Factors")
        unique_together = ('measure', 'esf')

    def __unicode__(self):
        return '%s - %i' % (self.measure, self.esf)


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

    valid = models.BooleanField(
        default=True,
        verbose_name=_('Valid'),
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
        srid=4326,
    )

    measure_type = models.ForeignKey(
        MeasureType,
        help_text="SGBP code",
        verbose_name='Maatregeltype',
        related_name='measures',
    )

    in_sgbp = models.NullBooleanField(
        default=None,
        verbose_name=_('in SGBP'),
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
        blank=True,
        help_text=_('Which waterbodies does this measure belong to?'),
        verbose_name=_('Waterbody'),
    )

    areas = models.ManyToManyField(
        Area,
        blank=True,
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
        blank=True,
        verbose_name=_('Categories'),
    )

    value = models.FloatField(
        blank=True,
        null=True,
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
        null=True,
        blank=True,
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
    land_costs = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Grondkosten',
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

    #
    is_indicator = models.BooleanField(default=False,
        help_text='focus maatregel')

    data_set = models.ForeignKey(DataSet,
                                 null=True,
                                 blank=True)

    objects = FilteredGeoManager()

    class Meta:
        verbose_name = _("Measure")
        verbose_name_plural = _("Measures")
        ordering = ('id', )

    def __unicode__(self):
        return self.title

    @property
    def shortname(self):
        return short_string(self.title, 17)

    @property
    def deleted(self):
        """
        For backwards compatibility
        """
        if self.valid is None:
            return False
        return not self.valid

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
        not_yet_created = MeasureStatus.objects.filter(
            valid=True
        ).exclude(
            measurestatusmoment__measure=self
        )
        for status in not_yet_created:
            self.measurestatusmoment_set.create(status=status)

    def set_statusmoments(self, statusmoments):
        """
        updates the many2many relation with the MeasureStatusMoments

        constraints by code: each status can occur only once for a
        measure.

        input:
            id = StatusMoment.id
            name = StatusMoment.name
            planning_date = MeasureStatusMoment.date
                for records with MeasureStatusMoment.isPlanning == True
            realisation_date = MeasureStatusMoment.date
                for records with MeasureStatusMoment.isPlanning == False
        """
        for moment in statusmoments:

            try:
                msm, new = self.measurestatusmoment_set.get_or_create(
                    status=MeasureStatus.objects.get(pk=moment['id']),
                )
            except MultipleObjectsReturned:
                #remove all other
                first = True

                for msm in self.measurestatusmoment_set.filter(
                    status=MeasureStatus.objects.get(pk=moment['id']),
                ):
                    if first:
                        first = False
                    else:
                        logger.warning(
                            'Multiple same statuses in database: %s' % str(msm))
                        msm.delete()

                msm, newDimim = self.measurestatusmoment_set.get_or_create(
                    status=MeasureStatus.objects.get(pk=moment['id']),
                )

            if (moment['realisation_date'] is None or
                moment['realisation_date'] == ''):
                msm.realisation_date = None
            else:
                msm.realisation_date = dateutil.parser.parse(moment['realisation_date'])

            if (moment['planning_date'] is None or
                moment['planning_date'] == ''):
                msm.planning_date = None
            else:
                msm.planning_date = dateutil.parser.parse(moment['planning_date'])

            msm.save()

    def get_statusmoments(self,
                          auto_create_missing_states=False,
                          only_valid=True):
        """
        updates the many2many relation with the MeasureStatusMoments
        return :
            ordered list with statusmoments with:
            id = statusMoment.id
            name = statusMoment.name
            planning_date = statusMoment.date for
                records with statusMoment.isPlanning == True
            realisation_datestatusMoment for
                records with statusMoment.isPlanning == False
        """
        output = []

        if auto_create_missing_states:
            self.create_empty_statusmoments()

        measure_status_moments = self.measurestatusmoment_set.filter(
            status__valid=only_valid,
        ).order_by('status__value')

        for measure_status_moment in measure_status_moments:
            output.append({
                'id': measure_status_moment.status_id,
                'name': measure_status_moment.status.name,
                'planning_date': measure_status_moment.planning_date,
                'realisation_date': measure_status_moment.realisation_date,
            })

        return output

    def create_empty_esflinks(self):
        """
        create esflinks for measure
        """
        created = self.esflink_set.all().values_list('esf',flat=True)
        for esf_nr in range(1,10):
            if esf_nr not in created:
                self.esflink_set.create(esf=esf_nr)


    def set_esflinks(self, esflinks):
        """
        updates the relation with the esflink
        input:
            id = EsfLink.id
            and other fields of esflink
        """

        for esflink in esflinks:

            esf = self.esflink_set.get(
                pk=esflink['id']
            )

            esf.is_target_esf = esflink['is_target_esf']
            esf.positive = esflink['positive']
            esf.negative = esflink['negative']

            esf.save()

    def get_esflinks(self,
                          auto_create_missing_states=False):
        """
        updates the many2many relation with the MeasureStatusMoments
        return :
            ordered list with esflinks with:
            id
            name
            is_target_esf
            positive
            negative
        """

        output = []

        if auto_create_missing_states:
            self.create_empty_esflinks()

        esflinks = self.esflink_set.all().order_by('esf')

        for esflink in esflinks:
            output.append({
                'id': esflink.id,
                'name': 'ESF %i'%esflink.esf,
                'is_target_esf': esflink.is_target_esf,
                'positive': esflink.positive,
                'negative': esflink.negative
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
        existing_links = dict(
            [(obj.id, obj)
             for obj in self.fundingorganization_set.all()],
        )

        for organization in organizations:

            if not 'comment' in organization:
                organization['comment'] = ''

            if organization['id'] in existing_links:
                #update record
                funding_org = existing_links[organization['id']]
                funding_org.percentage = organization['percentage']
                funding_org.comment = organization['comment']
                funding_org.save()
                del existing_links[organization['id']]
            else:
                #create new
                self.fundingorganization_set.create(
                    organization=Organization.objects.get(
                            pk=organization['id']),
                    percentage=organization['percentage'],
                    comment=organization['comment'])

        #remove existing links, that are not anymore
        for funding_org in existing_links.itervalues():
            funding_org.delete()

    def status_moment_self(self, dt=datetime.datetime.now(),
                           is_planning=False):
        """Returns own status_moment"""

        if is_planning:
            measure_status_moment_set = self.measurestatusmoment_set.filter(
                planning_date__lte=dt).distinct().order_by("-planning_date")
        else:
            measure_status_moment_set = self.measurestatusmoment_set.filter(
                realisation_date__lte=dt).distinct().order_by("-realisation_date")
        if measure_status_moment_set:
            return measure_status_moment_set[0]
        return None


    def status_moment_string(self, dt=datetime.datetime.now(), is_planning=False, aggretation_of_childs=False):
        """
        String representation of status_moment function

        """

        st = self.status_moment(dt=dt, is_planning=is_planning, aggretation_of_childs=aggretation_of_childs)

        if st == None:
            return '-'
        else:
            return st.status.name




    def status_moment(self, dt=datetime.datetime.now(), is_planning=False, aggretation_of_childs=False):
        """
        Get status for a given datetime (defaults to today)
        returns MeasureStatusMoment or None.

        If any children: Aggregates from child measures

        """
        # Collect status_moments from children OR self.
        if self.measure_set.all() and aggretation_of_childs:
            measure_status_moments = [
                m.status_moment(dt=dt, is_planning=is_planning)
                for m in self.measure_set.all()]
        else:
            msm_self = self.status_moment_self(dt=dt, is_planning=is_planning)
            measure_status_moments = [msm_self, ]

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



    def measure_status_moments(self, end_date=None, is_planning=False,
                               debug=False):
        """If the measure has no children, take own
        measure_status_moments.
        """
        msm_dates = self.measurestatusmoment_set.all()

        if end_date is not None:
            if is_planning:
                msm_dates = msm_dates.filter(
                    planning_date__lte=end_date,
                ).order_by(
                    'planning_date',
                )
                return msm_dates
            else:
                msm_dates = msm_dates.filter(
                    realisation_date__lte=end_date,
                ).order_by(
                    'realisation_date',
                )

        return msm_dates


    def measure_status_moments_aggregate_children(self, end_date=None, is_planning=False,
                               debug=False):
        """
            Else return calculated aggregated list
            of status moments
        """
        if end_date is not None:
            if is_planning:
                msm_dates = msm_dates.filter(planning_date__lte=end_date)
            else:
                msm_dates = msm_dates.filter(realisation_date__lte=end_date)

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
                if is_planning:
                    status_moment.datetime = msm_date.planning_date
                else:
                    status_moment.datetime = msn_date.realisation_date
                msm.append(status_moment)

        msm = sorted(msm, key=lambda m: m.datetime)

        return msm

    def value_sum(self):
        """
        Calculates sum of all children, where the unit is the same.
        """

        result = self.value
        descendants = self.measure_set.all()
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
        children = self.measure_set.all()
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
        children = self.measure_set.all()
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
        children = self.measure_set.all()
        if self.exploitation_costs is not None:
            result += self.exploitation_costs
        for child in children:
            result += child.exploitation_costs_sum()
        return result

    def obligation_end_date_min_max(self):
        minimum = self.obligation_end_date
        maximum = self.obligation_end_date
        descendants = self.measure_set.all()
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
        for descendant in self.measure_set.all():
            funding_organizations = descendant.fundingorganization_set.all()
            for funding_organization in funding_organizations:
                result += funding_organization.cost
        return result

    def target_esf_string(self):
        esf_list = self.esflink_set.filter(is_target_esf=True).order_by('esf').values_list('esf', flat=True)

        return ', '.join(['%i'%esf for esf in esf_list])

    def effect_esf_string(self):
        esf_list = self.esflink_set.filter(Q(positive=True)|Q(negative=True)).order_by('esf')
        output = ''
        for esf in esf_list:
            output += '%i'% esf.esf
            if esf.positive:
                output += '(+)'
            if esf.negative:
                output += '(-)'
            output += ', '
        return output


class EsfPattern(models.Model):

    class Meta:
        verbose_name = _("ESF pattern")
        verbose_name_plural = _("ESF patterns")
        ordering = ['pattern', 'data_set', ]

    pattern = models.CharField(help_text="Pattern that specifies critical ESFs",
         default='-' * 16, max_length=16)

    watertype_group = models.ForeignKey(WatertypeGroup,
        verbose_name=_('Watertype group'), blank=True, null=True,
        related_name='+')

    data_set = models.ForeignKey(DataSet, verbose_name=_('Water manager'),
        blank=True, null=True, related_name='+')

    measure_types = models.ManyToManyField(MeasureType,
        verbose_name=_('Measure type'), blank=True, null=True,
        related_name='+')

    @property
    def measures(self):
        """Return the list of measures of each MeasureType."""
        measures_list = []
        for measure_type in self.measure_types.all():
            measures_list += measure_type.measures.all()
        return measures_list

    def __unicode__(self):
        return self.pattern


# EKR Graphs

class HorizontalBarGraph(models.Model):
    """
    Predefined horizontal bar graph. EKR scores.
    """
    name = models.CharField(max_length=80)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)

    title = models.CharField(
        null=True, blank=True, max_length=80,
        help_text="Last filled in is used in graph")
    x_label = models.CharField(
        null=True, blank=True, max_length=80,
        help_text="Last filled in is used in graph")
    y_label = models.CharField(
        null=True, blank=True, max_length=80,
        help_text="Last filled in is used in graph")

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.slug)


class HorizontalBarGraphItem(GraphItemMixin):
    """
    Represent one row of a horizontal bar graph.

    The MeasuringRod together with the Area (ident=location.ident)
    determine the Score. The Score describes which value maps to which
    color.
    """
    horizontal_bar_graph = models.ForeignKey(HorizontalBarGraph)
    index = models.IntegerField(default=100)

    label = models.CharField(
        null=True, blank=True, max_length=80)
    measuring_rod = models.ForeignKey(
        MeasuringRod, null=True, blank=True)

    class Meta:
        # Graphs are drawn on y values in increasing order. The lowest
        # bar is drawn first.
        ordering = ('-index', )

    def __unicode__(self):
        return '%s' % self.label

    @classmethod
    def from_dict(cls, d):
        """
        Return a HorizontalBarGraphItem matching the provided dictionary.

        Note that the objects are not saved.

        The provided dictionary must have the following keys:
        - label: label that you want to show.
        - location: fews location id
        - parameter: fews parameter id
        - module: fews module id
        """
        try:
            location = GeoLocationCache.objects.get(ident=d['location'])
        except GeoLocationCache.DoesNotExist:
            # TODO: see if "db_name" is provided, then add
            # location anyway
            location = GeoLocationCache(ident=d['location'])
            logger.exception(
                "Ignored not existing GeoLocationCache for ident=%s" %
                d['location'])

        graph_item = HorizotalBarGraphItem()
        graph_item.location = location
        graph_item.parameter = ParameterCache(ident=d['parameter'])
        graph_item.module = ModuleCache(ident=d['module'])

