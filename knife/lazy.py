# -*- coding: utf-8 -*-
'''lazily evaluated knives'''

from itertools import tee, chain
from contextlib import contextmanager

from stuf.utils import clsname

from knife.output import OutflowMixin
from knife.base import SLOTS, KnifeMixin
from knife.map import RepeatMixin, MapMixin
from knife.reduce import SliceMixin, ReduceMixin
from knife.filter import FilterMixin, ExtractMixin
from knife.analyze import StatsMixin, TruthMixin, OrderMixin


class LazyMixin(KnifeMixin):

    '''lazy knife mixin'''

    def __init__(self, *things, **kw):
        incoming = iter([things[0]]) if len(things) == 1 else iter(things)
        super(LazyMixin, self).__init__(incoming, iter([]), **kw)
        # work pool
        self._work = iter([])
        # holding pool
        self._hold = iter([])

    ###########################################################################
    ## mode things ############################################################
    ###########################################################################

    def as_view(self):
        '''_as_flow to as_view mode'''
        with self._flow3(outflow=self._HOLDVAR, keep=False):
            self._xreplace(self._iterable)
        with self._flow1(hard=True, workq=self._HOLDVAR, keep=False):
            self._context = self._QUERY
            return self

    ###########################################################################
    ## _as_flow things ############################################################
    ###########################################################################

    @contextmanager
    def _flow2(self, **kw):
        '''switch to manually balanced two-stage _as_flow'''
        self._as_flow(
            _as_flow=self._flow2, output=kw.get(self._OUTCFG, self._INVAR), **kw
        )._clearworking()
        setr_ = lambda x, y: setattr(self, x, y)
        getr_ = lambda x: getattr(self, x)
        outflow = self._OUT
        # extend work pool with _outflow
        work, wrap = tee(getr_(outflow))
        setr_(self._WORK, work)
        setr_(outflow, wrap)
        yield
        # extend _outflow with holding pool
        hold = getr_(self._HOLD)
        setr_(
            outflow,
            hold if self._buildup else chain(hold, getr_(outflow)),
        )
        self._clearworking()
        # return to global _as_flow
        self._reflow()

    @contextmanager
    def _flow3(self, **kw):
        '''switch to manually balanced three-stage _as_flow'''
        self._as_flow(
            holdq=kw.get(self._WORKCFG, self._WORKVAR), _as_flow=self._flow3, **kw
        )._clearworking()
        setr_ = lambda x, y: setattr(self, x, y)
        getr_ = lambda x: getattr(self, x)
        INQ = self._IN
        # extend work pool with _inflow
        work, incoming = tee(getr_(INQ))
        setr_(self._WORK, work)
        setr_(INQ, incoming)
        yield
        # extend _outflow with holding pool
        hold = getr_(self._HOLD)
        setr_(
            self._OUT,
            hold if self._buildup else chain(hold, getr_(self._OUT)),
        )
        self._clearworking()
        # revert to current _as_flow
        self._reflow()

    @contextmanager
    def _flow4(self, **kw):
        '''switch to manually balanced four-stage _as_flow'''
        self._as_flow(_as_flow=self._flow4, **kw)._clearworking()
        setr_ = lambda x, y: setattr(self, x, y)
        getr_ = lambda x: getattr(self, x)
        INQ = self._IN
        # extend work pool with _inflow
        work, incoming = tee(getr_(INQ))
        setr_(self._WORK, work)
        setr_(INQ, incoming)
        yield
        # extend _outflow with holding pool
        hold = getr_(self._HOLD)
        setr_(
            self._OUT,
            hold if self._buildup else chain(hold, getr_(self._OUT)),
        )
        self._clearworking()
        # return to global _as_flow
        self._reflow()

    @contextmanager
    def _autoflow(self, **kw):
        '''switch to automatically balanced four-stage _as_flow'''
        self._as_flow(_as_flow=self._autoflow, **kw)._clearworking()
        setr_ = lambda x, y: setattr(self, x, y)
        getr_ = lambda x: getattr(self, x)
        INQ = self._IN
        # extend work pool with _inflow
        work, incoming = tee(getr_(INQ))
        setr_(self._WORK, work)
        setr_(INQ, incoming)
        yield
        # extend _inflow and _outflow with holding pool
        incoming, wrap = tee(getr_(self._HOLD))
        setr_(
            self._OUT,
            wrap if self._buildup else chain(wrap, getr_(self._OUT)),
        )
        setr_(INQ, incoming)
        self._clearworking()
        # return to global _as_flow
        self._reflow()

    ###########################################################################
    ## savepoint for things ###################################################
    ###########################################################################

    @staticmethod
    def _clone(self, iterable, n=2, tee_=tee):
        '''clone iterable'''
        return tee_(iterable, n)

    ###########################################################################
    ## iterate things #########################################################
    ###########################################################################

    @property
    def _iterable(self):
        '''iterable'''
        return getattr(self, self._WORK)

    ###########################################################################
    ## extend things ##########################################################
    ###########################################################################

    def _xtend(self, things):
        '''extend holding pool with `things`'''
        setattr(self, self._HOLD, chain(things, getattr(self, self._HOLD)))
        return self

    def _xtendleft(self, things):
        '''extend before of holding pool with `things`'''
        return self._xtend(reversed(things))

    def _xreplace(self, things):
        '''replace holding pool with `things`'''
        setattr(self, self._HOLD, things)
        return self

    def _iter(self, things):
        '''extend work pool with `things` wrapped in iterator'''
        return self._xtend(iter(things))

    ###########################################################################
    ## append things ##########################################################
    ###########################################################################

    def _append(self, things):
        '''append `things` to holding pool'''
        setattr(
            self, self._HOLD, chain(getattr(self, self._HOLD), iter([things])),
        )
        return self

    def _appendleft(self, things):
        '''append `things` before of holding pool'''
        return self._xtend(iter([things]))

    ###########################################################################
    ## know things ############################################################
    ###########################################################################

    def __repr__(self):
        list_, tee_ = list, tee
        setr_ = lambda x, y: setattr(self, x, y)
        getr_ = lambda x: getattr(self, x)
        in1, in2 = tee_(getr_(self._IN))
        setr_(self._IN, in1)
        out1, out2 = tee_(getr_(self._OUT))
        setr_(self._OUT, out1)
        work1, work2 = tee_(getr_(self._WORK))
        setr_(self._WORK, work1)
        hold1, hold2 = tee_(getr_(self._HOLD))
        setr_(self._HOLD, hold1)
        return self._repr(
            self.__module__,
            clsname(self),
            self._IN,
            list_(in2),
            self._WORK,
            list_(work2),
            self._HOLD,
            list_(hold2),
            self._OUT,
            list_(out2),
            self._context,
        )

    def __len__(self):
        '''number of _inflow'''
        self._inflow, incoming = tee(self._inflow)
        return len(list(incoming))

    count = __len__

    def countout(self):
        '''number of _outflow'''
        self._outflow, outflow = tee(self._outflow)
        return len(list(outflow))

    ###########################################################################
    ## clear things ###########################################################
    ###########################################################################

    def _clearworking(self):
        '''clear work pool and holding pool'''
        iter_ = iter
        setr_ = lambda x, y: setattr(self, x, y)
        delr_ = lambda x: delattr(self, x)
        # clear work pool
        delr_(self._WORK)
        setr_(self._WORK, iter_([]))
        # clear holding pool
        delr_(self._HOLD)
        setr_(self._HOLD, iter_([]))
        return self

    def _clearh(self):
        '''clear holding pool'''
        delattr(self, self._HOLD)
        setattr(self, self._HOLD, iter([]))
        return self

    def _clearw(self):
        '''clear work pool'''
        delattr(self, self._WORK)
        setattr(self, self._WORK, iter([]))
        return self

    def clearin(self):
        '''clear _inflow'''
        delattr(self, self._IN)
        setattr(self, self._IN, iter([]))
        return self

    def clearout(self):
        '''clear _outflow'''
        delattr(self, self._OUT)
        setattr(self, self._OUT, iter([]))
        return self


