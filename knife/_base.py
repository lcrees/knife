# -*- coding: utf-8 -*-
'''base knife mixins'''

from operator import truth
from threading import local
from collections import deque
from fnmatch import translate
from re import compile as rcompile

from stuf.six import map
from parse import compile as pcompile

SLOTS = [
     '_in', '_work', '_hold', '_out', '_original', '_baseline', '_each', '_kw',
     '_history', '_worker', '_wrapper', '_args', '_pipe',
]


class _KnifeMixin(local):

    '''base knife mixin'''

    def __init__(self, ins, fetch, **kw):
        super(_KnifeMixin, self).__init__()
        # incoming things
        self._in = ins
        # outgoing things
        self._out = fetch
        self._pipe = False
        # default mode
        self._each = False
        ## snapshot defaults ##################################################
        # original and baseline snapshots
        self._original = self._baseline = None
        # maximum number of history snapshots to keep (default: 5)
        self._history = deque(maxlen=kw.pop('snapshots', 5))
        ## callable defaults ##################################################
        # worker
        self._worker = None
        # position arguments
        self._args = ()
        # keyword arguments
        self._kw = {}
        # default output class
        self._wrapper = list

    ###########################################################################
    ## things called ##########################################################
    ###########################################################################

    @property
    def _identity(self):
        # substitute generic identity function for worker if no other worker is
        # assigned
        return self._worker if self._worker is not None else lambda x: x

    @property
    def _test(self, truth_=truth):
        # substitute truth operator function for worker if no other worker
        # assigned
        return self._worker if self._worker is not None else truth_

    @staticmethod
    def _pattern(pat, type, flag, t=translate, r=rcompile, p=pcompile):
        # compile search pattern
        if type == 'glob':
            pat = t(pat)
            type = 'regex'
        return r(pat, flag).search if type == 'regex' else p(pat).search

    ###########################################################################
    ## things coming in #######################################################
    ###########################################################################

    def _iter(self, call, iter_=iter, _imap=map):
        # extend fetch with incoming things if knifeing them as one thing
        return self._xtend(iter_(call(self._iterable)))

    def _one(self, call, _imap=map):
        # append incoming things to fetch if knifeing them as one thing
        return self._append(call(self._iterable))

    def _many(self, call, _imap=map):
        # extend fetch with incoming things if knifeing them as one thing
        return self._xtend(call(self._iterable))

    ###########################################################################
    ## knowing things #########################################################
    ###########################################################################

    _REPR = (
        '{0}.{1} ([IN: ({2}) => WORK: ({3}) => UTIL: ({4}) => OUT: ({5})])'
    )

    ###########################################################################
    ## clearing things up #####################################################
    ###########################################################################

    def _clearsp(self):
        # clear fetch snapshots
        self._history.clear()
        return self
