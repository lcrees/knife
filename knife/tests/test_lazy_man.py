# -*- coding: utf-8 -*-
'''manually balanced lazy knife tests'''

from knife.compat import unittest

from knife.tests.man.map import *  # @UnusedWildImport
from knife.tests.man.analyze import *  # @UnusedWildImport
from knife.tests.man.reduce import *  # @UnusedWildImport
from knife.tests.man.filter import *  # @UnusedWildImport
from knife.tests.man.manning import Manning
from knife.tests.man.base import MQMixin


class TestManQ(
    Manning, MQMixin, MFilterMixin, MMapMixin, MReduceMixin, MOrderMixin,
):

    def setUp(self):
        from knife.lazy import lazyknife
        self.qclass = lazyknife.as_manual()


class TestManFilterQ(Manning, MFilterMixin):

    def setUp(self):
        self.maxDiff = None
        from knife.lazy import filterknife
        self.qclass = filterknife.as_manual()


class TestManSliceQ(Manning, MQMixin, MSliceMixin):

    def setUp(self):
        from knife.lazy import sliceknife
        self.qclass = sliceknife.as_manual()


class TestManCollectQ(Manning, MQMixin, MCollectMixin):

    def setUp(self):
        from knife.lazy import collectknife
        self.qclass = collectknife.as_manual()


class TestManMap(Manning, MQMixin, MMapMixin):

    def setUp(self):
        from knife.lazy import mapknife
        self.qclass = mapknife.as_manual()


class TestManRepeatQ(Manning, MQMixin, MRepeatMixin):

    def setUp(self):
        from knife.lazy import repeatknife
        self.qclass = repeatknife.as_manual()


class TestManOrderQ(Manning, MQMixin, MOrderMixin):

    def setUp(self):
        from knife.lazy import orderknife
        self.qclass = orderknife.as_manual()


class TestManReduceQ(Manning, MQMixin, MReduceMixin):

    def setUp(self):
        from knife.lazy import reduceknife
        self.qclass = reduceknife.as_manual()


class TestManMathQ(Manning, MQMixin, MMathMixin):

    def setUp(self):
        from knife.lazy import mathknife
        self.qclass = mathknife.as_manual()


class TestManTruthQ(Manning, MQMixin, MTruthMixin):

    def setUp(self):
        from knife.lazy import truthknife
        self.qclass = truthknife.as_manual()

if __name__ == '__main__':
    unittest.main()
