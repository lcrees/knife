# -*- coding: utf-8 -*-
'''active chainsaw tests'''

from chainsaw._compat import unittest

from chainsaw.tests.base import Mixin
from chainsaw.tests.map import MapMixin, RepeatMixin
from chainsaw.tests.reduce import ReduceMixin, SliceMixin, FilterMixin
from chainsaw.tests.analyze import OrderMixin, NumberMixin, CompareMixin


class TestMain(
    unittest.TestCase, Mixin, FilterMixin, MapMixin, ReduceMixin, OrderMixin,
    SliceMixin, RepeatMixin, NumberMixin, CompareMixin
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


class TestMath(unittest.TestCase, Mixin, NumberMixin):

    def setUp(self):
        from chainsaw.active import numbersaw
        self.qclass = numbersaw.as_auto()
        self.mclass = numbersaw.as_manual()


class TestCompare(unittest.TestCase, Mixin, CompareMixin):

    def setUp(self):
        from chainsaw.active import comparesaw
        self.qclass = comparesaw.as_auto()
        self.mclass = comparesaw.as_manual()

if __name__ == '__main__':
    unittest.main()
