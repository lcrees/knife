# -*- coding: utf-8 -*-
'''Lazier evaluated knives.'''

from knife.base import OutMixin
from knife.mixins import (
    RepeatMixin, MapMixin, SliceMixin, ReduceMixin, FilterMixin, MathMixin,
    CmpMixin, OrderMixin)

from knife import _lazy
from knife import _base
from knife import _mixins


class lazyknife(
    _lazy._OutMixin, _base._KnifeMixin, _mixins._CmpMixin,
    _mixins._FilterMixin, _mixins._MapMixin, _mixins._MathMixin,
    _mixins._OrderMixin, _mixins._ReduceMixin, _mixins._SliceMixin,
    _mixins._RepeatMixin,
    OutMixin, FilterMixin, MapMixin, ReduceMixin, OrderMixin, RepeatMixin,
    MathMixin, SliceMixin, CmpMixin,
):

    '''
    Lazier evaluated combo knife. Features every :mod:`knife` method.

    .. note::

      Also aliased as :class:`~knife.__` when imported from :mod:`knife`.

    >>> from knife import __
    '''

    __slots__ = _base.SLOTS


class cmpknife(
    _lazy._OutMixin, _base._KnifeMixin, OutMixin, CmpMixin, _mixins._CmpMixin,
):

    '''
    Lazier evaluated comparing knife. Provides comparison operations for
    incoming things.

    >>> from knife.lazy import cmpknife
    '''

    __slots__ = _base.SLOTS


class filterknife(
    _lazy._OutMixin, _base._KnifeMixin, OutMixin, FilterMixin,
    _mixins._FilterMixin,
):

    '''
    Lazier evaluated filtering knife. Provides filtering operations for
    incoming things.

    >>> from knife.lazy import filterknife
    '''

    __slots__ = _base.SLOTS


class mapknife(
    _lazy._OutMixin, _base._KnifeMixin, OutMixin, MapMixin, _mixins._MapMixin
):

    '''
    Lazier evaluated mapping knife. Provides `mapping <http://docs.python.org
    /library/functions.html#map>`_ operations for incoming things.

    >>> from knife.lazy import mapknife
    '''

    __slots__ = _base.SLOTS


class mathknife(
    _lazy._OutMixin, _base._KnifeMixin, OutMixin, MathMixin,
    _mixins._MathMixin,
):

    '''
    Lazier evaluated mathing knife. Provides numeric and statistical
    operations for incoming things.

    >>> from knife.lazy import mathknife
    '''

    __slots__ = _base.SLOTS


class orderknife(
    _lazy._OutMixin, _base._KnifeMixin, OutMixin, OrderMixin,
    _mixins._OrderMixin,
):

    '''
    Lazier evaluated ordering knife. Provides sorting and grouping operations
    for incoming things.

    >>> from knife.lazy import orderknife
    '''

    __slots__ = _base.SLOTS


class reduceknife(
    _lazy._OutMixin, _base._KnifeMixin, OutMixin, ReduceMixin,
    _mixins._ReduceMixin,
):

    '''
    Lazier evaluated reducing knife. Provides `reducing <http://docs.python.
    org/library/functions.html#map>`_ operations for incoming things.

    >>> from knife.lazy import reduceknife
    '''

    __slots__ = _base.SLOTS


class repeatknife(
    _lazy._OutMixin, _base._KnifeMixin, OutMixin, RepeatMixin,
    _mixins._RepeatMixin,
):

    '''
    Lazier evaluated repeating knife. Provides repetition operations for
    incoming things.

    >>> from knife.lazy import repeatknife
    '''

    __slots__ = _base.SLOTS


class sliceknife(
    _lazy._OutMixin, _base._KnifeMixin, OutMixin, SliceMixin,
    _mixins._SliceMixin
):

    '''
    Lazier evaluated slicing knife. Provides `slicing <http://docs.python.
    org/library/functions.html#slice>`_ operations for incoming things.

    >>> from knife.lazy import sliceknife
    '''

    __slots__ = _base.SLOTS
