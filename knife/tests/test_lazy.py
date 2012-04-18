# -*- coding: utf-8 -*-
'''lazy knife tests'''

from knife._compat import unittest

from knife.tests.mixins import (
    Mixin, MapMixin, RepeatMixin, ReduceMixin, SliceMixin, FilterMixin,
    OrderMixin, MathMixin, CompareMixin)


class TestLazy(
    unittest.TestCase, Mixin, CompareMixin, MapMixin, ReduceMixin, OrderMixin,
    SliceMixin, RepeatMixin, MathMixin, FilterMixin
):

    def setUp(self):
        from knife import lazyknife
        self.mclass = lazyknife


class TestCompare(unittest.TestCase, Mixin, CompareMixin):

    def setUp(self):
        from knife.lazy import compareknife
        self.mclass = compareknife


class TestFilter(unittest.TestCase, Mixin, FilterMixin):

    def setUp(self):
        self.maxDiff = None
        from knife.lazy import filterknife
        self.mclass = filterknife


class TestMap(unittest.TestCase, Mixin, MapMixin):

    def setUp(self):
        from knife.lazy import mapknife
        self.mclass = mapknife


class TestMath(unittest.TestCase, Mixin, MathMixin):

    def setUp(self):
        from knife.lazy import mathknife
        self.mclass = mathknife


class TestOrder(unittest.TestCase, Mixin, OrderMixin):

    def setUp(self):
        from knife.lazy import orderknife
        self.mclass = orderknife


class TestRepeat(unittest.TestCase, Mixin, RepeatMixin):

    def setUp(self):
        from knife.lazy import repeatknife
        self.mclass = repeatknife


class TestReduce(unittest.TestCase, Mixin, ReduceMixin):

    def setUp(self):
        from knife.lazy import reduceknife
        self.mclass = reduceknife


class TestSlice(unittest.TestCase, Mixin, SliceMixin):

    def setUp(self):
        from knife.lazy import sliceknife
        self.mclass = sliceknife


if __name__ == '__main__':
    unittest.main()
