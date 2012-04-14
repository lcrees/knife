# -*- coding: utf-8 -*-
'''reference keys'''

from appspace.keys import AppspaceKey, Attribute


class KChainsaw(AppspaceKey):

    '''base chainsaw key'''

    def __init__(*things, **kw):  # @NoSelf
        '''
        init

        :params `*things`: incoming things
        '''

    ###########################################################################
    ## things in process ######################################################
    ###########################################################################

    def as_many():  # @NoSelf
        '''
        Switch to performing operations on each incoming thing as just one
        individual thing.
        '''

    def as_one():  # @NoSelf
        '''
        Switch to performing operations on all incoming things at once.
        '''

    ###########################################################################
    ## things in context ######################################################
    ###########################################################################

    def as_edit():  # @NoSelf
        '''
        Switch to editing context where operations can be performed on incoming
        things from initial placement to final extraction.
        '''

    def as_query():  # @NoSelf
        '''
        Switch to context where, upon exiting it by invoking ``results``
        or ``end`` method, incoming things automatically revert to the baseline
        snapshot so the unmodified baseline version of incoming things can be
        worked with.
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
        Take a snapshot of the current incoming things.

        :param baseline: make this snapshot the baseline snapshot (*default:*
          :const:`False`)
        :param original: make this snapshot the original snapshot (*default:*
          :const:`False`)
        '''

    def undo(snapshot=0, baseline=False, original=False):  # @NoSelf
        '''
        Revert incoming things to a previous snapshot.

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
        Assign positional or keyword arguments used anytime the worker
        is invoked.
        '''

    def tap(call):  # @NoSelf
        '''
        Assign worker.

        :param call: a callable
        '''

    def untap():  # @NoSelf
        '''
        Clear any active callable and global positional or keyword arguments.
        '''

    def pattern(pattern, flags=0, compiler='parse'):  # @NoSelf
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

        :param thing: incoming thing
        '''

    def appendstart(thing):  # @NoSelf
        '''
        Insert `thing` **before** any other incoming things.

        :param thing: incoming thing
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
        End the current chainsaw session and return outgoing things, wrapped
        with the `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ wrapper.
        '''

    def results():  # @NoSelf
        '''
        Clear and return outgoing things wrapped with the `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ wrapper.
        '''

    def preview():  # @NoSelf
        '''
        Take a peek at the current state of outgoing things.
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
        '''
        Reset current `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ wrapper to
        default.
        '''

    ###########################################################################
    ## wrapping things up #####################################################
    ###########################################################################

    def as_ascii(errors='strict'):  # @NoSelf
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to :class:`byte` encode each outgoing thing with the
        ``'ascii'`` codec.

        :param errors: error handling for decoding issues (*default*:
          ``'strict'``)
        '''

    def as_bytes(encoding='utf-8', errors='strict'):  # @NoSelf
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to :class:`byte` encode each outgoing thing.

        :param encoding: Unicode encoding (*default:* ``'utf-8'``)

        :param errors: error handling for encoding issues (*default:*
          ``'strict'``)
        '''

    def as_dict():  # @NoSelf
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to cast each outgoing thing as a :class:`dict`.
        '''

    def as_list():  # @NoSelf
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to cast each incoming thing as a :class:`list`.
        '''

    def as_set():  # @NoSelf
        '''
        Set `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ wrapper to cast
        each outgoing thing as a :class:`set`.
        '''

    def as_tuple():  # @NoSelf
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to cast each outgoing thing to a :class:`tuple`.
        '''

    def as_unicode(encoding='utf-8', errors='strict'):  # @NoSelf
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to :class:`unicode` (:class:`str` under Python 3) decode
        each outgoing thing.

        :param encoding: Unicode encoding (*default:* ``'utf-8'``)

        :param errors: error handling for decoding issues (*default:*
          ``'strict'``)
        '''


