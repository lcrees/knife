# -*- coding: utf-8 -*-
'''thingq lazy reducing queues'''

from thingq.mixins import SLOTS
from thingq.reducing import MathMixin, TruthMixin, ReducingMixin

from thingq.lazy.mixins import AutoResultMixin, ManResultMixin


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


class reduceq(AutoResultMixin, ReducingMixin):

    '''auto-balancing reduce queue'''

    __slots__ = SLOTS


class mreduceq(ManResultMixin, ReducingMixin):

    '''manually balanced reduce queue'''

    __slots__ = SLOTS
