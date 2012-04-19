# -*- coding: utf-8 -*-
'''active knifes'''

from knife.base import OutMixin
from knife.mixins import (
    RepeatMixin, MapMixin, SliceMixin, ReduceMixin, FilterMixin, MathMixin,
    CmpMixin, OrderMixin)

from knife._active import _OutMixin
from knife._base import SLOTS, _KnifeMixin
from knife._mixins import (
    _RepeatMixin, _MapMixin, _SliceMixin, _ReduceMixin, _FilterMixin,
    _MathMixin, _CmpMixin, _OrderMixin)


class activeknife(
    _OutMixin, _KnifeMixin, _CmpMixin, _FilterMixin, _MapMixin,
    _MathMixin, _OrderMixin, _ReduceMixin, _SliceMixin, _RepeatMixin,
    OutMixin, FilterMixin, MapMixin, ReduceMixin, OrderMixin, RepeatMixin,
    MathMixin, SliceMixin, CmpMixin,
):

    '''active knife'''

    __slots__ = SLOTS


class cmpknife(_OutMixin, _KnifeMixin, OutMixin, CmpMixin, _CmpMixin):

    '''comparing knife'''

    __slots__ = SLOTS


class filterknife(_OutMixin, _KnifeMixin, OutMixin, FilterMixin, _FilterMixin):

    '''filtering knife'''

    __slots__ = SLOTS


class mapknife(_OutMixin, _KnifeMixin, OutMixin, MapMixin, _MapMixin):

    '''mapping knife'''

    __slots__ = SLOTS


class mathknife(_OutMixin, _KnifeMixin, OutMixin, MathMixin, _MathMixin):

    '''mathing knife'''

    __slots__ = SLOTS


class orderknife(_OutMixin, _KnifeMixin, OutMixin, OrderMixin, _OrderMixin):

    '''ordering knife'''

    __slots__ = SLOTS


class reduceknife(_OutMixin, _KnifeMixin, OutMixin, ReduceMixin, _ReduceMixin):

    '''reducing knife'''

    __slots__ = SLOTS


class repeatknife(_OutMixin, _KnifeMixin, OutMixin, RepeatMixin, _RepeatMixin):

    '''repeating knife'''

    __slots__ = SLOTS


class sliceknife(_OutMixin, _KnifeMixin, OutMixin, SliceMixin, _SliceMixin):

    '''slicing knife'''

    __slots__ = SLOTS
