# -*- coding: utf-8 -*-
'''active chainsaws'''

from threading import local
from collections import deque
from contextlib import contextmanager

from stuf.utils import clsname

from chainsaw._compat import pickle


class _ActiveMixin(local):

    '''active chainsaw mixin'''

    def __init__(self, *things, **kw):
        # if just one thing, put it in incoming things or put everything in
        # incoming things
        try:
            inchain = deque(things[0]) if len(things) == 1 else deque(things)
        except TypeError:
            # handle non-iterable incoming things with length
            inchain = deque()
            inchain.append(things)
        super(_ActiveMixin, self).__init__(inchain, deque(), **kw)
        # work link
        self._work = deque()
        # holding link
        self._hold = deque()

    ###########################################################################
    ## things in chains #######################################################
    ###########################################################################

    @contextmanager
    def _chain(self, **kw):
        '''switch to a manually balanced four-link chain'''
        # move incoming things up to work link
        self._work.extend(getattr(self, self._IN))
        yield
        out = self._out
        # clear out
        if self._nokeep:
            out.clear()
        # extend outgoing things with holding link
        out.extend(self._hold)
        # clear work, holding links & return to current selected chain
        self._clearworking()

    ###########################################################################
    ## snapshot of things #####################################################
    ###########################################################################

    def _snapshot(self, baseline=False, original=False):
        '''take snapshot of incoming things'''
        # take snapshot
        snapshot = pickle.dumps(self._in, pickle.HIGHEST_PROTOCOL)
        test = self._history is not None and len(self._history) == 0
        # rebalance incoming with outcoming
        if self._original is not None:
            self._in.clear()
            self._in.extend(self._out)
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
            if snapshot:
                # clear everything
                self.clear()
                self._history.rotate(-(snapshot - 1))
                self._in.extend(pickle.loads(self._history.popleft()))
            # by default revert to most recent snapshot
            else:
                # clear everything
                self.clear()
                snapshot = pickle.loads(self._history.popleft())
                self._in.extend(snapshot)
        return self

    ###########################################################################
    ## stepping through things ################################################
    ###########################################################################

    @property
    def _iterable(self):
        '''iterable derived from link in chain'''
        return self._iterator(self._work)

    def _iterator(self, attr='_HOLD', getattr_=getattr):
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

    ###########################################################################
    ## adding things ##########################################################
    ###########################################################################

    def _xtend(self, things, getattr_=getattr):
        '''extend holding thing with things'''
        self._hold.extend(things)
        return self

    def _xtendfront(self, things, getattr_=getattr):
        '''
        extend holding things with things placed before anything already
        being held
        '''
        self._hold.extendleft(things)
        return self

    def _append(self, things, getattr_=getattr):
        '''append things to holding things'''
        self._hold.append(things)
        return self

    def _prepend(self, things, getattr_=getattr):
        '''
        append things to holding thing before anything already being
        held
        '''
        self._hold.appendleft(things)
        return self

    ###########################################################################
    ## know things ############################################################
    ###########################################################################

    def _repr(self, getattr_=getattr, clsname_=clsname, list_=list):
        '''object representation.'''
        return self._REPR.format(
            self.__module__,
            clsname_(self),
            list_(self._in),
            list_(self._work),
            list_(self._hold),
            list_(self._out),
            self._mode,
        )

    def _len(self):
        '''length of incoming things.'''
        return len(self._in)

    ###########################################################################
    ## clear things ###########################################################
    ###########################################################################

    def _clearworking(self):
        '''clear working, holding things'''
        # clear work link
        self._work.clear()
        # clear holding link
        self._hold.clear()
        return self


class _OutputMixin(_ActiveMixin):

    '''active output mixin'''

    def _baseline(self):
        if self._baseline is not None:
            # clear everything
            self.clear()
            # clear snapshots
            self._clearsp()
            # restore baseline version of incoming things
            self._in.extend(pickle.loads(self._baseline))
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
            self._in.extend(pickle.loads(self._original))
        return self

    def _clear(self):
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
        self._wrapper = list
        # remove all outgoing things
        self._out.clear()
        # remove all incoming things
        self._in.clear()
        # clear work link
        self._work.clear()
        # clear holding link
        self._hold.clear()
        return self

    def _iterate(self):
        '''yield outgoing things'''
        return self._iterator(self._OUT)

    def _results(self):
        '''peek at state of outgoing things'''
        wrapper, out = self._wrapper, self._out
        if not out:
            out.extend(self._in)
        if self._mode == self._MANY:
            value = tuple(wrapper(i) for i in out)
        else:
            value = wrapper(out)
        return value.pop() if len(value) == 1 else value
