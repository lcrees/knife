# -*- coding: utf-8 -*-
'''lazily evaluated tubings'''

from itertools import tee, chain
from contextlib import contextmanager

from stuf.utils import clsname

from tube.change import StringMixin
from tube.base import SLOTS, TubeMixin
from tube.mapping import RepeatMixin, MapMixin
from tube.order import RandomMixin, OrderMixin
from tube.reducing import MathMixin, TruthMixin, ReduceMixin
from tube.filtering import FilterMixin, ExtractMixin, SetMixin, SliceMixin


class LazyMixin(TubeMixin):

    '''base lazy tubing'''

    def __init__(self, *things, **kw):
        inflow = iter([things[0]]) if len(things) == 1 else iter(things)
        super(LazyMixin, self).__init__(inflow, iter([]))
        # work things
        self._work = iter([])
        # utility things
        self._util = iter([])

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
        util1, util2 = tee_(getr_(self._UTIL))
        setr_(self._UTIL, util1)
        return self._repr(
            self.__module__,
            clsname(self),
            self.channel.upper(),
            self._IN,
            list_(in2),
            self._WORK,
            list_(work2),
            self._UTIL,
            list_(util2),
            self._OUT,
            list_(out2),
            id(self),
        )

    ###########################################################################
    ## mode things ############################################################
    ###########################################################################

    def query(self):
        '''flow to query mode'''
        with self.flow3(outflow=self._UTILVAR, keep=False):
            self._xreplace(self._iterable)
        with self.flow1(hard=True, workq=self._UTILVAR, keep=False):
            self.channel = self._QUERY
            return self

    ###########################################################################
    ## flow things #########################################################
    ###########################################################################

    @contextmanager
    def flow2(self, **kw):
        '''two-step flow'''
        self.flow(
            flow=self.flow2, outflow=kw.get(self._OUTCFG, self._INVAR), **kw
        )._clearworking()
        setr_ = lambda x, y: setattr(self, x, y)
        getr_ = lambda x: getattr(self, x)
        OUTQ = self._OUT
        # extend work things with outflow
        work, wrap = tee(getr_(OUTQ))
        setr_(self._WORK, work)
        setr_(OUTQ, wrap)
        yield
        # extend outflow with utility things
        util = getr_(self._UTIL)
        setr_(
            self._OUT,
            util if self._buildup else chain(util, getr_(self._OUT)),
        )
        self._clearworking()
        # return to global flow
        self.reflow()

    @contextmanager
    def flow3(self, **kw):
        '''three-step flow'''
        self.flow(
            utilq=kw.get(self._WORKCFG, self._WORKVAR), flow=self.flow3, **kw
        )._clearworking()
        setr_ = lambda x, y: setattr(self, x, y)
        getr_ = lambda x: getattr(self, x)
        INQ = self._IN
        # extend work things with inflow
        work, inflow = tee(getr_(INQ))
        setr_(self._WORK, work)
        setr_(INQ, inflow)
        yield
        # extend outflow with utility things
        util = getr_(self._UTIL)
        setr_(
            self._OUT,
            util if self._buildup else chain(util, getr_(self._OUT)),
        )
        self._clearworking()
        # return to global flow
        self.reflow()

    @contextmanager
    def flow4(self, **kw):
        '''four-step flow'''
        self.flow(flow=self.flow4, **kw)._clearworking()
        setr_ = lambda x, y: setattr(self, x, y)
        getr_ = lambda x: getattr(self, x)
        INQ = self._IN
        # extend work things with inflow
        work, inflow = tee(getr_(INQ))
        setr_(self._WORK, work)
        setr_(INQ, inflow)
        yield
        # extend outflow with utility things
        util = getr_(self._UTIL)
        setr_(
            self._OUT,
            util if self._buildup else chain(util, getr_(self._OUT)),
        )
        self._clearworking()
        # return to global flow
        self.reflow()

    @contextmanager
    def autoflow(self, **kw):
        '''automatic four-step flow'''
        self.flow(flow=self.autoflow, **kw)._clearworking()
        setr_ = lambda x, y: setattr(self, x, y)
        getr_ = lambda x: getattr(self, x)
        INQ = self._IN
        # extend work things with inflow
        work, inflow = tee(getr_(INQ))
        setr_(self._WORK, work)
        setr_(INQ, inflow)
        yield
        # extend inflow and outflow with utility things
        inflow, wrap = tee(getr_(self._UTIL))
        setr_(
            self._OUT,
            wrap if self._buildup else chain(wrap, getr_(self._OUT)),
        )
        setr_(INQ, inflow)
        self._clearworking()
        # return to global flow
        self.reflow()

    ###########################################################################
    ## savepoint for things ###################################################
    ###########################################################################

    @staticmethod
    def _clone(self, iterable, num=2, tee_=tee):
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

    def _xtend(self, thing):
        '''build chain'''
        setattr(self, self._UTIL, chain(thing, getattr(self, self._UTIL)))
        return self

    __buildchain = _xtend

    def _xtendleft(self, things):
        '''extend left side of work things with `things`'''
        return self.__buildchain(reversed(things))

    def _xreplace(self, thing):
        '''build chain'''
        setattr(self, self._UTIL, thing)
        return self

    def _iter(self, things):
        '''extend work things with `things` wrapped in iterator'''
        return self.__buildchain(iter(things))

    ###########################################################################
    ## append things ##########################################################
    ###########################################################################

    def _append(self, things):
        '''append `things` to work things'''
        UTILQ = self._UTIL
        setattr(self, UTILQ, chain(getattr(self, UTILQ), iter([things])))
        return self

    def _appendleft(self, things):
        '''append `things` to left side of work things'''
        return self.__buildchain(iter([things]))

    ###########################################################################
    ## know things ############################################################
    ###########################################################################

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
        '''clear work things and utility things'''
        iter_ = iter
        setr_ = lambda x, y: setattr(self, x, y)
        delr_ = lambda x: delattr(self, x)
        WORKQ, UTILQ = self._WORK, self._UTIL
        # clear work things
        delr_(WORKQ)
        setr_(WORKQ, iter_([]))
        # clear utility things
        delr_(UTILQ)
        setr_(UTILQ, iter_([]))
        return self

    def _clearu(self):
        '''clear utility things'''
        UTILQ = self._UTIL
        delattr(self, UTILQ)
        setattr(self, UTILQ, iter([]))
        return self

    def _clearw(self):
        '''clear work things'''
        WORKQ = self._WORK
        delattr(self, WORKQ)
        setattr(self, WORKQ, iter([]))
        return self

    def clearin(self):
        '''clear inflow'''
        INQ = self._IN
        delattr(self, INQ)
        setattr(self, INQ, iter([]))
        return self

    def clearout(self):
        '''clear outflow'''
        OUTQ = self._OUT
        delattr(self, OUTQ)
        setattr(self, OUTQ, iter([]))
        return self


