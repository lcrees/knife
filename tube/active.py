# -*- coding: utf-8 -*-
'''actively evaluated tubes'''

from copy import copy
from itertools import repeat
from collections import deque
from contextlib import contextmanager

from stuf.utils import clsname

from tube.changing import OutMixin
from tube.base import SLOTS, TubeMixin
from tube.mapping import RepeatMixin, MapMixin
from tube.ordering import RandomMixin, OrderMixin
from tube.reducing import MathMixin, TruthMixin, ReduceMixin
from tube.filtering import FilterMixin, ExtractMixin, SliceMixin


class ActiveMixin(TubeMixin):

    '''base active tubing'''

    def __init__(self, *things, **kw):
        try:
            inflow = deque(things[0]) if len(things) == 1 else deque(things)
        except TypeError:
            inflow = deque()
            inflow.extend(things)
        super(ActiveMixin, self).__init__(inflow, deque())
        # set iterator
        self._iterator = self._iterexcept
        # work things
        self._work = deque()
        # utility things
        self._util = deque()

    ###########################################################################
    ## mode things ############################################################
    ###########################################################################

    def condition(self):
        '''switch to condition mode'''
        with self.flow3(outflow=self._UTILVAR, keep=False):
            self._xtend(self._iterable)
        with self.flow1(hard=True, workq=self._UTILVAR, keep=False):
            self.channel = self._COND
            return self

    def query(self):
        '''flow to query mode'''
        with self.flow3(outflow=self._UTILVAR, keep=False):
            self._xtend(self._iterable)
        with self.flow1(hard=True, workq=self._UTILVAR, keep=False):
            self.channel = self._QUERY
            return self

    ###########################################################################
    ## flow things #######################################################
    ###########################################################################

    @contextmanager
    def flow2(self, **kw):
        '''two-step flow'''
        self.flow(
            outflow=kw.get(self._OUTCFG, self._INVAR), flow=self.flow2(), **kw
        )
        getr_ = lambda x: getattr(self, x)
        outflow = getr_(self._OUT)
        utilq = getr_(self._UTIL)
        workq = getr_(self._WORK)
        # clear all work things
        workq.clear()
        # extend work things with outflow
        workq.extend(outflow)
        # flow iterator
        self._iterator = self._breakcount
        yield
        # clear outflow if so configured
        if self._buildup:
            outflow.clear()
        # extend outflow with utility things
        outflow.extend(utilq)
        # clear utility things
        utilq.clear()
        # return to global flow
        self.reflow()

    @contextmanager
    def flow3(self, **kw):
        '''flow to three-armed flow'''
        self.flow(
            utilq=kw.get(self._WORKCFG, self._WORKVAR), flow=self.flow3, **kw
        )
        getr_ = lambda x: getattr(self, x)
        outflow = getr_(self._OUT)
        utilq = getr_(self._UTIL)
        workq = getr_(self._WORK)
        # clear work things
        workq.clear()
        # extend work things with inflow
        workq.extend(getr_(self._IN))
        # flow iterators
        self._iterator = self._breakcount
        yield
        # clear outflow if so configured
        if self._buildup:
            outflow.clear()
        # extend outflow with utility things
        outflow.extend(utilq)
        # clear utility things
        utilq.clear()
        # return to global flow
        self.reflow()

    @contextmanager
    def flow4(self, **kw):
        '''flow to four-armed flow'''
        self.flow(flow=self.flow4, **kw)
        getr_ = lambda x: getattr(self, x)
        outflow = getr_(self._OUT)
        utilq = getr_(self._UTIL)
        workq = getr_(self._WORK)
        # clear work things
        workq.clear()
        # extend work things with inflow
        workq.extend(getr_(self._IN))
        # flow iterators
        self._iterator = self._iterexcept
        yield
        # clear outflow if so configured
        if self._buildup:
            outflow.clear()
        # extend outflow with utility things
        outflow.extend(utilq)
        # clear utility things
        utilq.clear()
        # return to global flow
        self.reflow()

    @contextmanager
    def autoflow(self, **kw):
        '''flow to auto-synchronizing flow'''
        self.flow(flow=self.autoflow, **kw)
        getr_ = lambda x: getattr(self, x)
        inflow, workq = getr_(self._IN), getr_(self._WORK)
        utilq,  outflow = getr_(self._UTIL), getr_(self._OUT)
        # clear work things
        workq.clear()
        # extend work things with inflow
        workq.extend(inflow)
        # flow iterators
        self._iterator = self._iterexcept
        yield
        # clear outflow if so configured
        if self._buildup:
            outflow.clear()
        outflow.extend(utilq)
        # clear inflow
        inflow.clear()
        inflow.extend(utilq)
        # clear utility things
        utilq.clear()
        # return to global flow
        self.reflow()

    ###########################################################################
    ## savepoint for things ###################################################
    ###########################################################################

    @staticmethod
    def _clone(self, iterable, num=2, copy_=copy):
        return iterable if num == 1 else copy_(iterable), iterable

    ###########################################################################
    ## iterate things #########################################################
    ###########################################################################

    @property
    def _iterable(self):
        '''iterable'''
        return self._iterator(self._WORK)

    def _breakcount(self, attr='_UTIL'):
        '''
        breakcount iterator

        @param attr: things to iterate over
        '''
        dq = getattr(self, attr)
        length, call = len(dq), dq.popleft
        for i in repeat(None, length):  # @UnusedVariable
            yield call()

    def _iterexcept(self, attr='_UTIL'):
        '''
        call a function repeatedly until an exception is raised

        Converts a call-until-exception interface to an iterator interface.
        Like `iter(call, sentinel)` but uses an exception instead of a sentinel
        to end the loop.

        Raymond Hettinger, Python Cookbook recipe # 577155
        '''
        call = getattr(self, attr).popleft
        try:
            while 1:
                yield call()
        except IndexError:
            pass

    ###########################################################################
    ## extend things ##########################################################
    ###########################################################################

    def _xtend(self, things):
        '''extend utility things with `things` wrapped'''
        getattr(self, self._UTIL).extend(things)
        return self

    def _xtendleft(self, things):
        '''extend left side of utility things with `things`'''
        getattr(self, self._UTIL).extendleft(things)
        return self

    def _iter(self, things):
        '''extend work things with `things` wrapped in iterator'''
        getattr(self, self._UTIL).extend(iter(things))
        return self

    ###########################################################################
    ## append things ##########################################################
    ###########################################################################

    def _append(self, things):
        '''append `things` to utility things'''
        getattr(self, self._UTIL).append(things)
        return self

    def _appendleft(self, things):
        '''append `things` to left side of utility things'''
        getattr(self, self._UTIL).appendleft(things)
        return self

    ###########################################################################
    ## know things ############################################################
    ###########################################################################

    def __repr__(self):
        getr_, list_ = lambda x: getattr(self, x), list
        return self._repr(
            self.__module__,
            clsname(self),
            self.channel.upper(),
            self._IN,
            list_(getr_(self._IN)),
            self._WORK,
            list_(getr_(self._WORK)),
            self._UTIL,
            list_(getr_(self._UTIL)),
            self._OUT,
            list_(getr_(self._OUT)),
            id(self),
        )

    def __len__(self):
        '''number of inflow'''
        return len(self.inflow)
    
    count = __len__

    def countout(self):
        '''number of outflow'''
        return len(self.outflow)

    ###########################################################################
    ## clear things ###########################################################
    ###########################################################################

    def _clearu(self):
        '''clear utility things'''
        self._util.clear()
        return self

    def _clearw(self):
        '''clear work things'''
        self._work.clear()
        return self

    def clearin(self):
        '''clear inflow'''
        self.inflow.clear()
        return self

    def clearout(self):
        '''clear outflow'''
        self.outflow.clear()
        return self


