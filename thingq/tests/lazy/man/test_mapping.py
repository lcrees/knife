# -*- coding: utf-8 -*-

from thingq.support import unittest
#pylint: disable-msg=w0614,w0401
from thingq.tests.man.mapping import *  # @UnusedWildImport
from thingq.tests.man.queuing import MQMixin
from thingq.tests.man.manning import Manning


class TestManMap(Manning, MQMixin, MMapQMixin):

    def setUp(self):
        from thingq.lazy.mapping import mmapq
        self.qclass = mmapq


class TestManRepeatQ(Manning, MQMixin, MRepeatQMixin):

    def setUp(self):
        from thingq.lazy.mapping import mrepeatq
        self.qclass = mrepeatq


class TestManDelayQ(Manning, MQMixin, MDelayQMixin):

    def setUp(self):
        from thingq.lazy.mapping import mdelayq
        self.qclass = mdelayq


if __name__ == '__main__':
    unittest.main()
