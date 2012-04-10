# -*- coding: utf-8 -*-
'''manually balanced lazy knife tests'''

from knife.compat import unittest

from knife.tests.man.map import *  # @UnusedWildImport
from knife.tests.man.analyze import *  # @UnusedWildImport
from knife.tests.man.reduce import *  # @UnusedWildImport
from knife.tests.man.filter import *  # @UnusedWildImport
from knife.tests.man.manning import Manning
from knife.tests.man.base import MQMixin


class TestMan(
    Manning, MQMixin, MFilterMixin, MMapMixin, MReduceMixin, MOrderMixin,
):

    def setUp(self):
        from knife.lazy import lazyknife
        self.qclass = lazyknife.as_manual()


class TestManFilter(Manning, MFilterMixin):

    def setUp(self):
        self.maxDiff = None
        from knife.lazy import filterknife
        self.qclass = filterknife.as_manual()


class TestManSlice(Manning, MQMixin, MSliceMixin):

    def setUp(self):
        from knife.lazy import sliceknife
        self.qclass = sliceknife.as_manual()


class TestManCollect(Manning, MQMixin, MCollectMixin):

    def setUp(self):
        from knife.lazy import collectknife
        self.qclass = collectknife.as_manual()


class TestManMap(Manning, MQMixin, MMapMixin):

    def setUp(self):
        from knife.lazy import mapknife
        self.qclass = mapknife.as_manual()


class TestManRepeat(Manning, MQMixin, MRepeatMixin):

    def setUp(self):
        from knife.lazy import repeatknife
        self.qclass = repeatknife.as_manual()


class TestManOrder(Manning, MQMixin, MOrderMixin):

    def setUp(self):
        from knife.lazy import orderknife
        self.qclass = orderknife.as_manual()


class TestManReduce(Manning, MQMixin, MReduceMixin):

    def setUp(self):
        from knife.lazy import reduceknife
        self.qclass = reduceknife.as_manual()


class TestManMath(Manning, MQMixin, MMathMixin):

    def setUp(self):
        from knife.lazy import mathknife
        self.qclass = mathknife.as_manual()


class TestManTruth(Manning, MQMixin, MTruthMixin):

    def setUp(self):
        from knife.lazy import truthknife
        self.qclass = truthknife.as_manual()

if __name__ == '__main__':
    unittest.main()
