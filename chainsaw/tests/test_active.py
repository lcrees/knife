# -*- coding: utf-8 -*-
'''active chainsaw tests'''

from chainsaw._compat import unittest

from chainsaw.tests.base import Mixin
from chainsaw.tests.map import MapMixin, RepeatMixin
from chainsaw.tests.reduce import ReduceMixin, SliceMixin
from chainsaw.tests.filter import FilterMixin, CollectMixin
from chainsaw.tests.analyze import OrderMixin, MathMixin, TruthMixin


class TestMain(
    unittest.TestCase, Mixin, FilterMixin, MapMixin, ReduceMixin, OrderMixin,
    SliceMixin, CollectMixin, RepeatMixin, MathMixin, TruthMixin
):

    def setUp(self):
        from chainsaw import activesaw
        self.qclass = activesaw.as_auto()
        self.mclass = activesaw.as_manual()


class TestFilter(unittest.TestCase, Mixin, FilterMixin):

    def setUp(self):
        self.maxDiff = None
        from chainsaw.active import filtersaw
        self.qclass = filtersaw.as_auto()
        self.mclass = filtersaw.as_manual()


class TestSlice(unittest.TestCase, Mixin, SliceMixin):

    def setUp(self):
        from chainsaw.active import slicesaw
        self.qclass = slicesaw.as_auto()
        self.mclass = slicesaw.as_manual()


class TestCollect(unittest.TestCase, Mixin, CollectMixin):

    def setUp(self):
        from chainsaw.active import collectsaw
        self.qclass = collectsaw.as_auto()
        self.mclass = collectsaw.as_manual()


class TestMap(unittest.TestCase, Mixin, MapMixin):

    def setUp(self):
        from chainsaw.active import mapsaw
        self.qclass = mapsaw.as_auto()
        self.mclass = mapsaw.as_manual()


class TestRepeat(unittest.TestCase, Mixin, RepeatMixin):

    def setUp(self):
        from chainsaw.active import repeatsaw
        self.qclass = repeatsaw.as_auto()
        self.mclass = repeatsaw.as_manual()


class TestOrder(unittest.TestCase, Mixin, OrderMixin):

    def setUp(self):
        from chainsaw.active import ordersaw
        self.qclass = ordersaw.as_auto()
        self.mclass = ordersaw.as_manual()


class TestReduce(unittest.TestCase, Mixin, ReduceMixin):

    def setUp(self):
        from chainsaw.active import reducesaw
        self.qclass = reducesaw.as_auto()
        self.mclass = reducesaw.as_manual()


class TestMath(unittest.TestCase, Mixin, MathMixin):

    def setUp(self):
        from chainsaw.active import mathsaw
        self.qclass = mathsaw.as_auto()
        self.mclass = mathsaw.as_manual()


class TestTruth(unittest.TestCase, Mixin, TruthMixin):

    def setUp(self):
        from chainsaw.active import truthsaw
        self.qclass = truthsaw.as_auto()
        self.mclass = truthsaw.as_manual()

if __name__ == '__main__':
    unittest.main()
