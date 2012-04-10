# -*- coding: utf-8 -*-
'''lazily evaluated knives'''

from itertools import tee, chain
from contextlib import contextmanager

from stuf.utils import clsname

from chainsaw.map import RepeatMixin, MapMixin
from chainsaw.reduce import SliceMixin, ReduceMixin
from chainsaw.filter import FilterMixin, CollectMixin
from chainsaw.base import SLOTS, ChainsawMixin, OutchainMixin
from chainsaw.analyze import StatsMixin, TruthMixin, OrderMixin


class LazyMixin(ChainsawMixin):

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
    def _man2(self, **kw):
        '''switch to a manually balanced two-link chain'''
        self._as_chain(
            chain=self._man2, outs=kw.get(self._OUTCFG, self._INVAR), **kw
        )
        # move outgoing things up to work link
        work, outs = tee(getattr(self, self._OUT))
        setattr(self, self._WORK, work)
        setattr(self, self._OUT, outs)
        yield
        # move things from holding state to outs
        hold = getattr(self, self._HOLD)
        setattr(
            self,
            outs,
            hold if self._buildup else chain(hold, getattr(self, self._OUT)),
        )
        # clear work & holding link & return to current selected chain
        self._rechain()._clearworking()

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

    @staticmethod
    def _dupe(iterable, n=2, tee_=tee):
        '''
        clone an iterable

        @param n: number of clones
        '''
        return tee_(iterable, n)[0]

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
        '''object representation'''
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
        self._ins, incoming = tee(self._ins)
        return len(list(incoming))

    count = __len__

    def count_out(self):
        '''Number of outgoing things.'''
        self._outs, outs = tee(self._outs)
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
        '''Clear inchain link.'''
        delattr(self, self._IN)
        setattr(self, self._IN, iter([]))
        return self

    def clear_out(self):
        '''Clear outs link.'''
        delattr(self, self._OUT)
        setattr(self, self._OUT, iter([]))
        return self


class OutputMixin(LazyMixin, OutchainMixin):

    '''active output chainsaw mixin'''

    def __iter__(self):
        '''Yield outgoing things, clearing outs as it goes.'''
        return getattr(self, self._OUT)

    def preview(self):
        '''Take a peek at the current state of outgoing things.'''
        outs, tell = tee(self._outs)
        wrap = self._wrapper
        if self._mode == self._MANY:
            value = list(wrap(i) for i in outs)
        else:
            value = wrap(outs)
        return value.pop() if len(wrap(tell)) == 1 else value


class lazychainsaw(
    OutputMixin, FilterMixin, MapMixin, ReduceMixin, OrderMixin, CollectMixin,
    SliceMixin, TruthMixin, StatsMixin, RepeatMixin,
):

    '''lazy chainsaw'''

    __slots__ = SLOTS


class collectchainsaw(OutputMixin, CollectMixin):

    '''collecting chainsaw'''

    __slots__ = SLOTS


class slicechainsaw(OutputMixin, SliceMixin):

    '''slicing chainsaw'''

    __slots__ = SLOTS


class filterchainsaw(OutputMixin, FilterMixin):

    '''filtering chainsaw'''

    __slots__ = SLOTS


class repeatchainsaw(OutputMixin, RepeatMixin):

    '''repeating chainsaw'''

    __slots__ = SLOTS


class mapchainsaw(OutputMixin, MapMixin):

    '''mapping chainsaw'''

    __slots__ = SLOTS


class orderchainsaw(OutputMixin, OrderMixin):

    '''ordering chainsaw'''

    __slots__ = SLOTS


class mathchainsaw(OutputMixin, StatsMixin):

    '''mathing chainsaw'''

    __slots__ = SLOTS


class truthchainsaw(OutputMixin, TruthMixin):

    '''truthing chainsaw'''

    __slots__ = SLOTS


class reducechainsaw(OutputMixin, ReduceMixin):

    '''reducing chainsaw'''

    __slots__ = SLOTS
