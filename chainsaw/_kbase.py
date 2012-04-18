# -*- coding: utf-8 -*-
'''base chainsaw keys'''

from appspace.keys import AppspaceKey


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
    ## things are called ######################################################
    ###########################################################################

    def worker(call):  # @NoSelf
        '''
        Assign worker.

        :argument worker: a Python callable
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
        <http://docs.python.org/glossary.html#term-positional-argument>`_ and
        `keyword <http://docs.python.org/glossary.html#term-keyword-argument>`_
        params used when the worker is invoked.
        '''

    ###########################################################################
    ## things coming in #######################################################
    ###########################################################################

    def prepend(things):  # @NoSelf
        '''
        Insert `things` **before** any other incoming things.

        :argument things: incoming things
        '''

    def append(things):  # @NoSelf
        '''
        Insert `things` **after** any other incoming things.

        :argument things: incoming things
        '''

    ###########################################################################
    ## knowing things #########################################################
    ###########################################################################

    def __len__():  # @NoSelf
        '''Number of incoming things.'''

    def __repr__(self):
        '''Object representation.'''
        return self._repr()


class KOutput(KChainsaw):

    '''output key'''

    ###########################################################################
    ## things going out #######################################################
    ###########################################################################

    def __iter__():  # @NoSelf
        '''Iterate over outgoing things.'''

    def fetch():  # @NoSelf
        '''
        Return outgoing things (wrapped with the current `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ wrapper.
        '''

    def peek():  # @NoSelf
        '''
        Preview current state of incoming things (wrapped with the current
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper).
        '''

    ###########################################################################
    ## state of things ########################################################
    ###########################################################################

    def undo(snapshot=0):  # @NoSelf
        '''
        Restore incoming things to a previous state.

        :keyword integer snapshot: number of steps ago e.g. ``1``, ``2``, ``3``
        '''

    def snapshot():  # @NoSelf
        '''
        Take baseline snapshot of the current state of incoming things.
        '''

    def stepback():  # @NoSelf
        '''
        Restore incoming things to baseline state.
        '''

    def original():  # @NoSelf
        '''
        Restore incoming things to initial state.
        '''

    ###########################################################################
    ## clean up things ########################################################
    ###########################################################################

    def clear():  # @NoSelf
        '''
        Clear everything.
        '''

    ###########################################################################
    ## wrap things up #########################################################
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
