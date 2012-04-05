# -*- coding: utf-8 -*-
'''autoq tests'''

from thingq.support import unittest
from thingq.tests.auto.queuing import AQMixin
from thingq.tests.auto.mapping import AMapQMixin
from thingq.tests.auto.ordering import AOrderQMixin
from thingq.tests.auto.reducing import AReduceQMixin
from thingq.tests.auto.filtering import AFilterQMixin


class TestAutoQ(
    unittest.TestCase, AQMixin, AFilterQMixin, AMapQMixin, AReduceQMixin,
    AOrderQMixin,
):

    def setUp(self):
        from thingq.lazy.core import autoq
        self.qclass = autoq


if __name__ == '__main__':
    unittest.main()
