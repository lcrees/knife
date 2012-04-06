# -*- coding: utf-8 -*-
'''lazy thingq mixins'''

from itertools import tee, chain
from contextlib import contextmanager

from stuf.utils import clsname

from thingq.mixins import ResultsMixin, ThingsMixin


class BaseMixin(ThingsMixin):

    '''base lazy things'''

    def __init__(self, *things, **kw):
        incoming = iter([things[0]]) if len(things) == 1 else iter(things)
        super(BaseMixin, self).__init__(incoming, iter([]))
        # work things
        self._work = iter([])
        # utility things
        self._util = iter([])

    def __repr__(self):
        list_, tee_ = list, tee
        setr_ = lambda x, y: setattr(self, x, y)
        getr_ = lambda x: getattr(self, x)
        in1, in2 = tee_(getr_(self._INQ))
        setr_(self._INQ, in1)
        out1, out2 = tee_(getr_(self._OUTQ))
        setr_(self._OUTQ, out1)
        work1, work2 = tee_(getr_(self._WORKQ))
        setr_(self._WORKQ, work1)
        util1, util2 = tee_(getr_(self._UTILQ))
        setr_(self._UTILQ, util1)
        return self._repr(
            self.__module__,
            clsname(self),
            self.current_mode.upper(),
            self._INQ,
            list_(in2),
            self._WORKQ,
            list_(work2),
            self._UTILQ,
            list_(util2),
            self._OUTQ,
            list_(out2),
            id(self),
        )

    ###########################################################################
    ## mode things ############################################################
    ###########################################################################

    def ro(self):
        '''switch to read-only mode'''
        with self.ctx3(outq=self._UTILVAR, savepoint=False):
            self._xreplace(self._iterable)
        with self.ctx1(hard=True, workq=self._UTILVAR, savepoint=False):
            self.current_mode = self._RO
            return self

    ###########################################################################
    ## context things #########################################################
    ###########################################################################

    @contextmanager
    def ctx2(self, **kw):
        '''swap for two-armed context'''
        self.swap(
            context=self.ctx2, outq=kw.get(self._OUTCFG, self._INVAR), **kw
        )._clearworking()
        setr_ = lambda x, y: setattr(self, x, y)
        getr_ = lambda x: getattr(self, x)
        OUTQ = self._OUTQ
        # extend work things with outgoing things
        work, wrap = tee(getr_(OUTQ))
        setr_(self._WORKQ, work)
        setr_(OUTQ, wrap)
        yield
        # extend outgoing things with utility things
        util = getr_(self._UTILQ)
        setr_(
            self._OUTQ,
            util if self._clearout else chain(util, getr_(self._OUTQ)),
        )
        self._clearworking()
        # return to global context
        self.reswap()

    @contextmanager
    def ctx3(self, **kw):
        '''swap for three-armed context'''
        self.swap(
            utilq=kw.get(self._WORKCFG, self._WORKVAR), context=self.ctx3, **kw
        )._clearworking()
        setr_ = lambda x, y: setattr(self, x, y)
        getr_ = lambda x: getattr(self, x)
        INQ = self._INQ
        # extend work things with incoming things
        work, inq = tee(getr_(INQ))
        setr_(self._WORKQ, work)
        setr_(INQ, inq)
        yield
        # extend outgoing things with utility things
        util = getr_(self._UTILQ)
        setr_(
            self._OUTQ,
            util if self._clearout else chain(util, getr_(self._OUTQ)),
        )
        self._clearworking()
        # return to global context
        self.reswap()

    @contextmanager
    def ctx4(self, **kw):
        '''swap for four-armed context'''
        self.swap(context=self.ctx4, **kw)._clearworking()
        setr_ = lambda x, y: setattr(self, x, y)
        getr_ = lambda x: getattr(self, x)
        INQ = self._INQ
        # extend work things with incoming things
        work, inq = tee(getr_(INQ))
        setr_(self._WORKQ, work)
        setr_(INQ, inq)
        yield
        # extend outgoing things with utility things
        util = getr_(self._UTILQ)
        setr_(
            self._OUTQ,
            util if self._clearout else chain(util, getr_(self._OUTQ)),
        )
        self._clearworking()
        # return to global context
        self.reswap()

    @contextmanager
    def autoctx(self, **kw):
        '''swap for auto-synchronizing context'''
        self.swap(context=self.autoctx, **kw)._clearworking()
        setr_ = lambda x, y: setattr(self, x, y)
        getr_ = lambda x: getattr(self, x)
        INQ = self._INQ
        # extend work things with incoming things
        work, inq = tee(getr_(INQ))
        setr_(self._WORKQ, work)
        setr_(INQ, inq)
        yield
        # extend incoming things and outgoing things with utility things
        inq, wrap = tee(getr_(self._UTILQ))
        setr_(
            self._OUTQ,
            wrap if self._clearout else chain(wrap, getr_(self._OUTQ)),
        )
        setr_(INQ, inq)
        self._clearworking()
        # return to global context
        self.reswap()

    ###########################################################################
    ## savepoint for things ###################################################
    ###########################################################################

    def _savepoint(self):
        '''make savepoint of incoming things'''
        savepoint, self.incoming = tee(getattr(self, self._INQ))
        self._savepoints.append(savepoint)
        return self

    ###########################################################################
    ## iterate things #########################################################
    ###########################################################################

    @property
    def _iterable(self):
        '''iterable'''
        return getattr(self, self._WORKQ)

    ###########################################################################
    ## extend things ##########################################################
    ###########################################################################

    def _xtend(self, thing):
        '''build chain'''
        UTILQ = self._UTILQ
        setattr(self, UTILQ, chain(thing, getattr(self, UTILQ)))
        return self

    __buildchain = _xtend

    def _xtendleft(self, things):
        '''extend left side of work things with `things`'''
        return self.__buildchain(reversed(things))

    def _xreplace(self, thing):
        '''build chain'''
        setattr(self, self._UTILQ, thing)
        return self

    def _iter(self, things):
        '''extend work things with `things` wrapped in iterator'''
        return self.__buildchain(iter(things))

    ###########################################################################
    ## append things ##########################################################
    ###########################################################################

    def _append(self, things):
        '''append `things` to work things'''
        UTILQ = self._UTILQ
        setattr(self, UTILQ, chain(getattr(self, UTILQ), iter([things])))
        return self

    def _appendleft(self, things):
        '''append `things` to left side of work things'''
        return self.__buildchain(iter([things]))

    ###########################################################################
    ## know things ############################################################
    ###########################################################################

    def __len__(self):
        '''number of incoming things'''
        self.incoming, incoming = tee(self.incoming)
        return len(list(incoming))
    
    count = __len__

    def countout(self):
        '''number of outgoing things'''
        self.outgoing, outgoing = tee(self.outgoing)
        return len(list(outgoing))

    ###########################################################################
    ## clear things ###########################################################
    ###########################################################################

    def _clearworking(self):
        '''clear work things and utility things'''
        iter_ = iter
        setr_ = lambda x, y: setattr(self, x, y)
        delr_ = lambda x: delattr(self, x)
        WORKQ, UTILQ = self._WORKQ, self._UTILQ
        # clear work things
        delr_(WORKQ)
        setr_(WORKQ, iter_([]))
        # clear utility things
        delr_(UTILQ)
        setr_(UTILQ, iter_([]))
        return self

    def _clearu(self):
        '''clear utility things'''
        UTILQ = self._UTILQ
        delattr(self, UTILQ)
        setattr(self, UTILQ, iter([]))
        return self

    def _clearw(self):
        '''clear work things'''
        WORKQ = self._WORKQ
        delattr(self, WORKQ)
        setattr(self, WORKQ, iter([]))
        return self

    def clearin(self):
        '''clear incoming things'''
        INQ = self._INQ
        delattr(self, INQ)
        setattr(self, INQ, iter([]))
        return self

    def clearout(self):
        '''clear outgoing things'''
        OUTQ = self._OUTQ
        delattr(self, OUTQ)
        setattr(self, OUTQ, iter([]))
        return self


