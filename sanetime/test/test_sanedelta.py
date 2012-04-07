import unittest
from sanetime import delta

class SaneDeltaTest(unittest.TestCase):

    def test_multiply(self):
        self.assertEquals(delta(15), delta(3) * 5)
