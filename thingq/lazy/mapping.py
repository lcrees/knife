# -*- coding: utf-8 -*-
'''thingq lazy mapping queues'''

from thingq.core import SLOTS
from thingq.mapping import DelayMixin, RepeatMixin, MappingMixin

from thingq.lazy.mixins import AutoResultMixin, ManResultMixin


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

    '''auto-balanced map queue'''

    __slots__ = SLOTS


class mmapq(ManResultMixin, MappingMixin):

    '''manually balanced map queue'''

    __slots__ = SLOTS
