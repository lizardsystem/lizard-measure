# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
import datetime
from dateutil import parser as timeparser
import os
import logging
from lxml import etree

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from treebeard.al_tree import AL_Node  # Adjacent list implementation

from lizard_fewsunblobbed.models import Timeserie


# Krw score categories.
SCORE_CATEGORY_FYTO = 1
SCORE_CATEGORY_FLORA = 2
SCORE_CATEGORY_FAUNA = 3
SCORE_CATEGORY_VIS = 4

SCORE_CATEGORIES = {
    SCORE_CATEGORY_FYTO: u'Fytoplankton',
    SCORE_CATEGORY_FLORA: u'Overige waterflora',
    SCORE_CATEGORY_FAUNA: u'Macrofauna',
    SCORE_CATEGORY_VIS: u'Vis'}

SCORE_CATEGORY_CHOICES = SCORE_CATEGORIES.items()


class KRWWaterType(models.Model):
    """
    TypeKRWTypologie, zie Aquo standaard domein
    """
    name = models.CharField(max_length=80)
    code = models.CharField(max_length=8)

    def __unicode__(self):
        return u'%s - %s' % (self.code, self.name)


class WaterBody(models.Model):
    """Specific area for which we want to know KRW scores"""

    class Meta:
        verbose_name = _("Waterbody")
        verbose_name_plural = _("Waterbodies")
        ordering = ("name",)

    name = models.CharField(max_length=80)
    ident = models.CharField(
        max_length=80,
        help_text=u"The ID corresponding to the shapefile ID.")
    slug = models.SlugField(help_text=u"Name used for URL.")
    water_type = models.ForeignKey(KRWWaterType, null=True, blank=True)

    description = models.TextField(null=True, blank=True,
                                   help_text="You can use markdown")

    def __unicode__(self):
        return u'%s - %s' % (self.ident, self.name)

    @models.permalink
    def get_absolute_url(self):
        return ('lizard_krw.waterbody',
                (),
                {'area': str(self.slug)})


class SingleIndicator(models.Model):
    """KRW indicator for a water body

    Points at a timeseries that must be displayed.

    """

    class Meta:
        verbose_name = _("Single indicator")
        verbose_name_plural = _("Single indicators")

    timeserie_id = models.IntegerField(
        help_text=u"ID of the timeserie that must be shown.")
    target_value = models.FloatField(
        help_text=u"Optimal value.",
        blank=True,
        null=True)
    boundary_value = models.FloatField(
        help_text=u"Maximum allowed value.",
        blank=True,
        null=True)
    y_min = models.FloatField(
        help_text=u"Lowest value on y axis.",
        blank=True,
        null=True)
    y_max = models.FloatField(
        help_text=u"Highest value on y axis.",
        blank=True,
        null=True)
    water_body = models.ForeignKey(
        WaterBody,
        related_name='indicators',
        help_text=u"Water body for which we're a graph.")

    def __unicode__(self):
        return u"%s for %s" % (self.timeserie.name, self.water_body)

    @models.permalink
    def get_absolute_url(self):
        return ('lizard_krw.indicator_graph',
                (),
                {'area': str(self.water_body.slug),
                 'id': str(self.id)})

    @property
    def timeserie(self):
        """Return Timeserie object pointed to by timeserie_id.

        Note that we cannot link to it directly with a foreign key as it is in
        a separate database.  Defining a foreign key would let postgres/oracle
        emit consistency-check errors as it cannot guarantee consistency.

        """
        return Timeserie.objects.get(pk=self.timeserie_id)


class Color(models.Model):
    """
    Color for krw scores
    """

    r = models.IntegerField()
    g = models.IntegerField()
    b = models.IntegerField()

    def __unicode__(self):
        return '#%02x%02x%02x' % (self.r, self.g, self.b)

    @property
    def html(self):
        return '#%02x%02x%02x' % (self.r, self.g, self.b)


class AlphaScore(models.Model):
    """Alphanumeric scores"""

    name = models.CharField(max_length=200)
    color = models.ForeignKey('Color', default=1)

    def __unicode__(self):
        return self.name

#krw scores


