# -*- coding: utf-8 -*-
'''Actively evaluated knives'''

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

    '''
    Actively evaluated combo knife.

    Combines features from every other :mod:`knife` knife.
    '''

    __slots__ = SLOTS


class cmpknife(_OutMixin, _KnifeMixin, OutMixin, CmpMixin, _CmpMixin):

    '''
    Actively evaluated comparing knife.

    Comparison operations for incoming things.
    '''

    __slots__ = SLOTS


class filterknife(_OutMixin, _KnifeMixin, OutMixin, FilterMixin, _FilterMixin):

    '''
    Actively evaluated filtering knife.

    Filtering operations for incoming things.
    '''

    __slots__ = SLOTS


class mapknife(_OutMixin, _KnifeMixin, OutMixin, MapMixin, _MapMixin):

    '''
    Actively evaluated mapping knife.

    `Map <http://docs.python.org/library/functions.html#map>`_ operations for incoming
    things.
    '''

    __slots__ = SLOTS


class mathknife(_OutMixin, _KnifeMixin, OutMixin, MathMixin, _MathMixin):

    '''
    Actively evaluated mathing knife.

    Numeric and statistical operations for incoming things.
    '''

    __slots__ = SLOTS


class orderknife(_OutMixin, _KnifeMixin, OutMixin, OrderMixin, _OrderMixin):

    '''
    Actively evaluated ordering knife.

    Sorting and grouping operations for incoming things.
    '''

    __slots__ = SLOTS


class reduceknife(_OutMixin, _KnifeMixin, OutMixin, ReduceMixin, _ReduceMixin):

    '''
    Actively evaluated reducing knife.

    `Reducing operations <http://docs.python.org/library/functions.html#map>`_ for
    incoming things.
    '''

    __slots__ = SLOTS


class repeatknife(_OutMixin, _KnifeMixin, OutMixin, RepeatMixin, _RepeatMixin):

    '''
    Actively evaluated repeating knife.

    `Repetition <http://docs.python.org/library/functions.html#reduce>`_ operations
    for incoming things.
    '''

    __slots__ = SLOTS


class sliceknife(_OutMixin, _KnifeMixin, OutMixin, SliceMixin, _SliceMixin):

    '''
    Actively evaluated slicing knife.

    `Slicing operations <http://docs.python.org/library/functions.html#slice>`_ for
    incoming things.
    '''

    __slots__ = SLOTS
