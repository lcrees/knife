# -*- coding: utf-8 -*-
'''reference keys'''

from appspace.keys import AppspaceKey, Attribute


class KChainsaw(AppspaceKey):

    '''base chainsaw key'''

    ###########################################################################
    ## things in process ######################################################
    ###########################################################################

    def as_one():  # @NoSelf
        '''
        Switch to performing operations on incoming things as one whole thing.
        '''

    def as_many():  # @NoSelf
        '''
        Switch to performing operations on each incoming thing as just one
        individual thing in a series of many individual things.
        '''

    ###########################################################################
    ## things in context ######################################################
    ###########################################################################

    def as_edit():  # @NoSelf
        '''
        Switch to editing context where operations can be performed on incoming
        things from initial placement to final extraction.
        '''

    def as_truth():  # @NoSelf
        '''
        Switch to evaluation context where the results of operations on
        incoming things determine which of two potential paths to execute.
        After exiting the evaluation context by invoking ``which``, incoming
        things automatically revert to a prior baseline snapshot of incoming
        things so further operations can be performed on an unmodified baseline
        version.
        '''

    def as_view():  # @NoSelf
        '''
        Switch to query context where the results of operations on incoming
        things queried. Upon exit from query context by invoking ``results``
        or ``end``, incoming things automatically revert to a prior baseline
        snapshot of so that further operations can be performed on an
        unmodified baseline version.
        '''

    ###########################################################################
    ## things in chain ########################################################
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

    def shift_in():  # @NoSelf
        '''Manually copy outgoing things back to incoming things.'''

    def shift_out():  # @NoSelf
        '''Manually copy incoming things to outgoing things.'''

    balanced = Attribute(
        '''Determine if incoming and outgoing things are in balance.'''
    )

    ###########################################################################
    ## snapshot of things #####################################################
    ###########################################################################

    def snapshot(baseline=False, original=False):  # @NoSelf
        '''
        Take a snapshot of current incoming things.

        :param baseline: make this snapshot the baseline snapshot (*default:*
          :const:`False`)
        :param original: make this snapshot the original snapshot (*default:*
          :const:`False`)
        '''

    def undo(snapshot=0, baseline=False, original=False):  # @NoSelf
        '''
        Revert incoming things to a previous snapshot of incoming things.

        :param snapshot: number of steps ago e.g. ``1``, ``2``, ``3``, etc.
          (*default:* ``0``)
        :param baseline: revert incoming things to baseline snapshot (
          *default:* :const:`False`)
        :param original: revert incoming things to original snapshot (
          *default:* :const:`False`)
        '''

    ###########################################################################
    ## things called ##########################################################
    ###########################################################################

    def arguments(*args, **kw):  # @NoSelf
        '''
        Assign any positional and/or keyword arguments to be used anytime the
        current callable or alternative callable is invoked.
        '''

    def tap(call, alt=None, factory=False):  # @NoSelf
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

    def untap():  # @NoSelf
        '''
        Clear any current callable, alternative callable, or assigned position
        or keywork arguments.
        '''

    ###########################################################################
    ## things coming in #######################################################
    ###########################################################################

    def extend(things):  # @NoSelf
        '''
        Insert `things` **after** any other incoming things.

        :param things: incoming things
        '''

    def extendstart(things):  # @NoSelf
        '''
        Insert `things` **before** any other incoming things.

        :param things: incoming things
        '''

    def append(thing):  # @NoSelf
        '''
        Insert `thing` **after** any other incoming things.

        :param thing: one incoming thing
        '''

    def appendstart(thing):  # @NoSelf
        '''
        Insert `thing` **before** any other incoming things.

        :param thing: one incoming thing
        '''

    ###########################################################################
    ## knowing things #########################################################
    ###########################################################################

    def __bool__():  # @NoSelf
        '''
        Return either results built up while in truth context or return the
        number of incoming things.
        '''

    ###########################################################################
    ## know things ############################################################
    ###########################################################################

    def __len__():  # @NoSelf
        '''Number of incoming things.'''

    def count():  # @NoSelf
        '''Number of incoming things.'''

    def count_out():  # @NoSelf
        '''Number of outgoing things.'''

    ###########################################################################
    ## clearing things up #####################################################
    ###########################################################################

    def clear():  # @NoSelf
        '''Clear out everything.'''

    def clear_in():  # @NoSelf
        '''Clear incoming things.'''

    def clear_out():  # @NoSelf
        '''Clear outgoing things.'''


