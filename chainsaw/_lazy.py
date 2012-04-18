# -*- coding: utf-8 -*-
'''lazily evaluated chainsaws'''

from threading import local
from itertools import tee, chain
from contextlib import contextmanager

from stuf.utils import clsname


class _LazyMixin(local):

    '''lazy chainsaw mixin'''

    def __init__(self, *things, **kw):
        # if just one thing, put it in incoming things or put everything in
        # incoming things
        incoming = iter([things[0]]) if len(things) == 1 else iter(things)
        super(_LazyMixin, self).__init__(incoming, iter([]), **kw)
        # working things
        self._work = iter([])
        # holding things
        self._hold = iter([])

    ###########################################################################
    ## things in chains #######################################################
    ###########################################################################

    @property
    @contextmanager
    def _chain(self, iter_=iter, tee_=tee):
        # take snapshot
        self._in, snapshot = tee_(self._in)
        # rebalance incoming with outcoming
        if self._original is not None:
            self._in, self._out = tee_(self._out)
        # make snapshot original snapshot?
        else:
            self._original = snapshot
        # place snapshot at beginning of snapshot stack
        self._history.appendleft(snapshot)
        # move incoming things to working things
        work, self._in = tee_(self._in)
        self._work = work
        yield
        # extend outgoing things with holding things
        self._out = self._hold
        # clear working things
        del self._work
        self._work = iter_([])
        # clear holding things
        del self._hold
        self._hold = iter_([])

    ###########################################################################
    ## adding things ##########################################################
    ###########################################################################

    @property
    def _iterable(self):
        # iterable derived from link in chain
        return self._work

    def _xtend(self, things, chain_=chain):
        # place things after holding things
        self._hold = chain_(things, self._hold)
        return self

    def _xtendleft(self, things, reversed_=reversed):
        # place things after holding things
        self._hold = self._xtend(reversed_(things))
        return self

    def _append(self, things, chain_=chain, iter_=iter):
        # append thing after other holding things
        self._hold = chain_(self._hold, iter_([things]))
        return self

    def _prependit(self, things, tee_=tee):
        # place things before other incoming things
        with self._chain:
            self._xtendleft(things)
        self._in, self._out = tee_(self._out)
        return self

    def _appendit(self, things, tee_=tee):
        # place things after other incoming things
        with self._chain:
            self._xtend(things)
        self._in, self._out = tee_(self._out)
        return self

    ###########################################################################
    ## know things ############################################################
    ###########################################################################

    def _repr(self, tee_=tee, l=list, clsname_=clsname):
        # object representation
        self._in, in2 = tee_(self._in)
        self._out, out2 = tee_(self._out)
        self._work, work2 = tee_(self._work)
        self._hold, hold2 = tee_(self._hold)
        return self._REPR.format(
            self.__module__,
            clsname_(self),
            l(in2),
            l(work2),
            l(hold2),
            l(out2),
            self._mode,
        )

    def _len(self, tee_=tee, len_=len, list_=list):
        # length of incoming things
        self._in, incoming = tee_(self._in)
        return len_(list_(incoming))


class _OutMixin(_LazyMixin):

    '''lazy output mixin'''

    def _snapshot(self, tee_=tee):
        # clear everything
        self.clear()
        # clear snapshots
        self._clearsp()
        # revert to baseline snapshot of incoming things
        self._in, self._baseline = tee_(self._baseline)
        return self

    def _undo(self, snapshot=0, iter_=iter):
        # clear everything
        self.clear()
        # if specified, use a specific snapshot
        if snapshot:
            self._history.rotate(-(snapshot - 1))
        self._in = self._history.popleft()
        # clear outgoing things
        del self._out
        self._out = iter_([])
        return self

    def _original(self, tee_=tee):
        # clear everything
        self.clear()
        # clear snapshots
        self._clearsp()
        # clear baseline
        self._baseline = None
        # restore original snapshot of incoming things
        self._in, self._original = tee_(self._original)
        return self

    def _clear(self, iter_=iter, list_=list):
        # clear worker
        self._worker = None
        # clear worker positional arguments
        self._args = ()
        # clear worker keyword arguments
        self._kw = {}
        # default iterable wrapper
        self._wrapper = list_
        # clear incoming things
        del self._in
        self._in = iter_([])
        # clear working things
        del self._work
        self._work = iter_([])
        # clear holding things
        del self._hold
        self._hold = iter_([])
        # clear outgoing things
        del self._out
        self._out = iter_([])
        return self

    def _iterate(self, tee_=tee, list_=list, len_=len):
        self._out, outs = tee_(self._out)
        return outs

    def _fetch(self, tee_=tee, list_=list, len_=len):
        tell, self._out, outs = tee(self._out, 3)
        wrapper = self._wrapper
        if self._mode == self._MANY:
            value = tuple(wrapper(i) for i in outs)
        else:
            value = wrapper(outs)
        return value.pop() if len(list_(tell)) == 1 else value
