# -*- coding: utf-8 -*-
'''automatically balanced active knife tests'''

from knife.compat import unittest
from knife.tests.auto.mapping import *  # @UnusedWildImport
from knife.tests.auto.ordering import *  # @UnusedWildImport
from knife.tests.auto.reducing import *  # @UnusedWildImport
from knife.tests.auto.filtering import *  # @UnusedWildImport
from knife.tests.auto.transforming import *  # @UnusedWildImport
from knife.tests.auto.queuing import AQMixin


class TestAutoQ(
    unittest.TestCase, AQMixin, AFilterQMixin, AMapQMixin, AReduceQMixin,
    AOrderQMixin,
):

    def setUp(self):
        from knife import activeknife
        self.qclass = activeknife


class TestAutoFilterQ(unittest.TestCase, AQMixin, AFilterQMixin):

    def setUp(self):
        self.maxDiff = None
        from knife.active import filterknife
        self.qclass = filterknife


class TestAutoSliceQ(unittest.TestCase, AQMixin, ASliceQMixin):

    def setUp(self):
        from knife.active import sliceknife
        self.qclass = sliceknife


class TestAutoCollectQ(unittest.TestCase, AQMixin, ACollectQMixin):

    def setUp(self):
        self.maxDiff = None
        from knife.active import collectknife
        self.qclass = collectknife


class TestAutoMap(unittest.TestCase, AQMixin, AMapQMixin):

    def setUp(self):
        from knife.active import mapknife
        self.qclass = mapknife


class TestAutoRepeatQ(unittest.TestCase, AQMixin, ARepeatQMixin):

    def setUp(self):
        from knife.active import repeatknife
        self.qclass = repeatknife


class TestAutoOrderQ(unittest.TestCase, AQMixin, AOrderQMixin):

    def setUp(self):
        from knife.active import orderknife
        self.qclass = orderknife


class TestAutoReduceQ(unittest.TestCase, AQMixin, AReduceQMixin):

    def setUp(self):
        from knife.active import reduceknife
        self.qclass = reduceknife


class TestAutoMathQ(unittest.TestCase, AQMixin, AMathQMixin):

    def setUp(self):
        from knife.active import mathknife
        self.qclass = mathknife


class TestAutoTruthQ(unittest.TestCase, AQMixin, ATruthQMixin):

    def setUp(self):
        from knife.active import truthknife
        self.qclass = truthknife


if __name__ == '__main__':
    unittest.main()
