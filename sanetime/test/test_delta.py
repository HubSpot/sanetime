import unittest
from sanetime import delta

class SaneDeltaTest(unittest.TestCase):
    def test_construction(self):
        self.assertEquals(1+1000*(2+1000*(3+60*(4+60*(5+24*(6+7*7))))),delta(us=1,ms=2,s=3,m=4,h=5,md=6,mw=7))

    def test_copy_construction(self):
        self.assertEquals(123, delta(delta(123)))

    def test_clone(self):
        self.assertEquals(123, delta(123).clone())

    def test_casting(self):
        self.assertEquals(123, int(delta(123)))
        self.assertEquals(123, long(delta(123)))
        self.assertEquals('6d 5h 4m 3.002001s', str(delta(us=1,ms=2,s=3,m=4,h=5,md=6)))
        self.assertEquals(u'6d 5h 4m 3.002001s', unicode(delta(us=1,ms=2,s=3,m=4,h=5,md=6)))
        self.assertEquals(hash(123), hash(delta(123))

    def test_arithmetic(self):
        t1 = time(JAN_MICROS)
        t2 = time(JAN_MICROS+1)

        self.assertEquals(t2.us, (t1+1).us)
        self.assertEquals(t1.us,(t2-1).us)

        self.assertEquals(1, t2 - t1)
        self.assertEquals(-1, t1 - t2)

    def test_multiply(self):
        self.assertEquals(delta(15), delta(3) * 5)


