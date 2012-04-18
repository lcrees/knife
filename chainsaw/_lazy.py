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
        self._snapshot()
        # move incoming things up to working things
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
    ## snapshot of things #####################################################
    ###########################################################################

    def _snapshot(self, baseline=False, original=False):
        # take snapshot
        self._in, snapshot = tee(self._in)
        test = self._history is not None and not len(self._history) == 0
        # rebalance incoming with outcoming
        if self._original is not None:
            self._in, self._out = tee(self._out)
        if test:
            # make snapshot original snapshot?
            if original:
                self._original = snapshot
            # make this snapshot the baseline snapshot
            if baseline:
                self._baseline = snapshot
        # place snapshot at beginning of snapshot stack
        self._history.appendleft(snapshot)
        return self

    def _undo(self, snapshot=0, baseline=False, original=False):
        '''revert incoming things to previous snapshot'''
        # if specified, use a specific snapshot
        if self._history:
            # clear everything
            self.clear()
            if snapshot:
                self._history.rotate(-(snapshot - 1))
                self._in = self._history.popleft()
            # by default revert to most recent snapshot
            else:
                self._in = self._history.popleft()
        return self

    ###########################################################################
    ## stepping through things ################################################
    ###########################################################################

    @property
    def _iterable(self):
        # iterable derived from link in chain
        return self._work

    ###########################################################################
    ## adding things ##########################################################
    ###########################################################################

    def _xtend(self, things, chain_=chain, iter_=iter):
        # extend holding thing with things
        if len(things) == 1:
            self._hold = chain_(self._hold, iter_([things]))
        # append things to holding things
        else:
            self._hold = chain_(things, self._hold)
        return self

    def _xtendleft(self, things, iter_=iter, reversed_=reversed):
        # append things to holding thing before anything already being held
        if len(things) == 1:
            return self._xtend(iter_([things]))
        # extend holding things with things placed before anything already
        # being held
        return self._xtend(reversed_(things))

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


class _OutputMixin(_LazyMixin):

    '''lazy output mixin'''

    def _baseline(self, tee_=tee):
        if self._baseline is not None:
            # clear everything
            self.clear()
            # clear snapshots
            self._clearsp()
            # revert to baseline snapshot of incoming things
            self._in, self._baseline = tee_(self._baseline)
        return self

    def _original(self, tee_=tee):
        if self._original is not None:
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

    def _iterate(self):
        if not self._out:
            self._in, self._out = tee(self._in)
        return self._out

    def _fetch(self):
        if not self._out:
            self._in, self._out = tee(self._in)
        outs, tell = tee(self._out)
        wrapper = self._wrapper
        if self._mode == self._MANY:
            value = tuple(wrapper(i) for i in outs)
        else:
            value = wrapper(outs)
        return value.pop() if len(wrapper(tell)) == 1 else value