class Score(models.Model):
    """krw score

    As far as I can tell, based on existing scores, the numeric value
    can be translated to an alpha score as follows:

    value < 0.2          slecht
    0.2 <= value < 0.4   ontoereikend
    0.4 <= value < 0.6   matig
    value >= 0.6         goed
    """

    # degene die het heeft ingevoerd
    owner = models.ForeignKey(User)

    class Meta:
        verbose_name = _("Score")
        verbose_name_plural = _("Scores")
        ordering = ('start_date', 'waterbody', 'category', 'alpha_score')

    waterbody = models.ForeignKey(WaterBody)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    category = models.IntegerField(choices=SCORE_CATEGORY_CHOICES)
    alpha_score = models.ForeignKey(AlphaScore)
    value = models.FloatField()  # Unused, but present in XML import file.

    def __unicode__(self):
        return '%s - %s - %s - %s (%.2f)' % (
            self.start_date, self.waterbody,
            SCORE_CATEGORIES[self.category], self.alpha_score,
            self.value)


class GoalScore(models.Model):
    """krw goal score, it has nothing to do with the FIFA worldcup"""

    owner = models.ForeignKey(User)

    waterbody = models.ForeignKey(WaterBody)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    category = models.IntegerField(choices=SCORE_CATEGORY_CHOICES)
    alpha_score = models.ForeignKey(AlphaScore, default=None)
    value = models.FloatField()  # Unused, but present in XML import file.

    class Meta:
        verbose_name = _("Goal Score")
        verbose_name_plural = _("Goal Scores")
        ordering = ('start_date', 'waterbody', 'category', 'alpha_score')

    def __unicode__(self):
        return '%s - %s - %s - %s' % (
            self.start_date, self.waterbody,
            SCORE_CATEGORIES[self.category], self.alpha_score)

    def save(self, *args, **kwargs):
        """
        Finds corresponding alpha score if not filled in
        manually. Expecting existing alpha scores 'slecht',
        'ontoereikend', 'matig', 'goed'. See also Score.
        """

        # Auto-generate alpha_score corresponding to value.
        if self.value < 0.2:
            self.alpha_score = AlphaScore.objects.get(name='Slecht')
        elif self.value >= 0.2 and self.value < 0.4:
            self.alpha_score = AlphaScore.objects.get(name='Ontoereikend')
        elif self.value >= 0.4 and self.value < 0.6:
            self.alpha_score = AlphaScore.objects.get(name='Matig')
        elif self.value >= 0.6 and self.value < 0.8:
            self.alpha_score = AlphaScore.objects.get(name='Goed')
        elif self.value >= 0.8:
            self.alpha_score = AlphaScore.objects.get(name='Zeer goed')

        super(GoalScore, self).save(*args, **kwargs)

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


class MeasureCode(models.Model):
    """Measure Code. i.e. BE01 Beheermaatregelen uitvoeren actief
    visstands- of schelpdierstandsbeheer
    """

    code = models.CharField(max_length=80)
    description = models.TextField()

    class Meta:
        verbose_name = _("Measure code")
        verbose_name_plural = _("Measure codes")
        ordering = ('code', )

    def __unicode__(self):
        return u'%s - %s' % (self.code, self.description)


