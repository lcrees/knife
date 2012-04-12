# -*- coding: utf-8 -*-
'''active chainsaws'''

from collections import deque
from contextlib import contextmanager

from stuf.utils import clsname

from chainsaw.map import RepeatMixin, MapMixin
from chainsaw.reduce import SliceMixin, ReduceMixin
from chainsaw.filter import FilterMixin, CollectMixin
from chainsaw.base import ChainsawMixin, OutchainMixin
from chainsaw.analyze import MathMixin, TruthMixin, OrderMixin

from chainsaw._base import SLOTS, _ChainsawMixin
from chainsaw._map import _RepeatMixin, _MapMixin
from chainsaw._reduce import _SliceMixin, _ReduceMixin
from chainsaw._filter import _FilterMixin, _CollectMixin
from chainsaw._analyze import _MathMixin, _TruthMixin, _OrderMixin


class ActiveMixin(ChainsawMixin, _ChainsawMixin):

    '''active chainsaw mixin'''

    def __init__(self, *things, **kw):
        '''
        init

        :params *things: incoming things
        '''
        # if just one thing, put it in inchain or put everything in inchain
        try:
            inchain = deque(things[0]) if len(things) == 1 else deque(things)
        except TypeError:
            # handle non-iterable incoming things with length
            inchain = deque()
            inchain.append(things)
        super(ActiveMixin, self).__init__(inchain, deque(), **kw)
        # work link
        self._work = deque()
        # holding link
        self._hold = deque()

    ###########################################################################
    ## chain things ###########################################################
    ###########################################################################

    @contextmanager
    def _man4(self, **kw):
        '''switch to a manually balanced four-link chain'''
        self._as_chain(chain=self._man4, **kw)
        # move incoming things up to work link
        getattr(self, self._WORK).extend(getattr(self, self._IN))
        yield
        out = getattr(self, self._OUT)
        # clear out
        if self._buildup:
            out.clear()
        # extend outgoing things with holding link
        out.extend(getattr(self, self._HOLD))
        # clear work, holding links & return to current selected chain
        self._rechain()._clearworking()

    @contextmanager
    def _auto(self, **kw):
        '''switch to an automatically balanced four-link chain'''
        self._as_chain(chain=self._auto, **kw)
        inchain = getattr(self, self._IN)
        # move incoming things up to work link
        getattr(self, self._WORK).extend(inchain)
        yield
        out = getattr(self, self._OUT)
        # clear out
        if self._buildup:
            out.clear()
        # extend outgoing things with holding link
        hold = getattr(self, self._HOLD)
        out.extend(hold)
        # extend incoming things with holding link
        inchain.clear()
        inchain.extend(hold)
        # clear work, holding links & return to current selected chain
        self._rechain()._clearworking()

    ###########################################################################
    ## snapshot of things #####################################################
    ###########################################################################

    def snapshot(self, baseline=False, original=False):
        '''
        Take a snapshot of current incoming things.

        :param baseline: make this snapshot the baseline snapshot (*default:*
          :const:`False`)
        :param original: make this snapshot the original snapshot (*default:*
          :const:`False`)
        '''
        # take snapshot
        snapshot = self._in.__copy__()
        # make this snapshot the baseline snapshot
        if self._context == self._EDIT or baseline:
            self._baseline = snapshot
        # make this snapshot the original snapshot
        if original:
            self._original = snapshot
        # place snapshot at beginning of snapshot stack
        self._ss.appendleft(snapshot)
        return self

    def undo(self, snapshot=0, baseline=False, original=False):
        '''
        Revert incoming things to a previous snapshot of incoming things.

        :param snapshot: number of steps ago e.g. ``1``, ``2``, ``3``, etc.
          (*default:* ``0``)
        :param baseline: revert incoming things to baseline snapshot (
          *default:* :const:`False`)
        :param original: revert incoming things to original snapshot (
          *default:* :const:`False`)
        '''
        # clear everything
        self.clear()
        if original:
            # clear snapshots
            self._clearsp()
            # clear baseline
            self._baseline = None
            # restore original version of incoming things
            self._in = self._original.__copy__()
        elif baseline:
            # clear snapshots
            self._clearsp()
            # restore baseline version of incoming things
            self._in = self._baseline.__copy__()
        # if specified, use a specific snapshot
        elif snapshot:
            self._ss.rotate(-(snapshot - 1))
            self._in = self._ss.popleft()
        # by default revert to most recent snapshot
        else:
            self._in = self._ss.popleft()
        return self

    ###########################################################################
    ## iterate things #########################################################
    ###########################################################################

    @property
    def _iterable(self):
        '''some iterable derived from a link in the chain'''
        return self._iterator(self._WORK)

    def _iterator(self, attr='_HOLD', getattr_=getattr):
        '''
        repeatedly invoke callable until IndexError is raised

        derived from Raymond Hettinger Python Cookbook recipe # 577155
        '''
        call = getattr_(self, attr).popleft
        try:
            while 1:
                yield call()
        except IndexError:
            pass

    ###########################################################################
    ## extend things ##########################################################
    ###########################################################################

    def _xtend(self, things, getattr_=getattr):
        '''extend the holding link with `things`'''
        getattr_(self, self._HOLD).extend(things)
        return self

    def _xtendfront(self, things, getattr_=getattr):
        '''
        extend holding link with `things` placed in front of anything already
        in the holding link
        '''
        getattr_(self, self._HOLD).extendleft(things)
        return self

    def _append(self, things, getattr_=getattr):
        '''append `things` to holding link'''
        getattr_(self, self._HOLD).append(things)
        return self

    def _appendfront(self, things, getattr_=getattr):
        '''
        append `things` to the holding link in front of anything already in
        the holding link
        '''
        getattr_(self, self._HOLD).appendleft(things)
        return self

    ###########################################################################
    ## know things ############################################################
    ###########################################################################

    def __repr__(self, getattr_=getattr, clsname_=clsname, list_=list):
        '''Object representation.'''
        return self._repr(
            self.__module__,
            clsname_(self),
            self._IN,
            list_(getattr_(self, self._IN)),
            self._WORK,
            list_(getattr_(self, self._WORK)),
            self._HOLD,
            list_(getattr_(self, self._HOLD)),
            self._OUT,
            list_(getattr_(self, self._OUT)),
            self._mode,
            self._context,
        )

    def __len__(self):
        '''Number of incoming things.'''
        return len(self._in)

    count = __len__

    def count_out(self):
        '''Number of outgoing things.'''
        return len(self._out)

    ###########################################################################
    ## clear things ###########################################################
    ###########################################################################

    def _clearworking(self):
        '''clear working and holding links'''
        # clear work link
        self._work.clear()
        # clear holding link
        self._hold.clear()
        return self

    def _clearh(self):
        '''Clear holding link.'''
        self._hold.clear()
        return self

    def _clearw(self):
        '''Clear work link.'''
        self._work.clear()
        return self

    def clear_in(self):
        '''Clear incoming things.'''
        self._in.clear()
        return self

    def clear_out(self):
        '''Clear outgoing things.'''
        self._out.clear()
        return self


