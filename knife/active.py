# -*- coding: utf-8 -*-
'''actively evaluating knives'''

from itertools import repeat
from collections import deque
from contextlib import contextmanager

from stuf.utils import clsname

from knife.map import RepeatMixin, MapMixin
from knife.reduce import SliceMixin, ReduceMixin
from knife.filter import FilterMixin, CollectMixin
from knife.base import SLOTS, KnifeMixin, OutflowMixin
from knife.analyze import StatsMixin, TruthMixin, OrderMixin


class ActiveMixin(KnifeMixin):

    '''active knife mixin'''

    def __init__(self, *things, **kw):
        '''
        init

        @param *things: wannabe incoming things
        '''
        # if just one thing, put it in inflow or put everything in inflow
        try:
            inflow = deque(things[0]) if len(things) == 1 else deque(things)
        except TypeError:
            # handle non-iterable incoming things with length
            inflow = deque()
            inflow.append(things)
        super(ActiveMixin, self).__init__(inflow, deque(), **kw)
        # assign default iterator
        self._iterator = self._iterexcept
        # work stage
        self._work = deque()
        # holding stage
        self._hold = deque()

    ###########################################################################
    ## flow things ############################################################
    ###########################################################################

    @contextmanager
    def _flow2(self, **kw):
        '''switch to a manually balanced two-stage flow'''
        self._as_flow(
            flow=self._flow2, outflow=kw.get(self._OUTCFG, self._INVAR), **kw
        )._clearworking()
        outflow = getattr(self, self._OUT)
        # move outgoing (usually incoming) things up to work stage
        getattr(self, self._WORK).extend(outflow)
        # assign flow iterator
        self._iterator = self._breakcount
        yield
        # clear outflow
        if self._buildup:
            outflow.clear()
        # move things from holding state to outflow
        outflow.extend(getattr(self, self._HOLD))
        # clear work & holding stage & return to current selected flow
        self._clearworking()._reflow()

    @contextmanager
    def _flow3(self, **kw):
        '''switch to a manually balanced three-stage flow'''
        self._as_flow(
            hold=kw.get(self._WORKCFG, self._WORKVAR), flow=self._flow3, **kw
        )._clearworking()
        # move incoming things up to work stage
        getattr(self, self._WORK).extend(getattr(self, self._IN))
        # assign flow iterator
        self._iterator = self._breakcount
        yield
        outflow = getattr(self, self._OUT)
        # clear outflow
        if self._buildup:
            outflow.clear()
        # move things from holding state to outflow
        outflow.extend(getattr(self, self._HOLD))
        # clear work, holding stages & return to current selected flow
        self._clearworking()._reflow()

    @contextmanager
    def _flow4(self, **kw):
        '''switch to a manually balanced four-stage flow'''
        self._as_flow(flow=self._flow4, **kw)._clearworking()
        # move incoming things up to work stage
        getattr(self, self._WORK).extend(getattr(self, self._IN))
        # assign flow iterator
        self._iterator = self._iterexcept
        yield
        outflow = getattr(self, self._OUT)
        # clear outflow
        if self._buildup:
            outflow.clear()
        # extend outgoing things with holding stage
        outflow.extend(getattr(self, self._HOLD))
        # clear work, holding stages & return to current selected flow
        self._clearworking()._reflow()

    @contextmanager
    def _autoflow(self, **kw):
        '''switch to an automatically balanced four-stage flow'''
        self._as_flow(flow=self._autoflow, **kw)._clearworking()
        inflow = getattr(self, self._IN)
        # move incoming things up to work stage
        getattr(self, self._WORK).extend(inflow)
        # assign flow iterator
        self._iterator = self._iterexcept
        yield
        outflow = getattr(self, self._OUT)
        # clear outflow
        if self._buildup:
            outflow.clear()
        # extend outgoing things with holding stage
        hold = getattr(self, self._HOLD)
        outflow.extend(hold)
        # extend incoming things with holding stage
        inflow.clear()
        inflow.extend(hold)
        # clear work, holding stages & return to current selected flow
        self._clearworking()._reflow()

    ###########################################################################
    ## iterate things #########################################################
    ###########################################################################

    def _breakcount(self, attr='_HOLD', repeat_=repeat, len_=len, g=getattr):
        '''
        breakcount iterator

        @param attr: stage to iterate over
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
        '''iterable derived from a stage in the flow'''
        return self._iterator(self._WORK)

    ###########################################################################
    ## extend things ##########################################################
    ###########################################################################

    def _xtend(self, things, getattr_=getattr):
        '''extend the holding stage with `things`'''
        getattr_(self, self._HOLD).extend(things)
        return self

    def _xtendfront(self, things, getattr_=getattr):
        '''
        extend holding stage with `things` placed in front of anything already
        in the holding stage
        '''
        getattr_(self, self._HOLD).extendleft(things)
        return self

    ###########################################################################
    ## append things ##########################################################
    ###########################################################################

    def _append(self, things, getattr_=getattr):
        '''append `things` to the holding stage'''
        getattr_(self, self._HOLD).append(things)
        return self

    def _appendfront(self, things, getattr_=getattr):
        '''
        append `things` to the holding stage in front of anything already in
        the holding stage
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
            self._context,
        )

    def __len__(self):
        '''Number of incoming things.'''
        return len(self._inflow)

    count = __len__

    def countout(self):
        '''Number of outgoing things.'''
        return len(self._outflow)

    ###########################################################################
    ## clear things ###########################################################
    ###########################################################################

    def _clearworking(self):
        '''clear working and holding stages'''
        # clear work stage
        self._work.clear()
        # clear holding stage
        self._hold.clear()
        return self

    def _clearh(self):
        '''Clear holding stage.'''
        self._hold.clear()
        return self

    def _clearw(self):
        '''Clear work stage.'''
        self._work.clear()
        return self

    def clearin(self):
        '''Clear inflow stage.'''
        self._inflow.clear()
        return self

    def clearout(self):
        '''Clear outflow stage.'''
        self._outflow.clear()
        return self


