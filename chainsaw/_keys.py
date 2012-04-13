# -*- coding: utf-8 -*-
'''reference keys'''

from appspace.keys import AppspaceKey, Attribute


class KChainsaw(AppspaceKey):

    '''base chainsaw key'''

    ###########################################################################
    ## things in process ######################################################
    ###########################################################################

    def as_many():  # @NoSelf
        '''
        Switch to performing operations on each incoming thing as just one
        individual thing in a series of many individual things.
        '''

    def as_one():  # @NoSelf
        '''
        Switch to performing operations on incoming things as one whole thing.
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
        active callable or alternative callable is invoked.
        '''

    def tap(call, alt=None, factory=False):  # @NoSelf
        '''
        Assign active callable. Optionally assign an alternative callable. If
        `factory` flag is set to :const:`True`, use the callable passed with
        the `call` argument as a factory to build the active callable.

        :param call: callable assigned as active callable

        :param alt: callable assigned as alternative callable (*default:*
          :const:`None`)

        :param factory: whether `call` is a factory that produces callables
          (*default:* :const:`False`)
        '''

    def untap():  # @NoSelf
        '''
        Clear any active callable, alternative callable, or assigned position
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

    def end():  # @NoSelf
        '''Return outgoing things, cleaning out everything afterwards.'''

    def results():  # @NoSelf
        '''Return outgoing things, clearing outgoing things afterwards.'''

    def preview():  # @NoSelf
        '''Take a peek at the current state of outgoing things.'''

    def which(call=None, alt=None):  # @NoSelf
        '''
        Choose active callable based on results of condition mode.

        :param call: new callable to use if condition is :const:`True`
          (*default:* :const:`None`)
        :param alt: new external callable to use if condition is :const:`False`
          (*default:* :const:`None`)
        '''

    ###########################################################################
    ## wrapping things ########################################################
    ###########################################################################

    def wrap(wrapper):  # @NoSelf
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper for outgoing things.

        :param wrapper: an `iterable
          <http://docs.python.org/glossary.html#term-iterable>`_ wrapper
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
        ``'ascii'`` codec.

        :param errors: error handling for decoding issues (*default*:
          ``'strict'``)
        '''

    def as_bytes(encoding='utf-8', errors='strict'):  # @NoSelf
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to :class:`byte` encode each incoming thing.

        :param encoding: Unicode encoding (*default:* ``'utf-8'``)

        :param errors: error handling for encoding issues (*default:*
          ``'strict'``)
        '''

    def as_unicode(encoding='utf-8', errors='strict'):  # @NoSelf
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to :class:`unicode` (:class:`str` under Python 3) decode
        each incoming thing.

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
        wrapper to :class:`list` each incoming thing.
        '''

    def as_deque():  # @NoSelf
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to :class:`deque` each incoming thing.
        '''

    def as_tuple():  # @NoSelf
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to :class:`tuple` each incoming thing.
        '''

    ###########################################################################
    ## map wrapping things ####################################################
    ###########################################################################

    def as_dict():  # @NoSelf
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to :class:`dict` each incoming thing.
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
        wrapper to :class:`frozenstuf` each incoming thing.
        '''

    def as_orderedstuf():  # @NoSelf
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to :class:`orderedstuf` each incoming thing.
        '''

    def as_stuf():  # @NoSelf
        '''
        Set `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ wrapper to
        :class:`stuf` each incoming thing.
        '''

    ###########################################################################
    ## set wrapping things ####################################################
    ###########################################################################

    def as_frozenset():  # @NoSelf
        '''
        Set `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ wrapper to
        :class:`frozenset` each incoming thing.
        '''

    def as_set():  # @NoSelf
        '''
        Set `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ wrapper to
        :class:`set` each incoming thing.
        '''


class KFilter(AppspaceKey):

    '''filtering key'''

    def attributes(*names):  # @NoSelf
        '''
        Collect `attributes
        <http://docs.python.org/glossary.html#term-attribute>`_ from things
        within an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_ by
        by matching their attribute `names`.

        :param names: attribute names
        '''

    def duality():  # @NoSelf
        '''
        Divide an iterable into two `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_ based on whether
        the active callable returns :const:`True` or :const:`False` for each
        thing within an iterable.
        '''

    def filter(invert=False):  # @NoSelf
        '''
        Collect everthing within an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        matched by the active callable.

        :param invert: return things for which the filter is :const:`False`
          rather than :const:`True` (*default:* :const:`False`)
        '''

    def items(*keys):  # @NoSelf
        '''
        Collect everything from things (usually `sequences
        <http://docs.python.org/glossary.html#term-sequence>`_ or `mappings
        <http://docs.python.org/glossary.html#term-mapping>`_) within an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        that matches `keys`.

        :param keys: item keys (or indexes)
        '''

    def mapping(keys=False, values=False):  # @NoSelf
        '''
        Collect all items, keys, or` within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ of `mappings
        <http://docs.python.org/glossary.html#term-mapping>`_.

        :param keys: collect keys only (*default:* :const:`False`)

        :param values: collect values only (*default:* :const:`False`)
        '''

    def pattern(pattern, flags=0, compiler='parse'):  # @NoSelf
        '''
        Compile a search pattern to use as the active callable.

        :param pattern: search pattern

        :param flags: regular expression `flags
          <http://docs.python.org/library/re.html#re.DEBUG>`_ (*default:*
          ``0``)

        :param compiler: engine to compile pattern with. Valid options are
          ``'parse'``, ``'re'``, or ``'glob'`` (default: ``'parse'``)
        '''

    def traverse(ancestors=False, invert=False):  # @NoSelf
        '''
        Collect things from things or their ancestors within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ matched by the
        active callable.

        :param ancestors: collect things from parents of a thing based on
          `method resolution order (MRO)
          <http://docs.python.org/glossary.html#term-method-resolution-order>`_
          (default: :const:`False`)

        :param invert: return things active callable evaluates as
          :const:`False` rather than :const:`True` (*default:* :const:`False`)
        '''


