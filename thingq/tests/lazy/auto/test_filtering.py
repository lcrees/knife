# -*- coding: utf-8 -*-

from thingq.support import unittest
#pylint: disable-msg=w0614,w0401
from thingq.tests.auto.filtering import *  # @UnusedWildImport
from thingq.tests.auto.queuing import AQMixin


class TestAutoFilterQ(unittest.TestCase, AQMixin, AFilterQMixin):

    def setUp(self):
        self.maxDiff = None
        from thingq.lazy.filtering import filterq
        self.qclass = filterq


class TestAutoSliceQ(unittest.TestCase, AQMixin, ASliceQMixin):

    def setUp(self):
        from thingq.lazy.filtering import sliceq
        self.qclass = sliceq


class TestAutoCollectQ(unittest.TestCase, AQMixin, ACollectQMixin):

    def setUp(self):
        self.maxDiff = None
        from thingq.lazy.filtering import collectq
        self.qclass = collectq


class TestAutoSetQ(unittest.TestCase, AQMixin, ASetQMixin):

    def setUp(self):
        from thingq.lazy.filtering import setq
        self.qclass = setq


if __name__ == '__main__':
    unittest.main()
