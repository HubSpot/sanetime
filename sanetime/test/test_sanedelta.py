import unittest
from sanetime import delta

class SaneDeltaTest(unittest.TestCase):

    def test_multiply(self):
        self.assertEquals(delta(15), delta(3) * 5)

    def test_construct_str(self):
        self.assertEquals('1m', delta(m=1).abbr)

    def test_positionals(self):
        d = delta(d=1,h=1,m=1,s=1,ms=1,us=1)
        self.assertEquals(1,d.ph)
        self.assertEquals(1,d.pm)
        self.assertEquals(1,d.ps)
        self.assertEquals(1,d.pms)
        self.assertEquals(1001,d.pus)

        d = delta(d=1,h=11,m=29,s=29,ms=499,us=499)
        self.assertEquals(11,d.prh)
        self.assertEquals(29,d.prm)
        self.assertEquals(29,d.prs)
        self.assertEquals(499,d.prms)
        self.assertEquals(499499,d.prus)

        d = delta(d=1,h=12,m=30,s=30,ms=500,us=500)
        self.assertEquals(13,d.prh)
        self.assertEquals(31,d.prm)
        self.assertEquals(31,d.prs)
        self.assertEquals(501,d.prms)
        self.assertEquals(500500,d.prus)

