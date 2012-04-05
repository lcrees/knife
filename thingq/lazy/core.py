# -*- coding: utf-8 -*-
'''thingq lazy queues'''

from thingq.mixins import SLOTS
from thingq.mapping import MappingMixin as MapMixin
from thingq.ordering import OrderingMixin as OrderMixin
from thingq.reducing import ReducingMixin as ReduceMixin
from thingq.filtering import FilteringMixin as FilterMixin

from thingq.lazy.mixins import AutoResultMixin, ManResultMixin


class autoq(AutoResultMixin, FilterMixin, MapMixin, ReduceMixin, OrderMixin):

    '''auto-balancing manipulation queue'''

    __slots__ = SLOTS


class manq(ManResultMixin, FilterMixin, MapMixin, ReduceMixin, OrderMixin):

    '''manually balanced manipulation queue'''

    __slots__ = SLOTS


lazyq = autoq
