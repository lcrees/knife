# -*- coding: utf-8 -*-
'''Actively evaluated knives.'''

from knife.base import OutMixin
from knife.mixins import (
    RepeatMixin, MapMixin, SliceMixin, ReduceMixin, FilterMixin, MathMixin,
    CmpMixin, OrderMixin)

import knife._base as _base
import knife._mixins as _mixins
import knife._active as _active


class activeknife(
    _active._OutMixin, _base._KnifeMixin, _mixins._CmpMixin,
    _mixins._FilterMixin, _mixins._MapMixin, _mixins._MathMixin,
    _mixins._OrderMixin, _mixins._ReduceMixin, _mixins._SliceMixin,
    _mixins._RepeatMixin,
    OutMixin, FilterMixin, MapMixin, ReduceMixin, OrderMixin, RepeatMixin,
    MathMixin, SliceMixin, CmpMixin,
):

    '''
    Actively evaluated combo knife. Provides every :mod:`knife` method.

    .. note::

      Also aliased as :class:`~knife.knife` when imported from :mod:`knife`.

    >>> from knife import knife
    '''

    __slots__ = _base.SLOTS


class cmpknife(
    _active._OutMixin, _base._KnifeMixin, OutMixin, CmpMixin,
    _mixins._CmpMixin,
):

    '''
    Actively evaluated comparing knife. Provides comparison operations for
    incoming things.

    >>> from knife.active import cmpknife
    '''

    __slots__ = _base.SLOTS


class filterknife(
    _active._OutMixin, _base._KnifeMixin, OutMixin, FilterMixin,
    _mixins._FilterMixin,
):

    '''
    Actively evaluated filtering knife. Provides filtering operations for
    incoming things.

    >>> from knife.active import filterknife
    '''

    __slots__ = _base.SLOTS


class mapknife(
    _active._OutMixin, _base._KnifeMixin, OutMixin, MapMixin,
    _mixins._MapMixin,
):

    '''
    Actively evaluated mapping knife. Provides `mapping <http://docs.python.org
    /library/functions.html#map>`_ operations for incoming things.

    >>> from knife.active import mapknife
    '''

    __slots__ = _base.SLOTS


class mathknife(
    _active._OutMixin, _base._KnifeMixin, OutMixin, MathMixin,
    _mixins._MathMixin,
):

    '''
    Actively evaluated mathing knife. Provides numeric and statistical
    operations for incoming things.

    >>> from knife.active import mathknife
    '''

    __slots__ = _base.SLOTS


class orderknife(
    _active._OutMixin, _base._KnifeMixin, OutMixin, OrderMixin,
    _mixins._OrderMixin,
):

    '''
    Actively evaluated ordering knife. Provides sorting and grouping operations
    for incoming things.

    >>> from knife.active import orderknife
    '''

    __slots__ = _base.SLOTS


class reduceknife(
    _active._OutMixin, _base._KnifeMixin, OutMixin, ReduceMixin,
    _mixins._ReduceMixin,
):

    '''
    Actively evaluated reducing knife. Provides `reducing <http://docs.python.
    org/library/functions.html#map>`_ operations for incoming things.

    >>> from knife.active import reduceknife
    '''

    __slots__ = _base.SLOTS


class repeatknife(
    _active._OutMixin, _base._KnifeMixin, OutMixin, RepeatMixin,
    _mixins._RepeatMixin,
):

    '''
    Actively evaluated repeating knife. Provides repetition operations for
    incoming things.

    >>> from knife.active import repeatknife
    '''

    __slots__ = _base.SLOTS


class sliceknife(
    _active._OutMixin, _base._KnifeMixin, OutMixin, SliceMixin,
    _mixins._SliceMixin
):

    '''
    Actively evaluated slicing knife. Provides `slicing <http://docs.python.
    org/library/functions.html#slice>`_ operations for incoming things.

    >>> from knife.active import sliceknife
    '''

    __slots__ = _base.SLOTS
