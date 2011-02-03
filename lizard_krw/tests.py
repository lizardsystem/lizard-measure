# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

import datetime
from django.test import TestCase

from lizard_krw.models import Department
from lizard_krw.models import Executive
from lizard_krw.models import Measure
from lizard_krw.models import MeasureCategory
from lizard_krw.models import MeasureCode
from lizard_krw.models import MeasureCollection
from lizard_krw.models import MeasureStatus
from lizard_krw.models import Organization
from lizard_krw.models import Unit
from lizard_krw.models import Urgency
from lizard_krw.models import WaterBody

class ModelTest(TestCase):
    fixtures = ('lizard_krw', )

    def setUp(self):
        self.wb = WaterBody.objects.get(name="Kortenhoefse Plassen")
        self.category = MeasureCategory.objects.get(pk=1)
        self.urgency = Urgency.objects.get(pk=1)
        self.organization = Organization.objects.get(pk=1)
        self.department = Department.objects.get(pk=1)
        self.code = MeasureCode.objects.all()[0]
        self.unit = Unit.objects.get(pk=1)
        self.executive = Executive.objects.get(pk=1)
        self.now = datetime.date(2011, 2, 3)


    def test_measure_collection(self):
        """Quick test using fixture"""
        mc = MeasureCollection.objects.get(name="Pakket2")
        msm = mc.measure_status_moments()
        self.assertEquals(len(msm), 2)
        self.assertEquals(msm[0].datetime, datetime.date(2010, 7, 1))
        self.assertEquals(msm[1].datetime, datetime.date(2010, 9, 1))


    def test_measure(self):
        """Test measure functions: status_moment. What is the status
        given a certain datetime?
        """
        m1 = Measure(waterbody=self.wb, name="Measure1",
                     category=self.category, code=self.code,
                     value=0.0, unit=self.unit, executive=self.executive)
        m1.save()

        # No status assigned: None
        self.assertEquals(m1.status_moment(dt=self.now), None)

        # Add status
        m1.measurestatusmoment_set.create(
            status=MeasureStatus.objects.get(name="Nieuw"),
            datetime=datetime.date(2010, 5, 25))
        self.assertEquals(
            m1.status_moment(dt=self.now).status.name,
            "Nieuw")
        self.assertEquals(
            m1.status_moment(dt=datetime.date(2010, 5, 25)).status.name,
            "Nieuw")
        self.assertEquals(
            m1.status_moment(dt=datetime.date(2010, 3, 31)),
            None)

        # Add another status
        m1.measurestatusmoment_set.create(
            status=MeasureStatus.objects.get(name="Afgerond"),
            datetime=datetime.date(2010, 8, 1))
        self.assertEquals(
            m1.status_moment(dt=self.now).status.name,
            "Afgerond")
        self.assertEquals(
            m1.status_moment(dt=datetime.date(2010, 7, 1)).status.name,
            "Nieuw")
        self.assertEquals(
            m1.status_moment(dt=datetime.date(2010, 3, 31)),
            None)


    def test_measure_collection2(self):
        """Testing statuses of measure collections. The status of a
        measure collection is aggregated from underlying measures.

           None      Nieuw               Afgerond
        m1 ---------|---------x---------|-------------------------
                    20100525            20100901

           None                Begroot
        m2 ---------x---------|---------x-------------------------
                              20100701

           None     (None)     Nieuw     Begroot
        mc ---------x---------|---------|-------------------------
                              20100701  20100901

        The aggregated status is the minimum of the underlying measure
        at any moment.

        """

        # Create brand new measure collection with 2 measures
        mc = MeasureCollection(name="MeasureCollection",
                               shortname="MeasureCollection",
                               waterbody=self.wb,
                               urgency=self.urgency,
                               responsible_organization=self.organization,
                               responsible_department=self.department)
        mc.save()
        m1 = Measure(waterbody=self.wb, name="Measure1",
                     category=self.category, code=self.code,
                     value=0.0, unit=self.unit, executive=self.executive,
                     measure_collection=mc)
        m1.save()
        m2 = Measure(waterbody=self.wb, name="Measure2",
                     category=self.category, code=self.code,
                     value=0.0, unit=self.unit, executive=self.executive,
                     measure_collection=mc)
        m2.save()


        # No status known for the collection
        self.assertEquals(mc.status_moment(dt=self.now), None)

        # 1 measure has a status, the other doesn't: still no status
        # for the collection.
        m1.measurestatusmoment_set.create(
            status=MeasureStatus.objects.get(name="Nieuw"),
            datetime=datetime.date(2010, 5, 25))
        self.assertEquals(mc.status_moment(dt=self.now), None)

        # Add status for the other measure. The aggregated status is
        # the "minimum".
        m2.measurestatusmoment_set.create(
            status=MeasureStatus.objects.get(name="Begroot"),
            datetime=datetime.date(2010, 7, 1))
        self.assertEquals(
            mc.status_moment(dt=datetime.date(2010, 6, 1)),
            None)
        self.assertEquals(
            mc.status_moment(dt=self.now).status.name,
            "Nieuw")

        # Let's upgrade m1 to "Afgerond". Aggregated value is then "Begroot"
        m1.measurestatusmoment_set.create(
            status=MeasureStatus.objects.get(name="Afgerond"),
            datetime=datetime.date(2010, 9, 1))
        self.assertEquals(
            mc.status_moment(dt=self.now).status.name,
            "Begroot")
        self.assertEquals(
            mc.status_moment(dt=datetime.date(2010, 8, 1)).status.name,
            "Nieuw")

        # See if the list of measure status moments is correct.
        #
        msm = mc.measure_status_moments()

        self.assertEquals(len(msm), 2)

        self.assertEquals(msm[0].status.name, "Nieuw")
        self.assertEquals(msm[0].datetime, datetime.date(2010, 7, 1))

        self.assertEquals(msm[1].status.name, "Begroot")
        self.assertEquals(msm[1].datetime, datetime.date(2010, 9, 1))
