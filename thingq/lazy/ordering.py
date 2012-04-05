# -*- coding: utf-8 -*-
'''thingq lazy ordering queues'''

from thingq.mixins import SLOTS
from thingq.ordering import RandomMixin, OrderingMixin

from thingq.lazy.mixins import AutoResultMixin, ManResultMixin


class randomq(AutoResultMixin, RandomMixin):

    '''auto-balanced random queue'''

    __slots__ = SLOTS


class mrandomq(ManResultMixin, RandomMixin):

    '''manually balanced random queue'''

    __slots__ = SLOTS


class orderq(AutoResultMixin, OrderingMixin):

    '''auto-balanced order queue'''

    __slots__ = SLOTS


class morderq(ManResultMixin, OrderingMixin):

    '''manually balanced order queue'''

    __slots__ = SLOTS