class ExitMixin(ActiveMixin):

    '''tubing with results extractor mixin'''
    
    def __iter__(self):
        '''yield outflow, clearing outflow as it iterates'''
        return self._iterexcept(self._OUT)
    
    results = __iter__

    def end(self):
        '''return outflow then clear wrap everything'''
        # return to default flow
        self.unflow()
        wrap, outflow = self._wrapper, self.outflow
        wrap = self.outflow.pop() if len(outflow) == 1 else wrap(outflow)
        # clear every last thing
        self.clear()._clearsp()
        return wrap

    def snapshot(self):
        '''snapshot of current outflow'''
        wrap = copy(self.outflow)
        return wrap.pop() if len(wrap) == 1 else self._wrapper(wrap)

    def out(self):
        '''return outflow and clear outflow'''
        # return to default flow
        self.unflow()
        wrap, outflow = self._wrapper, self.outflow
        wrap = outflow.pop() if len(outflow) == 1 else wrap(outflow)
        # clear outflow
        self.clearout()
        return wrap


class activetube(
    ExitMixin, OutMixin, FilterMixin, MapMixin, ReduceMixin, OrderMixin,
    ExtractMixin, SliceMixin, TruthMixin, MathMixin, RepeatMixin, RandomMixin,
):

    '''active tubing'''

    __slots__ = SLOTS


class collecttube(OutMixin, ExtractMixin):

    '''collecting tubing'''

    __slots__ = SLOTS


class slicetube(OutMixin, SliceMixin):

    '''slice tubing'''

    __slots__ = SLOTS


class filtertube(OutMixin, FilterMixin, ExtractMixin, SliceMixin):

    '''filter tubing'''

    __slots__ = SLOTS


class repeattube(OutMixin, RepeatMixin):

    '''repeat tubing'''

    __slots__ = SLOTS


class maptube(OutMixin, RepeatMixin, MapMixin):

    '''mapping tubing'''

    __slots__ = SLOTS


class randomtube(OutMixin, RandomMixin):

    '''randomizing tubing'''

    __slots__ = SLOTS


class sorttube(OutMixin, OrderMixin, RandomMixin):

    '''ordering tubing'''

    __slots__ = SLOTS


class mathtube(OutMixin, MathMixin):

    '''math tubing'''

    __slots__ = SLOTS


class truthtube(OutMixin, TruthMixin):

    '''truth tubing'''

    __slots__ = SLOTS


class reducetube(OutMixin, MathMixin, TruthMixin, ReduceMixin):

    '''reduce tubing'''

    __slots__ = SLOTS
