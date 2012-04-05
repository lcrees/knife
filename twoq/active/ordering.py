# -*- coding: utf-8 -*-
'''twoq active ordering queues'''

from twoq.core import SLOTS
from twoq.ordering import RandomMixin, OrderingMixin

from twoq.active.mixins import AutoResultMixin, ManResultMixin


class randomq(AutoResultMixin, RandomMixin):

    '''auto-balanced randomizing queue'''

    __slots__ = SLOTS


class mrandomq(ManResultMixin, RandomMixin):

    '''manually balanced randomizing queue'''

    __slots__ = SLOTS


class orderq(AutoResultMixin, OrderingMixin):

    '''auto-balanced ordering queue'''

    __slots__ = SLOTS


class morderq(ManResultMixin, OrderingMixin):

    '''manually balanced order queue'''

    __slots__ = SLOTS
