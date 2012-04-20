# -*- coding: utf-8 -*-
'''base knife keys'''

from appspace.keys import AppspaceKey


class KChainknife(AppspaceKey):

    '''base knife key'''

    def __init__(*things, **kw):  # @NoSelf
        '''
        init

        :argument `things`: incoming things
        '''

    ###########################################################################
    ## things are called ######################################################
    ###########################################################################

    def worker(call):  # @NoSelf
        '''
        Assign Python callable used to process incoming things.

        :argument worker: a Python callable
        '''

    def params(*args, **kw):  # @NoSelf
        '''
        Assign `positional
        <http://docs.python.org/glossary.html#term-positional-argument>`_ and
        `keyword <http://docs.python.org/glossary.html#term-keyword-argument>`_
        arguments used whenever :meth:`worker` is invoked.
        '''

    ###########################################################################
    ## things coming in #######################################################
    ###########################################################################

    def prepend(*things):  # @NoSelf
        '''
        Insert `things` **before** other incoming things.

        :argument things: incoming things

        >>> from knife import __
        >>> __(3, 4, 5).prepend(1, 2, 3, 4, 5, 6).peek()
        [1, 2, 3, 4, 5, 6, 3, 4, 5]
        '''

    def append(things):  # @NoSelf
        '''
        Insert `things` **after** other incoming things.

        :argument things: incoming things

        >>> __(3, 4, 5).append(1, 2, 3, 4, 5, 6).peek()
        [3, 4, 5, 1, 2, 3, 4, 5, 6]
        '''

    ###########################################################################
    ## knowing things #########################################################
    ###########################################################################

    def __len__():  # @NoSelf
        '''Number of incoming things.'''

    def __repr__(self):
        '''String representation.'''
        return self._repr()


class KOutput(KChainknife):

    '''output key'''

    ###########################################################################
    ## things going out #######################################################
    ###########################################################################

    def __iter__():  # @NoSelf
        '''Iterate over outgoing things.'''

    def get():  # @NoSelf
        '''
        Return outgoing things wrapped with :meth:`wrap`.
        '''

    def peek():  # @NoSelf
        '''
        Preview current incoming things wrapped with :meth:`wrap`.
        '''

    ###########################################################################
    ## state of things ########################################################
    ###########################################################################

    def undo(snapshot=0):  # @NoSelf
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

    def snapshot():  # @NoSelf
        '''
        Take baseline snapshot of current incoming things.
        '''

    def baseline():  # @NoSelf
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

    def original():  # @NoSelf
        '''
        Restore incoming things to original snapshot.

          >>> undone = __(1, 2, 3).prepend(1, 2, 3, 4, 5, 6)
          >>> undone.peek()
          [1, 2, 3, 1, 2, 3, 4, 5, 6]
          >>> undone.original().peek()
          [1, 2, 3]
        '''

    ###########################################################################
    ## clean up things ########################################################
    ###########################################################################

    def clear():  # @NoSelf
        '''
        Clear everything.
        '''

    ###########################################################################
    ## cast things out ########################################################
    ###########################################################################

    def oneach():  # @NoSelf
        '''
        Toggle whether each outgoing thing should be individually wrapped with
        :meth:`wrap` or whether all outgoing things should be wrapped with
        :meth:`wrap` all at once. Default behavior is to :meth:`wrap`
        everything at once.
        '''

    def wrap(wrapper):  # @NoSelf
        '''
        Assign object, type, or class used to wrap outgoing things. The default
        wrapper is :class:`list`.

        :argument wrapper: a Python object, type, or class

          >>> __(1, 2, 3, 4, 5, 6).wrap(tuple).peek()
          (1, 2, 3, 4, 5, 6)
        '''

    def ascii(errors='strict'):  # @NoSelf
        '''
        :class:`byte` encode outgoing things with the ``'ascii'`` codec.

        :keyword string errors: error handling for decoding issues

          >>> from knife import __
          >>> from stuf.six import u, b
          >>> test = __([1], True, r't', b('i'), u('g'), None, (1,))
          >>> test.ascii().oneach().peek()
          (b('[1]'), b('True'), b('t'), b('i'), b('g'), b('None'), b('(1,)'))
        '''

    def bytes(encoding='utf-8', errors='strict'):  # @NoSelf
        '''
        :class:`byte` encode outgoing things.

        :keyword string encoding: Unicode encoding

        :keyword string errors: error handling for encoding issues

          >>> test = __([1], True, r't', b('i'), u('g'), None, (1,))
          >>> test.bytes().oneach().peek()
          (b('[1]'), b('True'), b('t'), b('i'), b('g'), b('None'), b('(1,)'))
        '''

    def unicode(encoding='utf-8', errors='strict'):  # @NoSelf
        '''
        :class:`unicode` (:class:`str` under Python 3) decode outgoing things.

        :keyword string encoding: Unicode encoding

        :keyword string errors: error handling for decoding issues

          >>> test = __([1], True, r't', b('i'), u('g'), None, (1,))
          >>> test.unicode().oneach().peek()
          (u('[1]'), u('True'), u('t'), u('i'), u('g'), u('None'), u('(1,)'))
        '''
