# -*- coding: utf-8 -*-
'''base chainsaw mixins'''

from threading import local

from chainsaw._compat import tounicode, tobytes


class ChainsawMixin(local):

    '''base chainsaw mixin'''

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
    # reset incoming things back to a baseline snapshot after using results of
    # operations on incoming to determine which of two paths to follow
    _TRUTH = 'CONDITION'

    def as_edit(self):
        '''
        Switch to editing context where operations can be performed on incoming
        things from initial placement to final extraction.
        '''
        self._context = self._EDIT
        self._truth = None
        return self.clear().undo(baseline=True)._unchain()

    def as_truth(self):
        '''
        Switch to evaluation context where the results of operations on
        incoming things determine which of two potential paths to execute.
        After exiting the evaluation context by invoking ``which``, incoming
        things automatically revert to a prior baseline snapshot of incoming
        things so further operations can be performed on an unmodified baseline
        version.
        '''
        self._context = self._TRUTH
        return self.snapshot(baseline=True)._as_chain(hard=True, snap=False)

    def as_view(self):
        '''
        Switch to query context where the results of operations on incoming
        things queried. Upon exit from query context by invoking ``results``
        or ``end``, incoming things automatically revert to a prior baseline
        snapshot of so that further operations can be performed on an
        unmodified baseline version.
        '''
        self._context = self._QUERY
        self._truth = None
        return self.snapshot(baseline=True)._as_chain()

    ###########################################################################
    ## things in chain ########################################################
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

    ###########################################################################
    ## things called ##########################################################
    ###########################################################################

    def arguments(self, *args, **kw):
        '''
        Assign positional or keyword arguments used anytime assigned function
        (or its alternative) is invoked.
        '''
        # positional arguments
        self._args = args
        # keyword arguemnts
        self._kw = kw
        return self

    def tap(self, call, alt=None):
        '''
        Assign assigned function.

        :param call: function to assign

        :param alt: alternative function (*default:* :const:`None`)
        '''
        # reset stored position arguments
        self._args = ()
        # reset stored keyword arguments
        self._kw = {}
        # assign assigned function
        self._call = call
        # assign alternative function
        self._alt = alt
        return self

    def untap(self):
        '''Clear assigned function, alternative function, and arguments.'''
        # reset position arguments
        self._args = ()
        # reset keyword arguments
        self._kw = {}
        # reset assigned function
        self._call = None
        # reset alternative function
        self._alt = None
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

        :param thing: one incoming thing
        '''
        with self._man1():
            return self._append(thing)

    def appendstart(self, thing):
        '''
        Insert `thing` **before** any other incoming things.

        :param thing: one incoming thing
        '''
        with self._man1():
            return self._appendfront(thing)

    ###########################################################################
    ## knowing things #########################################################
    ###########################################################################

    def __bool__(self):
        '''
        Return either results built up while in truth context or return the
        number of incoming things.
        '''
        return self._truth if self._truth is not None else self.__len__()

    _REPR = (
        '{0}.{1} ([IN: {2}({3}) => WORK: {4}({5}) => UTIL: {6}({7}) => OUT: '
        '{8}: ({9})]) <<mode: {10}/context: {11}>>'
    )

    def __repr__(self):
        '''Object representation.'''
        return self._repr()

    ###########################################################################
    ## clearing things up #####################################################
    ###########################################################################

    def clear(self):
        '''Clear out everything.'''
        self._truth = None
        return self.untap().unwrap().clear_out().clear_in()._clearworking()


class OutchainMixin(local):

    '''chainsaw output mixin'''

    def end(self):
        '''Return outgoing things, cleaning out everything afterwards.'''
        value = self._unchain()._output()
        # clear every last thing
        self.clear()._clearsp()
        return value

    def results(self):
        '''Return outgoing things, clearing outgoing things afterwards.'''
        value = self._unchain()._output()
        # clear out
        self.clear_out()
        # restore baseline if in query context
        if self._context == self._QUERY:
            self.undo(baseline=True)
        return value

    def which(self, call=None, alt=None):
        '''
        Choose assigned function based on results of condition mode.

        :param call: new function to use if condition is :const:`True`
          (*default:* :const:`None`)
        :param alt: new external function to use if condition is :const:`False`
          (*default:* :const:`None`)
        '''
        if self.__bool__():
            # use external call or assigned function
            self._call = call if call is not None else self._call
        else:
            # use external function or current alternative function
            self._call = alt if alt is not None else self._alt
        # return to edit mode
        return self.as_edit()

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

    def as_ascii(self, errors='strict'):
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to :class:`byte` encode each incoming thing with the
        ``'ascii'`` codec.

        :param errors: error handling for decoding issues (*default*:
          ``'strict'``)
        '''
        self._wrapper = lambda x: tobytes(x, 'ascii', errors)
        return self

    def as_bytes(self, encoding='utf-8', errors='strict'):
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to :class:`byte` encode each incoming thing.

        :param encoding: Unicode encoding (*default:* ``'utf-8'``)

        :param errors: error handling for encoding issues (*default:*
          ``'strict'``)
        '''
        self._wrapper = lambda x: tobytes(x, encoding, errors)
        return self

    def as_dict(self):
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to :class:`dict` each incoming thing.
        '''
        self._wrapper = dict
        return self

    def as_list(self):
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to :class:`deque` each incoming thing.
        '''
        self._wrapper = list
        return self

    unwrap = as_list

    def as_set(self):
        '''
        Set `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ wrapper to
        :class:`set` each incoming thing.
        '''
        self._wrapper = set
        return self

    def as_tuple(self):
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to :class:`tuple` each incoming thing.
        '''
        self._wrapper = tuple
        return self

    def as_unicode(self, encoding='utf-8', errors='strict'):
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to :class:`unicode` (:class:`str` under Python 3) decode
        each incoming thing.

        :param encoding: Unicode encoding (*default:* ``'utf-8'``)

        :param errors: error handling for decoding issues (*default:*
          ``'strict'``)
        '''
        self._wrapper = lambda x: tounicode(x, encoding, errors)
        return self