class KOutchain(KChainsaw):

    '''active output chainsaw mixin'''

    def __iter__():  # @NoSelf
        '''Yield outgoing things.'''

    def which(call=None, alt=None):  # @NoSelf
        '''
        Choose current callable based on results of condition mode.

        :param call: new callable to use if condition is :const:`True`
          (*default:* :const:`None`)
        :param alt: new external callable to use if condition is :const:`False`
          (*default:* :const:`None`)
        '''

    def end():  # @NoSelf
        '''Return outgoing things, cleaning out everything afterwards.'''

    def results():  # @NoSelf
        '''Return outgoing things, clearing outgoing things afterwards.'''

    def preview():  # @NoSelf
        '''Take a peek at the current state of outgoing things.'''

    ###########################################################################
    ## wrapping things ########################################################
    ###########################################################################

    def wrap(wrapper):  # @NoSelf
        '''
        `Iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper for outgoing things.

        :param wrapper: an iterable wrapper
        '''

    def unwrap():  # @NoSelf
        '''Reset current wrapper to default.'''

    ###########################################################################
    ## string wrapping things #################################################
    ###########################################################################

    def as_ascii(errors='strict'):  # @NoSelf
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to :class:`byte` encode each incoming thing with the
        ``'ascii'`` codec (*regardless of its original type*)

        :param errors: error handling for decoding issues (*default:*
          ``'strict'``)
        '''

    def as_bytes(encoding='utf-8', errors='strict'):  # @NoSelf
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to :class:`byte` encode each incoming thing (*regardless of
        its original type*).

        :param encoding: Unicode encoding (*default:* ``'utf-8'``)

        :param errors: error handling for encoding issues (*default:*
          ``'strict'``)
        '''

    def as_unicode(encoding='utf-8', errors='strict'):  # @NoSelf
        '''
        Set`iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to :class:`unicode` (:class:`str`` under Python 3) decode
        each incoming thing (*regardless of its original type*).

        :param encoding: Unicode encoding (*default:* ``'utf-8'``)

        :param errors: error handling for decoding issues (*default:*
          ``'strict'``)
        '''

    ###########################################################################
    ## sequence wrapping things ###############################################
    ###########################################################################

    def as_list():  # @NoSelf
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to :class:`list`.
        '''

    def as_deque():  # @NoSelf
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to :class:`deque`.
        '''

    def as_tuple():  # @NoSelf
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to :class:`tuple`.
        '''

    ###########################################################################
    ## map wrapping things ####################################################
    ###########################################################################

    def as_dict():  # @NoSelf
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to :class:`dict`.
        '''

    def as_ordereddict():  # @NoSelf
        '''
        Set `iterable  <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to :class:`OrderedDict`.
        '''

    ###########################################################################
    ## stuf wrapping things ###################################################
    ###########################################################################

    def as_frozenstuf():  # @NoSelf
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to :class:`frozenstuf`.
        '''

    def as_orderedstuf():  # @NoSelf
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to :class:`orderedstuf`.
        '''

    def as_stuf():  # @NoSelf
        '''
        Set `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ wrapper to
        :class:`stuf`.
        '''

    ###########################################################################
    ## set wrapping things ####################################################
    ###########################################################################

    def as_frozenset():  # @NoSelf
        '''
        Set `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ wrapper to
        :class:`frozenset`.
        '''

    def as_set():  # @NoSelf
        '''
        Set `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ wrapper to
        :class:`set`.
        '''


