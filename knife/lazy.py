# -*- coding: utf-8 -*-
'''lazily evaluated knives'''

from itertools import tee, chain
from contextlib import contextmanager

from stuf.utils import clsname

from knife.map import RepeatMixin, MapMixin
from knife.reduce import SliceMixin, ReduceMixin
from knife.filter import FilterMixin, CollectMixin
from knife.base import SLOTS, KnifeMixin, OutflowMixin
from knife.analyze import StatsMixin, TruthMixin, OrderMixin


class LazyMixin(KnifeMixin):

    '''lazy knife mixin'''

    def __init__(self, *things, **kw):
        '''
        init

        @param *things: wannabe incoming things
        '''
        # if just one thing, put it in inflow or put everything in inflow
        inflow = iter([things[0]]) if len(things) == 1 else iter(things)
        super(LazyMixin, self).__init__(inflow, iter([]), **kw)
        # work stage
        self._work = iter([])
        # holding stage
        self._hold = iter([])

    ###########################################################################
    ## flow things ############################################################
    ###########################################################################

    @contextmanager
    def _flow2(self, **kw):
        '''switch to a manually balanced two-stage flow'''
        self._as_flow(
            flow=self._flow2, outflow=kw.get(self._OUTCFG, self._INVAR), **kw
        )._clearworking()
        # move outgoing things up to work stage
        work, outflow = tee(getattr(self, self._OUT))
        setattr(self, self._WORK, work)
        setattr(self, self._OUT, outflow)
        yield
        # move things from holding state to outflow
        hold = getattr(self, self._HOLD)
        setattr(
            self,
            outflow,
            hold if self._buildup else chain(hold, getattr(self, self._OUT)),
        )
        # clear work & holding stage & return to current selected flow
        self._clearworking()._reflow()

    @contextmanager
    def _flow3(self, **kw):
        '''switch to a manually balanced three-stage flow'''
        self._as_flow(
            hold=kw.get(self._WORKCFG, self._WORKVAR), flow=self._flow3, **kw
        )._clearworking()
        # move incoming things up to work stage
        work, incoming = tee(getattr(self, self._IN))
        setattr(self, self._WORK, work)
        setattr(self, self._IN, incoming)
        yield
        # move things from holding state to outflow
        hold = getattr(self, self._HOLD)
        setattr(
            self,
            self._OUT,
            hold if self._buildup else chain(hold, getattr(self, self._OUT)),
        )
        # clear work, holding stages & return to current selected flow
        self._clearworking()._reflow()

    @contextmanager
    def _flow4(self, **kw):
        '''switch to a manually balanced four-stage flow'''
        self._as_flow(flow=self._flow4, **kw)._clearworking()
        # move incoming things up to work stage
        work, incoming = tee(getattr(self, self._IN))
        setattr(self, self._WORK, work)
        setattr(self, self._IN, incoming)
        yield
        # extend outgoing things with holding stage
        hold = getattr(self, self._HOLD)
        setattr(
            self,
            self._OUT,
            hold if self._buildup else chain(hold, getattr(self, self._OUT)),
        )
        # clear work, holding stages & return to current selected flow
        self._clearworking()._reflow()

    @contextmanager
    def _autoflow(self, **kw):
        '''switch to an automatically balanced four-stage flow'''
        self._as_flow(flow=self._autoflow, **kw)._clearworking()
        # move incoming things up to work stage
        work, incoming = tee(getattr(self, self._IN))
        setattr(self, self._WORK, work)
        setattr(self, self._IN, incoming)
        yield
        # move things from holding stage to inflow and outflow
        incoming, out = tee(getattr(self, self._HOLD))
        setattr(
            self,
            self._OUT,
            out if self._buildup else chain(out, getattr(self, self._OUT)),
        )
        setattr(self, self._IN, incoming)
        # clear work, holding stages & return to current selected flow
        self._clearworking()._reflow()

    ###########################################################################
    ## iterate things #########################################################
    ###########################################################################

    @property
    def _iterable(self, getattr_=getattr):
        '''iterable'''
        return getattr_(self, self._WORK)

    ###########################################################################
    ## extend things ##########################################################
    ###########################################################################

    def _xtend(self, things, chain_=chain, getattr_=getattr):
        '''extend holding stage with `things`'''
        setattr(
            self,
            self._HOLD,
            chain_(things, getattr_(self, self._HOLD)))
        return self

    def _xtendfront(self, things, reversed_=reversed):
        '''extend before of holding stage with `things`'''
        return self._xtend(reversed_(things))

    ###########################################################################
    ## append things ##########################################################
    ###########################################################################

    def _append(self, things, chain_=chain, iter_=iter, getattr_=getattr):
        '''append `things` to holding stage'''
        setattr(
            self,
            self._HOLD,
            chain_(getattr_(self, self._HOLD), iter_([things])),
        )
        return self

    def _appendfront(self, things, iter_=iter):
        '''append `things` before of holding stage'''
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
            self._context,
        )

    def __len__(self):
        '''Number of incoming things.'''
        self._inflow, incoming = tee(self._inflow)
        return len(list(incoming))

    count = __len__

    def countout(self):
        '''Number of outgoing things.'''
        self._outflow, outflow = tee(self._outflow)
        return len(list(outflow))

    ###########################################################################
    ## clear things ###########################################################
    ###########################################################################

    def _clearworking(self, iter_=iter):
        '''clear working and holding stages'''
        # clear work stage
        delattr(self, self._WORK)
        setattr(self, self._WORK, iter_([]))
        # clear holding stage
        delattr(self, self._HOLD)
        setattr(self, self._HOLD, iter_([]))
        return self

    def _clearh(self):
        '''Clear holding stage.'''
        delattr(self, self._HOLD)
        setattr(self, self._HOLD, iter([]))
        return self

    def _clearw(self):
        '''Clear work stage.'''
        delattr(self, self._WORK)
        setattr(self, self._WORK, iter([]))
        return self

    def clearin(self):
        '''Clear inflow stage.'''
        delattr(self, self._IN)
        setattr(self, self._IN, iter([]))
        return self

    def clearout(self):
        '''Clear outflow stage.'''
        delattr(self, self._OUT)
        setattr(self, self._OUT, iter([]))
        return self


