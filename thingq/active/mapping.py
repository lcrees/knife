# -*- coding: utf-8 -*-
'''thingq active mapping queues'''

from thingq.mixins import SLOTS
from thingq.mapping import DelayMixin, RepeatMixin, MappingMixin

from thingq.active.mixins import AutoResultMixin, ManResultMixin


class delayq(AutoResultMixin, DelayMixin):

    '''auto-balanced delayed map queue'''

    __slots__ = SLOTS


class mdelayq(ManResultMixin, DelayMixin):

    '''manually balanced delayed map queue'''

    __slots__ = SLOTS


class repeatq(AutoResultMixin, RepeatMixin):

    '''auto-balanced repeat queue'''

    __slots__ = SLOTS


class mrepeatq(ManResultMixin, RepeatMixin):

    '''manually balanced repeat queue'''

    __slots__ = SLOTS


class mapq(AutoResultMixin, MappingMixin):

    '''auto-balanced mapping queue'''

    __slots__ = SLOTS


class mmapq(ManResultMixin, MappingMixin):

    '''manually balanced mapping queue'''

    __slots__ = SLOTS
