# -*- coding: utf-8 -*-
'''autoq tests'''

from thingq.support import unittest
from thingq.tests.auto.mapping import *  # @UnusedWildImport
from thingq.tests.auto.ordering import *  # @UnusedWildImport
from thingq.tests.auto.reducing import *  # @UnusedWildImport
from thingq.tests.auto.filtering import *  # @UnusedWildImport
from thingq.tests.auto.queuing import AQMixin


class TestAutoQ(
    unittest.TestCase, AQMixin, AFilterQMixin, AMapQMixin, AReduceQMixin,
    AOrderQMixin,
):

    def setUp(self):
        from thingq import autoq
        self.qclass = autoq


class TestAutoFilterQ(unittest.TestCase, AQMixin, AFilterQMixin):

    def setUp(self):
        self.maxDiff = None
        from thingq.active.core import filterq
        self.qclass = filterq


class TestAutoSliceQ(unittest.TestCase, AQMixin, ASliceQMixin):

    def setUp(self):
        from thingq.active.core import sliceq
        self.qclass = sliceq


class TestAutoCollectQ(unittest.TestCase, AQMixin, ACollectQMixin):

    def setUp(self):
        self.maxDiff = None
        from thingq.active.core import collectq
        self.qclass = collectq


class TestAutoSetQ(unittest.TestCase, AQMixin, ASetQMixin):

    def setUp(self):
        from thingq.active.core import setq
        self.qclass = setq


class TestAutoMap(unittest.TestCase, AQMixin, AMapQMixin):

    def setUp(self):
        from thingq.active.core import mapq
        self.qclass = mapq


class TestAutoRepeatQ(unittest.TestCase, AQMixin, ARepeatQMixin):

    def setUp(self):
        from thingq.active.core import repeatq
        self.qclass = repeatq


class TestAutoOrderQ(unittest.TestCase, AQMixin, AOrderQMixin):

    def setUp(self):
        from thingq.active.core import orderq
        self.qclass = orderq


class TestAutoRandomQ(unittest.TestCase, AQMixin, ARandomQMixin):

    def setUp(self):
        from thingq.active.core import randomq
        self.qclass = randomq


class TestAutoReduceQ(unittest.TestCase, AQMixin, AReduceQMixin):

    def setUp(self):
        from thingq.active.core import reduceq
        self.qclass = reduceq


class TestAutoMathQ(unittest.TestCase, AQMixin, AMathQMixin):

    def setUp(self):
        from thingq.active.core import mathq
        self.qclass = mathq


class TestAutoTruthQ(unittest.TestCase, AQMixin, ATruthQMixin):

    def setUp(self):
        from thingq.active.core import truthq
        self.qclass = truthq


if __name__ == '__main__':
    unittest.main()
