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
        Switch to performing operations on incoming things as one whole
        individual thing.
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
        After exting the evaluation context, incoming things automatically
        revert to a prior baseline snapshot of incoming things so further
        operations can be performed on the unmodified version.
        '''

    def as_view():  # @NoSelf
        '''
        Switch to query context where incoming things can be extracted and
        transformed so that the results of chainsawing them can be queried.
        Upon exit from query context by invoking `results` or `end`, all
        incoming things automatically revert to a prior baseline snapshot of
        incoming things so that further operations can be performed on the
        unmodified version.
        '''

    ###########################################################################
    ## things in chain ########################################################
    ###########################################################################

    def as_auto():  # @NoSelf
        '''
        Context where incoming things are automatically rebalanced with
        outgoing things.
        '''

    def as_manual():  # @NoSelf
        '''
        Context where incoming must be manually rebalanced with outgoing
        things.
        '''

    def shift_in():  # @NoSelf
        '''Manually copy outgoing things to incoming things.'''

    def shift_out():  # @NoSelf
        '''Manually copy incoming things to outgoing things.'''

    balanced = Attribute(
        'Determine if incoming and outgoing things are in balance'
    )

    ###########################################################################
    ## snapshot of things #####################################################
    ###########################################################################

    def snapshot(baseline=False, original=False):  # @NoSelf
        '''
        Take a snapshot of current incoming things.

        @param baseline: make snapshot baseline version (default: False)
        @param original: make snapshot original version (default: False)
        '''

    def undo(snapshot=0, baseline=False, original=False):  # @NoSelf
        '''
        Revert incoming things to a previous snapshot of incoming things.

        @param snapshot: steps ago 1, 2, 3 steps, etc.. (default: 0)
        @param baseline: return ins to baseline version (default: False)
        @param original: return ins to original version (default: False)
        '''

    ###########################################################################
    ## things called ##########################################################
    ###########################################################################

    def arguments(*args, **kw):  # @NoSelf
        '''
        Assign arguments to be used by the current or alternative callable.
        '''

    def tap(call, alt=None, factory=False):  # @NoSelf
        '''
        Assign current callable and, optionally, an alternative callable. If
        `factory` flag is set, use the `call` argument as a factory for
        building the current callable.

        @param call: primary callable to assign
        @param alt: alternative callable to assign (default: None)
        @param factor: whether `call` is a callable factory (default: False)
        '''

    def untap():  # @NoSelf
        '''
        Clear current callable, alternative callable, and stored arguments.
        '''

    ###########################################################################
    ## things coming in #######################################################
    ###########################################################################

    def extend(things):  # @NoSelf
        '''
        Place `things` after any current incoming things.

        @param things: wannabe incoming things
        '''

    def append(thing):  # @NoSelf
        '''
        Place `things` after any current incoming thing.

        @param thing: one wannabe incoming thing
        '''

    def extendfront(things):  # @NoSelf
        '''
        Place `things` before any current incoming things.

        @param thing: wannabe incoming things
        '''

    def appendfront(thing):  # @NoSelf
        '''
        Place `thing` before any current incoming things.

        @param thing: one wannabe incoming thing
        '''

    ###########################################################################
    ## knowing things #########################################################
    ###########################################################################

    def __bool__():  # @NoSelf
        '''
        Return results built up while in truth context or return the length of
        incoming things.
        '''

    ###########################################################################
    ## know things ############################################################
    ###########################################################################

    def __repr__():  # @NoSelf
        '''Object representation.'''

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

    '''knifing output mixin'''

    def __iter__():  # @NoSelf
        '''Yield outgoing things.'''

    def which(call=None, alt=None):  # @NoSelf
        '''
        Choose current callable based on results of condition mode

        @param call: external callable to use if condition is `True`
        @param alt: external callable to use if condition if `False`
        '''

    def end():  # @NoSelf
        '''Return outgoing things and clear out every last thing.'''

    def results():  # @NoSelf
        '''Return outgoing things and clear outgoing things.'''

    def preview():  # @NoSelf
        '''Take a peek at the current state of outgoing things.'''

    ###########################################################################
    ## wrapping things ########################################################
    ###########################################################################

    def wrap(wrapper):  # @NoSelf
        '''
        Iterable wrapper for outgoing things.

        @param wrapper: an iterable wrapper
        '''

    def unwrap():  # @NoSelf
        '''Reset current wrapper to default.'''

    ###########################################################################
    ## string wrapping things #################################################
    ###########################################################################

    def as_ascii(errors='strict'):  # @NoSelf
        '''
        Set wrapper to encode each thing in a series of things as string/byte
        type encoded as `ascii` (regardless of type)

        @param errors: error handling for encoding stringish things
            (default: 'strict')
        '''

    def as_bytes(encoding='utf-8', errors='strict'):  # @NoSelf
        '''
        Set wrapper to encode each thing in a series of things as `byte` type
        (regardless of type).

        @param encoding: encoding for stringish things (default: 'utf-8')
        @param errors: error handling for encoding stringish things
            (default: 'strict')
        '''

    def as_unicode(encoding='utf-8', errors='strict'):  # @NoSelf
        '''
        Set wrapper to decode each thing in a series of things as `unicode`
        type (regardless of type).

        @param encoding: encoding for stringish things (default: 'utf-8')
        @param errors: error handling for decoding stringish things
            (default: 'strict')
        '''

    ###########################################################################
    ## sequence wrapping things ###############################################
    ###########################################################################

    def as_list():  # @NoSelf
        '''Set wrapper to `list` type.'''

    def as_deque():  # @NoSelf
        '''Set wrapper to `deque` type.'''

    def as_tuple():  # @NoSelf
        '''Set wrapper to `tuple` type.'''

    ###########################################################################
    ## map wrapping things ####################################################
    ###########################################################################

    def as_dict():  # @NoSelf
        '''Set wrapper to `dict` type.'''

    def as_ordereddict():  # @NoSelf
        '''Set wrapper to `OrderedDict` type.'''

    ###########################################################################
    ## stuf wrapping things ###################################################
    ###########################################################################

    def as_frozenstuf():  # @NoSelf
        '''Set wrapper to `frozenstuf` type.'''

    def as_orderedstuf():  # @NoSelf
        '''Set iterable wrapper to `orderedstuf` type.'''

    def as_stuf():  # @NoSelf
        '''Set iterable wrapper to `stuf` type.'''

    ###########################################################################
    ## set wrapping things ####################################################
    ###########################################################################

    def as_frozenset():  # @NoSelf
        '''Set iterable wrapper to `frozenset` type.'''

    def as_set():  # @NoSelf
        '''Set iterable wrapper to `set` type.'''


class KReduce(AppspaceKey):

    '''reduce key'''

    def concat():  # @NoSelf
        '''Concatenate a series of things into one series of things.'''

    def flatten():  # @NoSelf
        '''Flatten a series of nested things into a flat series of things.'''

    def join(separator='', encoding='utf-8', errors='strict'):  # @NoSelf
        '''
        Combine a series of stringish things join into one unicode string
        (regardless of the original string type).

        @param separator: string to join at (default: '')
        @param encoding: encoding for stringish things (default: 'utf-8')
        @param errors: error handling when encoding stringish things
            (default: 'strict')
        '''

    def reduce(initial=None, reverse=False):  # @NoSelf
        '''
        Reduce a series of things down to one thing using the current callable.
        If `reverse` flag is set, reduction will come from the right side of
        the series. Otherwise, reduction will come from the left side of the
        series.

        @param initial: initial thing (default: `None`)
        @param reverse: reduce from right side of things (default: `False`)
        '''

    def weave():  # @NoSelf
        '''Interleave a series of things into one thing.'''

    def zip():  # @NoSelf
        '''
        Reduce of a series of things down to one thing, pairing each things by
        their position in the series.
        '''


class KSlice(AppspaceKey):

    '''slicing key'''

    def first(n=0):  # @NoSelf
        '''
        Return either the specified number of things from the beginning of a
        series of things or just the first thing.

        @param n: number of things (default: 0)
        '''

    def initial():  # @NoSelf
        '''
        Return everything within a series of things except the very last thing
        within the series of things.
        '''

    def last(n=0):  # @NoSelf
        '''
        Return either the specified number of things from the end of a series
        of things or just the last thing.

        @param n: number of things (default: 0)
        '''

    def index(n, default=None):  # @NoSelf
        '''
        Return each thing at a specified index in a series of incoming things
        or the passed default thing.

        @param n: index of thing
        @param default: default thing (default: `None`)
        '''

    def rest():  # @NoSelf
        '''
        Return everything within a series of things except the very first thing
        within the series of things.
        '''

    def slice(start, stop=None, step=None):  # @NoSelf
        '''
        Slice a series of things down to a certain size.

        @param start: starting point of slice
        @param stop: stopping point of slice (default: `None`)
        @param step: size of step in slice (default: `None`)
        '''

    def split(n, fill=None):  # @NoSelf
        '''
        Split a series of things into series of things of a specified length
        using `fill` argument to pad out incomplete series.

        @param n: number of things per split
        @param fill: value to pad out incomplete things (default: `None`)
        '''


class KRepeat(AppspaceKey):

    '''repeat key'''

    def combinations(n):  # @NoSelf
        '''
        Each possible combinations for every number of things within a series
        of things.

        @param n: number of things to derive combinations from
        '''

    def copy():  # @NoSelf
        '''Duplicate each thing in a series of things'''

    def product(n=1):  # @NoSelf
        '''
        Results of nested for each loops repeated a certain number of times.

        @param n: number of loops to repeat (default: 1)
        '''

    def permutations(n):  # @NoSelf
        '''
        Each possible permutation for every number of things within a series of
        things.

        @param n: number of things to derive permutations from
        '''

    def repeat(n=None, call=False):  # @NoSelf
        '''
        Repeat a series of things or the results of the current callable.

        @param n: number of times to repeat (default: `None`)
        @param call: repeat result of current callable (default: `False`)
        '''


class KMap(AppspaceKey):

    '''map key'''

    def invoke(name):  # @NoSelf
        '''
        Invoke method `name` on each thing within a series of things with the
        current positio nnd keyword arguments but return the thing as the
        result if the method returns `None`.

        @param name: method name
        '''

    def map(args=False, kwargs=False, current=False):  # @NoSelf
        '''
        Invoke current callable on each thing within a series of things. Pass
        results of iterable as *args to current callable if `args` flag is set.
        Pass results of iterable to current callable as tuple of *args and
        **kwargs if `kwargs` flag is set.

        @param args: map each thing as a tuple of Python *args for current
            callable (default: `False`)
        @param kwargs: map each thing as a tuple of Python *args and
            **kwargs for current callable (default: `False`)
        @param current: map each thing as a tuple of Python *args and **kwargs
            including current positional and keyword arguments for current
            callable (default: `False`)
        '''


class KCollect(AppspaceKey):

    '''collecting key'''

    def attributes(deep=False, ancestors=False, *names):  # @NoSelf
        '''
        Collect attributes from a series of objects by their attribute names.

        @param deep: traverse deep inside an object (default: `False`)
        @param ancestors: traverse deep inside classes within method resolution
            order (default: `False`)
        @param *keys: item keys
        '''

    def mapping(keys=False, values=False):  # @NoSelf
        '''
        Collect keys and values from a series of mappings.

        @param keys: gather keys only (default: `False`)
        @param values: gather values only (default: `False`)
        '''

    def items(*keys):  # @NoSelf
        '''
        Collect object items from a series of things matching their keys.

        @param *keys: item keys
        '''


class KFilter(AppspaceKey):

    '''filtering mixin'''

    def filter(pattern=None, reverse=False, flags=0):  # @NoSelf
        '''
        Things within a series of things that pass a filter. By default things
        that evaluate to `True` pass the filter but if the `reverse` flag is
        set to `True` than things that evaluate to `False` pass the filter
        while things that evaluate to False do not. If a `pattern` is supplied
        the filter will be a regular expression. Otherwise the current callable
        will be used.

        @param pattern: regular expression search pattern (default: `None`)
        @param reverse: return things for which filter is `False` rather than
            `True` (default: `False`)
        @param flags: regular expression flags (default: 0)
        '''

    def find(pattern=None, reverse=False, flags=0):  # @NoSelf
        '''
        The first in a series of things that pass a filter. By default things
        that evaluate to `True` pass the filter but if the `reverse` flag is
        set to `True` than things that evaluate to `False` pass the filter
        while things that evaluate to False do not. If a `pattern` is supplied
        the filter will be a regular expression. Otherwise the current callable
        will be used.

        @param pattern: regular expression search pattern (default: `None`)
        @param reverse: return things for which filter is `False` rather than
            `True` (default: `False`)
        @param flags: regular expression flags (default: 0)
        '''

    def replace(pattern, new, count=0, flags=0):  # @NoSelf
        '''
        Replace segments within a series of strings with a new string segment
        if they match a pattern.

        @param pattern: regular expression search pattern
        @param new: replacement string
        @param count: number of replacements to make in a string (default: 0)
        @param flags: regular expression flags (default: 0)
        '''

    def difference(symmetric=False):  # @NoSelf
        '''
        The difference between a series of things.

        @param symmetric: use symmetric difference (default: `False`)
        '''

    def disjointed():  # @NoSelf
        '''The disjoint between a series of things.'''

    def intersection():  # @NoSelf
        '''The intersection between a series of things.'''

    def partition(pattern=None, flags=0):  # @NoSelf
        '''
        Divide a series of things into `True` and `False` things based on the
        results returned by the current callable.

        @param pattern: regular expression search pattern (default: `None`)
        @param flags: regular expression flags (default: 0)
        '''

    def subset():  # @NoSelf
        '''
        Tell if a series of things is a subset of other series of things.
        '''

    def superset():  # @NoSelf
        '''
        Tell if a series of things is a superset of another series of things.
        '''

    def union():  # @NoSelf
        '''The union between two series of things.'''

    def unique():  # @NoSelf
        '''
        Get unique things within a series of things while preserving order and
        remember everything ever encountered.
        '''


class KMath(AppspaceKey):

    '''math key'''

    def average():  # @NoSelf
        '''Average value within a series of things.'''

    def max():  # @NoSelf
        '''
        Maximum value within a series of things using current callable as the
        key function.
        '''

    def median():  # @NoSelf
        '''Median value within a series of things.'''

    def min():  # @NoSelf
        '''
        Minimum value within a series of things using the current callable as
        the key function.
        '''

    def minmax():  # @NoSelf
        '''Minimum and maximum values within a series of things.'''

    def range():  # @NoSelf
        '''Statistical range within a series of things.'''

    def sum(start=0, floats=False):  # @NoSelf
        '''
        Add the value of a series of things together.

        @param start: starting number (default: 0)
        @param floats: incoming are floats (default: False)
        '''


class KTruth():

    '''truth mixin'''

    def all():  # @NoSelf
        '''Tell if everthing in a series of things is `True`.'''

    def any():  # @NoSelf
        '''Tell if anything in a series of things is `True`'''

    def frequency():  # @NoSelf
        '''Count of each thing in a series of things.'''

    def quantify():  # @NoSelf
        '''
        Number of how many times current callable evaluates to `True` in a
        series of things.
        '''


class KOrder(AppspaceKey):

    '''order mixin'''

    def choice():  # @NoSelf
        '''Select a random choice from a series of things.'''

    def groupby():  # @NoSelf
        '''
        Group things together using the current callable as the key function.
        '''

    def reverse():  # @NoSelf
        '''Reverse the order of a series of things.'''

    def sort():  # @NoSelf
        '''
        Sort a series of things using the current callable as the key function.
        '''

    def sample(n):  # @NoSelf
        '''
        Take a random sample drawn from a series of things.

        @param n: sample size
        '''

    def shuffle():  # @NoSelf
        '''Randomly reorder a series of things.'''