class KReduce(AppspaceKey):

    '''reduce key'''

    def concat():  # @NoSelf
        '''
        Collect one
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        created by merge multiple `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_ together.
        '''

    def flatten():  # @NoSelf
        '''
        Collect the result of reducing an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ of nested things
        to an `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        of unnested things because `flat is better than nested
        <http://www.python.org/dev/peps/pep-0020/>`_.
        '''

    def join(separator='', encoding='utf-8', errors='strict'):  # @NoSelf
        '''
        Collect the result of combining an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ of multiple
        things into one :class:`unicode` (:class:`str` on Python 3) decoded
        thing.

        :param separator: string to join at (*default:*: ``''``)

        :param encoding: Unicode encoding for things (*default:*: ``'utf-8'``)

        :param errors: error handling when encoding things (*default:*:
          ``'strict'``)
        '''

    def reduce(initial=None, reverse=False):  # @NoSelf
        '''
        Collect the result of reducing an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ down to one
        thing using the current callable. If ``reverse`` is set to
        :const:`True`, reduction `comes from the right side
        <http://www.zvon.org/other/haskell/Outputprelude/foldr_f.html>`_ of an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_.
        Otherwise, reduction comes from the left side of an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.

        :param initial: starting value (*default:*: :const:`None`)

        :param reverse: reduce from right side of an `iterable
          <http://docs.python.org/glossary.html#term-iterable>`_ (*default:*:
          :const:`False`)
        '''

    def weave():  # @NoSelf
        '''
        Collect the result of interleaving multiple `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_ into one
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_.
        '''

    def zip():  # @NoSelf
        '''
        Collect the result of reducing a series of `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_ to one `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ where every two
        things are paired in a :class:`tuple` of (*thing1*, *thing2*) based on
        where they were found within the original `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''


class KSlice(AppspaceKey):

    '''slicing key'''

    def first(n=0):  # @NoSelf
        '''
        Collect either `n` things from the starting end of an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ or just the
        **first* thing within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.

        :param n: number of things (*default:*: ``0``)
        '''

    def initial():  # @NoSelf
        '''
        Collect everything within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ except the very
        **last** thing.
        '''

    def last(n=0):  # @NoSelf
        '''
        Collect either `n` things from the trailing end of an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ or just the
        **last** thing within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.

        :param n: number of things (*default:*: ``0``)
        '''

    def at(n, default=None):  # @NoSelf
        '''
        Collect thing found at `n` position within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ or `default` if
        nothing is found at `n`.

        :param n: index of some thing

        :param default: default thing (*default:*: :const:`None`)
        '''

    def rest():  # @NoSelf
        '''
        Collect everything within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ except the very
        **first** thing.
        '''

    def slice(start, stop=False, step=False):  # @NoSelf
        '''
        Collect a `slice <http://docs.python.org/glossary.html#term-slice>`_ of
        things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.

        :param start: starting index of slice

        :param stop: stopping index of slice (*default:* :const:`False`)

        :param step: size of step in slice (*default:* :const:`False`)
        '''

    def split(n, fill=None):  # @NoSelf
        '''
        Split an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ into multiple
        `iterables <http://docs.python.org/glossary.html#term-iterable>`_ of
        `n` things while using `fill` to pad out results that fall short of
        `n`.

        :param n: number of things per split
        :param fill: value to pad out incomplete things (*default:*
          :const:`None`)
        '''


class KRepeat(AppspaceKey):

    '''repeat key'''

    def combinations(n):  # @NoSelf
        '''
        Collect every possible combination of every `n` things within an
        `iterable` <http://docs.python.org/glossary.html#term-iterable>`_.

        :param n: number of things to derive combinations from
        '''

    def copy():  # @NoSelf
        '''
        Collect duplicates of each thing within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''

    def product(n=1):  # @NoSelf
        '''
        Collect results of nested `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_ repeated `n`
        times.

        :param n: number of loops to repeat (*default:* ``1``)
        '''

    def permutations(n):  # @NoSelf
        '''
        Collect every possible permutation of every `n` things within an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_.

        :param n: number of things to derive permutations from
        '''

    def repeat(n=None, call=False):  # @NoSelf
        '''
        Collect the results of repeat an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ or results
        of invoking the current callable `n` times.

        :param n: number of times to repeat (*default:* :const:`None`)

        :param call: repeat result of current callable (*default:*
          :const:`False`)
        '''


