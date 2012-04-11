# -*- coding: utf-8 -*-
'''lazily evaluated chainsaws'''

from itertools import tee, chain
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


class LazyMixin(ChainsawMixin, _ChainsawMixin):

    '''lazy chainsaw mixin'''

    def __init__(self, *things, **kw):
        '''
        init

        @param *things: wannabe incoming things
        '''
        # if just one thing, put it in inchain or put everything in inchain
        inchain = iter([things[0]]) if len(things) == 1 else iter(things)
        super(LazyMixin, self).__init__(inchain, iter([]), **kw)
        # work link
        self._work = iter([])
        # holding link
        self._hold = iter([])

    ###########################################################################
    ## chain things ###########################################################
    ###########################################################################

    @contextmanager
    def _man4(self, **kw):
        '''switch to a manually balanced four-link chain'''
        self._as_chain(chain=self._man4, **kw)
        # move incoming things up to work link
        work, incoming = tee(getattr(self, self._IN))
        setattr(self, self._WORK, work)
        setattr(self, self._IN, incoming)
        yield
        # extend outgoing things with holding link
        hold = getattr(self, self._HOLD)
        setattr(
            self,
            self._OUT,
            hold if self._buildup else chain(hold, getattr(self, self._OUT)),
        )
        # clear work, holding links & return to current selected chain
        self._rechain()._clearworking()

    @contextmanager
    def _auto(self, **kw):
        '''switch to an automatically balanced four-link chain'''
        self._as_chain(chain=self._auto, **kw)
        # move ins things up to work link
        work, ins = tee(getattr(self, self._IN))
        setattr(self, self._WORK, work)
        setattr(self, self._IN, ins)
        yield
        # move things from holding link to inchain and outs
        ins, outs = tee(getattr(self, self._HOLD))
        setattr(
            self,
            self._OUT,
            outs if self._buildup else chain(outs, getattr(self, self._OUT)),
        )
        setattr(self, self._IN, ins)
        # clear work, holding links & return to current selected chain
        self._rechain()._clearworking()

    ###########################################################################
    ## snapshot of things #####################################################
    ###########################################################################

    def snapshot(self, baseline=False, original=False):
        '''
        Take a snapshot of current incoming things.

        @param baseline: make snapshot baseline version (default: False)
        @param original: make snapshot original version (default: False)
        '''
        # take snapshot
        snapshot, self._in = tee(self._in)
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

        @param snapshot: steps ago 1, 2, 3 steps, etc.. (default: 0)
        @param baseline: return ins to baseline version (default: False)
        @param original: return ins to original version (default: False)
        '''
        # clear everything
        self.clear()
        if original:
            # clear snapshots
            self._clearsp()
            # clear baseline
            self._baseline = None
            # restore original version of incoming things
            self._in, self._original = tee(self._original)
        elif baseline:
            # clear snapshots
            self._clearsp()
            # revert to baseline version of incoming things
            self._in, self._baseline = tee(self._baseline)
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
    def _iterable(self, getattr_=getattr):
        '''some iterable derived from a link in the chain'''
        return getattr_(self, self._WORK)

    ###########################################################################
    ## extend things ##########################################################
    ###########################################################################

    def _xtend(self, things, chain_=chain, getattr_=getattr):
        '''extend the holding link with `things`'''
        setattr(
            self,
            self._HOLD,
            chain_(things, getattr_(self, self._HOLD)))
        return self

    def _xtendfront(self, things, reversed_=reversed):
        '''
        extend holding link with `things` placed in front of anything already
        in the holding link
        '''
        return self._xtend(reversed_(things))

    def _append(self, things, chain_=chain, iter_=iter, getattr_=getattr):
        '''append `things` to holding link'''
        setattr(
            self,
            self._HOLD,
            chain_(getattr_(self, self._HOLD), iter_([things])),
        )
        return self

    def _appendfront(self, things, iter_=iter):
        '''
        append `things` to the holding link in front of anything already in
        the holding link
        '''
        return self._xtend(iter_([things]))

    ###########################################################################
    ## know things ############################################################
    ###########################################################################

    def __repr__(self, tee_=tee, setattr_=setattr, getattr_=getattr, l=list):
        '''Object representation.'''
        in1, in2 = tee_(getattr(self, self._IN))
        setattr_(self, self._IN, in1)
        out1, out2 = tee_(getattr(self, self._OUT))
        setattr_(self, self._OUT, out1)
        work1, work2 = tee_(getattr(self, self._WORK))
        setattr_(self, self._WORK, work1)
        hold1, hold2 = tee_(getattr(self, self._HOLD))
        setattr_(self, self._HOLD, hold1)
        return self._repr(
            self.__module__,
            clsname(self),
            self._IN,
            l(in2),
            self._WORK,
            l(work2),
            self._HOLD,
            l(hold2),
            self._OUT,
            l(out2),
            self._mode,
            self._context,
        )

    def __len__(self):
        '''Number of incoming things.'''
        self._in, incoming = tee(self._in)
        return len(list(incoming))

    count = __len__

    def count_out(self):
        '''Number of outgoing things.'''
        self._out, outs = tee(self._out)
        return len(list(outs))

    ###########################################################################
    ## clear things ###########################################################
    ###########################################################################

    def _clearworking(self, iter_=iter):
        '''clear working and holding links'''
        # clear work link
        delattr(self, self._WORK)
        setattr(self, self._WORK, iter_([]))
        # clear holding link
        delattr(self, self._HOLD)
        setattr(self, self._HOLD, iter_([]))
        return self

    def _clearh(self):
        '''Clear holding link.'''
        delattr(self, self._HOLD)
        setattr(self, self._HOLD, iter([]))
        return self

    def _clearw(self):
        '''Clear work link.'''
        delattr(self, self._WORK)
        setattr(self, self._WORK, iter([]))
        return self

    def clear_in(self):
        '''Clear incoming things.'''
        delattr(self, self._IN)
        setattr(self, self._IN, iter([]))
        return self

    def clear_out(self):
        '''Clear outgoing things.'''
        delattr(self, self._OUT)
        setattr(self, self._OUT, iter([]))
        return self


class OutputMixin(LazyMixin, OutchainMixin):

    '''active output chainsaw mixin'''

    def __iter__(self):
        '''Yield outgoing things.'''
        return getattr(self, self._OUT)

    def _output(self):
        '''Take a peek at the current state of outgoing things.'''
        outs, tell = tee(self._out)
        wrap = self._wrapper
        if self._mode == self._MANY:
            value = list(wrap(i) for i in outs)
        else:
            value = wrap(outs)
        return value.pop() if len(wrap(tell)) == 1 else value

    preview = _output


class lazysaw(
    OutputMixin, FilterMixin, _FilterMixin, MapMixin, _MapMixin, ReduceMixin,
    _ReduceMixin, OrderMixin, _OrderMixin, CollectMixin, _CollectMixin,
    SliceMixin, _SliceMixin, TruthMixin, _TruthMixin, MathMixin, _MathMixin,
    RepeatMixin, _RepeatMixin,
):

    '''lazy chainsaw'''

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
