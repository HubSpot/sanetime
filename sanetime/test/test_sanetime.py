import unittest2
from sanetime import sanetime
from sanetime.error import SaneTimeError
from datetime import datetime
import pytz

# IMPORTANT -- note to self -- you CANNOT use tzinfo on datetime-- ever! -- just pytz.timezone.localize everything to be safe

JAN_MICROS = 946684800*1000**2
JUL_MICROS = 962409600*1000**2
HOUR_MICROS = 60**2*1000**2

NY_JAN_MICROS = JAN_MICROS + HOUR_MICROS * 5
NY_JUL_MICROS = JUL_MICROS + HOUR_MICROS * 4

class SaneTimeTest(unittest2.TestCase):

    def assertSaneTimeEquals(self, st1, st2):
        self.assertInnards(st1.us, st1.tz, st2)

    def setUp(self):
        self.utc = pytz.utc
        self.ny = pytz.timezone('America/New_York')
        self.ac = pytz.timezone('Africa/Cairo')

    def test_micro_equality(self):
        st1 = sanetime(JAN_MICROS)
        st2 = sanetime(JAN_MICROS)
        st3 = sanetime(JAN_MICROS+1)
        self.assertEquals(st1, st2)
        self.assertEquals(st1, st2.us)
        self.assertEquals(st1.us, st2.us)
        self.assertEquals(st1.us, st2)
        self.assertNotEquals(st1, st3)
        self.assertNotEquals(st1, st3.us)
        self.assertNotEquals(st1.us, st3.us)
        self.assertNotEquals(st1.us, st3)

    def test_from_datetime_string(self):
        self.assertEquals(JAN_MICROS, sanetime('2000-01-01 00:00:00'))
        self.assertEquals(JAN_MICROS+1, sanetime('2000-01-01 00:00:00.000001'))
        self.assertEquals(JAN_MICROS, sanetime('2000-01-01'))
        self.assertEquals(JUL_MICROS, sanetime('July 1st, 2000'))

        self.assertEquals(JAN_MICROS, sanetime('2000-01-01', tz='UTC'))
        self.assertEquals(JAN_MICROS, sanetime('2000-01-01', tz=self.utc))

        self.assertEquals(NY_JAN_MICROS, sanetime('2000-01-01 00:00:00', tz='America/New_York'))
        self.assertEquals(NY_JAN_MICROS, sanetime('2000-01-01 00:00:00', tz=self.ny))

        self.assertEquals(NY_JUL_MICROS, sanetime('2000-07-01', tz='America/New_York'))
        self.assertEquals(NY_JUL_MICROS+1000, sanetime('2000-07-01 00:00:00.001', tz=self.ny))

    def test_from_datetime_params(self):
        and_one_hour = JAN_MICROS+60**2*1000**2
        and_one_minute = and_one_hour+60*1000**2
        and_one_second = and_one_minute+1000**2
        and_one_micro = and_one_second+1

        self.assertEquals(JAN_MICROS, sanetime(2000,1,1))
        self.assertEquals(and_one_hour, sanetime(2000,1,1,1))
        self.assertEquals(and_one_minute, sanetime(2000,1,1,1,1))
        self.assertEquals(and_one_second, sanetime(2000,1,1,1,1,1))
        self.assertEquals(and_one_micro, sanetime(2000,1,1,1,1,1,1))
        self.assertEquals(JUL_MICROS, sanetime(2000,7,1))
        with self.assertRaises(SaneTimeError):
            sanetime(2000,1)

        self.assertEquals(JAN_MICROS, sanetime(2000,1,1,0,0,0,0,tz='UTC'))
        self.assertEquals(JAN_MICROS, sanetime(2000,1,1,0,0,0,0,tz=self.utc))

        self.assertEquals(NY_JAN_MICROS, sanetime(2000,1,1,0,0,0,0,tz='America/New_York'))
        self.assertEquals(NY_JAN_MICROS, sanetime(2000,1,1,0,0,0,0,tz=self.ny))

        self.assertEquals(NY_JUL_MICROS, sanetime(2000,7,1, tz='America/New_York'))
        self.assertEquals(NY_JUL_MICROS, sanetime(2000,7,1, tz=self.ny))

    def test_from_datetime(self):
        self.assertEquals(JAN_MICROS, sanetime(datetime(2000,1,1)))
        self.assertEquals(JAN_MICROS, sanetime(datetime(2000,1,1, tzinfo=self.utc)))
        self.assertEquals(NY_JAN_MICROS, sanetime(self.ny.localize(datetime(2000,1,1))))
        self.assertEquals(NY_JUL_MICROS, sanetime(self.ny.localize(datetime(2000,7,1))))

    def test_now(self):
        past = pytz.utc.localize(datetime.utcnow())
        st = sanetime()
        future = pytz.utc.localize(datetime.utcnow())
        self.assertTrue(st.to_datetime() > past)
        self.assertTrue(st.to_datetime() < future)

        past = self.utc.localize(datetime.utcnow()).astimezone(self.ny)
        st = sanetime(tz='America/New_York')
        future = self.utc.localize(datetime.utcnow()).astimezone(self.ny)
        self.assertTrue(st.to_datetime() > past)
        self.assertTrue(st.to_datetime() < future)

    def test_properties(self):
        st = sanetime(2000,1,2,3,4,5,600700)
        self.assertEquals(700,st.us%1000)
        self.assertEquals(601,st.ms%1000) # remember, it rounds
        self.assertEquals(6,st.s%60) # remember, it rounds

    def test_transitives(self):
        st = sanetime()
        st2 = sanetime(st.to_datetime())
        self.assertEquals(st,st2)

        st = sanetime(tz='America/New_York')
        st2 = sanetime(st.to_datetime())
        self.assertEquals(st,st2)

        st = sanetime()
        st2 = sanetime(str(st))
        self.assertEquals(st,st2)

        st = sanetime(tz='America/New_York')
        st2 = sanetime(str(st))
        self.assertEquals(st, st2)

        st = sanetime()
        st2 = sanetime(st.us)
        self.assertEquals(st, st2)

        st = sanetime(tz='America/New_York')
        st2 = sanetime(st.us, tz='America/New_York')
        self.assertEquals(st, st2)

    def test_comparisons(self):
        t1 = sanetime(2000,1,1,0,0,0,0)
        t2 = sanetime(2000,1,1,0,0,0,1)

        self.assertFalse(t1 > t1)
        self.assertTrue(t2 > t1)
        self.assertFalse(t1 > t2)

        self.assertTrue(t1 >= t1)
        self.assertTrue(t2 >= t1)
        self.assertFalse(t1 >= t2)

        self.assertFalse(t1 < t1)
        self.assertFalse(t2 < t1)
        self.assertTrue(t1 < t2)

        self.assertTrue(t1 <= t1)
        self.assertFalse(t2 <= t1)
        self.assertTrue(t1 <= t2)

    def test_equality(self):
        t1 = sanetime(2000,1,1,0,0,0,0)
        t2 = sanetime(1999,12,31,19,0,0,0, tz='America/New_York')
        t3 = sanetime(2000,1,1,0,0,0,1)
        self.assertTrue(t1==t2)
        self.assertTrue(t2==t1)
        self.assertTrue(t1!=t3)
        self.assertTrue(t3!=t1)

    def test_hashability(self):
        t1 = sanetime(2000,1,1,0,0,0,0)
        t2 = sanetime(1999,12,31,19,0,0,0, tz='America/New_York')
        t3 = sanetime(2000,1,1,0,0,0,1)
        s = set([t1,t2,t3])
        self.assertEquals(2, len(s))
        self.assertIn(t1, s)
        self.assertIn(t2, s)
        self.assertIn(t3, s)

    def test_arithmetic(self):
        t1 = sanetime(2000,1,1,0,0,0,0)
        t2 = sanetime(2000,1,1,0,0,0,1)

        self.assertEquals(t2.us, (t1+1).us)
        self.assertEquals(t1.us,(t2-1).us)

        self.assertEquals(1, t2 - t1)
        self.assertEquals(-1, t1 - t2)


    def test_construction_errors(self):
        with self.assertRaises(SaneTimeError):
            sanetime(datetime(2000,1,1, tzinfo=self.ac), tz='America/New_York')
        with self.assertRaises(SaneTimeError):
            sanetime(datetime(2000,1,1, tzinfo=self.ac), tz=self.ny)

    def test_to_datetime(self):
        st = sanetime(JAN_MICROS)
        self.assertEquals(self.utc.localize(datetime(2000,1,1)), st.to_datetime())

        st = sanetime(JAN_MICROS, tz='America/New_York')
        self.assertEquals(self.utc.localize(datetime(2000,1,1)), st.to_datetime())

        st = sanetime(JUL_MICROS, tz='America/New_York')
        self.assertEquals(self.utc.localize(datetime(2000,7,1)), st.to_datetime())

    def test_to_utc_datetime(self):
        st = sanetime(JAN_MICROS)
        self.assertEquals(pytz.utc.localize(datetime(2000,1,1)), st.to_utc_datetime())

        st = sanetime(JAN_MICROS, tz='America/New_York')
        self.assertEquals(pytz.utc.localize(datetime(2000,1,1)), st.to_utc_datetime())

        st = sanetime(JUL_MICROS, tz='America/New_York')
        self.assertEquals(pytz.utc.localize(datetime(2000,7,1)), st.to_utc_datetime())

    def test_to_naive_datetime(self):
        st = sanetime(JAN_MICROS)
        self.assertEquals(datetime(2000,1,1), st.to_naive_datetime())

        st = sanetime(JAN_MICROS, tz='America/New_York')
        self.assertEquals(datetime(2000,1,1), st.to_naive_datetime())

        st = sanetime(JUL_MICROS, tz='America/New_York')
        self.assertEquals(datetime(2000,7,1), st.to_naive_datetime())

    def test_to_naive_utc_datetime(self):
        st = sanetime(JAN_MICROS)
        self.assertEquals(datetime(2000,1,1), st.to_naive_utc_datetime())

        st = sanetime(JAN_MICROS, tz='America/New_York')
        self.assertEquals(datetime(2000,1,1), st.to_naive_utc_datetime())

        st = sanetime(JUL_MICROS, tz='America/New_York')
        self.assertEquals(datetime(2000,7,1), st.to_naive_utc_datetime())

    def test_str(self):
        st = sanetime(JAN_MICROS)
        self.assertEquals('%sus'%JAN_MICROS, str(st))
        st = sanetime(JUL_MICROS)
        self.assertEquals('%sus'%JUL_MICROS, str(st))
        st = sanetime(JAN_MICROS, tz='America/New_York')
        self.assertEquals('%sus'%JAN_MICROS, str(st))
        st = sanetime(JUL_MICROS, tz='America/New_York')
        self.assertEquals('%sus'%JUL_MICROS, str(st))

    def test_repr(self):
        st = sanetime(JAN_MICROS)
        self.assertEquals('2000-01-01 00:00:00.000000 UTC', repr(st))
        st = sanetime(JUL_MICROS)
        self.assertEquals('2000-07-01 00:00:00.000000 UTC', repr(st))
        st = sanetime(JAN_MICROS, tz='America/New_York')
        self.assertEquals('2000-01-01 00:00:00.000000 UTC', repr(st))
        st = sanetime(JUL_MICROS, tz='America/New_York')  
        self.assertEquals('2000-07-01 00:00:00.000000 UTC', repr(st))


if __name__ == '__main__':
    unittest2.main()