class Unit(models.Model):
    """eenheid uit aquo standaard
    http://www.idsw.nl/Aquo/uitwisselmodellen/index.htm?goto=6:192
    """

    sign = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _("Unit")
        verbose_name_plural = _("Units")

    def __unicode__(self):
        return u'%s' % self.sign


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

    """

    class Meta:
        verbose_name = _("Funding organization")
        verbose_name_plural = _("Funding organizations")

    cost = models.FloatField()  # in euro's
    organization = models.ForeignKey(Organization)
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
    color = models.CharField(
        max_length=20,
        help_text="Color is matplotlib style, i.e. '0.75', 'red', '#eeff00'")
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

    class Meta:
        verbose_name = _("Measure status moment")
        verbose_name_plural = _("Measure status moments")
        ordering = ("datetime", )

    measure = models.ForeignKey('Measure')
    status = models.ForeignKey(MeasureStatus)
    datetime = models.DateField()
    is_planning = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)

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


class Measure(AL_Node):
    """
    KRW maatregel, uit voorbeeld maatregelen Martine Lodewijk

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

    owner = models.ForeignKey(User)

    # a measure can be splitted in a tree form
    parent = models.ForeignKey('Measure', blank=True, null=True)
    node_order_by = ['name']

    # aggregation is used to 'summarize' the statuses from child measures
    # and its own status (they are equal in value, normally one would not give
    # status to main measure if it has child measures)
    # affects function current_status_moment
    aggregation_type = models.IntegerField(choices=AGGREGATION_TYPE_CHOICES,
                                           default=AGGREGATION_TYPE_MIN)

    is_indicator = models.BooleanField(default=False)

    waterbody = models.ForeignKey(
        WaterBody,
        help_text="Bij welk waterlichaam hoort deze maatregel?")

    name = models.CharField(max_length=200)
    identity = models.CharField(
        blank=True, null=True, max_length=80,
        help_text="Maatregelidentiteit indien aanwezig")
    description = models.CharField(max_length=200, blank=True, null=True)

    category = models.ForeignKey(
        MeasureCategory,
        help_text="Hoofdcategorie")
    code = models.ForeignKey(
        MeasureCode,
        help_text="SGBP code")

    value = models.FloatField(
        help_text="Omvang van maatregel, inhoud afhankelijk van eenheid")
    unit = models.ForeignKey(
        Unit,
        help_text="Eenheid behorende bij omvang van maatregel")

    executive = models.ForeignKey(
        Executive,
        help_text="Initiatiefnemer/uitvoerder")
    total_costs = models.IntegerField(
        null=True, blank=True, help_text="Totale kosten in euro's")
    investment_costs = models.IntegerField(
        null=True, blank=True, help_text="Investeringskosten in euro's")
    exploitation_costs = models.IntegerField(
        null=True, blank=True, help_text="Exploitatiekosten in euro's")

    period = models.ForeignKey(MeasurePeriod, null=True, blank=True)

    status = models.ManyToManyField(MeasureStatus,
                                    through='MeasureStatusMoment')

    class Meta:
        verbose_name = _("Measure")
        verbose_name_plural = _("Measures")
        ordering = ('waterbody', 'name', )

    def __unicode__(self):
        return u'%s: %s' % (self.waterbody.name, self.name)

    def status_moment(self, dt=datetime.datetime.now(), is_planning=False):
        """
        Get status, defaults to today, return MeasureStatusMoment or
        None. Aggregates from child measures

        make artificial (aggregated) MeasureStatusMoment in case of
        AVG
        """
        # collect status_moments from children
        measure_status_moments = [
            m.status_moment(dt=dt, is_planning=is_planning) \
            for m in self.get_children()]
        # calc own status_moment
        measure_status_moment_set = self.measurestatusmoment_set.filter(
            is_planning=is_planning,
            datetime__lte=dt).distinct().order_by("-datetime")
        if measure_status_moment_set:
            measure_status_moments.append(measure_status_moment_set[0])

        # remove all Nones
        measure_status_moments = filter(None, measure_status_moments)

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


# Import iBever KRW scores in XML format


def get_storage_path(instance, filename):
    """
    Allows dynamic paths for uploaded files. Keeping it simple for now.
    (just storing in the uploads/ directory, which is in var/media/uploads/
    while developing with buildout.
    """
    return os.path.join('uploads', filename)


class XMLImportMeetobject(models.Model):
    """
    Maps WaterBody instances to XMLImports' water_body
    """
    name = models.CharField(
        max_length=255,
        help_text=u"Matches 'meetobject' from XML importfile with waterbody.")
    waterbodies = models.ManyToManyField('WaterBody')

    def __unicode__(self):
        waterbodies = [str(waterbody) for waterbody in self.waterbodies.all()]
        waterbodies_display = ', '.join(waterbodies)
        return '%s -> %s' % (self.name, waterbodies_display)


