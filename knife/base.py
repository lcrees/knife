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
        Assign Python callable for use as a processing filter.

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
        Compile a search pattern for use as :meth:`worker`.

        :argument string pattern: search pattern

        :keyword string type: engine to compile pattern with. Valid options are
          `'parse' <http://pypi.python.org/pypi/parse/>`_, `'re'
          <http://docs.python.org/library/re.html>`_, or `'glob'
          <http://docs.python.org/library/fnmatch.html>`_

        :keyword integer flags: regular expression `flags
          <http://docs.python.org/library/re.html#re.DEBUG>`_

        >>> # using parse expression
        >>> __('first test', 'second test', 'third test').pattern('first {}').filter().fetch()
        'first test'
        >>> # using regular expression
        >>> __('first test', 'second test', 'third test').pattern('third .', type='regex').filter().fetch()
        'third test'
        >>> # using glob pattern
        >>> __('first test', 'second test', 'third test').pattern('second*', type='glob').filter().fetch()
        'second test'
        '''
        self._worker = self._pattern(pattern, type, flags)
        return self

    def params(self, *args, **kw):
        '''
        Assign global `positional
        <http://docs.python.org/glossary.html#term-positional-argument>`_ and
        `keyword <http://docs.python.org/glossary.html#term-keyword-argument>`_
        params used when :meth:`worker` is invoked.
        '''
        # positional params
        self._args = args
        # keyword arguemnts
        self._kw = kw
        return self

    ###########################################################################
    ## things coming in #######################################################
    ###########################################################################

    def prepend(self, *things):
        '''
        Insert `things` **before** other incoming things.

        :argument things: incoming things

        >>> __(3, 4, 5).prepend(1, 2, 3, 4, 5, 6).peek()
        [1, 2, 3, 4, 5, 6, 3, 4, 5]
        '''
        return self._prependit(things)

    def append(self, *things):
        '''
        Insert `things` **after** other incoming things.

        :argument things: incoming things

        >>> __(3, 4, 5).append(1, 2, 3, 4, 5, 6).peek()
        [3, 4, 5, 1, 2, 3, 4, 5, 6]
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
        Return outgoing things (wrapped with the current type caster).
        '''
        return self._fetch()

    def peek(self):
        '''
        Preview current state of incoming things (wrapped with the current type
        caster).
        '''
        return self._peek()

    ###########################################################################
    ## state of things ########################################################
    ###########################################################################

    def undo(self, snapshot=0):
        '''
        Restore incoming things to a previous state.

        :keyword integer snapshot: number of steps ago e.g. ``1``, ``2``, ``3``

        >>> undone = __(1, 2, 3).prepend(1, 2, 3, 4, 5, 6).peek()
        [1, 2, 3, 4, 5, 6, 1, 2, 3]
        >>> # undo back one step
        >>> undone.append(1).undo().peek()
        [1, 2, 3, 4, 5, 6, 1, 2, 3]
        >>> # undo back one step
        >>>> undone.append(1).append(2).undo().peek()
        [1, 2, 3, 4, 5, 6, 1, 2, 3, 1]
        >>> # undo back 2 steps
        >>> undone.append(1).append(2).undo(2).peek()
        [1, 2, 3, 4, 5, 6, 1, 2, 3, 1]
        '''
        return self._undo(snapshot)

    def snapshot(self):
        '''
        Take baseline snapshot of the current state of incoming things.
        '''
        return self._snapshot()

    def stepback(self):
        '''
        Restore incoming things back to baseline snapshot.

        >>> undone = __(1, 2, 3).prepend(1, 2, 3, 4, 5, 6).peek()
        [1, 2, 3, 1, 2, 3, 4, 5, 6]
        >>> undone.snapshot().append(1).append(2).peek()
        [1, 2, 3, 1, 2, 3, 4, 5, 6, 1, 2]
        >>> undone.stepback().peek()
        [1, 2, 3, 4, 5, 6, 1, 2, 3]
        '''
        return self._rollback()

    def original(self):
        '''
        Restore incoming things back to initial snapshot.

        >>> undone = __(1, 2, 3).prepend(1, 2, 3, 4, 5, 6).peek()
        [1, 2, 3, 1, 2, 3, 4, 5, 6]
        >>> undone.original().peek()
        [1, 2, 3]
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
        Toggle whether each item should be cast to wrapping type or everything
        should be cast to wrapping type.
        '''
        self._mode = self._MANY if self._mode == self._ONE else self._ONE
        return self

    def as_type(self, wrapper):
        '''
        Assign type caster for outgoing things.

        :argument wrapper: type to cast results to

        >>> __(1, 2, 3, 4, 5, 6).as_type(tuple).peek()
        (1, 2, 3, 4, 5, 6)
        '''
        self._wrapper = wrapper
        return self

    def as_ascii(self, errors='strict'):
        '''
        Set type caster to :class:`byte` encode outgoing things with the
        ``'ascii'`` codec.

        :keyword string errors: error handling for decoding issues

        >>> __([1], True, r't', b('i'), u('g'), None, (1,)).as_ascii().cast_each().peek()
        (b('[1]'), b('True'), b('t'), b('i'), b('g'), b('None'), b('(1,)'))
        '''
        self._wrapper = lambda x: tobytes(x, 'ascii', errors)
        return self

    def as_bytes(self, encoding='utf-8', errors='strict'):
        '''
        Set type caster to :class:`byte` encode outgoing things.

        :keyword string encoding: Unicode encoding

        :keyword string errors: error handling for encoding issues

        >>> ([1], True, r't', b('i'), u('g'), None, (1,)).as_bytes().cast_each().peek()
        (b('[1]'), b('True'), b('t'), b('i'), b('g'), b('None'), b('(1,)'))
        '''
        self._wrapper = lambda x: tobytes(x, encoding, errors)
        return self

    def as_unicode(self, encoding='utf-8', errors='strict'):
        '''
        Set type caster to :class:`unicode` (:class:`str` under Python 3)
        decode outgoing things.

        :keyword string encoding: Unicode encoding

        :keyword string errors: error handling for decoding issues

        >>> __([1], True, r't', b('i'), u('g'), None, (1,)).as_unicode().cast_each().peek()
        (u('[1]'), u('True'), u('t'), u('i'), u('g'), u('None'), u('(1,)'))
        '''
        self._wrapper = lambda x: tounicode(x, encoding, errors)
        return self