class KMap(AppspaceKey):

    '''map key'''

    def invoke(name):  # @NoSelf
        '''
        Invoke method `name` on each thing within an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_ with
        currently assigned `positional
        <http://docs.python.org/glossary.html#term-positional-argument>`_ and
        `keyword arguments
        <http://docs.python.org/glossary.html#term-keyword-argument>`_ and
        collect the results but
        collect the original thing instead of the value returned after calling
        the method the return value is :const:`None`.

        :param name: method name
        '''

    def map(args=False, kwargs=False, current=False):  # @NoSelf
        '''
        Invoke the current callable on each thing within an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_.

        :param args: pass each thing within an `iterable
          <http://docs.python.org/glossary.html#term-iterable>`_ as `*args
          <http://docs.python.org/glossary.html#term-positional-argument>`_` to
          the current callable (*default:* :const:`False`)
        :param kwargs: pass each thing within an `iterable
          <http://docs.python.org/glossary.html#term-iterable>`_ to the current
          callable as a :class:`tuple` of `*args
          <http://docs.python.org/glossary.html#term-positional-argument>`_ and
          `**kwargs
          <http://docs.python.org/glossary.html#term-keyword-argument>
          (*default:* :const:`False`)
        :param current: pass each thing within an `iterable
          <http://docs.python.org/glossary.html#term-iterable>`_ as a
          :class:`tuple` of `*args
          <http://docs.python.org/glossary.html#term-positional-argument>`_ and
          `**kwargs
          <http://docs.python.org/glossary.html#term-keyword-argument>`_
          combined with any assigned `positional
          <http://docs.python.org/glossary.html#term-positional-argument>`_ or
          `keyword arguments
          <http://docs.python.org/glossary.html#term-keyword-argument>`_ for
          the current callable (*default:* :const:`False`)
        '''


class KCollect(AppspaceKey):

    '''collecting key'''

    def attributes(deep=False, ancestors=False, *names):  # @NoSelf
        '''
        Collect `attributes
        <http://docs.python.org/glossary.html#term-attribute>`_ from things
        within an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_ by
        by matching their `attribute
        <http://docs.python.org/glossary.html#term-attribute>`_ `names`.

        :param deep: traverse deep inside an object (default: :const:`False`)

        :param ancestors: traverse deep inside classes within method resolutio
            order (default: :const:`False`)
        :param *names: attribute
        '''

    def mapping(keys=False, values=False):  # @NoSelf
        '''
        Collect `keys` and `values` from an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_ of
        `mappings <http://docs.python.org/glossary.html#term-mapping>`_.

        :param keys: gather keys only (*default:* :const:`False`)

        :param values: gather values only (*default:* :const:`False`)
        '''

    def items(*keys):  # @NoSelf
        '''
        Collect things from things (usually `sequences
        <http://docs.python.org/glossary.html#term-sequence>`_ or `mappings
        <http://docs.python.org/glossary.html#term-mapping>`_) within an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        by matching their `*keys`.

        :param *keys: item keys or indexes
        '''


