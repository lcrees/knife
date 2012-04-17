# -*- coding: utf-8 -*-
'''lazy chainsaw tests'''

from chainsaw._compat import unittest

from chainsaw.tests.mixins import (
    Mixin, MapMixin, RepeatMixin, ReduceMixin, SliceMixin, FilterMixin,
    OrderMixin, MathMixin, CompareMixin)


class TestLazy(
    unittest.TestCase, Mixin, CompareMixin, MapMixin, ReduceMixin, OrderMixin,
    SliceMixin, RepeatMixin, MathMixin, FilterMixin
):

    def setUp(self):
        from chainsaw import lazysaw
        self.mclass = lazysaw


class TestCompare(unittest.TestCase, Mixin, CompareMixin):

    def setUp(self):
        from chainsaw.lazy import comparesaw
        self.mclass = comparesaw


class TestFilter(unittest.TestCase, Mixin, FilterMixin):

    def setUp(self):
        self.maxDiff = None
        from chainsaw.lazy import filtersaw
        self.mclass = filtersaw


class TestMap(unittest.TestCase, Mixin, MapMixin):

    def setUp(self):
        from chainsaw.lazy import mapsaw
        self.mclass = mapsaw


class TestMath(unittest.TestCase, Mixin, MathMixin):

    def setUp(self):
        from chainsaw.lazy import mathsaw
        self.mclass = mathsaw


class TestOrder(unittest.TestCase, Mixin, OrderMixin):

    def setUp(self):
        from chainsaw.lazy import ordersaw
        self.mclass = ordersaw


class TestRepeat(unittest.TestCase, Mixin, RepeatMixin):

    def setUp(self):
        from chainsaw.lazy import repeatsaw
        self.mclass = repeatsaw


class TestReduce(unittest.TestCase, Mixin, ReduceMixin):

    def setUp(self):
        from chainsaw.lazy import reducesaw
        self.mclass = reducesaw


class TestSlice(unittest.TestCase, Mixin, SliceMixin):

    def setUp(self):
        from chainsaw.lazy import slicesaw
        self.mclass = slicesaw


if __name__ == '__main__':
    unittest.main()
