# -*- coding: utf-8 -*-
'''automatically balanced active chainsaw tests'''

from chainsaw.compat import unittest
from chainsaw.tests.auto.map import *  # @UnusedWildImport
from chainsaw.tests.auto.analyze import *  # @UnusedWildImport
from chainsaw.tests.auto.reduce import *  # @UnusedWildImport
from chainsaw.tests.auto.filter import *  # @UnusedWildImport
from chainsaw.tests.auto.base import AMixin


class TestAuto(
    unittest.TestCase, AMixin, AFilterMixin, AMapMixin, AReduceMixin,
    AOrderMixin,
):

    def setUp(self):
        from chainsaw import activechainsaw
        self.qclass = activechainsaw


class TestAutoFilter(unittest.TestCase, AMixin, AFilterMixin):

    def setUp(self):
        self.maxDiff = None
        from chainsaw.active import filterchainsaw
        self.qclass = filterchainsaw


class TestAutoSlice(unittest.TestCase, AMixin, ASliceMixin):

    def setUp(self):
        from chainsaw.active import slicechainsaw
        self.qclass = slicechainsaw


class TestAutoCollect(unittest.TestCase, AMixin, ACollectMixin):

    def setUp(self):
        self.maxDiff = None
        from chainsaw.active import collectchainsaw
        self.qclass = collectchainsaw


class TestAutoMap(unittest.TestCase, AMixin, AMapMixin):

    def setUp(self):
        from chainsaw.active import mapchainsaw
        self.qclass = mapchainsaw


class TestAutoRepeat(unittest.TestCase, AMixin, ARepeatMixin):

    def setUp(self):
        from chainsaw.active import repeatchainsaw
        self.qclass = repeatchainsaw


class TestAutoOrder(unittest.TestCase, AMixin, AOrderMixin):

    def setUp(self):
        from chainsaw.active import orderchainsaw
        self.qclass = orderchainsaw


class TestAutoReduce(unittest.TestCase, AMixin, AReduceMixin):

    def setUp(self):
        from chainsaw.active import reducechainsaw
        self.qclass = reducechainsaw


class TestAutoMath(unittest.TestCase, AMixin, AMathMixin):

    def setUp(self):
        from chainsaw.active import mathchainsaw
        self.qclass = mathchainsaw


class TestAutoTruth(unittest.TestCase, AMixin, ATruthMixin):

    def setUp(self):
        from chainsaw.active import truthchainsaw
        self.qclass = truthchainsaw


if __name__ == '__main__':
    unittest.main()