class EndMixin(LazyMixin):

    '''result things mixin'''
    
    def __iter__(self):
        '''yield outflow, clearing outflow as it iterates'''
        return getattr(self, self._OUT)
    
    results = __iter__

    def end(self):
        '''return outflow then clear out everything'''
        # flow to default flow
        self.unflow()
        out, tell = tee(self.outflow)
        wrap = self._wrapper
        wrap = next(out) if len(wrap(tell)) == 1 else wrap(out)
        # clear every last thing
        self.clear()
        return wrap

    def snapshot(self):
        '''snapshot of outflow'''
        out, tell, self.outflow = tee(getattr(self, self._OUT), 3)
        wrap = self._wrapper
        return out.pop() if len(wrap(tell)) == 1 else wrap(out)

    def out(self):
        '''return outflow and clear outflow'''
        # flow to default flow
        self.unflow()
        out, tell = tee(self.outflow)
        wrap = self._wrapper
        wrap = next(out) if len(wrap(tell)) == 1 else wrap(out)
        # clear outflow
        self.clearout()
        return wrap


class OutMixin(EndMixin, LazyMixin):

    '''tubing with results extraction mixin'''


class lazytube(
    OutMixin, FilterMixin, MapMixin, ReduceMixin, OrderMixin, ExtractMixin,
    SetMixin, SliceMixin, TruthMixin, MathMixin, RepeatMixin, RandomMixin,
    StringMixin,
):

    '''tubing with results'''

    __slots__ = SLOTS


class collecttube(OutMixin, ExtractMixin):

    '''collecting tubing'''

    __slots__ = SLOTS


class settube(OutMixin, SetMixin):

    '''set tubing'''

    __slots__ = SLOTS


class slicetube(OutMixin, SliceMixin):

    '''slice tubing'''

    __slots__ = SLOTS


class filtertube(OutMixin, FilterMixin, ExtractMixin, SetMixin, SliceMixin):

    '''filter tubing'''

    __slots__ = SLOTS


class repeattube(OutMixin, RepeatMixin):

    '''repeat tubing'''

    __slots__ = SLOTS


class maptube(OutMixin, RepeatMixin, MapMixin):

    '''map tubing'''

    __slots__ = SLOTS


class randomtube(OutMixin, RandomMixin):

    '''random tubing'''

    __slots__ = SLOTS


class sorttube(OutMixin, OrderMixin, RandomMixin):

    '''order tubing'''

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


class stringtube(OutMixin, StringMixin):

    '''string transformation tubing'''

    __slots__ = SLOTS


class transformtube(OutMixin, StringMixin):

    '''transformation tubing'''