class KReduce(AppspaceKey):

    '''reducing key'''

    def flatten():  # @NoSelf
        '''
        Flatten nested things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''

    def merge():  # @NoSelf
        '''
        Combine multiple `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_ into one
        iterable.
        '''

    def reduce(initial=None, reverse=False):  # @NoSelf
        '''
        Reduce an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ to one
        thing with active callable.

        :param initial: starting value (*default:*: :const:`None`)

        :param reverse: reduce from `the right side
          <http://www.zvon.org/other/haskell/Outputprelude/foldr_f.html>`_
          of an iterable (*default:* :const:`False`)
        '''

    def weave():  # @NoSelf
        '''
        Interleave every other thing from multiple `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_ to make one
        iterable.
        '''

    def zip():  # @NoSelf
        '''
        Reduce multiple `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_ to one iterable
        by pairing every two things in a :class:`tuple` of
        (*thing1*, *thing2*).
        '''


class KSlice(AppspaceKey):

    '''slicing key'''

    def at(n, default=None):  # @NoSelf
        '''
        `Slice <http://docs.python.org/glossary.html#term-slice>`_ off a thing
        found at `n` position within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ or `default` if
        nothing is found at `n`.

        :param n: index of some thing

        :param default: default thing (*default:*: :const:`None`)
        '''

    def choice():  # @NoSelf
        '''
        `Slice <http://docs.python.org/glossary.html#term-slice>`_ off a thing
        at random from an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''

    def dice(n, fill=None):
        '''
        `Slice <http://docs.python.org/glossary.html#term-slice>`_ an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ into multiple
        iterables of `n` things.

        :param n: number of things per split

        :param fill: value to pad out incomplete things (*default:*
          :const:`None`)
        '''

    def first(n=0):  # @NoSelf
        '''
        Slice off either `n` things from the starting end of an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ or the
        **first** thing within an iterable.

        :param n: number of things (*default:*: ``0``)
        '''

    def initial():  # @NoSelf
        '''
        `Slice <http://docs.python.org/glossary.html#term-slice>`_ off
        everything within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ except the very
        **last** thing.
        '''

    def last(n=0):  # @NoSelf
        '''
        `Slice <http://docs.python.org/glossary.html#term-slice>`_ off either
        `n` things from the tail end of an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ or just the
        **last** thing within an iterable.

        :param n: number of things (*default:*: ``0``)
        '''

    def rest():  # @NoSelf
        '''
        `Slice <http://docs.python.org/glossary.html#term-slice>`_ off
        everything within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ except the very
        **first** thing.
        '''

    def sample(n):  # @NoSelf
        '''
        `Slice <http://docs.python.org/glossary.html#term-slice>`_ off a
        random sample of `n` things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.

        :param n: sample size
        '''

    def slice(start, stop=False, step=False):  # @NoSelf
        '''
        `Slice <http://docs.python.org/glossary.html#term-slice>`_ off things
        within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ from `start` to
        (optionally) `stop` in `step` steps.

        :param start: starting index of slice

        :param stop: stopping index of slice (*default:* :const:`False`)

        :param step: size of step in slice (*default:* :const:`False`)
        '''


