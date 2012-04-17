# -*- coding: utf-8 -*-
'''lazily evaluated chainsaws'''

from chainsaw.base import OutputMixin
from chainsaw.mixins import (
    RepeatMixin, MapMixin, SliceMixin, ReduceMixin, FilterMixin, MathMixin,
    CompareMixin, OrderMixin)

from chainsaw._lazy import _OutputMixin
from chainsaw._base import SLOTS, _ChainsawMixin
from chainsaw._mixins import (
    _RepeatMixin, _MapMixin, _SliceMixin, _ReduceMixin, _FilterMixin,
    _MathMixin, _CompareMixin, _OrderMixin)


class lazysaw(
    _OutputMixin, _ChainsawMixin, _CompareMixin, _FilterMixin, _MapMixin,
    _MathMixin, _OrderMixin, _ReduceMixin, _SliceMixin, _RepeatMixin,
    OutputMixin, FilterMixin, MapMixin, ReduceMixin, OrderMixin, RepeatMixin,
    MathMixin, SliceMixin, CompareMixin,
):

    '''lazy chainsaw'''

    __slots__ = SLOTS


class comparesaw(
    _OutputMixin, _ChainsawMixin, OutputMixin, CompareMixin, _CompareMixin,
):

    '''comparing chainsaw'''

    __slots__ = SLOTS


class filtersaw(
    _OutputMixin, _ChainsawMixin, OutputMixin, FilterMixin, _FilterMixin,
):

    '''filtering chainsaw'''

    __slots__ = SLOTS


class mapsaw(_OutputMixin, _ChainsawMixin, OutputMixin, MapMixin, _MapMixin):

    '''mapping chainsaw'''

    __slots__ = SLOTS


class mathsaw(
    _OutputMixin, _ChainsawMixin, OutputMixin, MathMixin, _MathMixin,
):

    '''mathing chainsaw'''

    __slots__ = SLOTS


class ordersaw(
    _OutputMixin, _ChainsawMixin, OutputMixin, OrderMixin, _OrderMixin,
):

    '''ordering chainsaw'''

    __slots__ = SLOTS


class reducesaw(
    _OutputMixin, _ChainsawMixin, OutputMixin, ReduceMixin, _ReduceMixin,
):

    '''reducing chainsaw'''

    __slots__ = SLOTS


class repeatsaw(
    _OutputMixin, _ChainsawMixin, OutputMixin, RepeatMixin, _RepeatMixin,
):

    '''repeating chainsaw'''

    __slots__ = SLOTS


class slicesaw(
    _OutputMixin, _ChainsawMixin, OutputMixin, SliceMixin, _SliceMixin,
):

    '''slicing chainsaw'''

    __slots__ = SLOTS
