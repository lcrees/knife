# -*- coding: utf-8 -*-
'''base chainsaw mixins'''

from threading import local
from collections import deque

from stuf.utils import OrderedDict
from stuf.core import stuf, frozenstuf, orderedstuf

from chainsaw._compat import tounicode, tobytes


class ChainsawMixin(local):

    '''base chainsaw mixin'''

    ###########################################################################
    ## things in process ######################################################
    ###########################################################################

    def as_one(self):
        '''
        Switch to performing operations on incoming things as one whole thing.
        '''
        self._mode = self._ONE
        return self

    def as_many(self):
        '''
        Switch to performing operations on each incoming thing as just one
        individual thing in a series of many individual things.
        '''
        self._mode = self._MANY
        return self

    ###########################################################################
    ## things in context ######################################################
    ###########################################################################

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

    @classmethod
    def as_auto(cls):
        '''
        Switch to context where incoming things are automatically rebalanced
        with outgoing things.
        '''
        cls._DEFAULT_CHAIN = cls._AUTO
        return cls

    @classmethod
    def as_manual(cls):
        '''
        Switch to context where incoming things must be manually rebalanced
        with outgoing things.
        '''
        cls._DEFAULT_CHAIN = cls._MANUAL
        return cls

    def shift_in(self):
        '''Manually copy outgoing things back to incoming things.'''
        with self._auto(
            chainin=self._OUTVAR, chainout=self._INVAR, snap=False,
        ):
            return self._xtend(self._iterable)

    def shift_out(self):
        '''Manually copy incoming things to outgoing things.'''
        with self._auto(snap=False):
            return self._xtend(self._iterable)

    @property
    def balanced(self):
        '''Determine if incoming and outgoing things are in balance'''
        return self.count_out() == self.__len__()

    ###########################################################################
    ## things called ##########################################################
    ###########################################################################

    def arguments(self, *args, **kw):
        '''
        Assign any positional and/or keyword arguments to be used anytime the
        current callable or alternative callable is invoked.
        '''
        # position arguments
        self._args = args
        # keyword arguemnts
        self._kw = kw
        return self

    def tap(self, call, alt=None, factory=False):
        '''
        Assign current callable. Optionally assign an alternative callable. If
        `factory` flag is set to :const:`True`, use the callable passed with
        the `call` argument as a factory to build the current callable.

        :param call: callable assigned as current callable

        :param alt: callable assigned as alternative callable (*default:*
          :const:`None`)

        :param factory: whether `call` is a factory that produces callables
          (*default:* :const:`False`)
        '''
        # reset stored position arguments
        self._args = ()
        # reset stored keyword arguments
        self._kw = {}
        # if callable is a factory for building current callable, configure
        if factory:
            def factory_(*args, **kw):
                return call(*args, **kw)
            self._call = factory_
        # or just assign current callable
        else:
            self._call = call
        # set any alternative callable
        self._alt = alt
        return self

    def untap(self):
        '''
        Clear any current callable, alternative callable, or assigned position
        or keywork arguments.
        '''
        # reset position arguments
        self._args = ()
        # reset keyword arguments
        self._kw = {}
        # reset current callable
        self._call = None
        # reset alternative callable
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
        return (self._truth if self._truth is not None else self.__len__())

    ###########################################################################
    ## clearing things up #####################################################
    ###########################################################################

    def clear(self):
        '''Clear out everything.'''
        self._truth = None
        return self.untap().unwrap().clear_out().clear_in()._clearw()._clearh()


class OutchainMixin(local):

    '''chainsaw output mixin'''

    def which(self, call=None, alt=None):
        '''
        Choose current callable based on results of condition mode.

        :param call: new callable to use if condition is :const:`True`
          (*default:* :const:`None`)
        :param alt: new external callable to use if condition is :const:`False`
          (*default:* :const:`None`)
        '''
        if self.__bool__():
            # use external call or current callable
            self._call = call if call is not None else self._call
        else:
            # use external callable or current alternative callable
            self._call = alt if alt is not None else self._alt
        # return to edit mode
        return self.as_edit()

    def end(self):
        '''Return outgoing things, cleaning out everything afterwards.'''
        self._unchain()
        value = self._output()
        # clear every last thing
        self.clear()._clearsp()
        return value

    def results(self):
        '''Return outgoing things, clearing outgoing things afterwards.'''
        self._unchain()
        value = self._output()
        # clear out
        self.clear_out()
        # restore baseline if in query context
        if self._context == self._QUERY:
            self.undo(baseline=True)
        return value

    ###########################################################################
    ## wrapping things ########################################################
    ###########################################################################

    def wrap(self, wrapper):
        '''
        `Iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper for outgoing things.

        :param wrapper: an iterable wrapper
        '''
        self._wrapper = wrapper
        return self

    ###########################################################################
    ## string wrapping things #################################################
    ###########################################################################

    def as_ascii(self, errors='strict'):
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to :class:`byte` encode each incoming thing with the
        ``'ascii'`` codec (*regardless of its original type*)

        :param errors: error handling for decoding issues (*default*:
          ``'strict'``)
        '''
        return self.wrap(lambda x: tobytes(x, 'ascii', errors))

    def as_bytes(self, encoding='utf-8', errors='strict'):
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to :class:`byte` encode each incoming thing (*regardless of
        its original type*).

        :param encoding: Unicode encoding (*default:* ``'utf-8'``)

        :param errors: error handling for encoding issues (*default:*
          ``'strict'``)
        '''
        return self.wrap(lambda x: tobytes(x, encoding, errors))

    def as_unicode(self, encoding='utf-8', errors='strict'):
        '''
        Set`iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to :class:`unicode` (:class:`str`` under Python 3) decode
        each incoming thing (*regardless of its original type*).

        :param encoding: Unicode encoding (*default:* ``'utf-8'``)

        :param errors: error handling for decoding issues (*default:*
          ``'strict'``)
        '''
        return self.wrap(lambda x: tounicode(x, encoding, errors))

    ###########################################################################
    ## sequence wrapping things ###############################################
    ###########################################################################

    def as_list(self):
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to :class:`list`.
        '''
        return self.wrap(list)

    unwrap = as_list

    def as_deque(self):
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to :class:`deque`.
        '''
        return self.wrap(deque)

    def as_tuple(self):
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to :class:`tuple`.
        '''
        return self.wrap(tuple)

    ###########################################################################
    ## map wrapping things ####################################################
    ###########################################################################

    def as_dict(self):
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to :class:`dict`.
        '''
        return self.wrap(dict)

    def as_ordereddict(self):
        '''
        Set `iterable  <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to :class:`OrderedDict`.
        '''
        return self.wrap(OrderedDict)

    ###########################################################################
    ## stuf wrapping things ###################################################
    ###########################################################################

    def as_frozenstuf(self):
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to :class:`frozenstuf`.
        '''
        return self.wrap(frozenstuf)

    def as_orderedstuf(self):
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to :class:`frozenstuf`.
        '''
        return self.wrap(orderedstuf)

    def as_stuf(self):
        '''
        Set `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ wrapper to
        :class:`stuf`.
        '''
        return self.wrap(stuf)

    ###########################################################################
    ## set wrapping things ####################################################
    ###########################################################################

    def as_frozenset(self):
        '''
        Set `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ wrapper to
        :class:`frozenset`.
        '''
        return self.wrap(frozenset)

    def as_set(self):
        '''
        Set `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ wrapper to
        :class:`set`.
        '''
        return self.wrap(set)
