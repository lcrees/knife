# -*- coding: utf-8 -*-
'''reference keys'''

from appspace.keys import AppspaceKey, Attribute


class KChainsaw(AppspaceKey):

    '''base chainsaw key'''

    def __init__(*things, **kw):  # @NoSelf
        '''
        init

        :argument `things`: incoming things
        '''

    ###########################################################################
    ## things in session ######################################################
    ###########################################################################

    def as_many():  # @NoSelf
        '''
        Treat each incoming thing as one processing unit within a series of
        multiple processing units.
        '''

    def as_one():  # @NoSelf
        '''
        Treat multiple incoming things as one processing unit.
        '''

    ###########################################################################
    ## things in transaction ##################################################
    ###########################################################################

    def as_edit():  # @NoSelf
        '''
        Work on incoming things **without** automatically reverting back to a
        baseline snapshot when :meth:`read()` is invoked.
        '''

    def as_query():  # @NoSelf
        '''
        Work on incoming things where incoming things revert to a baseline
        snapshot when :meth:`close()` is invoked.
        '''

    ###########################################################################
    ## things in chains #######################################################
    ###########################################################################

    def as_auto():  # @NoSelf
        '''
        Let incoming things be automatically rebalanced with outgoing things.
        '''

    def as_manual():  # @NoSelf
        '''
        Disallow incoming things from being manually rebalanced with outgoing
        things.
        '''

    def out_in():  # @NoSelf
        '''
        Copy outgoing things back to incoming things for further processing.
        '''

    def in_out():  # @NoSelf
        '''
        Copy incoming things to outgoing things for output.
        '''

    balanced = Attribute(
        '''
        If outgoing and incoming things are in balance.
        '''
    )

    ###########################################################################
    ## snapshot of things #####################################################
    ###########################################################################

    def snapshot(baseline=False, original=False):  # @NoSelf
        '''
        Take a snapshot of the current state of incoming things.

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
    ## things are called ######################################################
    ###########################################################################

    def worker(call):  # @NoSelf
        '''
        Assign worker callable.

        :argument call: a Python callable
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

    def params(*args, **kw):  # @NoSelf
        '''
        Assign global `positional
        <http://docs.python.org/glossary.html#term-positional-argument>`_ or
        `keyword <http://docs.python.org/glossary.html#term-keyword-argument>`_
        params used when the worker is invoked.
        '''

    ###########################################################################
    ## things coming in #######################################################
    ###########################################################################

    def extend(things):  # @NoSelf
        '''
        Insert `things` **after** any other incoming things.

        :argument things: incoming things
        '''

    def extendfront(things):  # @NoSelf
        '''
        Insert `things` **before** any other incoming things.

        :argument things: incoming things
        '''

    def append(thing):  # @NoSelf
        '''
        Insert `thing` **after** any other incoming things.

        :argument thing: incoming thing
        '''

    def prepend(thing):  # @NoSelf
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
        Clear everything.
        '''

    def clear_in():  # @NoSelf
        '''
        Clear incoming things.
        '''

    def clear_out():  # @NoSelf
        '''
        Clear outgoing things.
        '''


class KOutchain(KChainsaw):

    '''output key'''

    def __iter__():  # @NoSelf
        '''Yield outgoing things.'''

    def tell():  # @NoSelf
        '''
        Peek at the current state of outgoing things without modifying things.
        '''

    def read():  # @NoSelf
        '''
        1. Return outgoing things wrapped with the `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ wrapper.
        2. Close transaction by clearing outgoing things.
        '''

    def close():  # @NoSelf
        '''
        1. Return outgoing things wrapped in the `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ wrapper.
        2. Close session by clearing incoming, outgoing, and anything else.
        '''

    ###########################################################################
    ## wrapping things up #####################################################
    ###########################################################################

    def wrapper(wrapper):  # @NoSelf
        '''
        Assign `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper for outgoing things.

        :argument wrapper: an `iterable
          <http://docs.python.org/glossary.html#term-iterable>`_ wrapper
        '''

    def as_ascii(errors='strict'):  # @NoSelf
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to :class:`byte` encode outgoing things with the ``'ascii'``
        codec.

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
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to cast outgoing things to :class:`set`.
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
