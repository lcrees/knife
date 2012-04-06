# -*- coding: utf-8 -*-
'''thingq lazy queues'''

from thingq.mixins import SLOTS
from thingq.mapping import RepeatMixin, MapMixin
from thingq.ordering import RandomMixin, OrderMixin
from thingq.lazy.mixins import AutoResultMixin, ManResultMixin
from thingq.reducing import MathMixin, TruthMixin, ReduceMixin
from thingq.filtering import FilterMixin, CollectMixin, SetMixin, SliceMixin


class autoq(
    AutoResultMixin, FilterMixin, MapMixin, ReduceMixin, OrderMixin,
    CollectMixin, SetMixin, SliceMixin, TruthMixin, MathMixin, RepeatMixin,
    RandomMixin,
):

    '''auto-balancing manipulation queue'''

    __slots__ = SLOTS


class manq(
    ManResultMixin, FilterMixin, MapMixin, ReduceMixin, OrderMixin,
    CollectMixin, SetMixin, SliceMixin, TruthMixin, MathMixin, RepeatMixin,
    RandomMixin,
):

    '''manually balanced manipulation queue'''

    __slots__ = SLOTS


class collectq(AutoResultMixin, CollectMixin):

    '''auto-balanced collecting queue'''

    __slots__ = SLOTS


class mcollectq(ManResultMixin, CollectMixin):

    '''manually balanced collecting queue'''

    __slots__ = SLOTS


class setq(AutoResultMixin, SetMixin):

    '''auto-balanced set queue'''

    __slots__ = SLOTS


class msetq(ManResultMixin, SetMixin):

    '''manually balanced set queue'''

    __slots__ = SLOTS


class sliceq(AutoResultMixin, SliceMixin):

    '''auto-balanced slice queue'''

    __slots__ = SLOTS


class msliceq(ManResultMixin, SliceMixin):

    '''manually balanced slice queue'''

    __slots__ = SLOTS


class filterq(AutoResultMixin, FilterMixin):

    '''auto-balanced filter queue'''

    __slots__ = SLOTS


class mfilterq(ManResultMixin, FilterMixin):

    '''manually balanced filtering queue'''

    __slots__ = SLOTS


class repeatq(AutoResultMixin, RepeatMixin):

    '''auto-balanced repeat queue'''

    __slots__ = SLOTS


class mrepeatq(ManResultMixin, RepeatMixin):

    '''manually balanced repeat queue'''

    __slots__ = SLOTS


class mapq(AutoResultMixin, MapMixin):

    '''auto-balanced map queue'''

    __slots__ = SLOTS


class mmapq(ManResultMixin, MapMixin):

    '''manually balanced map queue'''

    __slots__ = SLOTS


class randomq(AutoResultMixin, RandomMixin):

    '''auto-balanced random queue'''

    __slots__ = SLOTS


class mrandomq(ManResultMixin, RandomMixin):

    '''manually balanced random queue'''

    __slots__ = SLOTS


class orderq(AutoResultMixin, OrderMixin):

    '''auto-balanced order queue'''

    __slots__ = SLOTS


class morderq(ManResultMixin, OrderMixin):

    '''manually balanced order queue'''

    __slots__ = SLOTS


class mathq(AutoResultMixin, MathMixin):

    '''auto-balancing math queue'''

    __slots__ = SLOTS


class mmathq(ManResultMixin, MathMixin):

    '''manually balanced math queue'''

    __slots__ = SLOTS


class truthq(AutoResultMixin, TruthMixin):

    '''auto-balancing truth queue'''

    __slots__ = SLOTS


class mtruthq(ManResultMixin, TruthMixin):

    '''manually balanced truth queue'''

    __slots__ = SLOTS


class reduceq(AutoResultMixin, ReduceMixin):

    '''auto-balancing reduce queue'''

    __slots__ = SLOTS


class mreduceq(ManResultMixin, ReduceMixin):

    '''manually balanced reduce queue'''

    __slots__ = SLOTS
