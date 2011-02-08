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


    def test_measure_planning(self):
        """Test measure functions: status_moment. What is the status
        given a certain datetime? Now for planning.
        """
        m1 = Measure(waterbody=self.wb, name="Measure1",
                     category=self.category, code=self.code,
                     value=0.0, unit=self.unit, executive=self.executive)
        m1.save()

        # No status assigned: None
        self.assertEquals(
            m1.status_moment(dt=self.now, is_planning=True),
            None)

        # Add status
        m1.measurestatusmoment_set.create(
            status=MeasureStatus.objects.get(name="Nieuw"),
            datetime=datetime.date(2010, 5, 25),
            is_planning=True)
        self.assertEquals(
            m1.status_moment(dt=self.now, is_planning=True).status.name,
            "Nieuw")
        self.assertEquals(
            m1.status_moment(dt=datetime.date(2010, 5, 25),
                             is_planning=True).status.name,
            "Nieuw")
        self.assertEquals(
            m1.status_moment(dt=datetime.date(2010, 3, 31),
                             is_planning=True),
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

        # Empty planning?
        msm_planning = mc.measure_status_moments(is_planning=True)

        self.assertEquals(len(msm_planning), 0)


    def test_measure_status(self):
        """A measure status is aggregated from its own
        measure_status_moments (if no children) OR that of its children.

        Measure m has children ma and mb. ma has child maa.

        Measure status moments:
        m   |--------------------------------------------------|
        ma  |--------------------------------------------------|

                      Nieuw                Afgerond
        maa |--------|--------------------|--------------------|
                      2009-01-01           2011-01-01

                           Gepland
        mb  |-------------|------------------------------------|
                           2010-01-01

        Aggregated status (takes "lowest" status):
                     (niks)Nieuw           Gepland
        m   |--------x----|---------------|--------------------|
                           2010-01-01      2011-01-01

                      Nieuw                Afgerond
        ma  |--------|--------------------|--------------------|
                      2009-01-01           2011-01-01

                      Nieuw                Afgerond
        maa |--------|--------------------|--------------------|
                      2009-01-01           2011-01-01

                           Gepland
        mb  |-------------|------------------------------------|
                           2010-01-01
        """

        m = Measure(waterbody=self.wb, name="Measure",
                    category=self.category, code=self.code,
                    value=0.0, unit=self.unit, executive=self.executive)
        m.save()

        ma = Measure(waterbody=self.wb, name="Measure-a",
                     category=self.category, code=self.code,
                     value=0.0, unit=self.unit, executive=self.executive,
                     parent=m)
        ma.save()

        maa = Measure(waterbody=self.wb, name="Measure-aa",
                      category=self.category, code=self.code,
                      value=0.0, unit=self.unit, executive=self.executive,
                      parent=ma)
        maa.save()

        mb = Measure(waterbody=self.wb, name="Measure-b",
                     category=self.category, code=self.code,
                     value=0.0, unit=self.unit, executive=self.executive,
                     parent=m)
        mb.save()

        # No statuses added: m has no status.
        self.assertEqual(m.status_moment(dt=self.now), None)
        self.assertEqual(m.measure_status_moments(end_date=self.now), [])

        # Add status to maa. Test ma and maa.
        maa.measurestatusmoment_set.create(
            status=MeasureStatus.objects.get(name="Afgerond"),
            datetime=datetime.date(2011, 1, 1))
        self.assertEquals(
            maa.status_moment(dt=self.now).status.name, "Afgerond")
        self.assertEquals(
            ma.status_moment(dt=self.now).status.name, "Afgerond")

        msm_ma = ma.measure_status_moments(end_date=self.now)
        msm_maa = maa.measure_status_moments(end_date=self.now)
        # ma has msm with 1 item, "Afgerond" at 2011-01-01
        self.assertEquals(len(msm_ma), 1)
        self.assertEquals(msm_ma[0].status.name, "Afgerond")
        self.assertEquals(msm_ma[0].datetime, datetime.date(2011, 1, 1))
        # ma has the same status as maa
        self.assertEquals(msm_ma[0].status.name, msm_maa[0].status.name)
        self.assertEquals(msm_ma[0].datetime, msm_maa[0].datetime)
        # m has no status, because of mb.
        self.assertEquals(m.measure_status_moments(end_date=self.now), [])

        # Add status to mb. Test m.
        mb.measurestatusmoment_set.create(
            status=MeasureStatus.objects.get(name="Gepland"),
            datetime=datetime.date(2010, 1, 1))
        maa.measurestatusmoment_set.create(
            status=MeasureStatus.objects.get(name="Nieuw"),
            datetime=datetime.date(2009, 1, 1))
        msm_m = m.measure_status_moments(end_date=self.now, debug=True)
        msm_ma = ma.measure_status_moments(end_date=self.now)
        msm_mb = mb.measure_status_moments(end_date=self.now)

        self.assertEquals(
            ma.status_moment(dt=datetime.date(2010, 1, 1)).status.name,
            "Nieuw")

        self.assertEquals(len(msm_m), 2)
        self.assertEquals(msm_m[0].status.name, "Nieuw")
        self.assertEquals(msm_m[0].datetime, datetime.date(2010, 1, 1))
        self.assertEquals(msm_m[1].status.name, "Gepland")
        self.assertEquals(msm_m[1].datetime, datetime.date(2011, 1, 1))
