import unittest2
from sanetime.sanetime import SaneTime
from sanetime.error import SaneTimeError
from datetime import datetime
import pytz

# IMPORTANT -- note to self -- you CANNOT use tzinfo on datetime-- just pytz.timezone.localize everything to be safe

JAN_MICROS = 946684800*1000**2
JULY_MICROS = 962409600*1000**2
HOUR_MICROS = 60**2*1000**2

class SaneTimeTest(unittest2.TestCase):
    """ A class that wraps all the date time timezone python insanity, so you don't have to know about that shitshow """

    def assertInnards(self, utc_micros, timezone, st):
        self.assertEquals(utc_micros, st.utc_micros)
        self.assertEquals(timezone, st.timezone)
        self.assertEquals(timezone.zone, st.tz)

    def setUp(self):
        self.utc = pytz.utc
        self.ny = pytz.timezone('America/New_York')
        self.ac = pytz.timezone('Africa/Cairo')

    def test_timezone_labels(self):
        self.assertEquals('UTC', self.utc.zone)
        self.assertEquals('America/New_York', self.ny.zone)
        self.assertEquals('Africa/Cairo', self.ac.zone)

    def test_from_millis(self):
        self.assertInnards(JAN_MICROS, self.utc, SaneTime(JAN_MICROS))
        self.assertInnards(JAN_MICROS, self.utc, SaneTime(JAN_MICROS,tz='UTC'))
        self.assertInnards(JAN_MICROS, self.ny, SaneTime(JAN_MICROS,tz='America/New_York'))
        self.assertInnards(JAN_MICROS, self.ny, SaneTime(JAN_MICROS,timezone=self.ny))

    def test_from_datetime_string(self):
        self.assertInnards(JAN_MICROS, self.utc, SaneTime('2000-01-01 00:00:00'))
        self.assertInnards(JAN_MICROS, self.utc, SaneTime('2000-01-01'))
        self.assertInnards(JULY_MICROS, self.utc, SaneTime('July 1st, 2000'))

        self.assertInnards(JAN_MICROS, self.utc, SaneTime('2000-01-01 00:00:00', tz='UTC'))
        self.assertInnards(JAN_MICROS, self.utc, SaneTime('2000-01-01 00:00:00', timezone=self.utc))

        self.assertInnards(JAN_MICROS+HOUR_MICROS*5, self.ny, SaneTime('2000-01-01 00:00:00', tz='America/New_York'))
        self.assertInnards(JAN_MICROS+HOUR_MICROS*5, self.ny, SaneTime('2000-01-01 00:00:00', timezone=self.ny))

        self.assertInnards(JULY_MICROS+HOUR_MICROS*4, self.ny, SaneTime('2000-07-01', tz='America/New_York'))
        self.assertInnards(JULY_MICROS+HOUR_MICROS*4, self.ny, SaneTime('2000-07-01', timezone=self.ny))

    def test_from_datetime_params(self):
        self.assertInnards(JAN_MICROS+60**2*1000**2+60*1000**2+1000**2+1, self.utc, SaneTime(2000,1,1,1,1,1,1))
        self.assertInnards(JAN_MICROS+60**2*1000**2+60*1000**2+1000**2, self.utc, SaneTime(2000,1,1,1,1,1))
        self.assertInnards(JAN_MICROS+60**2*1000**2+60*1000**2, self.utc, SaneTime(2000,1,1,1,1))
        self.assertInnards(JAN_MICROS+60**2*1000**2, self.utc, SaneTime(2000,1,1,1))
        self.assertInnards(JAN_MICROS, self.utc, SaneTime(2000,1,1))
        self.assertInnards(JULY_MICROS, self.utc, SaneTime(2000,7,1))
        with self.assertRaises(SaneTimeError):
            SaneTime(2000,1)

        self.assertInnards(JAN_MICROS, self.utc, SaneTime(2000,1,1,0,0,0,0,tz='UTC'))
        self.assertInnards(JAN_MICROS, self.utc, SaneTime(2000,1,1,0,0,0,0,timezone=self.utc))

        self.assertInnards(JAN_MICROS+HOUR_MICROS*5, self.ny, SaneTime(2000,1,1,0,0,0,0,tz='America/New_York'))
        self.assertInnards(JAN_MICROS+HOUR_MICROS*5, self.ny, SaneTime(2000,1,1,0,0,0,0,timezone=self.ny))

        self.assertInnards(JULY_MICROS+HOUR_MICROS*4, self.ny, SaneTime(2000,7,1, tz='America/New_York'))
        self.assertInnards(JULY_MICROS+HOUR_MICROS*4, self.ny, SaneTime(2000,7,1, timezone=self.ny))

    def test_from_datetime(self):
        self.assertInnards(JAN_MICROS, self.utc, SaneTime(datetime(2000,1,1)))
        self.assertInnards(JAN_MICROS, self.utc, SaneTime(datetime(2000,1,1, tzinfo=self.utc)))
        self.assertInnards(JAN_MICROS+HOUR_MICROS*5, self.ny, SaneTime(self.ny.localize(datetime(2000,1,1))))
        self.assertInnards(JULY_MICROS+HOUR_MICROS*4, self.ny, SaneTime(self.ny.localize(datetime(2000,7,1))))

    def test_now(self):
        past = pytz.utc.localize(datetime.utcnow())
        st = SaneTime()
        future = pytz.utc.localize(datetime.utcnow())
        self.assertTrue(st.to_datetime() > past)
        self.assertTrue(st.to_datetime() < future)
        self.assertEquals('UTC', st.tz)

        past = self.utc.localize(datetime.utcnow()).astimezone(self.ny)
        st = SaneTime(tz='America/New_York')
        future = self.utc.localize(datetime.utcnow()).astimezone(self.ny)
        self.assertTrue(st.to_datetime() > past)
        self.assertTrue(st.to_datetime() < future)
        self.assertEquals('America/New_York', st.tz)

    def test_properties(self):
        st = SaneTime(2000,1,2,3,4,5,600700)
        self.assertEquals(700,st.utc_micros%1000)
        self.assertEquals(601,st.utc_millis%1000)
        self.assertEquals(6,st.utc_seconds%60)

    def test_transitives(self):
        st = SaneTime()
        st2 = SaneTime(st.to_datetime())
        self.assertEquals(st.utc_micros, st2.utc_micros)
        self.assertEquals(st.tz, st2.tz)

        st = SaneTime()
        st2 = SaneTime(str(st))
        self.assertEquals(st.utc_micros, st2.utc_micros)
        self.assertEquals(st.tz, st2.tz)

        st = SaneTime()
        st2 = SaneTime(st.utc_micros)
        self.assertEquals(st.utc_micros, st2.utc_micros)
        self.assertEquals(st.tz, st2.tz)

        st = SaneTime(tz='America/New_York')
        st2 = SaneTime(st.to_datetime())
        self.assertEquals(st.utc_micros, st2.utc_micros)
        self.assertEquals(st.tz, st2.tz)

        st = SaneTime(tz='America/New_York')
        st2 = SaneTime(str(st),tz='America/New_York')
        self.assertEquals(st.utc_micros, st2.utc_micros)
        self.assertEquals(st.tz, st2.tz)

        st = SaneTime(tz='America/New_York')
        st2 = SaneTime(st.utc_micros,tz='America/New_York')
        self.assertEquals(st.utc_micros, st2.utc_micros)
        self.assertEquals(st.tz, st2.tz)

    def test_comparisons(self):
        t1 = SaneTime(2000,1,1,0,0,0,0)
        t2 = SaneTime(2000,1,1,0,0,0,1)

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

    def test_arithmetic(self):
        t1 = SaneTime(2000,1,1,0,0,0,0)
        t2 = SaneTime(2000,1,1,0,0,0,1)

        self.assertEquals(t2.utc_micros, (t1+1).utc_micros)
        self.assertEquals(t2.tz, (t1+1).tz)

        self.assertEquals(t1.utc_micros,(t2-1).utc_micros)
        self.assertEquals(t1.tz, (t2-1).tz)

    def test_construction_errors(self):
        with self.assertRaises(SaneTimeError):
            SaneTime(JAN_MICROS, tz='America/New_York', timezone=self.ny)
        with self.assertRaises(SaneTimeError):
            SaneTime(JAN_MICROS, tz='America/New_York', timezone=self.ac)
        with self.assertRaises(SaneTimeError):
            SaneTime(datetime(2000,1,1, tzinfo=self.ac), tz='America/New_York')
        with self.assertRaises(SaneTimeError):
            SaneTime(datetime(2000,1,1, tzinfo=self.ac), timzone=self.ny)

    def test_to_datetime(self):
        st = SaneTime(JAN_MICROS)
        self.assertEquals(datetime(2000,1,1,tzinfo=self.utc), st.to_datetime())

        st = SaneTime(JAN_MICROS, tz='America/New_York')
        self.assertEquals(datetime(2000,1,1,tzinfo=self.utc).astimezone(self.ny), st.to_datetime())

        st = SaneTime(JULY_MICROS, tz='America/New_York')
        self.assertEquals(datetime(2000,7,1,tzinfo=self.utc).astimezone(self.ny), st.to_datetime())

    def test_to_naive_datetime(self):
        st = SaneTime(JAN_MICROS)
        self.assertEquals(datetime(2000,1,1), st.to_naive_datetime())

        st = SaneTime(JAN_MICROS, tz='America/New_York')
        self.assertEquals(datetime(1999,12,31,19), st.to_naive_datetime())

        st = SaneTime(JULY_MICROS, tz='America/New_York')
        self.assertEquals(datetime(2000,6,30,20), st.to_naive_datetime())

    def test_to_naive_utc_datetime(self):
        st = SaneTime(JAN_MICROS)
        self.assertEquals(datetime(2000,1,1), st.to_naive_utc_datetime())

        st = SaneTime(JAN_MICROS, tz='America/New_York')
        self.assertEquals(datetime(2000,1,1), st.to_naive_utc_datetime())

        st = SaneTime(JULY_MICROS, tz='America/New_York')
        self.assertEquals(datetime(2000,7,1), st.to_naive_utc_datetime())

    def test_timezone_switch(self):
        st = SaneTime(JAN_MICROS)
        self.assertInnards(JAN_MICROS, self.ny, st.set_tz('America/New_York'))
        self.assertInnards(JAN_MICROS, self.ny, st) # make sure it operates on itself

        st = SaneTime(JAN_MICROS)
        self.assertInnards(JAN_MICROS, self.ny, st.set_timezone(self.ny)) # make sure it's returning an obj
        self.assertInnards(JAN_MICROS, self.ny, st) # make sure it operates on itself

        st = SaneTime(JULY_MICROS)
        self.assertInnards(JULY_MICROS, self.ny, st.new_tz('America/New_York'))
        self.assertInnards(JULY_MICROS, self.utc, st) # make sure it doesn't operates on itself

        st = SaneTime(JULY_MICROS)
        self.assertInnards(JULY_MICROS, self.ny, st.new_timezone(self.ny)) # make sure it's returning an obj
        self.assertInnards(JULY_MICROS, self.utc, st) # make sure it doesn't operates on itself


if __name__ == '__main__':
    unittest2.main()
