import unittest
import pytz
from .. import tztime

JAN_MICROS = 1325376000*1000**2
JAN_MILLIS = JAN_MICROS/1000
JAN_SECS = JAN_MILLIS/1000
JUL_MICROS = 1338508800*1000**2
HOUR_MICROS = 60**2*1000**2

NY_JAN_MICROS = JAN_MICROS + HOUR_MICROS * 5
NY_JUL_MICROS = JUL_MICROS + HOUR_MICROS * 4

TZ_UTC = pytz.utc
TZ_NY = pytz.timezone('America/New_York')
TZ_AC = pytz.timezone('Africa/Cairo')

class SaneTzTimeTest(unittest.TestCase):

    def setUp(self): pass

    def test_clone(self):
        self.assertEquals(tztime, type(tztime(JAN_MICROS,TZ_UTC).clone()))

    def test_equality(self):
        t1 = tztime(JAN_MICROS, tz='UTC')
        t2 = tztime(JAN_MICROS, tz='America/New_York')
        t3 = tztime(JAN_MICROS+1)
        self.assertTrue(t1==t1)
        self.assertTrue(t2==t2)
        self.assertTrue(t3==t3)
        self.assertFalse(t1!=t1)
        self.assertFalse(t2!=t2)
        self.assertFalse(t3!=t3)

        self.assertTrue(t1!=t2)
        self.assertTrue(t2!=t1)
        self.assertTrue(t1!=t3)
        self.assertTrue(t3!=t1)
        self.assertTrue(t2!=t3)
        self.assertTrue(t3!=t2)

        self.assertFalse(t1==t2)
        self.assertFalse(t2==t1)
        self.assertFalse(t1==t3)
        self.assertFalse(t3==t1)
        self.assertFalse(t2==t3)
        self.assertFalse(t3==t2)

        self.assertTrue(t1!=None)
        self.assertFalse(t1==None)
        self.assertTrue(None!=t1)
        self.assertFalse(None==t1)

        self.assertTrue(t1==t1.us)

    def test_comparisons(self):
        t1 = tztime(JAN_MICROS,'UTC')
        t2 = tztime(JAN_MICROS,'America/New_York')
        t3 = tztime(JAN_MICROS+1,'UTC')

        self.assertFalse(t1 > t1)
        self.assertFalse(t2 > t2)
        self.assertFalse(t3 > t3)
        self.assertTrue(t1 > t2)
        self.assertFalse(t2 > t1)
        self.assertFalse(t1 > t3)
        self.assertTrue(t3 > t1)
        self.assertFalse(t2 > t3)
        self.assertTrue(t3 > t2)

        self.assertTrue(t1 >= t1)
        self.assertTrue(t2 >= t2)
        self.assertTrue(t3 >= t3)
        self.assertTrue(t1 >= t2)
        self.assertFalse(t2 >= t1)
        self.assertFalse(t1 >= t3)
        self.assertTrue(t3 >= t1)
        self.assertFalse(t2 >= t3)
        self.assertTrue(t3 >= t2)

        self.assertTrue(t1 <= t1)
        self.assertTrue(t2 <= t2)
        self.assertTrue(t3 <= t3)
        self.assertFalse(t1 <= t2)
        self.assertTrue(t2 <= t1)
        self.assertTrue(t1 <= t3)
        self.assertFalse(t3 <= t1)
        self.assertTrue(t2 <= t3)
        self.assertFalse(t3 <= t2)

        self.assertFalse(t1 < t1)
        self.assertFalse(t2 < t2)
        self.assertFalse(t3 < t3)
        self.assertFalse(t1 < t2)
        self.assertTrue(t2 < t1)
        self.assertTrue(t1 < t3)
        self.assertFalse(t3 < t1)
        self.assertTrue(t2 < t3)
        self.assertFalse(t3 < t2)

    def test_hashability(self):
        t1 = tztime(JAN_MICROS, tz='UTC')
        t2 = tztime(JAN_MICROS, tz='America/New_York')
        t3 = tztime(JAN_MICROS+1)
        s = set([t1,t2,t3])
        self.assertEquals(3, len(s))
        self.assertIn(t1, s)
        self.assertIn(t2, s)
        self.assertIn(t3, s)

