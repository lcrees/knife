# -*- coding: utf-8 -*-

from thingq.support import unittest
#pylint: disable-msg=w0614,w0401
from thingq.tests.auto.ordering import *  # @UnusedWildImport
from thingq.tests.auto.queuing import AQMixin


class TestAutoOrderQ(unittest.TestCase, AQMixin, AOrderQMixin):

    def setUp(self):
        from thingq.active.ordering import orderq
        self.qclass = orderq


class TestAutoRandomQ(unittest.TestCase, AQMixin, ARandomQMixin):

    def setUp(self):
        from thingq.active.ordering import randomq
        self.qclass = randomq

if __name__ == '__main__':
    unittest.main()
