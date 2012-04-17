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
        inchain = iter([things[0]]) if len(things) == 1 else iter(things)
        super(_LazyMixin, self).__init__(inchain, iter([]), **kw)
        # work link
        self._work = iter([])
        # holding link
        self._hold = iter([])

    ###########################################################################
    ## things in chains #######################################################
    ###########################################################################

    @contextmanager
    def _man4(self, **kw):
        '''switch to a manually balanced four-link chain'''
        self._as_chain(chain=self._man4, **kw)
        # move incoming things up to work link
        work, incoming = tee(getattr(self, self._IN))
        setattr(self, self._WORK, work)
        setattr(self, self._IN, incoming)
        yield
        # extend outgoing things with holding link
        hold = getattr(self, self._HOLD)
        setattr(
            self,
            self._OUT,
            hold if self._nokeep else chain(hold, getattr(self, self._OUT)),
        )
        # clear work, holding links & return to current selected chain
        self._clearworking()

    def _outin(self):
        '''copy outgoing things -> incoming things.'''
        self._in, self._out = tee(self._out)
        return self

    def _inout(self):
        '''copy incoming things -> outgoing things.'''
        self._in, self._out = tee(self._in)
        return self

    ###########################################################################
    ## snapshot of things #####################################################
    ###########################################################################

    def _snapshot(self, baseline=False, original=False):
        '''take snapshot of incoming things'''
        # take snapshot
        self._in, snapshot = tee(self._in)
        test = (self._ss is not None and len(self._ss) == 0)
        # rebalance incoming with outcoming
        if self._AUTO and not test:
            self._in, self._out = tee(self._out)
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
        if original and self._original is not None:
            # clear everything
            self.clear()
            # clear snapshots
            self._clearsp()
            # clear baseline
            self._baseline = None
            # restore original version of incoming things
            self._in, self._original = tee(self._original)
        elif baseline and self._baseline is not None:
            # clear everything
            self.clear()
            # clear snapshots
            self._clearsp()
            # revert to baseline version of incoming things
            self._in, self._baseline = tee(self._baseline)
        # if specified, use a specific snapshot
        elif self._ss and snapshot:
            # clear everything
            self.clear()
            self._ss.rotate(-(snapshot - 1))
            self._in = self._ss.popleft()
        # by default revert to most recent snapshot
        elif self._ss:
            # clear everything
            self.clear()
            self._in = self._ss.popleft()
        return self

    ###########################################################################
    ## stepping through things ################################################
    ###########################################################################

    @property
    def _iterable(self, getattr_=getattr):
        '''iterable derived from link in chain'''
        return getattr_(self, self._WORK)

    ###########################################################################
    ## adding things ##########################################################
    ###########################################################################

    def _xtend(self, things, chain_=chain, getattr_=getattr):
        '''extend holding thing with things'''
        setattr(
            self,
            self._HOLD,
            chain_(things, getattr_(self, self._HOLD)),
        )
        return self

    def _xtendfront(self, things, reversed_=reversed):
        '''
        extend holding things with things placed before anything already
        being held
        '''
        return self._xtend(reversed_(things))

    def _append(self, things, chain_=chain, iter_=iter, getattr_=getattr):
        '''append things to holding things'''
        setattr(
            self,
            self._HOLD,
            chain_(getattr_(self, self._HOLD), iter_([things])),
        )
        return self

    def _prepend(self, things, iter_=iter):
        '''
        append things to holding thing before anything already being
        held
        '''
        return self._xtend(iter_([things]))

    ###########################################################################
    ## know things ############################################################
    ###########################################################################

    def _repr(self, tee_=tee, setattr_=setattr, getattr_=getattr, l=list):
        '''object representation.'''
        in1, in2 = tee_(getattr(self, self._IN))
        setattr_(self, self._IN, in1)
        out1, out2 = tee_(getattr(self, self._OUT))
        setattr_(self, self._OUT, out1)
        work1, work2 = tee_(getattr(self, self._WORK))
        setattr_(self, self._WORK, work1)
        hold1, hold2 = tee_(getattr(self, self._HOLD))
        setattr_(self, self._HOLD, hold1)
        return self._REPR.format(
            self.__module__,
            clsname(self),
            self._IN,
            l(in2),
            self._WORK,
            l(work2),
            self._HOLD,
            l(hold2),
            self._OUT,
            l(out2),
            self._mode,
            self._context,
        )

    def _len(self):
        '''length of incoming things.'''
        self._in, incoming = tee(self._in)
        return len(list(incoming))

    def _balanced(self):
        '''outgoing and incoming things in balance?'''
        self._out, outs = tee(self._out)
        return len(tuple(outs)) == self.__len__()

    ###########################################################################
    ## clear things ###########################################################
    ###########################################################################

    def _clearworking(self, iter_=iter):
        '''clear working, holding things'''
        # clear work link
        delattr(self, self._WORK)
        setattr(self, self._WORK, iter_([]))
        # clear holding link
        delattr(self, self._HOLD)
        setattr(self, self._HOLD, iter_([]))
        return self

    def _clearin(self):
        '''remove incoming things'''
        delattr(self, self._IN)
        setattr(self, self._IN, iter([]))
        return self

    def _clearout(self):
        '''remove outgoing things'''
        delattr(self, self._OUT)
        setattr(self, self._OUT, iter([]))
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
        delattr(self, self._OUT)
        setattr(self, self._OUT, iter([]))
        # remove all incoming things
        delattr(self, self._IN)
        setattr(self, self._IN, iter([]))
        # clear work link
        delattr(self, self._WORK)
        setattr(self, self._WORK, iter([]))
        # clear holding link
        delattr(self, self._HOLD)
        setattr(self, self._HOLD, iter([]))
        return self


class _OutputMixin(_LazyMixin):

    '''lazy output mixin'''

    def _iterate(self):
        '''yield outgoing things'''
        return getattr(self, self._OUT)

    def _output(self):
        '''peek at state of outgoing things'''
        outs, tell = tee(self._out)
        wrap = self._wrapper
        if self._mode == self._MANY:
            value = tuple(wrap(i) for i in outs)
        else:
            value = wrap(outs)
        return value.pop() if len(wrap(tell)) == 1 else value
