# -*- coding: utf-8 -*-
'''manually balanced lazy chainsaw tests'''

from chainsaw.compat import unittest

from chainsaw.tests.man.map import *  # @UnusedWildImport
from chainsaw.tests.man.analyze import *  # @UnusedWildImport
from chainsaw.tests.man.reduce import *  # @UnusedWildImport
from chainsaw.tests.man.filter import *  # @UnusedWildImport
from chainsaw.tests.man.manning import Manning
from chainsaw.tests.man.base import MQMixin


class TestMan(
    Manning, MQMixin, MFilterMixin, MMapMixin, MReduceMixin, MOrderMixin,
):

    def setUp(self):
        from chainsaw.lazy import lazychainsaw
        self.qclass = lazychainsaw.as_manual()


class TestManFilter(Manning, MFilterMixin):

    def setUp(self):
        self.maxDiff = None
        from chainsaw.lazy import filterchainsaw
        self.qclass = filterchainsaw.as_manual()


class TestManSlice(Manning, MQMixin, MSliceMixin):

    def setUp(self):
        from chainsaw.lazy import slicechainsaw
        self.qclass = slicechainsaw.as_manual()


class TestManCollect(Manning, MQMixin, MCollectMixin):

    def setUp(self):
        from chainsaw.lazy import collectchainsaw
        self.qclass = collectchainsaw.as_manual()


class TestManMap(Manning, MQMixin, MMapMixin):

    def setUp(self):
        from chainsaw.lazy import mapchainsaw
        self.qclass = mapchainsaw.as_manual()


class TestManRepeat(Manning, MQMixin, MRepeatMixin):

    def setUp(self):
        from chainsaw.lazy import repeatchainsaw
        self.qclass = repeatchainsaw.as_manual()


class TestManOrder(Manning, MQMixin, MOrderMixin):

    def setUp(self):
        from chainsaw.lazy import orderchainsaw
        self.qclass = orderchainsaw.as_manual()


class TestManReduce(Manning, MQMixin, MReduceMixin):

    def setUp(self):
        from chainsaw.lazy import reducechainsaw
        self.qclass = reducechainsaw.as_manual()


class TestManMath(Manning, MQMixin, MMathMixin):

    def setUp(self):
        from chainsaw.lazy import mathchainsaw
        self.qclass = mathchainsaw.as_manual()


class TestManTruth(Manning, MQMixin, MTruthMixin):

    def setUp(self):
        from chainsaw.lazy import truthchainsaw
        self.qclass = truthchainsaw.as_manual()

if __name__ == '__main__':
    unittest.main()
