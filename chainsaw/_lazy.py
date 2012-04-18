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
        # work link
        self._work = iter([])
        # holding link
        self._hold = iter([])

    ###########################################################################
    ## things in chains #######################################################
    ###########################################################################

    @property
    @contextmanager
    def _chain(self):
        '''switch to a manually balanced four-link chain'''
        # move incoming things up to work link
        work, self._in = tee(self._in)
        self._work = work
        yield
        # extend outgoing things with holding link
        self._out = self._hold
        # clear work, holding links & return to current selected chain
        self._clearworking()

    ###########################################################################
    ## snapshot of things #####################################################
    ###########################################################################

    def _snapshot(self, baseline=False, original=False):
        '''take snapshot of incoming things'''
        # take snapshot
        self._in, snapshot = tee(self._in)
        test = self._history is not None and len(self._history) == 0
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
        '''iterable derived from link in chain'''
        return self._work

    ###########################################################################
    ## adding things ##########################################################
    ###########################################################################

    def _xtend(self, things, chain_=chain):
        '''extend holding thing with things'''
        self._hold = chain_(things, self._hold)
        return self

    def _xtendfront(self, things, reversed_=reversed):
        '''
        extend holding things with things placed before anything already
        being held
        '''
        return self._xtend(reversed_(things))

    def _append(self, things, chain_=chain, iter_=iter):
        '''append things to holding things'''
        self._hold = chain_(self._hold, iter_([things]))
        return self

    def _prepend(self, things, iter_=iter):
        '''
        append things to holding thing before anything already being held
        '''
        return self._xtend(iter_([things]))

    ###########################################################################
    ## know things ############################################################
    ###########################################################################

    def _repr(self, tee_=tee, setattr_=setattr, getattr_=getattr, l=list):
        '''object representation.'''
        self._in, in2 = tee_(self._in)
        self._out, out2 = tee_(self._out)
        self._work, work2 = tee_(self._work)
        self._hold, hold2 = tee_(self._hold)
        return self._REPR.format(
            self.__module__,
            clsname(self),
            l(in2),
            l(work2),
            l(hold2),
            l(out2),
            self._mode,
        )

    def _len(self):
        '''length of incoming things.'''
        self._in, incoming = tee(self._in)
        return len(list(incoming))

    ###########################################################################
    ## clear things ###########################################################
    ###########################################################################

    def _clearworking(self, iter_=iter):
        '''clear working and holding things'''
        # clear work link
        del self._work
        self._work = iter_([])
        # clear holding link
        del self._hold
        self._hold = iter_([])
        return self

    def _clear(self, iter_=iter, list_=list):
        '''remove everything'''
        # active callable
        self._worker = None
        # position arguments
        self._args = ()
        # keyword arguments
        self._kw = {}
        # current alternate callable
        self._alt = None
        # default output class
        self._wrapper = list_
        # remove all outgoing things
        del self._out
        self._out = iter_([])
        # remove all incoming things
        del self._in
        self._in = iter_([])
        # clear work link
        del self._work
        self._work = iter_([])
        # clear holding link
        del self._hold
        self._hold = iter_([])
        return self


class _OutputMixin(_LazyMixin):

    '''lazy output mixin'''

    def _baseline(self):
        if self._baseline is not None:
            # clear everything
            self.clear()
            # clear snapshots
            self._clearsp()
            # revert to baseline version of incoming things
            self._in, self._baseline = tee(self._baseline)
        return self

    def _original(self):
        if self._original is not None:
            # clear everything
            self.clear()
            # clear snapshots
            self._clearsp()
            # clear baseline
            self._baseline = None
            # restore original version of incoming things
            self._in, self._original = tee(self._original)
        return self

    def _iterate(self):
        '''yield outgoing things'''
        return self._out

    def _fetch(self):
        '''peek at state of outgoing things'''
        if not self._out:
            self._in, self._out = tee(self._in)
        outs, tell = tee(self._out)
        wrapper = self._wrapper
        if self._mode == self._MANY:
            value = tuple(wrapper(i) for i in outs)
        else:
            value = wrapper(outs)
        return value.pop() if len(wrapper(tell)) == 1 else value