class KFilter(AppspaceKey):

    '''filtering key'''

    def attributes(*names):  # @NoSelf
        '''
        Collect `attribute
        <http://docs.python.org/glossary.html#term-attribute>`_ values from
        things within an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_ that
        matches an attribute name value in `names`.

        :param names: attribute names
        '''

    def duality():  # @NoSelf
        '''
        Divide one `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ into two
        iterables, the first being everything the worker evaluates as
        :const:`True` and the second being everything the worker evaluates as
        :const:`False`.
        '''

    def filter(invert=False):  # @NoSelf
        '''
        Collect each thing within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ matched by the
        worker.

        :param invert: return things the worker evaluates as :const:`False`
          instead of :const:`True` (*default:* :const:`False`)
        '''

    def items(*keys):  # @NoSelf
        '''
        Collect values from things (usually `sequences
        <http://docs.python.org/glossary.html#term-sequence>`_ or `mappings
        <http://docs.python.org/glossary.html#term-mapping>`_) within an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        that match a key value in `keys`.

        :param keys: item keys (or indexes)
        '''

    def mapping(keys=False, values=False):  # @NoSelf
        '''
        Collect items, keys, or values from things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ of `mappings
        <http://docs.python.org/glossary.html#term-mapping>`_.

        :param keys: collect keys only (*default:* :const:`False`)

        :param values: collect values only (*default:* :const:`False`)
        '''

    def traverse(ancestors=False, invert=False):  # @NoSelf
        '''
        Collect nested values from each thing within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ the worker
        matches.

        :param ancestors: collect things from parents of a thing based on
          `method resolution order (MRO)
          <http://docs.python.org/glossary.html#term-method-resolution-order>`
          (default: :const:`False`)

        :param invert: return things worker evaluates as
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
        <http://docs.python.org/glossary.html#term-iterable>`_ down to one
        thing using the worker.

        :param initial: starting value (*default:*: :const:`None`)

        :param reverse: reduce from `the right side
          <http://www.zvon.org/other/haskell/Outputprelude/foldr_f.html>`_
          of an iterable (*default:* :const:`False`)
        '''

    def weave():  # @NoSelf
        '''
        Interleave every sequence of corresponding thing from multiple
        `iterables <http://docs.python.org/glossary.html#term-iterable>`_ into
        one iterable.
        '''

    def zip():  # @NoSelf
        '''
        Reduce multiple `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_ to one iterable
        by pairing every two things in a :class:`tuple` of (*thing1*,
        *thing2*).
        '''