class XMLImport(models.Model):
    """
    XMLImport facilitates uploading and parsing (importing) of KRW specific
    data in XML format.

    The 'import_type' field is used to determine what this import is about.
    (as this is not apparent from the XML docs itself)

    TODO: What about the 'period' in the Score model? Link to Period class?
    Extract from XML?

    TODO: What about the WaterBody ID? (it's not 1:1 mappable by name from XML
    to Django)
    """
    xml_file = models.FileField(upload_to=get_storage_path,
        help_text=u"The original XML file")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    import_category = models.IntegerField(choices=SCORE_CATEGORY_CHOICES,
        help_text=u"What kind of import is this?")

    # However you MUST fill in a user in order to be able to save.
    owner = models.ForeignKey(User, null=True, blank=True)

    def __unicode__(self):
        return '%s: %s' % (
            SCORE_CATEGORIES[self.import_category], self.xml_file)

    # To consider: text field with status report.

    def save(self):
        """
        Domain-specific XML parsing code based on discussion with customer
        WaterNet. See http://twiki.nelen-schuurmans.nl/cgi-bin/twiki/view/
        ITOntwikkeling/QBWatEnIBever
        """
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(levelname)s %(message)s',
        )
        PREFIX = '{http://www.idsw.nl/umam2008}'
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(self.xml_file)
        logging.debug("XML Parsing errorcount: %d", (len(parser.error_log)))
        root = tree.getroot()

        mode_wait_meetobject = 1
        mode_collecting_data = 2
        current_mode = mode_wait_meetobject

        for member in root.iterchildren(
            tag='{http://www.opengis.net/gml}featureMembers'):

            for element in member.iterchildren():

                # if parent() is a meetobject, we're done with the
                # previous meetobject
                if current_mode == mode_wait_meetobject:
                    if element.tag == PREFIX + 'MeetObject':
                        for f in element.iterchildren(tag=PREFIX + 'identificatie'):
                            meetobject_identification = f.text
                            try:
                                meetobject = XMLImportMeetobject.objects.get(
                                    name=meetobject_identification)
                                current_mode = mode_collecting_data
                                logging.debug("Going to mode: collecting_data")
                            except XMLImportMeetobject.DoesNotExist:
                                logging.warn("%s not found in XMLImportMeetobject."
                                             " Nothing imported for this Meetobject." %
                                             meetobject_identification)

                elif current_mode == mode_collecting_data:
                    if element.tag == PREFIX + 'WaardeReeksTijd':
                        element_reekswaarde = element.find(PREFIX + 'reekswaarde')
                        element_tijdwaarde = element_reekswaarde.find(PREFIX + 'TijdWaarde')
                        element_begintijd = element_tijdwaarde.find(PREFIX + 'beginTijd')
                        beginTijd = element_begintijd.find(PREFIX + 'DatumTijdDataType')
                        beginTijdDatum = beginTijd.find(PREFIX + 'datum').text
                        beginTijdTijd = beginTijd.find(PREFIX + 'tijd').text

                        start_date = datetime.datetime.strptime(beginTijdDatum, "%Y-%M-%d")
                        start_time = timeparser.parse(beginTijdTijd)

                        start_period = datetime.datetime(
                            start_date.year, start_date.month, start_date.day,
                            start_time.hour, start_time.minute, start_time.second)
                        start_period = start_period.replace(tzinfo=start_time.tzinfo)
                        ###############################
                        #element_eindtijd = element_tijdwaarde.find(PREFIX + 'eindTijd')
                        eindTijd = element_begintijd.find(PREFIX + 'DatumTijdDataType')
                        eindTijdDatum = eindTijd.find(PREFIX + 'datum').text
                        eindTijdTijd = eindTijd.find(PREFIX + 'tijd').text

                        end_date = datetime.datetime.strptime(eindTijdDatum, "%Y-%M-%d")
                        end_time = timeparser.parse(eindTijdTijd)

                        end_period = datetime.datetime(
                            end_date.year, end_date.month, end_date.day,
                            end_time.hour, end_time.minute, end_time.second)
                        end_period = end_period.replace(tzinfo=end_time.tzinfo)

                        #############
                        alphaNumericScore = element_tijdwaarde.find(PREFIX + 'alfaNumeriekeWaarde').text

                        score = element_tijdwaarde.find(PREFIX + 'numeriekeWaarde')
                        waarde = score.find(PREFIX + 'WaardeDataType')
                        getalswaarde = waarde.find(PREFIX + 'getalswaarde').text

                        # printen waardes
                        logging.debug("waterlichamen: %s" % (meetobject.waterbodies.all()))
                        logging.debug("begin: %s" % (start_period))
                        logging.debug("end: %s" % (end_period))
                        logging.debug("alphaNumericScore: %s" % (alphaNumericScore))
                        logging.debug("score: %s" % (getalswaarde))

                        logging.debug("COMMITTING KRW SCORE TO DATABASE...")

                        # Tries to find an existing alpha score.
                        alpha_score, created = AlphaScore.objects.get_or_create(
                            name=alphaNumericScore)

                        # Save a single score to (multiple) waterbod(y)/(ies).
                        for waterbody in meetobject.waterbodies.all():
                            # Fetch score that may exist already.
                            try:
                                new_score = Score.objects.get(
                                    waterbody=waterbody,
                                    start_date=start_period,
                                    category=self.import_category)
                            except Score.DoesNotExist:
                                new_score = Score(
                                    waterbody=waterbody,
                                    start_date=start_period,
                                    category=self.import_category)

                            # Write new properties to score.
                            new_score.owner = self.owner
                            new_score.end_date = end_period
                            new_score.alpha_score = alpha_score
                            new_score.value = getalswaarde

                            # Save.
                            new_score.save()

                        current_mode = mode_wait_meetobject
                        logging.debug("Going to mode: wait_meetobject")

        super(XMLImport, self).save()
