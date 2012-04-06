# -*- coding: utf-8 -*-
'''autotube tests'''

from tube.compat import unittest
from tube.tests.auto.mapping import *  # @UnusedWildImport
from tube.tests.auto.ordering import *  # @UnusedWildImport
from tube.tests.auto.reducing import *  # @UnusedWildImport
from tube.tests.auto.filtering import *  # @UnusedWildImport
from tube.tests.auto.transforming import *  # @UnusedWildImport
from tube.tests.auto.queuing import AQMixin


class TestAutoQ(
    unittest.TestCase, AQMixin, AFilterQMixin, AMapQMixin, AReduceQMixin,
    AOrderQMixin,
):

    def setUp(self):
        from tube import autotube
        self.qclass = autotube


class TestAutoFilterQ(unittest.TestCase, AQMixin, AFilterQMixin):

    def setUp(self):
        self.maxDiff = None
        from tube.active import filtertube
        self.qclass = filtertube


class TestAutoSliceQ(unittest.TestCase, AQMixin, ASliceQMixin):

    def setUp(self):
        from tube.active import slicetube
        self.qclass = slicetube


class TestAutoCollectQ(unittest.TestCase, AQMixin, ACollectQMixin):

    def setUp(self):
        self.maxDiff = None
        from tube.active import collecttube
        self.qclass = collecttube


class TestAutoSetQ(unittest.TestCase, AQMixin, ASetQMixin):

    def setUp(self):
        from tube.active import settube
        self.qclass = settube


class TestAutoMap(unittest.TestCase, AQMixin, AMapQMixin):

    def setUp(self):
        from tube.active import maptube
        self.qclass = maptube


class TestAutoRepeatQ(unittest.TestCase, AQMixin, ARepeatQMixin):

    def setUp(self):
        from tube.active import repeattube
        self.qclass = repeattube


class TestAutoOrderQ(unittest.TestCase, AQMixin, AOrderQMixin):

    def setUp(self):
        from tube.active import sorttube
        self.qclass = sorttube


class TestAutoRandomQ(unittest.TestCase, AQMixin, ARandomQMixin):

    def setUp(self):
        from tube.active import randomtube
        self.qclass = randomtube


class TestAutoReduceQ(unittest.TestCase, AQMixin, AReduceQMixin):

    def setUp(self):
        from tube.active import reducetube
        self.qclass = reducetube


class TestAutoMathQ(unittest.TestCase, AQMixin, AMathQMixin):

    def setUp(self):
        from tube.active import mathtube
        self.qclass = mathtube


class TestAutoTruthQ(unittest.TestCase, AQMixin, ATruthQMixin):

    def setUp(self):
        from tube.active import truthtube
        self.qclass = truthtube


class TestStringQ(unittest.TestCase, AQMixin, AStringQMixin):

    def setUp(self):
        from tube.active import stringtube
        self.qclass = stringtube


class TestTransformQ(unittest.TestCase, AQMixin, AStringQMixin):

    def setUp(self):
        from tube.active import transformtube
        self.qclass = transformtube


if __name__ == '__main__':
    unittest.main()