class AutoMixin(BaseMixin):

    '''auto-balancing things mixin'''

    _DEFAULT_CONTEXT = 'autoctx'


class ManMixin(BaseMixin):

    '''manually balanced things mixin'''

    _DEFAULT_CONTEXT = 'ctx4'


class EndMixin(ResultsMixin):

    '''result things mixin'''
    
    def __iter__(self):
        '''yield outgoing things, clearing outgoing things as it iterates'''
        return getattr(self, self._OUTQ)
    
    results = __iter__

    def end(self):
        '''return outgoing things then clear out everything'''
        # swap for default context
        self.unswap()
        out, tell = tee(self.outgoing)
        wrap = self._wrapper
        wrap = next(out) if len(wrap(tell)) == 1 else wrap(out)
        # clear every last thing
        self.clear()
        return wrap

    def snapshot(self):
        '''snapshot of outgoing things'''
        out, tell, self.outgoing = tee(getattr(self, self._OUTQ), 3)
        wrap = self._wrapper
        return out.pop() if len(wrap(tell)) == 1 else wrap(out)

    def out(self):
        '''return outgoing things and clear outgoing things'''
        # swap for default context
        self.unswap()
        out, tell = tee(self.outgoing)
        wrap = self._wrapper
        wrap = next(out) if len(wrap(tell)) == 1 else wrap(out)
        # clear outgoing things
        self.clearout()
        return wrap


class AutoResultMixin(EndMixin, AutoMixin):

    '''auto-balancing things (with results extraction) mixin'''


class ManResultMixin(EndMixin, ManMixin):

    '''manually balanced things (with results extraction) mixin'''
