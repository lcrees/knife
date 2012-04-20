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
        Assign callable used to work on incoming things.

        :argument worker: a callable
        '''
        # reset stored position params
        self._args = ()
        # reset stored keyword params
        self._kw = {}
        # assign worker
        self._worker = worker
        return self

    def params(self, *args, **kw):
        '''
        Assign `positional
        <http://docs.python.org/glossary.html#term-positional-argument>`_ and
        `keyword <http://docs.python.org/glossary.html#term-keyword-argument>`_
        arguments used when :meth:`worker` is invoked.
        '''
        # positional params
        self._args = args
        # keyword arguemnts
        self._kw = kw
        return self

    def pattern(self, pattern, type='parse', flags=0):
        '''
        Compile search `pattern` for use as :meth:`worker`.

        :argument string pattern: search pattern

        :keyword string type: engine to compile `pattern` with. Valid options
          are `'parse' <http://pypi.python.org/pypi/parse/>`_, `'re'
          <http://docs.python.org/library/re.html>`_, or `'glob'
          <http://docs.python.org/library/fnmatch.html>`_

        :keyword integer flags: regular expression `flags
          <http://docs.python.org/library/re.html#re.DEBUG>`_

        >>> # using parse expression
        >>> test = __('first test', 'second test', 'third test')
        >>> test.pattern('first {}').filter().get()
        'first test'
        >>> # using regular expression
        >>> test.original().pattern('third .', type='regex').filter().get()
        'third test'
        >>> # using glob pattern
        >>> test.original().pattern('second*', type='glob').filter().get()
        'second test'
        '''
        self._worker = self._pattern(pattern, type, flags)
        return self

    ###########################################################################
    ## things coming in #######################################################
    ###########################################################################

    def prepend(self, *things):
        '''
        Insert `things` **before** other incoming things.

        :argument things: incoming things

        >>> from knife import __
        >>> __(3, 4, 5).prepend(1, 2, 3, 4, 5, 6).peek()
        [1, 2, 3, 4, 5, 6, 3, 4, 5]
        '''
        return self._prependit(things)

    def append(self, *things):
        '''
        Insert `things` **after** other incoming things.

        :argument things: incoming things

        >>> from knife import __
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
        '''String representation.'''
        return self._repr()


class OutMixin(ChainknifeMixin):

    '''output mixin'''

    ###########################################################################
    ## things going out #######################################################
    ###########################################################################

    def __iter__(self):
        '''Iterate over outgoing things.'''
        return self._iterate()

    def get(self):
        '''
        Return outgoing things wrapped with :meth:`wrap`.
        '''
        return self._get()

    def peek(self):
        '''
        Preview current incoming things wrapped with :meth:`wrap`.
        '''
        return self._peek()

    ###########################################################################
    ## wrap things up #########################################################
    ###########################################################################

    # type cast outgoing things as type caster
    _ONE = _DEFAULT_MODE = 'ONE'
    # type cast oneach outgoing thing as type caster
    _MANY = 'MANY'

    def wrap(self, wrapper):
        '''
        Assign object, type, or class used to wrap outgoing things. Default
        wrapper is :class:`list`.

        :argument wrapper: a object, type, or class

        >>> __(1, 2, 3, 4, 5, 6).wrap(tuple).peek()
        (1, 2, 3, 4, 5, 6)
        '''
        self._wrapper = wrapper
        return self

    def oneach(self):
        '''
        Toggle whether each outgoing thing should be individually wrapped with
        :meth:`wrap` or whether all outgoing things should be wrapped with
        :meth:`wrap` all at once. Default behavior is to :meth:`wrap`
        everything at once.
        '''
        self._mode = self._MANY if self._mode == self._ONE else self._ONE
        return self

    def ascii(self, errors='strict'):
        '''
        :class:`byte` encode outgoing things with the ``'ascii'`` codec.

        :keyword string errors: error handling for decoding issues

        >>> from knife import __
        >>> from stuf.six import u, b
        >>> test = __([1], True, r't', b('i'), u('g'), None, (1,))
        >>> test.ascii().oneach().peek()
        ('[1]', 'True', 't', 'i', 'g', 'None', '(1,)')
        '''
        self._wrapper = lambda x: tobytes(x, 'ascii', errors)
        return self

    def bytes(self, encoding='utf-8', errors='strict'):
        '''
        :class:`byte` encode outgoing things.

        :keyword string encoding: Unicode encoding

        :keyword string errors: error handling for encoding issues

        >>> test = __([1], True, r't', b('i'), u('g'), None, (1,))
        >>> test.bytes().oneach().peek()
        ('[1]', 'True', 't', 'i', 'g', 'None', '(1,)')
        '''
        self._wrapper = lambda x: tobytes(x, encoding, errors)
        return self

    def unicode(self, encoding='utf-8', errors='strict'):
        '''
        :class:`unicode` (:class:`str` under Python 3) decode outgoing things.

        :keyword string encoding: Unicode encoding

        :keyword string errors: error handling for decoding issues

        >>> test = __([1], True, r't', b('i'), u('g'), None, (1,))
        >>> test.unicode().oneach().peek()
        (u'[1]', u'True', u't', u'i', u'g', u'None', u'(1,)')
        '''
        self._wrapper = lambda x: tounicode(x, encoding, errors)
        return self

    ###########################################################################
    ## state of things ########################################################
    ###########################################################################

    def undo(self, snapshot=0):
        '''
        Restore incoming things to a previous snapshot.

        :keyword integer snapshot: number of steps ago ``1``, ``2``, ``3``,
          etc.

        >>> undone = __(1, 2, 3).prepend(1, 2, 3, 4, 5, 6)
        >>> undone.peek()
        [1, 2, 3, 4, 5, 6, 1, 2, 3]
        >>> # undo back one step
        >>> undone.append(1).undo().peek()
        [1, 2, 3, 4, 5, 6, 1, 2, 3]
        >>> # undo back one step
        >>> undone.append(1).append(2).undo().peek()
        [1, 2, 3, 4, 5, 6, 1, 2, 3, 1]
        >>> # undo back 2 steps
        >>> undone.append(1).append(2).undo(2).peek()
        [1, 2, 3, 4, 5, 6, 1, 2, 3, 1]
        '''
        return self._undo(snapshot)

    def snapshot(self):
        '''
        Take baseline snapshot of current incoming things.
        '''
        return self._snapshot()

    def baseline(self):
        '''
        Restore incoming things to baseline :meth:`snapshot`.

        >>> from knife import __
        >>> undone = __(1, 2, 3).prepend(1, 2, 3, 4, 5, 6)
        >>> undone.peek()
        [1, 2, 3, 4, 5, 6, 1, 2, 3]
        >>> undone.snapshot().append(1).append(2).peek()
        [1, 2, 3, 4, 5, 6, 1, 2, 3, 1, 2]
        >>> undone.baseline().peek()
        [1, 2, 3, 4, 5, 6, 1, 2, 3]
        '''
        return self._rollback()

    def original(self):
        '''
        Restore incoming things to original snapshot.

        >>> undone = __(1, 2, 3).prepend(1, 2, 3, 4, 5, 6)
        >>> undone.peek()
        [1, 2, 3, 4, 5, 6, 1, 2, 3]
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
