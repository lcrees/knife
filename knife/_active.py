# -*- coding: utf-8 -*-
'''active knifes'''

from threading import local
from collections import deque
from contextlib import contextmanager

from stuf.utils import clsname

from knife._compat import pickle


class _ActiveMixin(local):

    '''active knife mixin'''

    def __init__(self, *things, **kw):
        # if just one thing, put it in incoming things or put everything in
        # incoming things
        incoming = deque()
        incoming.extend(things)
        super(_ActiveMixin, self).__init__(incoming, deque(), **kw)
        # working things
        self._work = deque()
        # holding things
        self._hold = deque()

    ###########################################################################
    ## things in chains #######################################################
    ###########################################################################

    @property
    @contextmanager
    def _chain(self, dumps_=pickle.dumps, protocol_=pickle.HIGHEST_PROTOCOL):
        # take snapshot
        snapshot = dumps_(self._in, protocol_)
        # rebalance incoming with outcoming
        if self._original is not None:
            self._in.clear()
            self._in.extend(self._out)
        # make snapshot original snapshot?
        else:
            self._original = snapshot
        # place snapshot at beginning of snapshot stack
        self._history.appendleft(snapshot)
        # move incoming things to working things
        self._work.extend(self._in)
        yield
        out = self._out
        # clear outgoing things
        out.clear()
        # extend outgoing things with holding things
        out.extend(self._hold)
        # clear working things
        self._work.clear()
        # clear holding things
        self._hold.clear()

    ###########################################################################
    ## stepping through things ################################################
    ###########################################################################

    @property
    def _iterable(self):
        # derived from Raymond Hettinger Python Cookbook recipe # 577155
        call = self._work.popleft
        try:
            while 1:
                yield call()
        except IndexError:
            pass

    def _append(self, thing):
        # append thing after other holding things
        self._hold.append(thing)
        return self

    def _xtend(self, things):
        # place things after holding things
        self._hold.extend(things)
        return self

    def _prependit(self, things, d=pickle.dumps, p_=pickle.HIGHEST_PROTOCOL):
        # take snapshot
        snapshot = d(self._in, p_)
        # make snapshot original snapshot?
        if self._original is None:
            self._original = snapshot
        # place snapshot at beginning of snapshot stack
        self._history.appendleft(snapshot)
        self._in.extendleft(things)
        return self

    def _appendit(self, things, d=pickle.dumps, p_=pickle.HIGHEST_PROTOCOL):
        # place things after other incoming things
        # take snapshot
        snapshot = d(self._in, p_)
        # make snapshot original snapshot?
        if self._original is None:
            self._original = snapshot
        # place snapshot at beginning of snapshot stack
        self._history.appendleft(snapshot)
        self._in.extend(things)
        return self

    ###########################################################################
    ## know things ############################################################
    ###########################################################################

    def _repr(self, clsname_=clsname, list_=list):
        # object representation
        return self._REPR.format(
            self.__module__,
            clsname_(self),
            list_(self._in),
            list_(self._work),
            list_(self._hold),
            list_(self._out),
        )

    def _len(self):
        # length of incoming things
        return len(self._in)


class _OutMixin(_ActiveMixin):

    '''active output mixin'''

    def _snapshot(self, d=pickle.dumps, p=pickle.HIGHEST_PROTOCOL):
        # take baseline snapshot of incoming things
        self._baseline = d(self._in, p)
        return self

    def _rollback(self, loads_=pickle.loads):
        # clear everything
        self.clear()
        # clear snapshots
        self._clearsp()
        # revert to baseline snapshot of incoming things
        self._in.extend(loads_(self._baseline))
        return self

    def _revert(self, loads_=pickle.loads):
        # clear everything
        self.clear()
        # clear snapshots
        self._clearsp()
        # clear baseline
        self._baseline = None
        # restore original snapshot of incoming things
        self._in.extend(loads_(self._original))
        return self

    def _undo(self, snapshot=0, loads_=pickle.loads):
        # clear everything
        self.clear()
        # if specified, use a specific snapshot
        if snapshot:
            self._history.rotate(-(snapshot - 1))
        self._in.extend(loads_(self._history.popleft()))
        return self

    def _clear(self, list_=list):
        # clear worker
        self._worker = None
        # clear worker positional arguments
        self._args = ()
        # clear worker keyword arguments
        self._kw = {}
        # default iterable wrapper
        self._wrapper = list_
        # clear incoming things
        self._in.clear()
        # clear working things
        self._work.clear()
        # clear holding things
        self._hold.clear()
        # clear outgoing things
        self._out.clear()
        return self

    def _iterate(self, iter_=iter):
        return iter_(self._out)

    def _peek(self, len_=len, tuple_=tuple):
        wrap, out = self._wrapper, self._in
        if self._mode == self._MANY:
            value = tuple_(wrap(i) for i in out)
        else:
            value = wrap(out)
        return value.pop() if len_(value) == 1 else value

    def _fetch(self, len_=len, tuple_=tuple):
        wrap, out = self._wrapper, self._out
        if self._mode == self._MANY:
            value = tuple_(wrap(i) for i in out)
        else:
            value = wrap(out)
        return value.pop() if len_(value) == 1 else value