class OutputMixin(LazyMixin, OutflowMixin):

    '''active output knife mixin'''

    def __iter__(self):
        '''Yield outgoing things, clearing outflow as it goes.'''
        return getattr(self, self._OUT)

    def end(self):
        '''Return outgoing things and clear out everything.'''
        self._unflow()
        outflow, tell = tee(self._outflow)
        wrap = self._wrapper
        results = next(outflow) if len(wrap(tell)) == 1 else wrap(outflow)
        # clear every last thing
        self.clear()._clearsp()
        self._baseline = self._original = None
        return results

    def preview(self):
        '''Take a peek at the current state of outgoing things.'''
        outflow, tell, self._outflow = tee(getattr(self, self._OUT), 3)
        wrap = self._wrapper
        return outflow.pop() if len(wrap(tell)) == 1 else wrap(outflow)

    def results(self):
        '''Return outgoing things and clear outflow.'''
        self._unflow()
        outflow, tell = tee(self._outflow)
        wrap = self._wrapper
        results = next(outflow) if len(wrap(tell)) == 1 else wrap(outflow)
        # clear outflow
        self.clearout()
        # restore baseline if in query context
        if self._context == self._QUERY:
            self.undo(baseline=True)
        return results


class lazyknife(
    OutputMixin, FilterMixin, MapMixin, ReduceMixin, OrderMixin, CollectMixin,
    SliceMixin, TruthMixin, StatsMixin, RepeatMixin,
):

    '''lazy knife'''

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
