# -*- coding: utf-8 -*-
'''manually balanced active knife tests'''

from knife.compat import unittest
from knife.tests.man.mapping import *  # @UnusedWildImport
from knife.tests.man.ordering import *  # @UnusedWildImport
from knife.tests.man.reducing import *  # @UnusedWildImport
from knife.tests.man.filtering import *  # @UnusedWildImport
from knife.tests.man.transforming import *  # @UnusedWildImport
from knife.tests.man.manning import Manning
from knife.tests.man.queuing import MQMixin


class TestManQ(
    Manning, MQMixin, MFilterQMixin, MMapQMixin, MReduceQMixin, MOrderQMixin,
):

    def setUp(self):
        from knife import activeknife
        self.qclass = activeknife.manual()


class TestManFilterQ(Manning, MFilterQMixin):

    def setUp(self):
        self.maxDiff = None
        from knife.active import filterknife
        self.qclass = filterknife.manual()


class TestManSliceQ(Manning, MQMixin, MSliceQMixin):

    def setUp(self):
        from knife.active import sliceknife
        self.qclass = sliceknife.manual()


class TestManCollectQ(Manning, MQMixin, MCollectQMixin):

    def setUp(self):
        from knife.active import collectknife
        self.qclass = collectknife.manual()


class TestManMap(Manning, MQMixin, MMapQMixin):

    def setUp(self):
        from knife.active import mapknife
        self.qclass = mapknife.manual()


class TestManRepeatQ(Manning, MQMixin, MRepeatQMixin):

    def setUp(self):
        from knife.active import repeatknife
        self.qclass = repeatknife.manual()


class TestManOrderQ(Manning, MQMixin, MOrderQMixin):

    def setUp(self):
        from knife.active import orderknife
        self.qclass = orderknife.manual()


class TestManReduceQ(Manning, MQMixin, MReduceQMixin):

    def setUp(self):
        from knife.active import reduceknife
        self.qclass = reduceknife.manual()


class TestManMathQ(Manning, MQMixin, MMathQMixin):

    def setUp(self):
        from knife.active import mathknife
        self.qclass = mathknife.manual()


class TestManTruthQ(Manning, MQMixin, MTruthQMixin):

    def setUp(self):
        from knife.active import truthknife
        self.qclass = truthknife.manual()


if __name__ == '__main__':
    unittest.main()
