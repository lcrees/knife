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
        # if just one thing, put it in inchain or put everything in inchain
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
    def _man4(self, **kw):
        '''switch to a manually balanced four-link chain'''
        self._as_chain(chain=self._man4, **kw)
        # move incoming things up to work link
        getattr(self, self._WORK).extend(getattr(self, self._IN))
        yield
        out = getattr(self, self._OUT)
        # clear out
        if self._nokeep:
            out.clear()
        # extend outgoing things with holding link
        out.extend(getattr(self, self._HOLD))
        # clear work, holding links & return to current selected chain
        self._clearworking()._rechain()

    def _outin(self):
        '''copy outgoing things -> incoming things.'''
        self._in.clear()
        self._in.extend(self._out)
        return self

    def _inout(self):
        '''copy incoming things -> outgoing things.'''
        self._out.clear()
        self._out.extend(self._in)
        return self

    ###########################################################################
    ## snapshot of things #####################################################
    ###########################################################################

    def _snapshot(self, baseline=False, original=False):
        '''take snapshot of incoming things'''
        # take snapshot
        snapshot = pickle.dumps(self._in, pickle.HIGHEST_PROTOCOL)
        test = (self._ss is not None and len(self._ss) == 0)
        # rebalance incoming with outcoming
        if self._AUTO and not test:
            self._in.clear()
            self._in.extend(self._out)
        # make snapshot original snapshot?
        if test or original:
            self._original = snapshot
        # make this snapshot the baseline snapshot
        if test or self._context == self._EDIT or baseline:
            self._baseline = snapshot
        # place snapshot at beginning of snapshot stack
        self._ss.appendleft(snapshot)
        return self

    def _undo(self, snapshot=0, baseline=False, original=False):
        '''revert incoming things to previous snapshot'''
        # clear everything
        self.clear()
        if original:
            # clear snapshots
            self._clearsp()
            # clear baseline
            self._baseline = None
            # restore original version of incoming things
            snapshot = pickle.loads(self._original)
        elif baseline:
            # clear snapshots
            self._clearsp()
            # restore baseline version of incoming things
            snapshot = pickle.loads(self._baseline)
        # if specified, use a specific snapshot
        elif snapshot:
            self._ss.rotate(-(snapshot - 1))
            snapshot = pickle.loads(self._ss.popleft())
        # by default revert to most recent snapshot
        else:
            snapshot = pickle.loads(self._ss.popleft())
        self._in.extend(snapshot)
        return self

    ###########################################################################
    ## stepping through things ################################################
    ###########################################################################

    @property
    def _iterable(self):
        '''iterable derived from link in chain'''
        return self._iterator(self._WORK)

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
        getattr_(self, self._HOLD).extend(things)
        return self

    def _xtendfront(self, things, getattr_=getattr):
        '''
        extend holding things with things placed before anything already
        being held
        '''
        getattr_(self, self._HOLD).extendleft(things)
        return self

    def _append(self, things, getattr_=getattr):
        '''append things to holding things'''
        getattr_(self, self._HOLD).append(things)
        return self

    def _appendfront(self, things, getattr_=getattr):
        '''
        append things to holding thing before anything already being
        held
        '''
        getattr_(self, self._HOLD).appendleft(things)
        return self

    ###########################################################################
    ## know things ############################################################
    ###########################################################################

    def _repr(self, getattr_=getattr, clsname_=clsname, list_=list):
        '''object representation.'''
        return self._REPR.format(
            self.__module__,
            clsname_(self),
            self._IN,
            list_(getattr_(self, self._IN)),
            self._WORK,
            list_(getattr_(self, self._WORK)),
            self._HOLD,
            list_(getattr_(self, self._HOLD)),
            self._OUT,
            list_(getattr_(self, self._OUT)),
            self._mode,
            self._context,
        )

    def _len(self):
        '''length of incoming things.'''
        return len(self._in)

    def _balanced(self):
        '''outgoing and incoming things in balance?'''
        return len(self._out) == len(self._in)

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

    def _clearin(self):
        '''remove incoming things'''
        self._in.clear()
        return self

    def _clearout(self):
        '''remove outgoing things'''
        self._out.clear()
        return self

    def _clear(self):
        '''remove everything'''
        # active callable
        self._call = None
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


class _OutputMixin(_ActiveMixin):

    '''active output mixin'''

    def _iterate(self):
        '''yield outgoing things'''
        return self._iterator(self._OUT)

    def _output(self):
        '''peek at state of outgoing things'''
        wrap, out = self._wrapper, self._out
        if self._mode == self._MANY:
            value = tuple(wrap(i) for i in out)
        else:
            value = wrap(out)
        return value.pop() if len(value) == 1 else value