class OutputMixin(LazyMixin, OutflowMixin):

    '''active output knife mixin'''

    def __iter__(self):
        '''yield _outflow, clearing _outflow as it iterates'''
        return getattr(self, self._OUT)

    def close(self):
        '''return _outflow and clear out everything'''
        # revert to default _as_flow
        self._unflow()
        out, tell = tee(self._outflow)
        wrap = self._wrapper
        wrap = next(out) if len(wrap(tell)) == 1 else wrap(out)
        # clear every last thing
        self.clear()._clearsp()
        return wrap

    def peek(self):
        '''snapshot of current _outflow'''
        out, tell, self._outflow = tee(getattr(self, self._OUT), 3)
        wrap = self._wrapper
        return wrap(out).pop() if len(wrap(tell)) == 1 else wrap(out)

    def out(self):
        '''return _outflow and clear _outflow'''
        # revert to default _as_flow
        self._unflow()
        out, tell = tee(self._outflow)
        wrap = self._wrapper
        wrap = next(out) if len(wrap(tell)) == 1 else wrap(out)
        # clear _outflow
        self.clearout()
        if self._context == self._QUERY:
            self.baseline()
        return wrap


class lazyknife(
    OutputMixin, FilterMixin, MapMixin, ReduceMixin, OrderMixin, ExtractMixin,
    SliceMixin, TruthMixin, StatsMixin, RepeatMixin,
):

    '''lazy knife'''

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


class orderknife(OutputMixin, OrderMixin):

    '''ordering knife'''

    __slots__ = SLOTS


class mathknife(OutputMixin, StatsMixin):

    '''math knife'''

    __slots__ = SLOTS


class truthknife(OutputMixin, TruthMixin):

    '''truth knife'''

    __slots__ = SLOTS


class reduceknife(OutputMixin, ReduceMixin):

    '''reduce knife'''

    __slots__ = SLOTS
