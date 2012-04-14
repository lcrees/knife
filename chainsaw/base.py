# -*- coding: utf-8 -*-
'''base chainsaw mixins'''

from threading import local

from chainsaw._compat import tounicode, tobytes


class ChainsawMixin(local):

    '''base chainsaw mixin'''

    def __init__(self, *things, **kw):
        '''
        init

        :params `*things`: incoming things
        '''
        super(ChainsawMixin, self).__init__(*things, **kw)

    ###########################################################################
    ## things in process ######################################################
    ###########################################################################

    # chainsaw all incoming things as one thing
    _ONE = _DEFAULT_MODE = 'TREAT AS ONE'
    # chainsaw each incoming thing as one of many individual things
    _MANY = 'TREAT AS MANY'

    def as_many(self):
        '''
        Switch to performing operations on each incoming thing as just one
        individual thing in a series of many individual things.
        '''
        self._mode = self._MANY
        return self

    def as_one(self):
        '''
        Switch to performing operations on incoming things as one whole thing.
        '''
        self._mode = self._ONE
        return self

    ###########################################################################
    ## things in context ######################################################
    ###########################################################################

    # modify incoming things from input to output in one series of operations
    _EDIT = _DEFAULT_CONTEXT = 'EDIT'
    # reset incoming things back to a baseline snapshot after each query
    _QUERY = 'QUERY'

    def as_edit(self):
        '''
        Switch to editing context where operations can be performed on incoming
        things from initial placement to final extraction.
        '''
        self._context = self._EDIT
        self._truth = None
        return self.clear().undo(baseline=True)._unchain()

    def as_query(self):
        '''
        Switch to context where, upon exiting it by invoking ``results``
        or ``end`` method, incoming things automatically revert to the baseline
        snapshot so the unmodified baseline version of incoming things can be
        worked with.
        '''
        self._context = self._QUERY
        self._truth = None
        return self.snapshot(baseline=True)._as_chain()

    ###########################################################################
    ## things in chains #######################################################
    ###########################################################################

    # automatically balance ins with out
    _AUTO = True
    # manually balance ins with out
    _DEFAULT_CHAIN = _MANUAL = '_man4'
    # 1. link for incoming things which is chained to =>
    _INCFG = 'chainin'
    _INVAR = '_in'
    # 2. link for working on incoming things which is chained to =>
    _WORKCFG = 'work'
    _WORKVAR = '_work'
    # 3. link temporarily holding chainsawed things which is chained to =>
    _HOLDCFG = 'hold'
    _HOLDVAR = '_hold'
    # 4. link where outgoing things can be removed from chain
    _OUTCFG = 'chainout'
    _OUTVAR = '_out'

    @classmethod
    def as_auto(cls):
        '''
        Switch to context where incoming things are automatically rebalanced
        with outgoing things.
        '''
        cls._AUTO = True
        return cls

    @classmethod
    def as_manual(cls):
        '''
        Switch to context where incoming things must be manually rebalanced
        with outgoing things.
        '''
        cls._AUTO = False
        return cls

    def out_in(self):
        '''
        Copy outgoing things to incoming things.
        '''
        return self._outin()

    def in_out(self):
        '''
        Copy incoming things to outgoing things.
        '''
        return self._inout()

    @property
    def balanced(self):
        '''
        Whether outgoing things and incoming things are in balance.
        '''
        return self._balanced()

    ###########################################################################
    ## snapshot of things #####################################################
    ###########################################################################

    def snapshot(self, baseline=False, original=False):
        '''
        Take a snapshot of the current incoming things.

        :param baseline: make this snapshot the baseline snapshot (*default:*
          :const:`False`)
        :param original: make this snapshot the original snapshot (*default:*
          :const:`False`)
        '''
        return self._snapshot(baseline, original)

    def undo(self, snapshot=0, baseline=False, original=False):
        '''
        Revert incoming things to a previous snapshot.

        :param snapshot: number of steps ago e.g. ``1``, ``2``, ``3``, etc.
          (*default:* ``0``)
        :param baseline: revert incoming things to baseline snapshot (
          *default:* :const:`False`)
        :param original: revert incoming things to original snapshot (
          *default:* :const:`False`)
        '''
        return self._undo(snapshot, baseline, original)

    ###########################################################################
    ## things called ##########################################################
    ###########################################################################

    def arguments(self, *args, **kw):
        '''
        Assign positional or keyword arguments used anytime the worker
        is invoked.
        '''
        # positional arguments
        self._args = args
        # keyword arguemnts
        self._kw = kw
        return self

    def tap(self, call):
        '''
        Assign worker.

        :param call: a callable
        '''
        # reset stored position arguments
        self._args = ()
        # reset stored keyword arguments
        self._kw = {}
        # assign worker
        self._call = call
        return self

    def untap(self):
        '''
        Clear any active callable and global positional or keyword arguments.
        '''
        # reset position arguments
        self._args = ()
        # reset keyword arguments
        self._kw = {}
        # reset worker
        self._call = None
        return self

    def pattern(self, pattern, type='parse', flags=0):
        '''
        Compile a search pattern and use it as the worker.

        :param pattern: search pattern

        :param type: engine to compile pattern with. Valid options are
          ``'parse'``, ``'regex'``, or ``'glob'`` (default: ``'parse'``)

        :param flags: regular expression `flags
          <http://docs.python.org/library/re.html#re.DEBUG>`_ (*default:*
          ``0``)

        :param compiler: engine to compile pattern with. Valid options are
          ``'`parse <http://pypi.python.org/pypi/parse/>_```, ``'`re
          <http://docs.python.org/library/re.html>_`'``, or ``'`glob
          <http://docs.python.org/library/fnmatch.html>_`'`` (default:
          ``'parse'``)
        '''
        self._call = self._pattern(pattern, type, flags)
        return self

    ###########################################################################
    ## things coming in #######################################################
    ###########################################################################

    def extend(self, things):
        '''
        Insert `things` **after** any other incoming things.

        :param things: incoming things
        '''
        with self._man1():
            return self._xtend(things)

    def extendstart(self, things):
        '''
        Insert `things` **before** any other incoming things.

        :param things: incoming things
        '''
        with self._man1():
            return self._xtendfront(things)

    def append(self, thing):
        '''
        Insert `thing` **after** any other incoming things.

        :param thing: incoming thing
        '''
        with self._man1():
            return self._append(thing)

    def appendstart(self, thing):
        '''
        Insert `thing` **before** any other incoming things.

        :param thing: incoming thing
        '''
        with self._man1():
            return self._appendfront(thing)

    ###########################################################################
    ## knowing things #########################################################
    ###########################################################################

    _REPR = (
        '{0}.{1} ([IN: {2}({3}) => WORK: {4}({5}) => UTIL: {6}({7}) => OUT: '
        '{8}: ({9})]) <<mode: {10}/context: {11}>>'
    )

    def __len__(self):
        '''Number of incoming things.'''
        return self._len()

    def __repr__(self):
        '''Object representation.'''
        return self._repr()

    ###########################################################################
    ## cleaning up things #####################################################
    ###########################################################################

    def clear(self):
        '''
        Remove everything.
        '''
        return self._clear()

    def clear_in(self):
        '''
        Remove incoming things.
        '''
        return self._clearin()

    def clear_out(self):
        '''
        Remove outgoing things.
        '''
        return self._clearout()


