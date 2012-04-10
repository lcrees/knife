# -*- coding: utf-8 -*-
'''actively evaluating knives'''

from itertools import repeat
from collections import deque
from contextlib import contextmanager

from stuf.utils import clsname

from chainsaw.map import RepeatMixin, MapMixin
from chainsaw.reduce import SliceMixin, ReduceMixin
from chainsaw.filter import FilterMixin, CollectMixin
from chainsaw.base import SLOTS, ChainsawMixin, OutchainMixin
from chainsaw.analyze import StatsMixin, TruthMixin, OrderMixin


class ActiveMixin(ChainsawMixin):

    '''active chainsaw mixin'''

    def __init__(self, *things, **kw):
        '''
        init

        @param *things: wannabe incoming things
        '''
        # if just one thing, put it in inchain or put everything in inchain
        try:
            inchain = deque(things[0]) if len(things) == 1 else deque(things)
        except TypeError:
            # handle non-iterable incoming things with length
            inchain = deque()
            inchain.append(things)
        super(ActiveMixin, self).__init__(inchain, deque(), **kw)
        # assign default iterator
        self._iterator = self._iterexcept
        # work link
        self._work = deque()
        # holding link
        self._hold = deque()

    ###########################################################################
    ## chain things ###########################################################
    ###########################################################################

    @contextmanager
    def _man2(self, **kw):
        '''switch to a manually balanced two-link chain'''
        self._as_chain(
            chain=self._man2, outs=kw.get(self._OUTCFG, self._INVAR), **kw
        )
        outchain = getattr(self, self._OUT)
        # move outgoing (usually incoming) things up to work link
        getattr(self, self._WORK).extend(outchain)
        # assign chain iterator
        self._iterator = self._breakcount
        yield
        # clear outchain
        if self._buildup:
            outchain.clear()
        # move things from holding state to outchain
        outchain.extend(getattr(self, self._HOLD))
        # clear work & holding link & return to current selected chain
        self._rechain()._clearworking()

    @contextmanager
    def _man4(self, **kw):
        '''switch to a manually balanced four-link chain'''
        self._as_chain(chain=self._man4, **kw)
        # move incoming things up to work link
        getattr(self, self._WORK).extend(getattr(self, self._IN))
        # assign chain iterator
        self._iterator = self._iterexcept
        yield
        outchain = getattr(self, self._OUT)
        # clear outchain
        if self._buildup:
            outchain.clear()
        # extend outgoing things with holding link
        outchain.extend(getattr(self, self._HOLD))
        # clear work, holding links & return to current selected chain
        self._rechain()._clearworking()

    @contextmanager
    def _auto(self, **kw):
        '''switch to an automatically balanced four-link chain'''
        self._as_chain(chain=self._auto, **kw)
        inchain = getattr(self, self._IN)
        # move incoming things up to work link
        getattr(self, self._WORK).extend(inchain)
        # assign chain iterator
        self._iterator = self._iterexcept
        yield
        outchain = getattr(self, self._OUT)
        # clear outchain
        if self._buildup:
            outchain.clear()
        # extend outgoing things with holding link
        hold = getattr(self, self._HOLD)
        outchain.extend(hold)
        # extend incoming things with holding link
        inchain.clear()
        inchain.extend(hold)
        # clear work, holding links & return to current selected chain
        self._rechain()._clearworking()

    @staticmethod
    def _dupe(iterable, deque_=deque):
        '''
        clone an iterable

        @param n: number of clones
        '''
        return deque_(iterable)

    ###########################################################################
    ## iterate things #########################################################
    ###########################################################################

    def _breakcount(self, attr='_HOLD', repeat_=repeat, len_=len, g=getattr):
        '''
        breakcount iterator

        @param attr: link to iterate over
        '''
        dq = g(self, attr)
        length, call = len_(dq), dq.popleft
        for i in repeat_(None, length):  # @UnusedVariable
            yield call()

    def _iterexcept(self, attr='_HOLD', getattr_=getattr):
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

    @property
    def _iterable(self):
        '''iterable link in the chain'''
        return self._iterator(self._WORK)

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
        '''append `things` to the holding link'''
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
        '''object representation'''
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
        return len(self._ins)

    count = __len__

    def count_out(self):
        '''Number of outgoing things.'''
        return len(self._outs)

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
        '''Clear inchain link.'''
        self._ins.clear()
        return self

    def clear_out(self):
        '''Clear outchain link.'''
        self._outs.clear()
        return self


class OutputMixin(ActiveMixin, OutchainMixin):

    '''lazy output chainsaw mixin'''

    def __iter__(self):
        '''Yield outgoing things, clearing outchain as it goes.'''
        return self._iterexcept(self._OUT)

    def preview(self):
        '''Take a peek at the current state of outgoing things.'''
        wrap, outchain = self._wrapper, self._outs
        if self._mode == self._MANY:
            value = list(wrap(i) for i in outchain)
        else:
            value = wrap(outchain)
        return value.pop() if len(value) == 1 else value


class activechainsaw(
    OutputMixin, FilterMixin, MapMixin, ReduceMixin, OrderMixin, CollectMixin,
    SliceMixin, TruthMixin, StatsMixin, RepeatMixin,
):

    '''active chainsaw'''

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
