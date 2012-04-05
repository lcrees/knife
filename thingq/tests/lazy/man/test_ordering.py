# -*- coding: utf-8 -*-

from thingq.support import unittest
#pylint: disable-msg=w0614,w0401
from thingq.tests.man.ordering import *  # @UnusedWildImport
from thingq.tests.man.queuing import MQMixin
from thingq.tests.man.manning import Manning


class TestManOrderQ(Manning, MQMixin, MOrderQMixin):

    def setUp(self):
        from thingq.lazy.ordering import morderq
        self.qclass = morderq


class TestManRandomQ(Manning, MQMixin, MRandomQMixin):

    def setUp(self):
        from thingq.lazy.ordering import mrandomq
        self.qclass = mrandomq


if __name__ == '__main__':
    unittest.main()
