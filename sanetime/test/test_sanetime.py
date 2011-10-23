import unittest2
from sanetime import sanetime
from sanetime.error import SaneTimeError
from datetime import datetime
import pytz

# IMPORTANT -- note to self -- you CANNOT use tzinfo on datetime-- just pytz.timezone.localize everything to be safe

JAN_MICROS = 946684800*1000**2
JULY_MICROS = 962409600*1000**2
HOUR_MICROS = 60**2*1000**2

class SaneTimeTest(unittest2.TestCase):
    """ A class that wraps all the date time timezone python insanity, so you don't have to know about that shitshow """

    def assertInnards(self, us, tz, st):
        self.assertEquals(us, st.us)
        self.assertEquals(tz.zone, st.tz.zone)

    def assertSaneTimeEquals(self, st1, st2):
        self.assertInnards(st1.us, st1.tz, st2)

    def setUp(self):
        self.utc = pytz.utc
        self.ny = pytz.timezone('America/New_York')
        self.ac = pytz.timezone('Africa/Cairo')

    def test_timezone_labels(self):
        self.assertEquals('UTC', self.utc.zone)
        self.assertEquals('America/New_York', self.ny.zone)
        self.assertEquals('Africa/Cairo', self.ac.zone)

    def test_from_micros(self):
        self.assertInnards(JAN_MICROS, self.utc, sanetime(JAN_MICROS))
        self.assertInnards(JAN_MICROS, self.utc, sanetime(JAN_MICROS,tz='UTC'))
        self.assertInnards(JAN_MICROS, self.ny, sanetime(JAN_MICROS,tz='America/New_York'))
        self.assertInnards(JAN_MICROS, self.ny, sanetime(JAN_MICROS,tz=self.ny))

    def test_from_datetime_string(self):
        self.assertInnards(JAN_MICROS, self.utc, sanetime('2000-01-01 00:00:00'))
        self.assertInnards(JAN_MICROS, self.utc, sanetime('2000-01-01'))
        self.assertInnards(JULY_MICROS, self.utc, sanetime('July 1st, 2000'))

        self.assertInnards(JAN_MICROS, self.utc, sanetime('2000-01-01 00:00:00', tz='UTC'))
        self.assertInnards(JAN_MICROS, self.utc, sanetime('2000-01-01 00:00:00', tz=self.utc))

        self.assertInnards(JAN_MICROS+HOUR_MICROS*5, self.ny, sanetime('2000-01-01 00:00:00', tz='America/New_York'))
        self.assertInnards(JAN_MICROS+HOUR_MICROS*5, self.ny, sanetime('2000-01-01 00:00:00', tz=self.ny))

        self.assertInnards(JULY_MICROS+HOUR_MICROS*4, self.ny, sanetime('2000-07-01', tz='America/New_York'))
        self.assertInnards(JULY_MICROS+HOUR_MICROS*4, self.ny, sanetime('2000-07-01', tz=self.ny))

    def test_from_datetime_params(self):
        self.assertInnards(JAN_MICROS+60**2*1000**2+60*1000**2+1000**2+1, self.utc, sanetime(2000,1,1,1,1,1,1))
        self.assertInnards(JAN_MICROS+60**2*1000**2+60*1000**2+1000**2, self.utc, sanetime(2000,1,1,1,1,1))
        self.assertInnards(JAN_MICROS+60**2*1000**2+60*1000**2, self.utc, sanetime(2000,1,1,1,1))
        self.assertInnards(JAN_MICROS+60**2*1000**2, self.utc, sanetime(2000,1,1,1))
        self.assertInnards(JAN_MICROS, self.utc, sanetime(2000,1,1))
        self.assertInnards(JULY_MICROS, self.utc, sanetime(2000,7,1))
        with self.assertRaises(SaneTimeError):
            sanetime(2000,1)

        self.assertInnards(JAN_MICROS, self.utc, sanetime(2000,1,1,0,0,0,0,tz='UTC'))
        self.assertInnards(JAN_MICROS, self.utc, sanetime(2000,1,1,0,0,0,0,tz=self.utc))

        self.assertInnards(JAN_MICROS+HOUR_MICROS*5, self.ny, sanetime(2000,1,1,0,0,0,0,tz='America/New_York'))
        self.assertInnards(JAN_MICROS+HOUR_MICROS*5, self.ny, sanetime(2000,1,1,0,0,0,0,tz=self.ny))

        self.assertInnards(JULY_MICROS+HOUR_MICROS*4, self.ny, sanetime(2000,7,1, tz='America/New_York'))
        self.assertInnards(JULY_MICROS+HOUR_MICROS*4, self.ny, sanetime(2000,7,1, tz=self.ny))

    def test_from_datetime(self):
        self.assertInnards(JAN_MICROS, self.utc, sanetime(datetime(2000,1,1)))
        self.assertInnards(JAN_MICROS, self.utc, sanetime(datetime(2000,1,1, tzinfo=self.utc)))
        self.assertInnards(JAN_MICROS+HOUR_MICROS*5, self.ny, sanetime(self.ny.localize(datetime(2000,1,1))))
        self.assertInnards(JULY_MICROS+HOUR_MICROS*4, self.ny, sanetime(self.ny.localize(datetime(2000,7,1))))

    def test_now(self):
        past = pytz.utc.localize(datetime.utcnow())
        st = sanetime()
        future = pytz.utc.localize(datetime.utcnow())
        self.assertTrue(st.to_datetime() > past)
        self.assertTrue(st.to_datetime() < future)
        self.assertEquals('UTC', st.tz.zone)

        past = self.utc.localize(datetime.utcnow()).astimezone(self.ny)
        st = sanetime(tz='America/New_York')
        future = self.utc.localize(datetime.utcnow()).astimezone(self.ny)
        self.assertTrue(st.to_datetime() > past)
        self.assertTrue(st.to_datetime() < future)
        self.assertEquals('America/New_York', st.tz.zone)

    def test_properties(self):
        st = sanetime(2000,1,2,3,4,5,600700)
        self.assertEquals(700,st.us%1000)
        self.assertEquals(601,st.ms%1000) # remember, it rounds
        self.assertEquals(6,st.s%60) # remember, it rounds

    def test_transitives(self):
        st = sanetime()
        st2 = sanetime(st.to_datetime())
        self.assertSaneTimeEquals(st, st2)

        st = sanetime()
        st2 = sanetime(str(st))
        self.assertSaneTimeEquals(st, st2)

        st = sanetime()
        st2 = sanetime(st.us)
        self.assertSaneTimeEquals(st, st2)

        st = sanetime(tz='America/New_York')
        st2 = sanetime(st.to_datetime())
        self.assertSaneTimeEquals(st, st2)


        st = sanetime(tz='America/New_York')
        st2 = sanetime(str(st))
        self.assertEquals(st.us, st2.us)
        # yes we are doing this on purpose -- timezone aren't really transitive when going through strings, so let's not pretend they are
        self.assertEquals('America/New_York', st.tz.zone)
        self.assertEquals('UTC', st2.tz.zone)

        st = sanetime(tz='America/New_York')
        st2 = sanetime(st.us,tz='America/New_York')
        self.assertSaneTimeEquals(st, st2)

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

    def test_arithmetic(self):
        t1 = sanetime(2000,1,1,0,0,0,0)
        t2 = sanetime(2000,1,1,0,0,0,1)

        self.assertEquals(t2.us, (t1+1).us)
        self.assertEquals(t2.tz, (t1+1).tz)

        self.assertEquals(t1.us,(t2-1).us)
        self.assertEquals(t1.tz, (t2-1).tz)

    def test_construction_errors(self):
        with self.assertRaises(SaneTimeError):
            sanetime(datetime(2000,1,1, tzinfo=self.ac), tz='America/New_York')
        with self.assertRaises(SaneTimeError):
            sanetime(datetime(2000,1,1, tzinfo=self.ac), tz=self.ny)

    def test_to_datetime(self):
        st = sanetime(JAN_MICROS)
        self.assertEquals(datetime(2000,1,1,tzinfo=self.utc), st.to_datetime())

        st = sanetime(JAN_MICROS, tz='America/New_York')
        self.assertEquals(datetime(2000,1,1,tzinfo=self.utc).astimezone(self.ny), st.to_datetime())

        st = sanetime(JULY_MICROS, tz='America/New_York')
        self.assertEquals(datetime(2000,7,1,tzinfo=self.utc).astimezone(self.ny), st.to_datetime())

    def test_to_naive_datetime(self):
        st = sanetime(JAN_MICROS)
        self.assertEquals(datetime(2000,1,1), st.to_naive_datetime())

        st = sanetime(JAN_MICROS, tz='America/New_York')
        self.assertEquals(datetime(1999,12,31,19), st.to_naive_datetime())

        st = sanetime(JULY_MICROS, tz='America/New_York')
        self.assertEquals(datetime(2000,6,30,20), st.to_naive_datetime())

    def test_to_naive_utc_datetime(self):
        st = sanetime(JAN_MICROS)
        self.assertEquals(datetime(2000,1,1), st.to_naive_utc_datetime())

        st = sanetime(JAN_MICROS, tz='America/New_York')
        self.assertEquals(datetime(2000,1,1), st.to_naive_utc_datetime())

        st = sanetime(JULY_MICROS, tz='America/New_York')
        self.assertEquals(datetime(2000,7,1), st.to_naive_utc_datetime())

    def test_timezone_switch(self):
        st = sanetime(JAN_MICROS)
        self.assertInnards(JAN_MICROS, self.ny, st.set_tz('America/New_York'))
        self.assertInnards(JAN_MICROS, self.ny, st) # make sure it operates on itself

        st = sanetime(JAN_MICROS)
        self.assertInnards(JAN_MICROS, self.ny, st.set_tz(self.ny)) # make sure it's returning an obj
        self.assertInnards(JAN_MICROS, self.ny, st) # make sure it operates on itself

        st = sanetime(JULY_MICROS)
        self.assertInnards(JULY_MICROS, self.ny, st.with_tz('America/New_York'))
        self.assertInnards(JULY_MICROS, self.utc, st) # make sure it doesn't operates on itself

        st = sanetime(JULY_MICROS)
        self.assertInnards(JULY_MICROS, self.ny, st.with_tz(self.ny)) # make sure it's returning an obj
        self.assertInnards(JULY_MICROS, self.utc, st) # make sure it doesn't operates on itself


if __name__ == '__main__':
    unittest2.main()
