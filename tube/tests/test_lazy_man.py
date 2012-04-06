# -*- coding: utf-8 -*-
'''mantube tests'''

from tube.compat import unittest

from tube.tests.man.mapping import *  # @UnusedWildImport
from tube.tests.man.ordering import *  # @UnusedWildImport
from tube.tests.man.reducing import *  # @UnusedWildImport
from tube.tests.man.filtering import *  # @UnusedWildImport
from tube.tests.man.transforming import *  # @UnusedWildImport
from tube.tests.man.manning import Manning
from tube.tests.man.queuing import MQMixin


class TestManQ(
    Manning, MQMixin, MFilterQMixin, MMapQMixin, MReduceQMixin, MOrderQMixin,
):

    def setUp(self):
        from tube.lazy import mantube
        self.qclass = mantube


class TestManFilterQ(Manning, MFilterQMixin):

    def setUp(self):
        self.maxDiff = None
        from tube.lazy import mfiltertube
        self.qclass = mfiltertube


class TestManSliceQ(Manning, MQMixin, MSliceQMixin):

    def setUp(self):
        from tube.lazy import mslicetube
        self.qclass = mslicetube


class TestManCollectQ(Manning, MQMixin, MCollectQMixin):

    def setUp(self):
        from tube.lazy import mcollecttube
        self.qclass = mcollecttube


class TestManSetQ(Manning, MQMixin, MSetQMixin):

    def setUp(self):
        from tube.lazy import msettube
        self.qclass = msettube


class TestManMap(Manning, MQMixin, MMapQMixin):

    def setUp(self):
        from tube.lazy import mmaptube
        self.qclass = mmaptube


class TestManRepeatQ(Manning, MQMixin, MRepeatQMixin):

    def setUp(self):
        from tube.lazy import mrepeattube
        self.qclass = mrepeattube


class TestManOrderQ(Manning, MQMixin, MOrderQMixin):

    def setUp(self):
        from tube.lazy import mordertube
        self.qclass = mordertube


class TestManRandomQ(Manning, MQMixin, MRandomQMixin):

    def setUp(self):
        from tube.lazy import mrandomtube
        self.qclass = mrandomtube


class TestManReduceQ(Manning, MQMixin, MReduceQMixin):

    def setUp(self):
        from tube.lazy import mreducetube
        self.qclass = mreducetube


class TestManMathQ(Manning, MQMixin, MMathQMixin):

    def setUp(self):
        from tube.lazy import mmathtube
        self.qclass = mmathtube


class TestManTruthQ(Manning, MQMixin, MTruthQMixin):

    def setUp(self):
        from tube.lazy import mtruthtube
        self.qclass = mtruthtube


class TestStringQ(Manning, MQMixin, MStringQMixin):

    def setUp(self):
        from tube.active import stringtube
        self.qclass = stringtube


class TestTransformQ(Manning, MQMixin, MStringQMixin):

    def setUp(self):
        from tube.active import transformtube
        self.qclass = transformtube

if __name__ == '__main__':
    unittest.main()
