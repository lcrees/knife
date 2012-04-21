# -*- coding: utf-8 -*-
'''Lazily evaluated knives.'''

from knife.base import OutMixin
from knife.mixins import (
    RepeatMixin, MapMixin, SliceMixin, ReduceMixin, FilterMixin, MathMixin,
    CmpMixin, OrderMixin)

from knife._lazy import _OutMixin
from knife._base import SLOTS, _KnifeMixin
from knife._mixins import (
    _RepeatMixin, _MapMixin, _SliceMixin, _ReduceMixin, _FilterMixin,
    _MathMixin, _CmpMixin, _OrderMixin)


class lazyknife(
    _OutMixin, _KnifeMixin, _CmpMixin, _FilterMixin, _MapMixin,
    _MathMixin, _OrderMixin, _ReduceMixin, _SliceMixin, _RepeatMixin,
    OutMixin, FilterMixin, MapMixin, ReduceMixin, OrderMixin, RepeatMixin,
    MathMixin, SliceMixin, CmpMixin,
):

    '''
    Lazily evaluated combo knife.

    Combines features from every other :mod:`knife` knife.
    '''

    __slots__ = SLOTS


class cmpknife(_OutMixin, _KnifeMixin, OutMixin, CmpMixin, _CmpMixin):

    '''
    Lazily evaluated comparing knife.

    Comparison operations for incoming things.
    '''

    __slots__ = SLOTS


class filterknife(_OutMixin, _KnifeMixin, OutMixin, FilterMixin, _FilterMixin):

    '''Lazily evaluated filtering knife.'''

    __slots__ = SLOTS


class mapknife(_OutMixin, _KnifeMixin, OutMixin, MapMixin, _MapMixin):

    '''
    Lazily evaluated mapping knife.

    Filtering operations for incoming things.
    '''

    __slots__ = SLOTS


class mathknife(_OutMixin, _KnifeMixin, OutMixin, MathMixin, _MathMixin):

    '''
    Lazily evaluated mathing knife.

    Numeric and statistical operations on incoming things.
    '''

    __slots__ = SLOTS


class orderknife(_OutMixin, _KnifeMixin, OutMixin, OrderMixin, _OrderMixin):

    '''
    Lazily evaluated ordering knife.

    Sorting and grouping operations for incoming things.
    '''

    __slots__ = SLOTS


class reduceknife(_OutMixin, _KnifeMixin, OutMixin, ReduceMixin, _ReduceMixin):

    '''
    Lazily evaluated reducing knife.

    `Reducing operations <http://docs.python.org/library/functions.html#map>`_
    for incoming things.
    '''

    __slots__ = SLOTS


class repeatknife(_OutMixin, _KnifeMixin, OutMixin, RepeatMixin, _RepeatMixin):

    '''
    Lazily evaluated repeating knife.

    `Repetition <http://docs.python.org/library/functions.html#reduce>`_
    operations for incoming things.
    '''

    __slots__ = SLOTS


class sliceknife(_OutMixin, _KnifeMixin, OutMixin, SliceMixin, _SliceMixin):

    '''
    Lazily evaluated slicing knife.

    `Slicing operations <http://docs.python.org/library/functions.html#slice>`_
    for incoming things.
    '''

    __slots__ = SLOTS
