# -*- coding: utf-8 -*-
'''active knifes'''

from knife.base import OutputMixin
from knife.mixins import (
    RepeatMixin, MapMixin, SliceMixin, ReduceMixin, FilterMixin, MathMixin,
    CompareMixin, OrderMixin)

from knife._active import _OutputMixin
from knife._base import SLOTS, _KnifeMixin
from knife._mixins import (
    _RepeatMixin, _MapMixin, _SliceMixin, _ReduceMixin, _FilterMixin,
    _MathMixin, _CompareMixin, _OrderMixin)


class activeknife(
    _OutputMixin, _KnifeMixin, _CompareMixin, _FilterMixin, _MapMixin,
    _MathMixin, _OrderMixin, _ReduceMixin, _SliceMixin, _RepeatMixin,
    OutputMixin, FilterMixin, MapMixin, ReduceMixin, OrderMixin, RepeatMixin,
    MathMixin, SliceMixin, CompareMixin,
):

    '''active knife'''

    __slots__ = SLOTS


class compareknife(
    _OutputMixin, _KnifeMixin, OutputMixin, CompareMixin, _CompareMixin,
):

    '''comparing knife'''

    __slots__ = SLOTS


class filterknife(
    _OutputMixin, _KnifeMixin, OutputMixin, FilterMixin, _FilterMixin,
):

    '''filtering knife'''

    __slots__ = SLOTS


class mapknife(_OutputMixin, _KnifeMixin, OutputMixin, MapMixin, _MapMixin):

    '''mapping knife'''

    __slots__ = SLOTS


class mathknife(
    _OutputMixin, _KnifeMixin, OutputMixin, MathMixin, _MathMixin,
):

    '''mathing knife'''

    __slots__ = SLOTS


class orderknife(
    _OutputMixin, _KnifeMixin, OutputMixin, OrderMixin, _OrderMixin,
):

    '''ordering knife'''

    __slots__ = SLOTS


class reduceknife(
    _OutputMixin, _KnifeMixin, OutputMixin, ReduceMixin, _ReduceMixin,
):

    '''reducing knife'''

    __slots__ = SLOTS


class repeatknife(
    _OutputMixin, _KnifeMixin, OutputMixin, RepeatMixin, _RepeatMixin,
):

    '''repeating knife'''

    __slots__ = SLOTS


class sliceknife(
    _OutputMixin, _KnifeMixin, OutputMixin, SliceMixin, _SliceMixin,
):

    '''slicing knife'''

    __slots__ = SLOTS