class KSlice(AppspaceKey):

    '''slicing key'''

    def at(n):  # @NoSelf
        '''
        `Slice <http://docs.python.org/glossary.html#term-slice>`_ off one
        thing found at `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ index `n` .

        :param n: index of some thing

        :param default: default thing collected if nothing is found at `n`
          (*default:*: :const:`None`)
        '''

    def choice():  # @NoSelf
        '''
        `Randomly slice <http://docs.python.org/glossary.html#term-slice>`_ off
        one thing from an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''

    def dice(n, fill=None):  # @NoSelf
        '''
        `Slice <http://docs.python.org/glossary.html#term-slice>`_ one
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_ into
        multiple iterables of size `n` things.

        :param n: number of things per split

        :param fill: value to pad out incomplete things (*default:*
          :const:`None`)
        '''

    def first(n=0):  # @NoSelf
        '''
        Slice off `n` things from the starting end of an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ or just the very
        **first** thing.

        :param n: number of things (*default:*: ``0``)
        '''

    def initial():  # @NoSelf
        '''
        `Slice <http://docs.python.org/glossary.html#term-slice>`_ off
        everything from an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ except the very
        **last** thing.
        '''

    def last(n=0):  # @NoSelf
        '''
        `Slice <http://docs.python.org/glossary.html#term-slice>`_ off either
        `n` things from the tail end of an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ or just the very
        **last** thing.

        :param n: number of things (*default:*: ``0``)
        '''

    def rest():  # @NoSelf
        '''
        `Slice <http://docs.python.org/glossary.html#term-slice>`_ off
        everything from an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ except the very
        **first** thing.
        '''

    def sample(n):  # @NoSelf
        '''
        Randomly `slice <http://docs.python.org/glossary.html#term-slice>`_ off
        `n` things from an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.

        :param n: size of sample
        '''

    def slice(start, stop=False, step=False):  # @NoSelf
        '''
        `Slice <http://docs.python.org/glossary.html#term-slice>`_ off things
        from `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.

        :param start: starting index of slice

        :param stop: stopping index of slice (*default:* :const:`False`)

        :param step: size of step in slice (*default:* :const:`False`)
        '''


class KRepeat(AppspaceKey):

    '''repeating key'''

    def combinations(n):  # @NoSelf
        '''
        Find combinations of every `n` things withing an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.

        :param n: length of things to derive combinations from
        '''

    def copy():  # @NoSelf
        '''
        Duplicate each thing within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''

    def permutations(n):  # @NoSelf
        '''
        Find permutations of every `n` things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.

        :param n: length of things to derive permutations from
        '''

    def repeat(n=None, call=False):  # @NoSelf
        '''
        Repeat either an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ or invoke
        worker `n` times.

        :param n: number of times to repeat (*default:* :const:`None`)

        :param call: repeat results of invoking worker (*default:*
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
        the worker.

        :param merge: merge global positional arguments with wildcard
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
        worker.

        :param merge: merge global positional or keyword arguments with
          positional and keyword arguments within an iterable into a single
          :class:`tuple` of wildcard positional and keyword arguments (
          *default:* :const:`False`)
        '''

    def map():  # @NoSelf
        '''
        Feed each thing within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ to the worker.
        '''


class KCompare(AppspaceKey):

    '''comparing key'''

    def all():  # @NoSelf
        '''
        Discover if the worker returns :const:`True` for **everything** within
        an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ (or if
        the iterable is empty).
        '''

    def any():  # @NoSelf
        '''
        Discover if the worker returns :const:`True` for **anything** within an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_ (or if
        the iterable is empty).
        '''

    def difference(symmetric=False):  # @NoSelf
        '''
        Find differences within a series of
        `iterables <http://docs.python.org/glossary.html#term-iterable>`_.

        :param symmetric: use symmetric difference (*default:* :const:`False`)
        '''

    def disjoint():  # @NoSelf
        '''
        Find disjoints within a series of `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''

    def intersect():  # @NoSelf
        '''
        Find intersections within a series of `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''

    def subset():  # @NoSelf
        '''
        Find out if `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_ are subsets
        other iterables.
        '''

    def superset():  # @NoSelf
        '''
        Find out if `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_ are supersets of
        others iterables.
        '''

    def union():  # @NoSelf
        '''
        Find unions within a series of `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''

    def unique():  # @NoSelf
        '''
        Find unique things within an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_.
        '''


class KMath(AppspaceKey):

    '''mathing key'''

    def average():  # @NoSelf
        '''
        Find the average value within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''

    def count():  # @NoSelf
        '''
        Count how many times each thing occurs within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_. Result is a
        :class:`tuple` consisting of (*least common thing*, *most common
        thing*, *count of everything* consisting of a :class:`list` of
        :class:`tuple` pairs of (*thing*, *count*).
        '''

    def max():  # @NoSelf
        '''
        Find the maximum value within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ using the
        worker as the `key function
        <http://docs.python.org/glossary.html#term-key-function>`_.
        '''

    def median():  # @NoSelf
        '''
        Find the median value within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''

    def min():  # @NoSelf
        '''
        Find the minimum value within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ using the
        worker as the `key function
        <http://docs.python.org/glossary.html#term-key-function>`_.
        '''

    def minmax():  # @NoSelf
        '''
        Find the minimum and maximum values within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_. Result is a
        :class:`tuple` of (*minimum value*, *maximum value*).
        '''

    def range():  # @NoSelf
        '''
        Find the length of the smallest interval that can contain everything
        within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''

    def sum(start=0, precision=False):  # @NoSelf
        '''
        Total up by adding `start` and everything within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ together.

        :param start: starting number (*default:* ``0``)

        :param precision: add floats with extended precision (*default:*
          :const:`False`)
        '''


class KOrder(AppspaceKey):

    '''ordering mixin'''

    def group():  # @NoSelf
        '''
        Group things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ using the
        worker as the `key function
        <http://docs.python.org/glossary.html#term-key-function>`_.
        '''

    def reverse():  # @NoSelf
        '''
        Reverse the order of things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''

    def sort():  # @NoSelf
        '''
        Sort things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ using the
        worker as the `key function
        <http://docs.python.org/glossary.html#term-key-function>`_.
        '''

    def shuffle():  # @NoSelf
        '''
        Randomly reorder things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''


class KSaw(KOutchain, KCompare, KFilter, KReduce, KMap, KMath, KSlice,
    KOrder, KRepeat):

    '''combined key'''
