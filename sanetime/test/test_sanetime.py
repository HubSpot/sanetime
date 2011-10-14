import unittest2
from sanetime.sanetime import SaneTime
from sanetime.error import SaneTimeError
from datetime import datetime
import pytz

# IMPORTANT-- you CANNOT use tzinfo on datetime-- you can mostly get it working if you associate it to pytz.utc, and then astimezone it to the correct timezone
#   ONLY HAVE RESOLUTION TO SECONDS-- NO MILLIS UNFORTUNATELY IN PYTHON-- ONLY MICROSECONDS, but there are no utilities to convert

JAN_MILLIS = 946684800000L
JULY_MILLIS = 962409600000L
HOUR_MILLIS = 1000L*60*60

class SaneTimeTest(unittest2.TestCase):
    """ A class that wraps all the date time timezone python insanity, so you don't have to know about that shitshow """

    def assertInnards(self, utc_millis, timezone, st):
        self.assertEquals(utc_millis, st.utc_millis)
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
        self.assertInnards(JAN_MILLIS, self.utc, SaneTime(JAN_MILLIS))
        self.assertInnards(JAN_MILLIS, self.utc, SaneTime(JAN_MILLIS,tz='UTC'))
        self.assertInnards(JAN_MILLIS, self.ny, SaneTime(JAN_MILLIS,tz='America/New_York'))
        self.assertInnards(JAN_MILLIS, self.ny, SaneTime(JAN_MILLIS,timezone=self.ny))

    def test_from_datetime_string(self):
        self.assertInnards(JAN_MILLIS, self.utc, SaneTime('2000-01-01 00:00:00'))
        self.assertInnards(JAN_MILLIS, self.utc, SaneTime('2000-01-01'))
        self.assertInnards(JULY_MILLIS, self.utc, SaneTime('July 1st, 2000'))

        self.assertInnards(JAN_MILLIS, self.utc, SaneTime('2000-01-01 00:00:00', tz='UTC'))
        self.assertInnards(JAN_MILLIS, self.utc, SaneTime('2000-01-01 00:00:00', timezone=self.utc))

        self.assertInnards(JAN_MILLIS+HOUR_MILLIS*5, self.ny, SaneTime('2000-01-01 00:00:00', tz='America/New_York'))
        self.assertInnards(JAN_MILLIS+HOUR_MILLIS*5, self.ny, SaneTime('2000-01-01 00:00:00', timezone=self.ny))

        self.assertInnards(JULY_MILLIS+HOUR_MILLIS*4, self.ny, SaneTime('2000-07-01', tz='America/New_York'))
        self.assertInnards(JULY_MILLIS+HOUR_MILLIS*4, self.ny, SaneTime('2000-07-01', timezone=self.ny))

    def test_from_datetime_params(self):
        self.assertInnards(JAN_MILLIS+60*60*1000L+60*1000L+1001L, self.utc, SaneTime(2000,1,1,1,1,1,1000))
        self.assertInnards(JAN_MILLIS+60*60*1000L+60*1000L+1000L, self.utc, SaneTime(2000,1,1,1,1,1))
        self.assertInnards(JAN_MILLIS+60*60*1000L+60*1000L, self.utc, SaneTime(2000,1,1,1,1))
        self.assertInnards(JAN_MILLIS+60*60*1000L, self.utc, SaneTime(2000,1,1,1))
        self.assertInnards(JAN_MILLIS, self.utc, SaneTime(2000,1,1))
        self.assertInnards(JULY_MILLIS, self.utc, SaneTime(2000,7,1))
        with self.assertRaises(SaneTimeError):
            SaneTime(2000,1)

        self.assertInnards(JAN_MILLIS, self.utc, SaneTime(2000,1,1,0,0,0,0,tz='UTC'))
        self.assertInnards(JAN_MILLIS, self.utc, SaneTime(2000,1,1,0,0,0,0,timezone=self.utc))

        self.assertInnards(JAN_MILLIS+HOUR_MILLIS*5, self.ny, SaneTime(2000,1,1,0,0,0,0,tz='America/New_York'))
        self.assertInnards(JAN_MILLIS+HOUR_MILLIS*5, self.ny, SaneTime(2000,1,1,0,0,0,0,timezone=self.ny))

        self.assertInnards(JULY_MILLIS+HOUR_MILLIS*4, self.ny, SaneTime(2000,7,1, tz='America/New_York'))
        self.assertInnards(JULY_MILLIS+HOUR_MILLIS*4, self.ny, SaneTime(2000,7,1, timezone=self.ny))

    def test_from_datetime(self):
        self.assertInnards(JAN_MILLIS, self.utc, SaneTime(datetime(2000,1,1)))
        self.assertInnards(JAN_MILLIS, self.utc, SaneTime(datetime(2000,1,1, tzinfo=self.utc)))
        self.assertInnards(JAN_MILLIS+HOUR_MILLIS*5, self.ny, SaneTime(self.ny.localize(datetime(2000,1,1))))
        self.assertInnards(JULY_MILLIS+HOUR_MILLIS*4, self.ny, SaneTime(self.ny.localize(datetime(2000,7,1))))

    def test_construction_errors(self):
        with self.assertRaises(SaneTimeError):
            SaneTime(JAN_MILLIS, tz='America/New_York', timezone=self.ny)
        with self.assertRaises(SaneTimeError):
            SaneTime(JAN_MILLIS, tz='America/New_York', timezone=self.ac)
        with self.assertRaises(SaneTimeError):
            SaneTime(datetime(2000,1,1, tzinfo=self.ac), tz='America/New_York')
        with self.assertRaises(SaneTimeError):
            SaneTime(datetime(2000,1,1, tzinfo=self.ac), timzone=self.ny)

    def test_to_datetime(self):
        st = SaneTime(JAN_MILLIS)
        self.assertEquals(datetime(2000,1,1,tzinfo=self.utc), st.to_datetime())

        st = SaneTime(JAN_MILLIS, tz='America/New_York')
        self.assertEquals(datetime(2000,1,1,tzinfo=self.utc).astimezone(self.ny), st.to_datetime())

        st = SaneTime(JULY_MILLIS, tz='America/New_York')
        self.assertEquals(datetime(2000,7,1,tzinfo=self.utc).astimezone(self.ny), st.to_datetime())

    def test_timezone_switch(self):
        st = SaneTime(JAN_MILLIS)
        self.assertInnards(JAN_MILLIS, self.ny, st.set_tz('America/New_York'))
        self.assertInnards(JAN_MILLIS, self.ny, st) # make sure it operates on itself

        st = SaneTime(JAN_MILLIS)
        self.assertInnards(JAN_MILLIS, self.ny, st.set_timezone(self.ny)) # make sure it's returning an obj
        self.assertInnards(JAN_MILLIS, self.ny, st) # make sure it operates on itself

        st = SaneTime(JULY_MILLIS)
        self.assertInnards(JULY_MILLIS, self.ny, st.new_tz('America/New_York'))
        self.assertInnards(JULY_MILLIS, self.utc, st) # make sure it doesn't operates on itself

        st = SaneTime(JULY_MILLIS)
        self.assertInnards(JULY_MILLIS, self.ny, st.new_timezone(self.ny)) # make sure it's returning an obj
        self.assertInnards(JULY_MILLIS, self.utc, st) # make sure it doesn't operates on itself


if __name__ == '__main__':
    unittest2.main()
