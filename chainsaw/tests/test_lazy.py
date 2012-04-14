# -*- coding: utf-8 -*-
'''lazy chainsaw tests'''

from chainsaw._compat import unittest

from chainsaw.tests.base import Mixin
from chainsaw.tests.map import MapMixin, RepeatMixin
from chainsaw.tests.reduce import ReduceMixin, SliceMixin, FilterMixin
from chainsaw.tests.analyze import OrderMixin, MathMixin, CompareMixin


class TestLazy(
    unittest.TestCase, Mixin, CompareMixin, MapMixin, ReduceMixin, OrderMixin,
    SliceMixin, RepeatMixin, MathMixin, FilterMixin
):

    def setUp(self):
        from chainsaw import lazysaw
        self.qclass = lazysaw.as_auto()
        self.mclass = lazysaw.as_manual()


class TestCompare(unittest.TestCase, Mixin, CompareMixin):

    def setUp(self):
        from chainsaw.lazy import comparesaw
        self.qclass = comparesaw.as_auto()
        self.mclass = comparesaw.as_manual()


class TestFilter(unittest.TestCase, Mixin, FilterMixin):

    def setUp(self):
        self.maxDiff = None
        from chainsaw.lazy import filtersaw
        self.qclass = filtersaw.as_auto()
        self.mclass = filtersaw.as_manual()


class TestMap(unittest.TestCase, Mixin, MapMixin):

    def setUp(self):
        from chainsaw.lazy import mapsaw
        self.qclass = mapsaw.as_auto()
        self.mclass = mapsaw.as_manual()


class TestMath(unittest.TestCase, Mixin, MathMixin):

    def setUp(self):
        from chainsaw.lazy import mathsaw
        self.qclass = mathsaw.as_auto()
        self.mclass = mathsaw.as_manual()


class TestOrder(unittest.TestCase, Mixin, OrderMixin):

    def setUp(self):
        from chainsaw.lazy import ordersaw
        self.qclass = ordersaw.as_auto()
        self.mclass = ordersaw.as_manual()


class TestRepeat(unittest.TestCase, Mixin, RepeatMixin):

    def setUp(self):
        from chainsaw.lazy import repeatsaw
        self.qclass = repeatsaw.as_auto()
        self.mclass = repeatsaw.as_manual()


class TestReduce(unittest.TestCase, Mixin, ReduceMixin):

    def setUp(self):
        from chainsaw.lazy import reducesaw
        self.qclass = reducesaw.as_auto()
        self.mclass = reducesaw.as_manual()


class TestSlice(unittest.TestCase, Mixin, SliceMixin):

    def setUp(self):
        from chainsaw.lazy import slicesaw
        self.qclass = slicesaw.as_auto()
        self.mclass = slicesaw.as_manual()


if __name__ == '__main__':
    unittest.main()
