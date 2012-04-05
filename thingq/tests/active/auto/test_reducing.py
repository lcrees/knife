# -*- coding: utf-8 -*-

from thingq.support import unittest
#pylint: disable-msg=w0614,w0401
from thingq.tests.auto.reducing import *  # @UnusedWildImport
from thingq.tests.auto.queuing import AQMixin


class TestAutoReduceQ(unittest.TestCase, AQMixin, AReduceQMixin):

    def setUp(self):
        from thingq.active.reducing import reduceq
        self.qclass = reduceq


class TestAutoMathQ(unittest.TestCase, AQMixin, AMathQMixin):

    def setUp(self):
        from thingq.active.reducing import mathq
        self.qclass = mathq


class TestAutoTruthQ(unittest.TestCase, AQMixin, ATruthQMixin):

    def setUp(self):
        from thingq.active.reducing import truthq
        self.qclass = truthq


if __name__ == '__main__':
    unittest.main()
