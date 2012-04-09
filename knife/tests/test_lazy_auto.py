# -*- coding: utf-8 -*-
'''automatically balancing lazy knife tests'''

from knife.compat import unittest
from knife.tests.auto.map import *  # @UnusedWildImport
from knife.tests.auto.analyze import *  # @UnusedWildImport
from knife.tests.auto.reduce import *  # @UnusedWildImport
from knife.tests.auto.filter import *  # @UnusedWildImport
from knife.tests.auto.base import AMixin


class TestAutoQ(
    unittest.TestCase, AMixin, AFilterMixin, AMapMixin, AReduceMixin,
    AOrderMixin,
):

    def setUp(self):
        from knife.lazy import lazyknife
        self.qclass = lazyknife


class TestAutoFilterQ(unittest.TestCase, AMixin, AFilterMixin):

    def setUp(self):
        self.maxDiff = None
        from knife.lazy import filterknife
        self.qclass = filterknife


class TestAutoSliceQ(unittest.TestCase, AMixin, ASliceMixin):

    def setUp(self):
        from knife.lazy import sliceknife
        self.qclass = sliceknife


class TestAutoCollectQ(unittest.TestCase, AMixin, ACollectMixin):

    def setUp(self):
        self.maxDiff = None
        from knife.lazy import collectknife
        self.qclass = collectknife


class TestAutoMap(unittest.TestCase, AMixin, AMapMixin):

    def setUp(self):
        from knife.lazy import mapknife
        self.qclass = mapknife


class TestAutoRepeatQ(unittest.TestCase, AMixin, ARepeatMixin):

    def setUp(self):
        from knife.lazy import repeatknife
        self.qclass = repeatknife


class TestAutoOrderQ(unittest.TestCase, AMixin, AOrderMixin):

    def setUp(self):
        from knife.lazy import orderknife
        self.qclass = orderknife


class TestAutoReduceQ(unittest.TestCase, AMixin, AReduceMixin):

    def setUp(self):
        from knife.lazy import reduceknife
        self.qclass = reduceknife


class TestAutoMathQ(unittest.TestCase, AMixin, AMathMixin):

    def setUp(self):
        from knife.lazy import mathknife
        self.qclass = mathknife


class TestAutoTruthQ(unittest.TestCase, AMixin, ATruthMixin):

    def setUp(self):
        from knife.lazy import truthknife
        self.qclass = truthknife

if __name__ == '__main__':
    unittest.main()
