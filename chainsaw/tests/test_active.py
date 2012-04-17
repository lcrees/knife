# -*- coding: utf-8 -*-
'''active chainsaw tests'''

from chainsaw._compat import unittest

from chainsaw.tests.mixins import (
    Mixin, MapMixin, RepeatMixin, ReduceMixin, SliceMixin, FilterMixin,
    OrderMixin, MathMixin, CompareMixin)


class TestActive(
    unittest.TestCase, Mixin, FilterMixin, MapMixin, ReduceMixin, OrderMixin,
    SliceMixin, RepeatMixin, MathMixin, CompareMixin
):

    def setUp(self):
        from chainsaw import activesaw
        self.mclass = activesaw


class TestCompare(unittest.TestCase, Mixin, CompareMixin):

    def setUp(self):
        from chainsaw.active import comparesaw
        self.mclass = comparesaw


class TestFilter(unittest.TestCase, Mixin, FilterMixin):

    def setUp(self):
        self.maxDiff = None
        from chainsaw.active import filtersaw
        self.mclass = filtersaw


class TestMap(unittest.TestCase, Mixin, MapMixin):

    def setUp(self):
        from chainsaw.active import mapsaw
        self.mclass = mapsaw


class TestMath(unittest.TestCase, Mixin, MathMixin):

    def setUp(self):
        from chainsaw.active import mathsaw
        self.mclass = mathsaw


class TestOrder(unittest.TestCase, Mixin, OrderMixin):

    def setUp(self):
        from chainsaw.active import ordersaw
        self.mclass = ordersaw


class TestReduce(unittest.TestCase, Mixin, ReduceMixin):

    def setUp(self):
        from chainsaw.active import reducesaw
        self.mclass = reducesaw


class TestRepeat(unittest.TestCase, Mixin, RepeatMixin):

    def setUp(self):
        from chainsaw.active import repeatsaw
        self.mclass = repeatsaw


class TestSlice(unittest.TestCase, Mixin, SliceMixin):

    def setUp(self):
        from chainsaw.active import slicesaw
        self.mclass = slicesaw


if __name__ == '__main__':
    unittest.main()