class KFilter(AppspaceKey):

    '''filtering key'''

    def filter(pattern=None, invert=False, flags=0):  # @NoSelf
        '''
        Collect anything within an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_ that
        passes a filter. Usually the first thing that the filter evaluates as
        :const:`True` is returned. If `reverse` is :const:`True`, things that
        the filter evaluates as :const:`False` are returned. The current
        callable is used as the filter unless regular expression `pattern`
        is supplied, in which case `pattern` is used as the filter.

        :param pattern: regular expression search pattern (*default:*
          :const:`None`)
        :param invert: return things for which filter is :const:`False` rather
          than :const:`True` (*default:* :const:`False`)
        :param flags: `regular expression flags
          <http://docs.python.org/library/re.html#re.DEBUG>`_ (*default:*
         ``0``)
        '''

    def find(pattern=None, invert=False, flags=0):  # @NoSelf
        '''
        Collect the first thing within an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_ that
        passes a filter. Usually the first thing that the filter evaluates as
        :const:`True` is returned. If `reverse` is :const:`True`, the first
        thing that the filter evaluates as :const:`False` is returned.
        The current callable is used as the filter unless regular expression
        `pattern` is supplied, in which case `pattern` is used as the filter.

        :param pattern: regular expression search pattern (default:
          :const:`None`)
        :param invert: return things for which filter is :const:`False` and not
          :const:`True` (*default:* :const:`False`)
        :param flags: `regular expression flags
          <http://docs.python.org/library/re.html#re.DEBUG>`_ (*default:*
         ``0``)
        '''

    def replace(pattern, new, count=0, flags=0):  # @NoSelf
        '''
        Replace parts of string things within an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_ with a
        new string thing if they match regular expression `pattern`.

        :param pattern: regular expression pattern

        :param new: replacement string

        :param count: maximum number of replacements to make within a string
          (*default:* ``0``)
        :param flags: `regular expression flags
          <http://docs.python.org/library/re.html#re.DEBUG>`_ (*default:*
          ``0``)
        '''

    def difference(symmetric=False):  # @NoSelf
        '''
        Collect differences within a series of
        `iterables <http://docs.python.org/glossary.html#term-iterable>`_.

        :param symmetric: use symmetric difference (*default:* :const:`False`)
        '''

    def disjointed():  # @NoSelf
        '''
        Collect disjoints within a series of `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''

    def intersection():  # @NoSelf
        '''
        Collect intersections within a series of `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''

    def partition(pattern=None, flags=0):  # @NoSelf
        '''
        Collect two `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_ divided into
        :const:`True` and :const:`False` based on whether the current callable
        returns :const:`True` or :const:`False` for each thing within an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_.
        The current callable is used as the filter unless regular expression
        `pattern` is supplied, in which case `pattern` is used as the filter.

        :param pattern: regular expression search pattern (*default:*
          :const:`None`)
        :param flags: `regular expression flags
          <http://docs.python.org/library/re.html#re.DEBUG>`_ (*default:*
          ``0``)
        '''

    def subset():  # @NoSelf
        '''
        Collect :const:True: if an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ is a
        subset of another `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''

    def superset():  # @NoSelf
        '''
        Collect :const:True: if an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ is
        a superset of another `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''

    def union():  # @NoSelf
        '''
        Collect the union of things within a series of `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''

    def unique():  # @NoSelf
        '''
        Collect unique things within an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_.
        '''


class KMath(AppspaceKey):

    '''math key'''

    def average():  # @NoSelf
        '''
        Collect average thing within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''

    def max():  # @NoSelf
        '''
        Collect maximum thing within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ using the
        current callable as the `key function
        <http://docs.python.org/glossary.html#term-key-function>`_.
        '''

    def median():  # @NoSelf
        '''
        Collect median thing within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''

    def min():  # @NoSelf
        '''
        Collect minimum thing within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ using the
        current callable as the `key function
        <http://docs.python.org/glossary.html#term-key-function>`_.
        '''

    def minmax():  # @NoSelf
        '''
        Collect minimum and maximum things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_
        as a :class:`tuple` consisting of (*minimum value*, *maximum value*).
        '''

    def range():  # @NoSelf
        '''
        Collect length of the smallest interval that can contain each thing
        within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''

    def sum(start=0, floats=False):  # @NoSelf
        '''
        Collect total from adding up `start` and each thing within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.

        :param start: starting number (*default:* ``0``)

        :param floats: add floats with extended precision (*default:*
          :const:`False`)
        '''


class KTruth():

    '''truth key'''

    def all():  # @NoSelf
        '''
        Collect :const:`True` if the current callable returns :const:`True` for
        **everything** within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ (or if
        the `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        is empty).
        '''

    def any():  # @NoSelf
        '''
        Collect :const:`True` if the current callable returns :const:`True` for
        **anything** within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ (or if
        the `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        is empty).
        '''

    def frequency():  # @NoSelf
        '''
        Collect the number of times each thing occurs within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_. Returns a
        :class:`tuple` consisting of (*least common thing*, *most common
        thing*, *count of everything* consisting of a :class:`list` of
        :class:`tuple` pairs of (*thing*, *count*).
        '''

    def quantify():  # @NoSelf
        '''
        Collect the number of times the current callable returns :const:`True`
        for *anything* within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''


class KOrder(AppspaceKey):

    '''order mixin'''

    def choice():  # @NoSelf
        '''
        Collect a randomly selected thing from an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''

    def groupby():  # @NoSelf
        '''
        Collect things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ grouped using
        the current callable as the `key function
        <http://docs.python.org/glossary.html#term-key-function>`_.
        '''

    def reverse():  # @NoSelf
        '''
        Collect the current order of things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''

    def sort():  # @NoSelf
        '''
        Collect things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ sorted using the
        current callable as the `key function
        <http://docs.python.org/glossary.html#term-key-function>`_.
        '''

    def sample(n):  # @NoSelf
        '''
        Collect a randomly sample of `n` size from things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.

        :param n: size of sample
        '''

    def shuffle():  # @NoSelf
        '''
        Collect things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ that have been
        randomly rearranged from their previous order.
        '''


class KSaw(KOutchain, KCollect, KFilter, KReduce, KMap, KMath, KSlice, KTruth,
    KOrder, KRepeat):

    '''combined key'''
