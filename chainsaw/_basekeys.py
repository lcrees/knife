# -*- coding: utf-8 -*-
'''reference keys'''

from appspace.keys import AppspaceKey, Attribute


class KChainsaw(AppspaceKey):

    '''base chainsaw key'''

    def __init__(*things, **kw):  # @NoSelf
        '''
        init

        :argument `*things`: incoming things
        '''

    ###########################################################################
    ## things in process ######################################################
    ###########################################################################

    def as_many():  # @NoSelf
        '''
        Switch to working on each incoming thing as one individual thing among
        many.
        '''

    def as_one():  # @NoSelf
        '''
        Switch to working on all incoming things as one whole thing.
        '''

    ###########################################################################
    ## things in session ######################################################
    ###########################################################################

    def as_edit():  # @NoSelf
        '''
        Start session where work is performed on incoming things **without**
        automatically reverting back to an earlier baseline snapshot when
        invoking the :meth:`results()` or iterating over outgoing things.
        '''

    def as_query():  # @NoSelf
        '''
        Switch to session where, upon exiting it by invoking :meth:`results()`
        or :meth:`end()` or iterating over outgoing things, incoming things
        **automatically** revert back to an earlier baseline snapshot.
        '''

    ###########################################################################
    ## things in chains #######################################################
    ###########################################################################

    def as_auto():  # @NoSelf
        '''
        Switch to context where incoming things are automatically rebalanced
        with outgoing things.
        '''

    def as_manual():  # @NoSelf
        '''
        Switch to context where incoming things must be manually rebalanced
        with outgoing things.
        '''

    def out_in():  # @NoSelf
        '''
        Copy outgoing things to incoming things.
        '''

    def in_out():  # @NoSelf
        '''
        Copy incoming things to outgoing things.
        '''

    balanced = Attribute(
        '''
        Whether outgoing things and incoming things are in balance.
        '''
    )

    ###########################################################################
    ## snapshot of things #####################################################
    ###########################################################################

    def snapshot(baseline=False, original=False):  # @NoSelf
        '''
        Take a snapshot of current incoming things.

        :keyword boolean baseline: make snapshot the baseline snapshot

        :keyword boolean original: make snapshot the original snapshot
        '''

    def undo(snapshot=0, baseline=False, original=False):  # @NoSelf
        '''
        Revert incoming things back to a previous snapshot.

        :keyword integer snapshot: number of steps ago e.g. ``1``, ``2``, ``3``

        :keyword boolean baseline: revert incoming things to baseline snapshot

        :keyword boolean original: revert incoming things to original snapshot
        '''

    ###########################################################################
    ## things called ##########################################################
    ###########################################################################

    def arguments(*args, **kw):  # @NoSelf
        '''
        Assign global `positional
        <http://docs.python.org/glossary.html#term-positional-argument>`_ or
        `keyword <http://docs.python.org/glossary.html#term-keyword-argument>`_
        arguments used when the worker is invoked.
        '''

    def tap(call):  # @NoSelf
        '''
        Assign worker.

        :argument callable call: a callable
        '''

    def untap():  # @NoSelf
        '''
        Remove worker and global `positional
        <http://docs.python.org/glossary.html#term-positional-argument>`_ and
        `keyword <http://docs.python.org/glossary.html#term-keyword-argument>`_
        arguments.
        '''

    def pattern(pattern, type='parse', flags=0):  # @NoSelf
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

    ###########################################################################
    ## things coming in #######################################################
    ###########################################################################

    def extend(things):  # @NoSelf
        '''
        Insert `things` **after** any other incoming things.

        :argument things: incoming things
        '''

    def extendstart(things):  # @NoSelf
        '''
        Insert `things` **before** any other incoming things.

        :argument things: incoming things
        '''

    def append(thing):  # @NoSelf
        '''
        Insert `thing` **after** any other incoming things.

        :argument thing: incoming thing
        '''

    def appendstart(thing):  # @NoSelf
        '''
        Insert `thing` **before** any other incoming things.

        :argument thing: incoming thing
        '''

    ###########################################################################
    ## knowing things #########################################################
    ###########################################################################

    def __len__():  # @NoSelf
        '''Number of incoming things.'''

    def __repr__(self):
        '''Object representation.'''

    ###########################################################################
    ## cleaning up things #####################################################
    ###########################################################################

    def clear():  # @NoSelf
        '''
        Remove everything.
        '''

    def clear_in():  # @NoSelf
        '''
        Remove incoming things.
        '''

    def clear_out():  # @NoSelf
        '''
        Remove outgoing things.
        '''


class KOutchain(KChainsaw):

    '''output key'''

    def __iter__():  # @NoSelf
        '''Yield outgoing things.'''

    def end():  # @NoSelf
        '''
        End the current session and return outgoing things wrapped with the
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper.
        '''

    def results():  # @NoSelf
        '''
        Clear and return outgoing things wrapped with the `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ wrapper. Also
        ends query sessions.
        '''

    def preview():  # @NoSelf
        '''
        Take a peek at the current state of outgoing things.
        '''

    ###########################################################################
    ## wrapping things up #####################################################
    ###########################################################################

    def wrap(wrapper):  # @NoSelf
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper for outgoing things.

        :argument wrapper: an `iterable
          <http://docs.python.org/glossary.html#term-iterable>`_ wrapper
        '''

    def unwrap():  # @NoSelf
        '''
        Reset current `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ wrapper to
        default iterable wrapper.
        '''

    def as_ascii(errors='strict'):  # @NoSelf
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to :class:`byte` encode outgoing things with the
        ``'ascii'`` codec.

        :keyword string errors: error handling for decoding issues
        '''

    def as_bytes(encoding='utf-8', errors='strict'):  # @NoSelf
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to :class:`byte` encode outgoing things.

        :keyword string encoding: Unicode encoding

        :keyword string errors: error handling for encoding issues
        '''

    def as_dict():  # @NoSelf
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to cast outgoing things to :class:`dict`.
        '''

    def as_list():  # @NoSelf
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to cast outgoing things to :class:`list`.
        '''

    def as_set():  # @NoSelf
        '''
        Set `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ wrapper to cast
        outgoing things to :class:`set`.
        '''

    def as_tuple():  # @NoSelf
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to cast outgoing things to :class:`tuple`.
        '''

    def as_unicode(encoding='utf-8', errors='strict'):  # @NoSelf
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to :class:`unicode` (:class:`str` under Python 3) decode
        outgoing things.

        :keyword string encoding: Unicode encoding

        :keyword string errors: error handling for decoding issues
        '''
