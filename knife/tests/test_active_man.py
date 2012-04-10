# -*- coding: utf-8 -*-
'''manually balanced active knife tests'''

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
        from knife import activeknife
        self.qclass = activeknife.as_manual()


class TestManFilter(Manning, MFilterMixin):

    def setUp(self):
        self.maxDiff = None
        from knife.active import filterknife
        self.qclass = filterknife.as_manual()


class TestManSlice(Manning, MQMixin, MSliceMixin):

    def setUp(self):
        from knife.active import sliceknife
        self.qclass = sliceknife.as_manual()


class TestManCollect(Manning, MQMixin, MCollectMixin):

    def setUp(self):
        from knife.active import collectknife
        self.qclass = collectknife.as_manual()


class TestManMap(Manning, MQMixin, MMapMixin):

    def setUp(self):
        from knife.active import mapknife
        self.qclass = mapknife.as_manual()


class TestManRepeat(Manning, MQMixin, MRepeatMixin):

    def setUp(self):
        from knife.active import repeatknife
        self.qclass = repeatknife.as_manual()


class TestManOrder(Manning, MQMixin, MOrderMixin):

    def setUp(self):
        from knife.active import orderknife
        self.qclass = orderknife.as_manual()


class TestManReduce(Manning, MQMixin, MReduceMixin):

    def setUp(self):
        from knife.active import reduceknife
        self.qclass = reduceknife.as_manual()


class TestManMath(Manning, MQMixin, MMathMixin):

    def setUp(self):
        from knife.active import mathknife
        self.qclass = mathknife.as_manual()


class TestManTruth(Manning, MQMixin, MTruthMixin):

    def setUp(self):
        from knife.active import truthknife
        self.qclass = truthknife.as_manual()


if __name__ == '__main__':
    unittest.main()
