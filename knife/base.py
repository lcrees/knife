# -*- coding: utf-8 -*-
'''base knife mixins'''

from threading import local

from stuf.six import tounicode, tobytes


class ChainknifeMixin(local):

    '''base knife mixin'''

    ###########################################################################
    ## things are called ######################################################
    ###########################################################################

    def worker(self, worker):
        '''
        Assign worker.

        :argument worker: a Python callable
        '''
        # reset stored position params
        self._args = ()
        # reset stored keyword params
        self._kw = {}
        # assign worker
        self._worker = worker
        return self

    def pattern(self, pattern, type='parse', flags=0):
        '''
        Compile a search pattern and use it as the worker.

        :argument string pattern: search pattern

        :keyword string type: engine to compile pattern with. Valid options are
          `'parse' <http://pypi.python.org/pypi/parse/>`_, `'re'
          <http://docs.python.org/library/re.html>`_, or `'glob'
          <http://docs.python.org/library/fnmatch.html>`_

        :keyword integer flags: regular expression `flags
          <http://docs.python.org/library/re.html#re.DEBUG>`_
        '''
        self._worker = self._pattern(pattern, type, flags)
        return self

    def params(self, *args, **kw):
        '''
        Assign global `positional
        <http://docs.python.org/glossary.html#term-positional-argument>`_ and
        `keyword <http://docs.python.org/glossary.html#term-keyword-argument>`_
        params used when the worker is invoked.
        '''
        # positional params
        self._args = args
        # keyword arguemnts
        self._kw = kw
        return self

    ###########################################################################
    ## things coming in #######################################################
    ###########################################################################

    def map(self):
        '''
        Feed each thing within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ to the worker.
        '''
        with self._chain:
            return self._many(self._map(self._worker))

    def merge(self):
        '''
        Combine multiple `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_ into one
        iterable.
        '''
        with self._chain:
            return self._many(self._merge)

    def prepend(self, *things):
        '''
        Insert `things` **before** any other incoming things.

        :argument things: incoming things
        '''
        return self._prependit(things)

    def append(self, *things):
        '''
        Insert `things` **after** any other incoming things.

        :argument things: incoming things
        '''
        return self._appendit(things)

    ###########################################################################
    ## knowing things #########################################################
    ###########################################################################

    def __len__(self):
        '''Number of incoming things.'''
        return self._len()

    def __repr__(self):
        '''Object representation.'''
        return self._repr()


class OutMixin(ChainknifeMixin):

    '''output mixin'''

    ###########################################################################
    ## things going out #######################################################
    ###########################################################################

    def __iter__(self):
        '''Iterate over outgoing things.'''
        return self._iterate()

    def fetch(self):
        '''
        Return outgoing things (wrapped with the current `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ as_type.
        '''
        return self._fetch()

    def peek(self):
        '''
        Preview current state of incoming things (wrapped with the current
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        as_type).
        '''
        return self._peek()

    ###########################################################################
    ## state of things ########################################################
    ###########################################################################

    def undo(self, snapshot=0):
        '''
        Restore incoming things to a previous state.

        :keyword integer snapshot: number of steps ago e.g. ``1``, ``2``, ``3``
        '''
        return self._undo(snapshot)

    def snapshot(self):
        '''
        Take baseline snapshot of the current state of incoming things.
        '''
        return self._snapshot()

    def stepback(self):
        '''
        Restore incoming things to baseline state.
        '''
        return self._rollback()

    def original(self):
        '''
        Restore incoming things to initial state.
        '''
        return self._revert()

    ###########################################################################
    ## clean up things ########################################################
    ###########################################################################

    def clear(self):
        '''
        Clear everything.
        '''
        return self._clear()

    ###########################################################################
    ## cast things out ########################################################
    ###########################################################################

    # type cast outgoing things as type caster
    _ONE = _DEFAULT_MODE = 'ONE'
    # type cast each outgoing thing as type caster
    _MANY = 'MANY'

    def cast_each(self):
        '''
        Toggle whether each item should be cast to wrapping type or everything.
        '''
        self._mode = self._MANY if self._mode == self._ONE else self._ONE
        return self

    def as_type(self, wrapper):
        '''
        Assign type caster for outgoing things.

        :argument wrapper: an `iterable
          <http://docs.python.org/glossary.html#term-iterable>`_ as_type
        '''
        self._wrapper = wrapper
        return self

    def as_ascii(self, errors='strict'):
        '''
        Set type caster to :class:`byte` encode outgoing things with the
        ``'ascii'`` codec.

        :keyword string errors: error handling for decoding issues
        '''
        self._wrapper = lambda x: tobytes(x, 'ascii', errors)
        return self

    def as_bytes(self, encoding='utf-8', errors='strict'):
        '''
        Set type caster to :class:`byte` encode outgoing things.

        :keyword string encoding: Unicode encoding

        :keyword string errors: error handling for encoding issues
        '''
        self._wrapper = lambda x: tobytes(x, encoding, errors)
        return self

    def as_dict(self):
        '''
        Set type caster to cast outgoing things to :class:`dict`.
        '''
        self._wrapper = dict
        return self

    def as_list(self):
        '''
        Set type caster to cast outgoing things to :class:`list`.
        '''
        self._wrapper = list
        return self

    def as_set(self):
        '''
        Set type caster to cast outgoing things to :class:`set`.
        '''
        self._wrapper = set
        return self

    def as_tuple(self):
        '''
        Set type caster to cast outgoing things to :class:`tuple`.
        '''
        self._wrapper = tuple
        return self

    def as_unicode(self, encoding='utf-8', errors='strict'):
        '''
        Set type caster to :class:`unicode` (:class:`str` under Python 3)
        decode outgoing things.

        :keyword string encoding: Unicode encoding

        :keyword string errors: error handling for decoding issues
        '''
        self._wrapper = lambda x: tounicode(x, encoding, errors)
        return self