class KRepeat(AppspaceKey):

    '''repeat key'''

    def combinations(n):  # @NoSelf
        '''
        Find every possible combination of each `n` things within an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_.

        :param n: length of things to derive combinations from
        '''

    def copy():  # @NoSelf
        '''
        Duplicate each thing within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''

    def product(n=1):  # @NoSelf
        '''
        Repeat results of nested `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_ `n` times.

        :param n: number of nested loops to repeat (*default:* ``1``)
        '''

    def permutations(n):  # @NoSelf
        '''
        Find every possible permutation of each `n` things within an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_.

        :param n: length of things to derive permutations from
        '''

    def repeat(n=None, call=False):  # @NoSelf
        '''
        Repeat either an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ or the results
        of invoking the active callable `n` times.

        :param n: number of times to repeat (*default:* :const:`None`)

        :param call: repeat result of active callable (*default:*
          :const:`False`)
        '''


class KMap(AppspaceKey):

    '''mapping key'''

    def argmap(merge=False):  # @NoSelf
        '''
        Feed each thing within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ as wildcard
        `positional arguments
        <http://docs.python.org/glossary.html#term-positional-argument>`_ to
        the active callable.

        :param merge: combine global positional arguments with wildcard
          positional arguments from an iterable (*default:* :const:`False`)
        '''

    def invoke(name):  # @NoSelf
        '''
        Call method `name` from each thing within an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_ with
        the global `positional
        <http://docs.python.org/glossary.html#term-positional-argument>`_ and
        `keyword arguments
        <http://docs.python.org/glossary.html#term-keyword-argument>`_ but
        take the original thing if the return value of the method call is
        :const:`None`.

        :param name: method name
        '''

    def kwargmap(merge=False):  # @NoSelf
        '''
        Feed each thing within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ as a
        :class:`tuple` of wildcard `positional
        <http://docs.python.org/glossary.html#term-positional-argument>`_ and
        `keyword arguments
        <http://docs.python.org/glossary.html#term-keyword-argument>`_ to the
        active callable.

        :param merge: combine global positional and keyword arguments with
          positional and keyword arguments from an iterable into a single
          :class:`tuple` of wildcard positional and keyword arguments for the
          active callable (*default:* :const:`False`)
        '''

    def map():  # @NoSelf
        '''
        Feed each thing within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ to the active
        callable.
        '''


class KCompare(AppspaceKey):

    '''comparing key'''

    def all():  # @NoSelf
        '''
        :const:`True` if the active callable returns :const:`True` for
        **everything** within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ (or if
        the iterable is empty).
        '''

    def any():  # @NoSelf
        '''
        :const:`True` if the active callable returns :const:`True` for
        **anything** within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ (or if the
        iterable is empty).
        '''

    def difference(symmetric=False):  # @NoSelf
        '''
        Differences within a series of
        `iterables <http://docs.python.org/glossary.html#term-iterable>`_.

        :param symmetric: use symmetric difference (*default:* :const:`False`)
        '''

    def disjoint():  # @NoSelf
        '''
        Disjoints within a series of `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''

    def intersect():  # @NoSelf
        '''
        Intersections within a series of `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''

    def subset():  # @NoSelf
        '''
        :const:`True` if `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_ are subsets
        each other.
        '''

    def superset():  # @NoSelf
        '''
        :const:`True` if an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ is a superset of
        another iterable.
        '''

    def union():  # @NoSelf
        '''
        Union of things within a series of `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''

    def unique():  # @NoSelf
        '''
        Unique things within an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_.
        '''


class KNumber(AppspaceKey):

    '''number key'''

    def average():  # @NoSelf
        '''
        Take average of things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''

    def count():  # @NoSelf
        '''
        Count the number of times each thing occurs within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_. Returns a
        :class:`tuple` consisting of (*least common thing*, *most common
        thing*, *count of everything* consisting of a :class:`list` of
        :class:`tuple` pairs of (*thing*, *count*).
        '''

    def max():  # @NoSelf
        '''
        Take the maximum thing within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ using the
        active callable as the `key function
        <http://docs.python.org/glossary.html#term-key-function>`_.
        '''

    def median():  # @NoSelf
        '''
        Take the median thing within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''

    def min():  # @NoSelf
        '''
        Take the minimum thing within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ using the
        active callable as the `key function
        <http://docs.python.org/glossary.html#term-key-function>`_.
        '''

    def minmax():  # @NoSelf
        '''
        Take the minimum and maximum things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_
        as a :class:`tuple` consisting of (*minimum value*, *maximum value*).
        '''

    def range():  # @NoSelf
        '''
        Take the length of the smallest interval that can contain each thing
        within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''

    def sum(start=0, precision=False):  # @NoSelf
        '''
        Take the total from adding up `start` and each thing within an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_.

        :param start: starting number (*default:* ``0``)

        :param precision: add floats with extended precision (*default:*
          :const:`False`)
        '''


class KOrder(AppspaceKey):

    '''order mixin'''

    def group():  # @NoSelf
        '''
        Group things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ using
        the active callable as the `key function
        <http://docs.python.org/glossary.html#term-key-function>`_.
        '''

    def reverse():  # @NoSelf
        '''
        Reverse the current order of things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''

    def sort():  # @NoSelf
        '''
        Sort things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ using the
        active callable as the `key function
        <http://docs.python.org/glossary.html#term-key-function>`_.
        '''

    def shuffle():  # @NoSelf
        '''
        Randomly reorder things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''


class KSaw(KOutchain, KCompare, KFilter, KReduce, KMap, KNumber, KSlice,
    KOrder, KRepeat):

    '''combined key'''
