# -*- coding: utf-8 -*-
'''thingq active queues'''

from thingq.core import SLOTS
from thingq.mapping import MappingMixin as MapMixin
from thingq.ordering import OrderingMixin as OrderMixin
from thingq.reducing import ReducingMixin as ReduceMixin
from thingq.filtering import FilteringMixin as FilterMixin

from thingq.active.mixins import AutoResultMixin, ManResultMixin


class autoq(AutoResultMixin, FilterMixin, MapMixin, ReduceMixin, OrderMixin):

    '''auto-balancing manipulation queue'''

    __slots__ = SLOTS


class manq(ManResultMixin, FilterMixin, MapMixin, ReduceMixin, OrderMixin):

    '''manually balanced manipulation queue'''

    __slots__ = SLOTS
