# -*- coding: utf-8 -*-
'''active chainsaws'''

from chainsaw.base import OutputMixin
from chainsaw.mixins import (
    RepeatMixin, MapMixin, SliceMixin, ReduceMixin, FilterMixin, MathMixin,
    CompareMixin, OrderMixin)

from chainsaw._active import _OutMixin
from chainsaw._base import SLOTS, _ChainsawMixin
from chainsaw._mixins import (
    _RepeatMixin, _MapMixin, _SliceMixin, _ReduceMixin, _FilterMixin,
    _MathMixin, _CompareMixin, _OrderMixin)


class activesaw(
    _OutMixin, _ChainsawMixin, _CompareMixin, _FilterMixin, _MapMixin,
    _MathMixin, _OrderMixin, _ReduceMixin, _SliceMixin, _RepeatMixin,
    OutputMixin, FilterMixin, MapMixin, ReduceMixin, OrderMixin, RepeatMixin,
    MathMixin, SliceMixin, CompareMixin,
):

    '''active chainsaw'''

    __slots__ = SLOTS


class comparesaw(
    _OutMixin, _ChainsawMixin, OutputMixin, CompareMixin, _CompareMixin,
):

    '''comparing chainsaw'''

    __slots__ = SLOTS


class filtersaw(
    _OutMixin, _ChainsawMixin, OutputMixin, FilterMixin, _FilterMixin,
):

    '''filtering chainsaw'''

    __slots__ = SLOTS


class mapsaw(_OutMixin, _ChainsawMixin, OutputMixin, MapMixin, _MapMixin):

    '''mapping chainsaw'''

    __slots__ = SLOTS


class mathsaw(
    _OutMixin, _ChainsawMixin, OutputMixin, MathMixin, _MathMixin,
):

    '''mathing chainsaw'''

    __slots__ = SLOTS


class ordersaw(
    _OutMixin, _ChainsawMixin, OutputMixin, OrderMixin, _OrderMixin,
):

    '''ordering chainsaw'''

    __slots__ = SLOTS


class reducesaw(
    _OutMixin, _ChainsawMixin, OutputMixin, ReduceMixin, _ReduceMixin,
):

    '''reducing chainsaw'''

    __slots__ = SLOTS


class repeatsaw(
    _OutMixin, _ChainsawMixin, OutputMixin, RepeatMixin, _RepeatMixin,
):

    '''repeating chainsaw'''

    __slots__ = SLOTS


class slicesaw(
    _OutMixin, _ChainsawMixin, OutputMixin, SliceMixin, _SliceMixin,
):

    '''slicing chainsaw'''

    __slots__ = SLOTS
