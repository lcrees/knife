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
        Assign Python callable used to process incoming things.

        :argument worker: a Python callable
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
        arguments used whenever :meth:`worker` is invoked.
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

        >>> from knife import __
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
        '''Knife innard representation.'''
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
        Return outgoing things wrapped with :meth:`wrap`.
        '''
        return self._fetch()

    def peek(self):
        '''
        Preview current incoming things wrapped with :meth:`wrap`.
        '''
        return self._peek()

    ###########################################################################
    ## state of things ########################################################
    ###########################################################################

    def undo(self, snapshot=0):
        '''
        Restore incoming things to a previous snapshot.

        :keyword integer snapshot: number of steps ago e.g. ``1``, ``2``, ``3``

        >>> from knife import __
        >>> undone = __(1, 2, 3).prepend(1, 2, 3, 4, 5, 6)
        >>> undone.peek()
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
        Take baseline snapshot of current incoming things.
        '''
        return self._snapshot()

    def baseline(self):
        '''
        Restore incoming things to baseline :meth:`snapshot`.

          >>> from knife import __
          >>> undone = __(1, 2, 3).prepend(1, 2, 3, 4, 5, 6)
          >>> undone.peek()
          [1, 2, 3, 1, 2, 3, 4, 5, 6]
          >>> undone.snapshot().append(1).append(2).peek()
          [1, 2, 3, 1, 2, 3, 4, 5, 6, 1, 2]
          >>> undone.baseline().peek()
          [1, 2, 3, 4, 5, 6, 1, 2, 3]
        '''
        return self._rollback()

    def original(self):
        '''
        Restore incoming things to original snapshot.

          >>> undone = __(1, 2, 3).prepend(1, 2, 3, 4, 5, 6)
          >>> undone.peek()
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
    ## wrap things up #########################################################
    ###########################################################################

    # type cast outgoing things as type caster
    _ONE = _DEFAULT_MODE = 'ONE'
    # type cast each outgoing thing as type caster
    _MANY = 'MANY'

    def wrap_each(self):
        '''
        Toggle whether each outgoing thing should be individually wrapped with
        :meth:`wrap` or whether all outgoing things should be wrapped with
        :meth:`wrap` all at once. Default behavior is to :meth:`wrap`
        everything at once.
        '''
        self._mode = self._MANY if self._mode == self._ONE else self._ONE
        return self

    def wrap(self, wrapper):
        '''
        Assign object, type, or class used to wrap outgoing things. The default
        wrapper is :class:`list`.

        :argument wrapper: a Python object, type, or class

          >>> __(1, 2, 3, 4, 5, 6).wrap(tuple).peek()
          (1, 2, 3, 4, 5, 6)
        '''
        self._wrapper = wrapper
        return self

    def ascii(self, errors='strict'):
        '''
        :class:`byte` encode outgoing things with the ``'ascii'`` codec.

        :keyword string errors: error handling for decoding issues

          >>> from knife import __
          >>> from stuf.six import u, b
          >>> test = __([1], True, r't', b('i'), u('g'), None, (1,))
          >>> test.ascii().wrap_each().peek()
          (b('[1]'), b('True'), b('t'), b('i'), b('g'), b('None'), b('(1,)'))
        '''
        self._wrapper = lambda x: tobytes(x, 'ascii', errors)
        return self

    def bytes(self, encoding='utf-8', errors='strict'):
        '''
        :class:`byte` encode outgoing things.

        :keyword string encoding: Unicode encoding

        :keyword string errors: error handling for encoding issues

          >>> test = __([1], True, r't', b('i'), u('g'), None, (1,))
          >>> test.bytes().wrap_each().peek()
          (b('[1]'), b('True'), b('t'), b('i'), b('g'), b('None'), b('(1,)'))
        '''
        self._wrapper = lambda x: tobytes(x, encoding, errors)
        return self

    def unicode(self, encoding='utf-8', errors='strict'):
        '''
        :class:`unicode` (:class:`str` under Python 3) decode outgoing things.

        :keyword string encoding: Unicode encoding

        :keyword string errors: error handling for decoding issues

          >>> test = __([1], True, r't', b('i'), u('g'), None, (1,))
          >>> test.unicode().wrap_each().peek()
          (u('[1]'), u('True'), u('t'), u('i'), u('g'), u('None'), u('(1,)'))
        '''
        self._wrapper = lambda x: tounicode(x, encoding, errors)
        return self
