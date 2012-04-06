# -*- coding: utf-8 -*-
'''autopipe tests'''

from thingpipe.compat import unittest
from thingpipe.tests.auto.mapping import *  # @UnusedWildImport
from thingpipe.tests.auto.ordering import *  # @UnusedWildImport
from thingpipe.tests.auto.reducing import *  # @UnusedWildImport
from thingpipe.tests.auto.filtering import *  # @UnusedWildImport
from thingpipe.tests.auto.transforming import *  # @UnusedWildImport
from thingpipe.tests.auto.queuing import AQMixin


class TestAutoQ(
    unittest.TestCase, AQMixin, AFilterQMixin, AMapQMixin, AReduceQMixin,
    AOrderQMixin,
):

    def setUp(self):
        from thingpipe import autopipe
        self.qclass = autopipe


class TestAutoFilterQ(unittest.TestCase, AQMixin, AFilterQMixin):

    def setUp(self):
        self.maxDiff = None
        from thingpipe.active import filterpipe
        self.qclass = filterpipe


class TestAutoSliceQ(unittest.TestCase, AQMixin, ASliceQMixin):

    def setUp(self):
        from thingpipe.active import slicepipe
        self.qclass = slicepipe


class TestAutoCollectQ(unittest.TestCase, AQMixin, ACollectQMixin):

    def setUp(self):
        self.maxDiff = None
        from thingpipe.active import collectpipe
        self.qclass = collectpipe


class TestAutoSetQ(unittest.TestCase, AQMixin, ASetQMixin):

    def setUp(self):
        from thingpipe.active import setpipe
        self.qclass = setpipe


class TestAutoMap(unittest.TestCase, AQMixin, AMapQMixin):

    def setUp(self):
        from thingpipe.active import mappipe
        self.qclass = mappipe


class TestAutoRepeatQ(unittest.TestCase, AQMixin, ARepeatQMixin):

    def setUp(self):
        from thingpipe.active import repeatpipe
        self.qclass = repeatpipe


class TestAutoOrderQ(unittest.TestCase, AQMixin, AOrderQMixin):

    def setUp(self):
        from thingpipe.active import sortpipe
        self.qclass = sortpipe


class TestAutoRandomQ(unittest.TestCase, AQMixin, ARandomQMixin):

    def setUp(self):
        from thingpipe.active import randompipe
        self.qclass = randompipe


class TestAutoReduceQ(unittest.TestCase, AQMixin, AReduceQMixin):

    def setUp(self):
        from thingpipe.active import reducepipe
        self.qclass = reducepipe


class TestAutoMathQ(unittest.TestCase, AQMixin, AMathQMixin):

    def setUp(self):
        from thingpipe.active import mathpipe
        self.qclass = mathpipe


class TestAutoTruthQ(unittest.TestCase, AQMixin, ATruthQMixin):

    def setUp(self):
        from thingpipe.active import truthpipe
        self.qclass = truthpipe


class TestStringQ(unittest.TestCase, AQMixin, AStringQMixin):

    def setUp(self):
        from thingpipe.active import stringpipe
        self.qclass = stringpipe


class TestTransformQ(unittest.TestCase, AQMixin, AStringQMixin):

    def setUp(self):
        from thingpipe.active import transformpipe
        self.qclass = transformpipe


if __name__ == '__main__':
    unittest.main()
