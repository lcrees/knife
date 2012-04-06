# -*- coding: utf-8 -*-
'''manpipe tests'''

from thingpipe.compat import unittest
from thingpipe.tests.man.mapping import *  # @UnusedWildImport
from thingpipe.tests.man.ordering import *  # @UnusedWildImport
from thingpipe.tests.man.reducing import *  # @UnusedWildImport
from thingpipe.tests.man.filtering import *  # @UnusedWildImport
from thingpipe.tests.man.transforming import *  # @UnusedWildImport
from thingpipe.tests.man.manning import Manning
from thingpipe.tests.man.queuing import MQMixin


class TestManQ(
    Manning, MQMixin, MFilterQMixin, MMapQMixin, MReduceQMixin, MOrderQMixin,
):

    def setUp(self):
        from thingpipe import manpipe
        self.qclass = manpipe


class TestManFilterQ(Manning, MFilterQMixin):

    def setUp(self):
        self.maxDiff = None
        from thingpipe.active import mfilterpipe
        self.qclass = mfilterpipe


class TestManSliceQ(Manning, MQMixin, MSliceQMixin):

    def setUp(self):
        from thingpipe.active import mslicepipe
        self.qclass = mslicepipe


class TestManCollectQ(Manning, MQMixin, MCollectQMixin):

    def setUp(self):
        from thingpipe.active import mcollectpipe
        self.qclass = mcollectpipe


class TestManSetQ(Manning, MQMixin, MSetQMixin):

    def setUp(self):
        from thingpipe.active import msetpipe
        self.qclass = msetpipe


class TestManMap(Manning, MQMixin, MMapQMixin):

    def setUp(self):
        from thingpipe.active import mmappipe
        self.qclass = mmappipe


class TestManRepeatQ(Manning, MQMixin, MRepeatQMixin):

    def setUp(self):
        from thingpipe.active import mrepeatpipe
        self.qclass = mrepeatpipe


class TestManOrderQ(Manning, MQMixin, MOrderQMixin):

    def setUp(self):
        from thingpipe.active import morderpipe
        self.qclass = morderpipe


class TestManRandomQ(Manning, MQMixin, MRandomQMixin):

    def setUp(self):
        from thingpipe.active import mrandompipe
        self.qclass = mrandompipe


class TestManReduceQ(Manning, MQMixin, MReduceQMixin):

    def setUp(self):
        from thingpipe.active import mreducepipe
        self.qclass = mreducepipe


class TestManMathQ(Manning, MQMixin, MMathQMixin):

    def setUp(self):
        from thingpipe.active import mmathpipe
        self.qclass = mmathpipe


class TestManTruthQ(Manning, MQMixin, MTruthQMixin):

    def setUp(self):
        from thingpipe.active import mtruthpipe
        self.qclass = mtruthpipe


class TestStringQ(Manning, MQMixin, MStringQMixin):

    def setUp(self):
        from thingpipe.active import mstringpipe
        self.qclass = mstringpipe


class TestTransformQ(Manning, MQMixin, MStringQMixin):

    def setUp(self):
        from thingpipe.active import mtransformpipe
        self.qclass = mtransformpipe


if __name__ == '__main__':
    unittest.main()
