# -*- coding: utf-8 -*-
'''manq tests'''

from thingq.support import unittest
from thingq.tests.man.mapping import *  # @UnusedWildImport
from thingq.tests.man.ordering import *  # @UnusedWildImport
from thingq.tests.man.reducing import *  # @UnusedWildImport
from thingq.tests.man.filtering import *  # @UnusedWildImport
from thingq.tests.man.manning import Manning
from thingq.tests.man.queuing import MQMixin


class TestManQ(
    Manning, MQMixin, MFilterQMixin, MMapQMixin, MReduceQMixin, MOrderQMixin,
):

    def setUp(self):
        from thingq import manq
        self.qclass = manq


class TestManFilterQ(Manning, MFilterQMixin):

    def setUp(self):
        self.maxDiff = None
        from thingq.active.core import mfilterq
        self.qclass = mfilterq


class TestManSliceQ(Manning, MQMixin, MSliceQMixin):

    def setUp(self):
        from thingq.active.core import msliceq
        self.qclass = msliceq


class TestManCollectQ(Manning, MQMixin, MCollectQMixin):

    def setUp(self):
        from thingq.active.core import mcollectq
        self.qclass = mcollectq


class TestManSetQ(Manning, MQMixin, MSetQMixin):

    def setUp(self):
        from thingq.active.core import msetq
        self.qclass = msetq


class TestManMap(Manning, MQMixin, MMapQMixin):

    def setUp(self):
        from thingq.active.core import mmapq
        self.qclass = mmapq


class TestManRepeatQ(Manning, MQMixin, MRepeatQMixin):

    def setUp(self):
        from thingq.active.core import mrepeatq
        self.qclass = mrepeatq


class TestManOrderQ(Manning, MQMixin, MOrderQMixin):

    def setUp(self):
        from thingq.active.core import morderq
        self.qclass = morderq


class TestManRandomQ(Manning, MQMixin, MRandomQMixin):

    def setUp(self):
        from thingq.active.core import mrandomq
        self.qclass = mrandomq


class TestManReduceQ(Manning, MQMixin, MReduceQMixin):

    def setUp(self):
        from thingq.active.core import mreduceq
        self.qclass = mreduceq


class TestManMathQ(Manning, MQMixin, MMathQMixin):

    def setUp(self):
        from thingq.active.core import mmathq
        self.qclass = mmathq


class TestManTruthQ(Manning, MQMixin, MTruthQMixin):

    def setUp(self):
        from thingq.active.core import mtruthq
        self.qclass = mtruthq


if __name__ == '__main__':
    unittest.main()
