# -*- coding: utf-8 -*-
'''active chainsaw tests'''

from chainsaw.compat import unittest

from chainsaw.tests.map import *  # @UnusedWildImport
from chainsaw.tests.reduce import *  # @UnusedWildImport
from chainsaw.tests.filter import *  # @UnusedWildImport
from chainsaw.tests.analyze import *  # @UnusedWildImport
from chainsaw.tests.base import Mixin


class TestMain(
    Mixin, FilterMixin, MapMixin, ReduceMixin, OrderMixin,
    SliceMixin, CollectMixin, RepeatMixin, MathMixin, TruthMixin
):

    def setUp(self):
        from chainsaw import activechainsaw
        self.qclass = activechainsaw.as_auto()
        self.mclass = activechainsaw.as_manual()


class TestFilter(unittest.TestCase, Mixin, FilterMixin):

    def setUp(self):
        self.maxDiff = None
        from chainsaw.active import filterchainsaw
        self.qclass = filterchainsaw.as_auto()
        self.mclass = filterchainsaw.as_manual()


class TestSlice(unittest.TestCase, Mixin, SliceMixin):

    def setUp(self):
        from chainsaw.active import slicechainsaw
        self.qclass = slicechainsaw.as_auto()
        self.mclass = slicechainsaw.as_manual()


class TestCollect(unittest.TestCase, Mixin, CollectMixin):

    def setUp(self):
        from chainsaw.active import collectchainsaw
        self.qclass = collectchainsaw.as_auto()
        self.mclass = collectchainsaw.as_manual()


class TestMap(unittest.TestCase, Mixin, MapMixin):

    def setUp(self):
        from chainsaw.active import mapchainsaw
        self.qclass = mapchainsaw.as_auto()
        self.mclass = mapchainsaw.as_manual()


class TestRepeat(unittest.TestCase, Mixin, RepeatMixin):

    def setUp(self):
        from chainsaw.active import repeatchainsaw
        self.qclass = repeatchainsaw.as_auto()
        self.mclass = repeatchainsaw.as_manual()


class TestOrder(unittest.TestCase, Mixin, OrderMixin):

    def setUp(self):
        from chainsaw.active import orderchainsaw
        self.qclass = orderchainsaw.as_auto()
        self.mclass = orderchainsaw.as_manual()


class TestReduce(unittest.TestCase, Mixin, ReduceMixin):

    def setUp(self):
        from chainsaw.active import reducechainsaw
        self.qclass = reducechainsaw.as_auto()
        self.mclass = reducechainsaw.as_manual()


class TestMath(unittest.TestCase, Mixin, MathMixin):

    def setUp(self):
        from chainsaw.active import mathchainsaw
        self.qclass = mathchainsaw.as_auto()
        self.mclass = mathchainsaw.as_manual()


class TestTruth(unittest.TestCase, Mixin, TruthMixin):

    def setUp(self):
        from chainsaw.active import truthchainsaw
        self.qclass = truthchainsaw.as_auto()
        self.mclass = truthchainsaw.as_manual()

if __name__ == '__main__':
    unittest.main()
