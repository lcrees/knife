# -*- coding: utf-8 -*-
'''manq tests'''

from thingq.support import unittest
from thingq.tests.man.manning import Manning
from thingq.tests.man.queuing import MQMixin
from thingq.tests.man.mapping import MMapQMixin
from thingq.tests.man.ordering import MOrderQMixin
from thingq.tests.man.reducing import MReduceQMixin
from thingq.tests.man.filtering import MFilterQMixin


class TestManQ(
    Manning, MQMixin, MFilterQMixin, MMapQMixin, MReduceQMixin, MOrderQMixin,
):

    def setUp(self):
        from thingq import manq
        self.qclass = manq


if __name__ == '__main__':
    unittest.main()
