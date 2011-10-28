import unittest2
from sanetime import sanetztime
from sanetime.error import SaneTimeError
from datetime import datetime
import pytz

# IMPORTANT -- note to self -- you CANNOT use tzinfo on datetime-- just pytz.timezone.localize everything to be safe

JAN_MICROS = 946684800*1000**2
JUL_MICROS = 962409600*1000**2
HOUR_MICROS = 60**2*1000**2

NY_JAN_MICROS = JAN_MICROS + HOUR_MICROS * 5
NY_JUL_MICROS = JUL_MICROS + HOUR_MICROS * 4

class SaneTzTimeTest(unittest2.TestCase):
    """ A class that wraps all the date time timezone python insanity, so you don't have to know about that shitshow """

    def setUp(self):
        self.utc = pytz.utc
        self.ny = pytz.timezone('America/New_York')
        self.ac = pytz.timezone('Africa/Cairo')

    def assertInnards(self, us, tz, st):
        self.assertEquals(us, st.us)
        self.assertEquals(tz.zone, st.tz.zone)

    def test_timezone_labels(self):
        self.assertEquals('UTC', self.utc.zone)
        self.assertEquals('America/New_York', self.ny.zone)
        self.assertEquals('Africa/Cairo', self.ac.zone)

    def test_equality(self):
        st1 = sanetztime(JAN_MICROS)
        st2 = sanetztime(JAN_MICROS, tz='America/New_York')
        st3 = sanetztime(JAN_MICROS, tz='US/Eastern')
        st4 = sanetztime(JAN_MICROS, tz='US/Eastern')
        st5 = sanetztime(JAN_MICROS+1)
        items = [st1,st2,st3,st4,st5]
        for i in xrange(0,5):
            for j in xrange(0,5):
                if i==j or (i,j)==(2,3) or (i,j)==(3,2):
                    self.assertEquals(items[i],items[j])
                else:
                    self.assertNotEquals(items[i],items[j])

    def test_from_micros(self):
        self.assertInnards(JAN_MICROS, self.utc, sanetztime(JAN_MICROS))
        self.assertInnards(JAN_MICROS, self.utc, sanetztime(JAN_MICROS, tz='UTC'))
        self.assertInnards(JAN_MICROS, self.ny, sanetztime(JAN_MICROS, tz='America/New_York'))
        self.assertInnards(JAN_MICROS, self.ny, sanetztime(JAN_MICROS, tz=self.ny))

    def test_from_datetime_string(self):
        self.assertInnards(JAN_MICROS, self.utc, sanetztime('2000-01-01 00:00:00'))
        self.assertInnards(JAN_MICROS, self.utc, sanetztime('2000-01-01'))
        self.assertInnards(JUL_MICROS, self.utc, sanetztime('July 1st, 2000'))

        self.assertInnards(JAN_MICROS, self.utc, sanetztime('2000-01-01 00:00:00', tz='UTC'))
        self.assertInnards(JAN_MICROS, self.utc, sanetztime('2000-01-01 00:00:00', tz=self.utc))

        self.assertInnards(NY_JAN_MICROS, self.ny, sanetztime('2000-01-01 00:00:00', tz='America/New_York'))
        self.assertInnards(NY_JAN_MICROS, self.ny, sanetztime('2000-01-01 00:00:00', tz=self.ny))

        self.assertInnards(NY_JUL_MICROS, self.ny, sanetztime('2000-07-01', tz='America/New_York'))
        self.assertInnards(NY_JUL_MICROS, self.ny, sanetztime('2000-07-01', tz=self.ny))

    def test_from_datetime_params(self):
        and_one_hour = JAN_MICROS+60**2*1000**2
        and_one_minute = and_one_hour+60*1000**2
        and_one_second = and_one_minute+1000**2
        and_one_micro = and_one_second+1

        self.assertInnards(JAN_MICROS, self.utc, sanetztime(2000,1,1))
        self.assertInnards(and_one_hour, self.utc, sanetztime(2000,1,1,1))
        self.assertInnards(and_one_minute, self.utc, sanetztime(2000,1,1,1,1))
        self.assertInnards(and_one_second, self.utc, sanetztime(2000,1,1,1,1,1))
        self.assertInnards(and_one_micro, self.utc, sanetztime(2000,1,1,1,1,1,1))
        self.assertInnards(JUL_MICROS, self.utc, sanetztime(2000,7,1))
        with self.assertRaises(SaneTimeError):
            sanetztime(2000,1)

        self.assertInnards(JAN_MICROS, self.utc, sanetztime(2000,1,1,0,0,0,0,tz='UTC'))
        self.assertInnards(JAN_MICROS, self.utc, sanetztime(2000,1,1,0,0,0,0,tz=self.utc))

        self.assertInnards(NY_JAN_MICROS, self.ny, sanetztime(2000,1,1,0,0,0,0,tz='America/New_York'))
        self.assertInnards(NY_JAN_MICROS, self.ny, sanetztime(2000,1,1,0,0,0,0,tz=self.ny))

        self.assertInnards(NY_JUL_MICROS, self.ny, sanetztime(2000,7,1, tz='America/New_York'))
        self.assertInnards(NY_JUL_MICROS, self.ny, sanetztime(2000,7,1, tz=self.ny))

    def test_from_datetime(self):
        self.assertInnards(JAN_MICROS, self.utc, sanetztime(datetime(2000,1,1)))
        self.assertInnards(JAN_MICROS, self.utc, sanetztime(datetime(2000,1,1, tzinfo=self.utc)))
        self.assertInnards(NY_JAN_MICROS, self.ny, sanetztime(self.ny.localize(datetime(2000,1,1))))
        self.assertInnards(NY_JUL_MICROS, self.ny, sanetztime(self.ny.localize(datetime(2000,7,1))))

    def test_now(self):
        past = pytz.utc.localize(datetime.utcnow())
        st = sanetztime()
        future = pytz.utc.localize(datetime.utcnow())
        self.assertTrue(st.to_datetime() > past)
        self.assertTrue(st.to_datetime() < future)
        self.assertEquals('UTC', st.tz.zone)

        past = self.utc.localize(datetime.utcnow()).astimezone(self.ny)
        st = sanetztime(tz='America/New_York')
        future = self.utc.localize(datetime.utcnow()).astimezone(self.ny)
        self.assertTrue(st.to_datetime() > past)
        self.assertTrue(st.to_datetime() < future)
        self.assertEquals('America/New_York', st.tz.zone)

    def test_properties(self):
        st = sanetztime(2000,1,2,3,4,5,600700)
        self.assertEquals(700,st.us%1000)
        self.assertEquals(601,st.ms%1000) # remember, it rounds
        self.assertEquals(6,st.s%60) # remember, it rounds

        st = sanetztime(2000,1,1,tz='America/New_York')
        self.assertEquals('EST', st.tz_abbr)
        self.assertEquals('America/New_York', st.tz_name)

    def test_transitives(self):
        st = sanetztime()
        st2 = sanetztime(st.to_datetime())
        self.assertEquals(st, st2)

        st = sanetztime()
        st2 = sanetztime(str(st))
        self.assertEquals(st, st2)

        st = sanetztime()
        st2 = sanetztime(st.us)
        self.assertEquals(st, st2)

        st = sanetztime(tz='America/New_York')
        st2 = sanetztime(st.to_datetime())
        self.assertEquals(st, st2)

        st = sanetztime(tz='America/New_York')
        st2 = sanetztime(str(st))
        self.assertEquals(st, st2)

        st = sanetztime(tz='America/New_York')
        st2 = sanetztime(st.us,tz='America/New_York')
        self.assertEquals(st, st2)

    def test_comparisons(self):
        t1 = sanetztime(2000,1,1,0,0,0,0)
        t2 = sanetztime(2000,1,1,0,0,0,1)

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

    def test_hashability(self):
        t1 = sanetztime(2000,1,1,0,0,0,0)
        t2 = sanetztime(1999,12,31,19,0,0,0, tz='America/New_York')
        t3 = sanetztime(1999,12,31,19,0,0,0, tz='America/New_York')
        t4 = sanetztime(2000,1,1,0,0,0,1)
        s = set([t1,t2,t3,t4])
        self.assertEquals(3, len(s))
        self.assertIn(t1, s)
        self.assertIn(t2, s)
        self.assertIn(t3, s)
        self.assertIn(t4, s)

    def test_arithmetic(self):
        t1 = sanetztime(2000,1,1,0,0,0,0)
        t2 = sanetztime(2000,1,1,0,0,0,1)

        self.assertEquals(t2.us, (t1+1).us)
        self.assertEquals(t2.tz, (t1+1).tz)

        self.assertEquals(t1.us,(t2-1).us)
        self.assertEquals(t1.tz, (t2-1).tz)


    def test_construction_errors(self):
        with self.assertRaises(SaneTimeError):
            sanetztime(datetime(2000,1,1, tzinfo=self.ac), tz='America/New_York')
        with self.assertRaises(SaneTimeError):
            sanetztime(datetime(2000,1,1, tzinfo=self.ac), tz=self.ny)

    def test_to_datetime(self):
        st = sanetztime(JAN_MICROS)
        self.assertEquals(self.utc.localize(datetime(2000,1,1)), st.to_datetime())

        st = sanetztime(JAN_MICROS, tz='America/New_York')
        self.assertEquals(self.utc.localize(datetime(2000,1,1)).astimezone(self.ny), st.to_datetime())

        st = sanetztime(JUL_MICROS, tz='America/New_York')
        self.assertEquals(self.utc.localize(datetime(2000,7,1)).astimezone(self.ny), st.to_datetime())

    def test_to_utc_datetime(self):
        st = sanetztime(JAN_MICROS)
        self.assertEquals(self.utc.localize(datetime(2000,1,1)), st.to_utc_datetime())

        st = sanetztime(JAN_MICROS, tz='America/New_York')
        self.assertEquals(self.utc.localize(datetime(2000,1,1)), st.to_utc_datetime())

        st = sanetztime(JUL_MICROS, tz='America/New_York')
        self.assertEquals(self.utc.localize(datetime(2000,7,1)), st.to_utc_datetime())

    def test_to_naive_datetime(self):
        st = sanetztime(JAN_MICROS)
        self.assertEquals(datetime(2000,1,1), st.to_naive_datetime())

        st = sanetztime(JAN_MICROS, tz='America/New_York')
        self.assertEquals(datetime(1999,12,31,19), st.to_naive_datetime())

        st = sanetztime(JUL_MICROS, tz='America/New_York')
        self.assertEquals(datetime(2000,6,30,20), st.to_naive_datetime())

    def test_to_naive_utc_datetime(self):
        st = sanetztime(JAN_MICROS)
        self.assertEquals(datetime(2000,1,1), st.to_naive_utc_datetime())

        st = sanetztime(JAN_MICROS, tz='America/New_York')
        self.assertEquals(datetime(2000,1,1), st.to_naive_utc_datetime())

        st = sanetztime(JUL_MICROS, tz='America/New_York')
        self.assertEquals(datetime(2000,7,1), st.to_naive_utc_datetime())

    def test_timezone_switch(self):
        st = sanetztime(JAN_MICROS)
        self.assertInnards(JAN_MICROS, self.ny, st.set_tz('America/New_York'))
        self.assertInnards(JAN_MICROS, self.ny, st) # make sure it operates on itself

        st = sanetztime(JAN_MICROS)
        self.assertInnards(JAN_MICROS, self.ny, st.set_tz(self.ny)) # make sure it's returning an obj
        self.assertInnards(JAN_MICROS, self.ny, st) # make sure it operates on itself

        st = sanetztime(JUL_MICROS)
        self.assertInnards(JUL_MICROS, self.ny, st.with_tz('America/New_York'))
        self.assertInnards(JUL_MICROS, self.utc, st) # make sure it doesn't operates on itself

        st = sanetztime(JUL_MICROS)
        self.assertInnards(JUL_MICROS, self.ny, st.with_tz(self.ny)) # make sure it's returning an obj
        self.assertInnards(JUL_MICROS, self.utc, st) # make sure it doesn't operates on itself

    def test_str(self):
        st = sanetztime(JAN_MICROS)
        self.assertEquals('%sus UTC'%JAN_MICROS, str(st))
        st = sanetztime(JUL_MICROS)
        self.assertEquals('%sus UTC'%JUL_MICROS, str(st))
        st = sanetztime(JAN_MICROS, tz='America/New_York')
        self.assertEquals('%sus America/New_York'%JAN_MICROS, str(st))
        st = sanetztime(JUL_MICROS, tz='US/Eastern')
        self.assertEquals('%sus US/Eastern'%JUL_MICROS, str(st))

    def test_repr(self):
        st = sanetztime(JAN_MICROS)
        self.assertEquals('2000-01-01 00:00:00.000000 UTC', repr(st))
        st = sanetztime(JUL_MICROS)
        self.assertEquals('2000-07-01 00:00:00.000000 UTC', repr(st))
        st = sanetztime(JAN_MICROS, tz='America/New_York')
        self.assertEquals('1999-12-31 19:00:00.000000 America/New_York', repr(st))
        st = sanetztime(JUL_MICROS, tz='US/Eastern')  
        self.assertEquals('2000-06-30 20:00:00.000000 US/Eastern', repr(st))


if __name__ == '__main__':
    unittest2.main()
