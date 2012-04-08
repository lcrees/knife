# -*- coding: utf-8 -*-
'''actively evaluated knives'''

from itertools import repeat
from collections import deque
from contextlib import contextmanager

from stuf.utils import clsname

from knife.output import OutflowMixin
from knife.base import SLOTS, TubeMixin
from knife.mapping import RepeatMixin, MapMixin
from knife.ordering import RandomMixin, OrderMixin
from knife.reducing import MathMixin, TruthMixin, ReduceMixin
from knife.filtering import FilterMixin, ExtractMixin, SliceMixin


class ActiveMixin(TubeMixin):

    '''active knife mixin'''

    def __init__(self, *things, **kw):
        try:
            input = deque(things[0]) if len(things) == 1 else deque(things)
        except TypeError:
            input = deque()
            input.extend(things)
        super(ActiveMixin, self).__init__(input, deque(), **kw)
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
        with self._flow3(output=self._HOLDVAR, keep=False):
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
            flow=self._flow2, output=kw.get(self._OUTCFG, self._INVAR), **kw
        )
        getr_ = lambda x: getattr(self, x)
        output = getr_(self._OUT)
        utilq = getr_(self._HOLD)
        workq = getr_(self._WORK)
        # clear all work pool
        workq.clear()
        # extend work pool with output
        workq.extend(output)
        # flow iterator
        self._iterator = self._breakcount
        yield
        # clear output if so configured
        if self._buildup:
            output.clear()
        # extend output with holding pool
        output.extend(utilq)
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
        output = getr_(self._OUT)
        utilq = getr_(self._HOLD)
        workq = getr_(self._WORK)
        # clear work pool
        workq.clear()
        # extend work pool with incoming
        workq.extend(getr_(self._IN))
        # flow iterators
        self._iterator = self._breakcount
        yield
        # clear output if so configured
        if self._buildup:
            output.clear()
        # extend output with holding pool
        output.extend(utilq)
        # clear holding pool
        utilq.clear()
        # revert to current flow
        self._reflow()

    @contextmanager
    def _flow4(self, **kw):
        '''switch to manually balanced four-stage flow'''
        self.flow(flow=self._flow4, **kw)
        getr_ = lambda x: getattr(self, x)
        output = getr_(self._OUT)
        utilq = getr_(self._HOLD)
        workq = getr_(self._WORK)
        # clear work pool
        workq.clear()
        # extend work pool with incoming
        workq.extend(getr_(self._IN))
        # flow iterators
        self._iterator = self._iterexcept
        yield
        # clear output if so configured
        if self._buildup:
            output.clear()
        # extend output with holding pool
        output.extend(utilq)
        # clear holding pool
        utilq.clear()
        # return to global flow
        self._reflow()

    @contextmanager
    def _autoflow(self, **kw):
        '''switch to automatically balanced four-stage flow'''
        self.flow(flow=self._autoflow, **kw)
        getr_ = lambda x: getattr(self, x)
        incoming, workq = getr_(self._IN), getr_(self._WORK)
        utilq,  output = getr_(self._HOLD), getr_(self._OUT)
        # clear work pool
        workq.clear()
        # extend work pool with incoming
        workq.extend(incoming)
        # flow iterators
        self._iterator = self._iterexcept
        yield
        # clear output if so configured
        if self._buildup:
            output.clear()
        output.extend(utilq)
        # clear incoming
        incoming.clear()
        incoming.extend(utilq)
        # clear holding pool
        utilq.clear()
        # return to global flow
        self._reflow()

    ###########################################################################
    ## savepoint for things ###################################################
    ###########################################################################

    @staticmethod
    def _clone(self, iterable, n=2, deque_=deque):
        '''clone iterable'''
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

    def _xtend(self, things):
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

    def _append(self, things):
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
        '''number of incoming'''
        return len(self.incoming)

    count = __len__

    def countout(self):
        '''number of output'''
        return len(self.output)

    ###########################################################################
    ## clear things ###########################################################
    ###########################################################################

    def _clearh(self):
        '''clear holding pool'''
        self._util.clear()
        return self

    def _clearw(self):
        '''clear work pool'''
        self._work.clear()
        return self

    def clearin(self):
        '''clear incoming'''
        self.incoming.clear()
        return self

    def clearout(self):
        '''clear output'''
        self.output.clear()
        return self


class OutputMixin(ActiveMixin, OutflowMixin):

    '''lazy output knife mixin'''

    def __iter__(self):
        '''yield output, clearing output as it iterates'''
        return self._iterexcept(self._OUT)

    def end(self):
        '''return output and clear out everything'''
        # revert to default flow
        self.unflow()
        wrap, output = self._wrapper, self.output
        wrap = self.output.pop() if len(output) == 1 else wrap(output)
        # clear every last thing
        self.clear()._clearsp()
        return wrap

    def peek(self):
        '''snapshot of current output'''
        out = deque(self.output)
        return out.pop() if len(out) == 1 else self._wrapper(out)

    def out(self):
        '''clear output and return outgoing things'''
        self.unflow()
        wrap, output = self._wrapper, self.output
        wrap = output.pop() if len(output) == 1 else wrap(output)
        # clear outgoing things
        self.clearout()
        return wrap


class activeknife(
    OutputMixin, FilterMixin, MapMixin, ReduceMixin, OrderMixin, ExtractMixin,
    SliceMixin, TruthMixin, MathMixin, RepeatMixin, RandomMixin,
):

    '''active knife'''

    __slots__ = SLOTS


class collectknife(OutputMixin, ExtractMixin):

    '''collecting knife'''

    __slots__ = SLOTS


class sliceknife(OutputMixin, SliceMixin):

    '''slice knife'''

    __slots__ = SLOTS


class filterknife(OutputMixin, FilterMixin):

    '''filter knife'''

    __slots__ = SLOTS


class repeatknife(OutputMixin, RepeatMixin):

    '''repeat knife'''

    __slots__ = SLOTS


class mapknife(OutputMixin, MapMixin):

    '''mapping knife'''

    __slots__ = SLOTS


class randomknife(OutputMixin, RandomMixin):

    '''randomizing knife'''

    __slots__ = SLOTS


class orderknife(OutputMixin, OrderMixin):

    '''ordering knife'''

    __slots__ = SLOTS


class mathknife(OutputMixin, MathMixin):

    '''mathing knife'''

    __slots__ = SLOTS


class truthknife(OutputMixin, TruthMixin):

    '''truthing knife'''

    __slots__ = SLOTS


class reduceknife(OutputMixin, ReduceMixin):

    '''reducing knife'''

    __slots__ = SLOTS