class OutputMixin(ChainsawMixin):

    '''output mixin'''

    def __iter__(self):
        '''Yield outgoing things.'''
        return self._iterate()

    def end(self):
        '''
        End the current chainsaw session and return outgoing things, wrapped
        with the `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ wrapper.
        '''
        value = self._unchain()._output()
        # remove every thing
        self.clear()._clearsp()
        return value

    def results(self):
        '''
        Clear and return outgoing things wrapped with the `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ wrapper.
        '''
        value = self._unchain()._output()
        # remove outgoing things
        self.clear_out()
        return value

    def preview(self):
        '''
        Take a peek at the current state of outgoing things.
        '''
        return self._output()

    ###########################################################################
    ## wrapping things ########################################################
    ###########################################################################

    def wrap(self, wrapper):
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper for outgoing things.

        :param wrapper: an `iterable
          <http://docs.python.org/glossary.html#term-iterable>`_ wrapper
        '''
        self._wrapper = wrapper
        return self

    ###########################################################################
    ## wrapping things up #####################################################
    ###########################################################################

    def as_ascii(self, errors='strict'):
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to :class:`byte` encode each outgoing thing with the
        ``'ascii'`` codec.

        :param errors: error handling for decoding issues (*default*:
          ``'strict'``)
        '''
        self._wrapper = lambda x: tobytes(x, 'ascii', errors)
        return self

    def as_bytes(self, encoding='utf-8', errors='strict'):
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to :class:`byte` encode each outgoing thing.

        :param encoding: Unicode encoding (*default:* ``'utf-8'``)

        :param errors: error handling for encoding issues (*default:*
          ``'strict'``)
        '''
        self._wrapper = lambda x: tobytes(x, encoding, errors)
        return self

    def as_dict(self):
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to cast each outgoing thing as a :class:`dict`.
        '''
        self._wrapper = dict
        return self

    def as_list(self):
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to cast each incoming thing as a :class:`list`.
        '''
        self._wrapper = list
        return self

    unwrap = as_list

    def as_set(self):
        '''
        Set `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ wrapper to cast
        each outgoing thing as a :class:`set`.
        '''
        self._wrapper = set
        return self

    def as_tuple(self):
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to cast each outgoing thing to a :class:`tuple`.
        '''
        self._wrapper = tuple
        return self

    def as_unicode(self, encoding='utf-8', errors='strict'):
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to :class:`unicode` (:class:`str` under Python 3) decode
        each outgoing thing.

        :param encoding: Unicode encoding (*default:* ``'utf-8'``)

        :param errors: error handling for decoding issues (*default:*
          ``'strict'``)
        '''
        self._wrapper = lambda x: tounicode(x, encoding, errors)
        return self