class OutputMixin(ActiveMixin, OutchainMixin):

    '''lazy output chainsaw mixin'''

    def __iter__(self):
        '''Yield outgoing things.'''
        return self._iterator(self._OUT)

    def _output(self):
        '''Take a peek at the current state of outgoing things.'''
        wrap, out = self._wrapper, self._out
        if self._mode == self._MANY:
            value = tuple(wrap(i) for i in out)
        else:
            value = wrap(out)
        return value.pop() if len(value) == 1 else value

    preview = _output


class activesaw(
    OutputMixin, FilterMixin, _FilterMixin, MapMixin, _MapMixin, ReduceMixin,
    _ReduceMixin, OrderMixin, _OrderMixin, CollectMixin, _CollectMixin,
    SliceMixin, _SliceMixin, TruthMixin, _TruthMixin, MathMixin, _MathMixin,
    RepeatMixin, _RepeatMixin,
):

    '''active chainsaw'''

    __slots__ = SLOTS


class collectsaw(OutputMixin, CollectMixin, _CollectMixin):

    '''collecting chainsaw'''

    __slots__ = SLOTS


class slicesaw(OutputMixin, SliceMixin, _SliceMixin):

    '''slicing chainsaw'''

    __slots__ = SLOTS


class filtersaw(OutputMixin, FilterMixin, _FilterMixin):

    '''filtering chainsaw'''

    __slots__ = SLOTS


class repeatsaw(OutputMixin, RepeatMixin, _RepeatMixin):

    '''repeating chainsaw'''

    __slots__ = SLOTS


class mapsaw(OutputMixin, MapMixin, _MapMixin):

    '''mapping chainsaw'''

    __slots__ = SLOTS


class ordersaw(OutputMixin, OrderMixin, _OrderMixin):

    '''ordering chainsaw'''

    __slots__ = SLOTS


class mathsaw(OutputMixin, MathMixin, _MathMixin):

    '''mathing chainsaw'''

    __slots__ = SLOTS


class truthsaw(OutputMixin, TruthMixin, _TruthMixin):

    '''truthing chainsaw'''

    __slots__ = SLOTS


class reducesaw(OutputMixin, ReduceMixin, _ReduceMixin):

    '''reducing chainsaw'''

    __slots__ = SLOTS
