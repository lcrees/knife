# -*- coding: utf-8 -*-
'''actively evaluated tubing'''

from itertools import repeat
from collections import deque
from contextlib import contextmanager

from stuf.utils import clsname

from tube.mapping import RepeatMixin, MapMixin
from tube.base import SLOTS, TubeMixin, OutflowMixin
from tube.ordering import RandomMixin, OrderMixin
from tube.reducing import MathMixin, TruthMixin, ReduceMixin
from tube.filtering import FilterMixin, ExtractMixin, SliceMixin


class ActiveMixin(TubeMixin):

    '''active tubing'''

    def __init__(self, *things, **kw):
        try:
            inflow = deque(things[0]) if len(things) == 1 else deque(things)
        except TypeError:
            inflow = deque()
            inflow.extend(things)
        super(ActiveMixin, self).__init__(inflow, deque())
        # set iterator
        self._iterator = self._iterexcept
        # work pool
        self._work = deque()
        # holding pool
        self._util = deque()

    ###########################################################################
    ## mode things ############################################################
    ###########################################################################

    def query(self):
        '''flow to query mode'''
        with self._flow3(outflow=self._HOLDVAR, keep=False):
            self._many(self._iterable)
        with self._flow1(hard=True, workq=self._HOLDVAR, keep=False):
            self._channel = self._QUERY
            return self

    ###########################################################################
    ## flow things ############################################################
    ###########################################################################

    @contextmanager
    def _flow2(self, **kw):
        '''switch to manually balanced two-stage flow'''
        self.flow(
            flow=self._flow2, outflow=kw.get(self._OUTCFG, self._INVAR), **kw
        )
        getr_ = lambda x: getattr(self, x)
        outflow = getr_(self._OUT)
        utilq = getr_(self._HOLD)
        workq = getr_(self._WORK)
        # clear all work pool
        workq.clear()
        # extend work pool with outflow
        workq.extend(outflow)
        # flow iterator
        self._iterator = self._breakcount
        yield
        # clear outflow if so configured
        if self._buildup:
            outflow.clear()
        # extend outflow with holding pool
        outflow.extend(utilq)
        # clear holding pool
        utilq.clear()
        # revert to current flow
        self._reflow()

    @contextmanager
    def _flow3(self, **kw):
        '''switch to manually balanced three-stage flow'''
        self.flow(
            utilq=kw.get(self._WORKCFG, self._WORKVAR), flow=self._flow3, **kw
        )
        getr_ = lambda x: getattr(self, x)
        outflow = getr_(self._OUT)
        utilq = getr_(self._HOLD)
        workq = getr_(self._WORK)
        # clear work pool
        workq.clear()
        # extend work pool with inflow
        workq.extend(getr_(self._IN))
        # flow iterators
        self._iterator = self._breakcount
        yield
        # clear outflow if so configured
        if self._buildup:
            outflow.clear()
        # extend outflow with holding pool
        outflow.extend(utilq)
        # clear holding pool
        utilq.clear()
        # revert to current flow
        self._reflow()

    @contextmanager
    def _flow4(self, **kw):
        '''switch to manually balanced four-stage flow'''
        self.flow(flow=self._flow4, **kw)
        getr_ = lambda x: getattr(self, x)
        outflow = getr_(self._OUT)
        utilq = getr_(self._HOLD)
        workq = getr_(self._WORK)
        # clear work pool
        workq.clear()
        # extend work pool with inflow
        workq.extend(getr_(self._IN))
        # flow iterators
        self._iterator = self._iterexcept
        yield
        # clear outflow if so configured
        if self._buildup:
            outflow.clear()
        # extend outflow with holding pool
        outflow.extend(utilq)
        # clear holding pool
        utilq.clear()
        # return to global flow
        self._reflow()

    @contextmanager
    def _autoflow(self, **kw):
        '''switch to automatically balanced four-stage flow'''
        self.flow(flow=self._autoflow, **kw)
        getr_ = lambda x: getattr(self, x)
        inflow, workq = getr_(self._IN), getr_(self._WORK)
        utilq,  outflow = getr_(self._HOLD), getr_(self._OUT)
        # clear work pool
        workq.clear()
        # extend work pool with inflow
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
        # clear holding pool
        utilq.clear()
        # return to global flow
        self._reflow()

    ###########################################################################
    ## savepoint for things ###################################################
    ###########################################################################

    @staticmethod
    def _clone(self, iterable, n=2, deque_=deque):
        '''clone an iterable'''
        return iterable, iterable if n == 1 else deque_(iterable), iterable

    ###########################################################################
    ## iterate things #########################################################
    ###########################################################################

    def _breakcount(self, attr='_HOLD', repeat_=repeat):
        '''
        breakcount iterator

        @param attr: things to iterate over
        '''
        dq = getattr(self, attr)
        length, call = len(dq), dq.popleft
        for i in repeat(None, length):  # @UnusedVariable
            yield call()

    def _iterexcept(self, attr='_HOLD'):
        '''
        invoke callable until exception is raised

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

    @property
    def _iterable(self):
        '''iterable'''
        return self._iterator(self._WORK)

    ###########################################################################
    ## extend things ##########################################################
    ###########################################################################

    def _many(self, things):
        '''extend holding pool with `things`'''
        getattr(self, self._HOLD).extend(things)
        return self

    def _xtendleft(self, things):
        '''extend before of holding pool with `things`'''
        getattr(self, self._HOLD).extendleft(things)
        return self

    def _iter(self, things):
        '''extend work pool with `things` wrapped in iterator'''
        getattr(self, self._HOLD).extend(iter(things))
        return self

    ###########################################################################
    ## append things ##########################################################
    ###########################################################################

    def _one(self, things):
        '''append `things` to holding pool'''
        getattr(self, self._HOLD).append(things)
        return self

    def _appendleft(self, things):
        '''append `things` before things already in holding pool'''
        getattr(self, self._HOLD).appendleft(things)
        return self

    ###########################################################################
    ## know things ############################################################
    ###########################################################################

    def __repr__(self):
        return self._repr(
            self.__module__,
            clsname(self),
            self._IN,
            list(getattr(self, self._IN)),
            self._WORK,
            list(getattr(self, self._WORK)),
            self._HOLD,
            list(getattr(self, self._HOLD)),
            self._OUT,
            list(getattr(self, self._OUT)),
            self._channel,
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
        '''clear holding pool'''
        self._util.clear()
        return self

    def _clearw(self):
        '''clear work pool'''
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


class OutputMixin(ActiveMixin, OutflowMixin):

    '''lazy output tubing mixin'''

    def __iter__(self):
        '''yield outflow, clearing outflow as it iterates'''
        return self._iterexcept(self._OUT)

    def end(self):
        '''return outflow and clear out everything'''
        # revert to default flow
        self.unflow()
        wrap, outflow = self._wrapper, self.outflow
        wrap = self.outflow.pop() if len(outflow) == 1 else wrap(outflow)
        # clear every last thing
        self.clear()._clearsp()
        return wrap

    def snapshot(self):
        '''snapshot of current outflow'''
        out = deque(self.outflow)
        return out.pop() if len(out) == 1 else self._wrapper(out)

    def out(self):
        '''clear outflow and return outgoing things'''
        self.unflow()
        wrap, outflow = self._wrapper, self.outflow
        wrap = outflow.pop() if len(outflow) == 1 else wrap(outflow)
        # clear outgoing things
        self.clearout()
        return wrap


class activetube(
    OutputMixin, FilterMixin, MapMixin, ReduceMixin, OrderMixin, ExtractMixin,
    SliceMixin, TruthMixin, MathMixin, RepeatMixin, RandomMixin,
):

    '''active tubing'''

    __slots__ = SLOTS


class collecttube(OutflowMixin, ExtractMixin):

    '''collecting tubing'''

    __slots__ = SLOTS


class slicetube(OutflowMixin, SliceMixin):

    '''slice tubing'''

    __slots__ = SLOTS


class filtertube(OutflowMixin, FilterMixin, ExtractMixin, SliceMixin):

    '''filter tubing'''

    __slots__ = SLOTS


class repeattube(OutflowMixin, RepeatMixin):

    '''repeat tubing'''

    __slots__ = SLOTS


class maptube(OutflowMixin, RepeatMixin, MapMixin):

    '''mapping tubing'''

    __slots__ = SLOTS


class randomtube(OutflowMixin, RandomMixin):

    '''randomizing tubing'''

    __slots__ = SLOTS


class sorttube(OutflowMixin, OrderMixin, RandomMixin):

    '''ordering tubing'''

    __slots__ = SLOTS


class mathtube(OutflowMixin, MathMixin):

    '''math tubing'''

    __slots__ = SLOTS


class truthtube(OutflowMixin, TruthMixin):

    '''truth tubing'''

    __slots__ = SLOTS


class reducetube(OutflowMixin, MathMixin, TruthMixin, ReduceMixin):

    '''reduce tubing'''

    __slots__ = SLOTS
