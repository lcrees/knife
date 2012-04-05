# -*- coding: utf-8 -*-

from thingq.support import unittest
#pylint: disable-msg=w0614,w0401
from thingq.tests.auto.mapping import *  # @UnusedWildImport
from thingq.tests.auto.queuing import AQMixin


class TestAutoMap(unittest.TestCase, AQMixin, AMapQMixin):

    def setUp(self):
        from thingq.lazy.mapping import mapq
        self.qclass = mapq


class TestAutoRepeatQ(unittest.TestCase, AQMixin, ARepeatQMixin):

    def setUp(self):
        from thingq.lazy.mapping import repeatq
        self.qclass = repeatq


class TestAutoDelayQ(unittest.TestCase, AQMixin, ADelayQMixin):

    def setUp(self):
        from thingq.lazy.mapping import delayq
        self.qclass = delayq

if __name__ == '__main__':
    unittest.main()
