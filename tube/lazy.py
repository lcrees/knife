# -*- coding: utf-8 -*-
'''lazily evaluated tubing'''

from itertools import tee, chain
from contextlib import contextmanager

from stuf.utils import clsname

from tube.mapping import RepeatMixin, MapMixin
from tube.base import SLOTS, TubeMixin, OutflowMixin
from tube.ordering import RandomMixin, OrderMixin
from tube.reducing import MathMixin, TruthMixin, ReduceMixin
from tube.filtering import FilterMixin, ExtractMixin, SliceMixin


class LazyMixin(TubeMixin):

    '''lazy tubing'''

    def __init__(self, *things, **kw):
        inflow = iter([things[0]]) if len(things) == 1 else iter(things)
        super(LazyMixin, self).__init__(inflow, iter([]))
        # work pool
        self._work = iter([])
        # holding pool
        self._util = iter([])

    ###########################################################################
    ## mode things ############################################################
    ###########################################################################

    def query(self):
        '''flow to query mode'''
        with self._flow3(outflow=self._HOLDVAR, keep=False):
            self._xreplace(self._iterable)
        with self._flow1(hard=True, workq=self._HOLDVAR, keep=False):
            self._channel = self._QUERY
            return self

    ###########################################################################
    ## flow things ############################################################
    ###########################################################################

    @contextmanager
    def _flow2(self, **kw):
        '''switch to manual two-stage flow'''
        self.flow(
            flow=self._flow2, outflow=kw.get(self._OUTCFG, self._INVAR), **kw
        )._clearworking()
        setr_ = lambda x, y: setattr(self, x, y)
        getr_ = lambda x: getattr(self, x)
        outflow = self._OUT
        # extend work pool with outflow
        work, wrap = tee(getr_(outflow))
        setr_(self._WORK, work)
        setr_(outflow, wrap)
        yield
        # extend outflow with holding pool
        util = getr_(self._HOLD)
        setr_(
            outflow,
            util if self._buildup else chain(util, getr_(outflow)),
        )
        self._clearworking()
        # return to global flow
        self._reflow()

    @contextmanager
    def _flow3(self, **kw):
        '''switch to manual three-stage flow'''
        self.flow(
            utilq=kw.get(self._WORKCFG, self._WORKVAR), flow=self._flow3, **kw
        )._clearworking()
        setr_ = lambda x, y: setattr(self, x, y)
        getr_ = lambda x: getattr(self, x)
        INQ = self._IN
        # extend work pool with inflow
        work, inflow = tee(getr_(INQ))
        setr_(self._WORK, work)
        setr_(INQ, inflow)
        yield
        # extend outflow with holding pool
        util = getr_(self._HOLD)
        setr_(
            self._OUT,
            util if self._buildup else chain(util, getr_(self._OUT)),
        )
        self._clearworking()
        # revert to current flow
        self._reflow()

    @contextmanager
    def _flow4(self, **kw):
        '''switch to manual four-stage flow'''
        self.flow(flow=self._flow4, **kw)._clearworking()
        setr_ = lambda x, y: setattr(self, x, y)
        getr_ = lambda x: getattr(self, x)
        INQ = self._IN
        # extend work pool with inflow
        work, inflow = tee(getr_(INQ))
        setr_(self._WORK, work)
        setr_(INQ, inflow)
        yield
        # extend outflow with holding pool
        util = getr_(self._HOLD)
        setr_(
            self._OUT,
            util if self._buildup else chain(util, getr_(self._OUT)),
        )
        self._clearworking()
        # return to global flow
        self._reflow()

    @contextmanager
    def _autoflow(self, **kw):
        '''switch to auto-balanced four-stage flow'''
        self.flow(flow=self._autoflow, **kw)._clearworking()
        setr_ = lambda x, y: setattr(self, x, y)
        getr_ = lambda x: getattr(self, x)
        INQ = self._IN
        # extend work pool with inflow
        work, inflow = tee(getr_(INQ))
        setr_(self._WORK, work)
        setr_(INQ, inflow)
        yield
        # extend inflow and outflow with holding pool
        inflow, wrap = tee(getr_(self._HOLD))
        setr_(
            self._OUT,
            wrap if self._buildup else chain(wrap, getr_(self._OUT)),
        )
        setr_(INQ, inflow)
        self._clearworking()
        # return to global flow
        self._reflow()

    ###########################################################################
    ## savepoint for things ###################################################
    ###########################################################################

    @staticmethod
    def _clone(self, iterable, num=2, tee_=tee):
        '''clone an iterable'''
        return tee_(iterable, num)

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
        util1, util2 = tee_(getr_(self._HOLD))
        setr_(self._HOLD, util1)
        return self._repr(
            self.__module__,
            clsname(self),
            self._IN,
            list_(in2),
            self._WORK,
            list_(work2),
            self._HOLD,
            list_(util2),
            self._OUT,
            list_(out2),
            self._channel,
        )

    def __len__(self):
        '''number of inflow'''
        self.inflow, inflow = tee(self.inflow)
        return len(list(inflow))

    count = __len__

    def countout(self):
        '''number of outflow'''
        self.outflow, outflow = tee(self.outflow)
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

    def _clearu(self):
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
        '''clear inflow'''
        delattr(self, self._IN)
        setattr(self, self._IN, iter([]))
        return self

    def clearout(self):
        '''clear outflow'''
        delattr(self, self._OUT)
        setattr(self, self._OUT, iter([]))
        return self


class OutputMixin(LazyMixin, OutflowMixin):

    '''active output tubing mixin'''

    def __iter__(self):
        '''yield outflow, clearing outflow as it iterates'''
        return getattr(self, self._OUT)

    def end(self):
        '''return outflow and clear out everything'''
        # revert to default flow
        self.unflow()
        out, tell = tee(self.outflow)
        wrap = self._wrapper
        wrap = next(out) if len(wrap(tell)) == 1 else wrap(out)
        # clear every last thing
        self.clear()._clearsp()
        return wrap

    def snapshot(self):
        '''snapshot of current outflow'''
        out, tell, self.outflow = tee(getattr(self, self._OUT), 3)
        wrap = self._wrapper
        return wrap(out).pop() if len(wrap(tell)) == 1 else wrap(out)

    def out(self):
        '''return outflow and clear outflow'''
        # revert to default flow
        self.unflow()
        out, tell = tee(self.outflow)
        wrap = self._wrapper
        wrap = next(out) if len(wrap(tell)) == 1 else wrap(out)
        # clear outflow
        self.clearout()
        return wrap


class lazytube(
    OutputMixin, FilterMixin, MapMixin, ReduceMixin, OrderMixin, ExtractMixin,
    SliceMixin, TruthMixin, MathMixin, RepeatMixin, RandomMixin,
):

    '''lazy tubing'''

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