class OutputMixin(ActiveMixin, OutflowMixin):

    '''lazy output knife mixin'''

    def __iter__(self):
        '''Yield outgoing things, clearing outflow as it goes.'''
        return self._iterexcept(self._OUT)

    def end(self):
        '''Return outgoing things and clear out everything.'''
        self._unflow()
        wrap, outflow = self._wrapper, self._outflow
        value = outflow.pop() if len(outflow) == 1 else wrap(outflow)
        # clear every last thing
        self.clear()._clearsp()
        return value

    def preview(self):
        '''Take a peek at the current state of outgoing things.'''
        outflow, wrap = deque(self._outflow), self._wrapper
        return outflow.pop() if len(outflow) == 1 else wrap(outflow)

    def results(self):
        '''Return outgoing things and clear outflow.'''
        self._unflow()
        wrap, outflow = self._wrapper, self._outflow
        value = outflow.pop() if len(outflow) == 1 else wrap(outflow)
        # clear outflow
        self.clearout()
        # restore baseline if in query context
        if self._context == self._QUERY:
            self.undo(baseline=True)
        return value


class activeknife(
    OutputMixin, FilterMixin, MapMixin, ReduceMixin, OrderMixin, CollectMixin,
    SliceMixin, TruthMixin, StatsMixin, RepeatMixin,
):

    '''active knife'''

    __slots__ = SLOTS


class collectknife(OutputMixin, CollectMixin):

    '''collecting knife'''

    __slots__ = SLOTS


class sliceknife(OutputMixin, SliceMixin):

    '''slicing knife'''

    __slots__ = SLOTS


class filterknife(OutputMixin, FilterMixin):

    '''filtering knife'''

    __slots__ = SLOTS


class repeatknife(OutputMixin, RepeatMixin):

    '''repeating knife'''

    __slots__ = SLOTS


class mapknife(OutputMixin, MapMixin):

    '''mapping knife'''

    __slots__ = SLOTS


class orderknife(OutputMixin, OrderMixin):

    '''ordering knife'''

    __slots__ = SLOTS


class mathknife(OutputMixin, StatsMixin):

    '''mathing knife'''

    __slots__ = SLOTS


class truthknife(OutputMixin, TruthMixin):

    '''truthing knife'''

    __slots__ = SLOTS


class reduceknife(OutputMixin, ReduceMixin):

    '''reducing knife'''

    __slots__ = SLOTS
