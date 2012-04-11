# -*- coding: utf-8 -*-
'''reference keys'''

from appspace.keys import AppspaceKey, Attribute


class KChainsaw(AppspaceKey):

    '''base chainsaw key'''

    ###########################################################################
    ## things in process ######################################################
    ###########################################################################

    def as_one():  # @NoSelf
        '''Switch to chainsawing incoming things as one individual thing.'''

    def as_many():  # @NoSelf
        '''
        Switch to chainsawing each incoming thing as one individual thing among
        many individual things.
        '''

    ###########################################################################
    ## things in context ######################################################
    ###########################################################################

    def as_edit():  # @NoSelf
        '''
        Switch to editing context where incoming things can be extracted and
        transformed in sequence of operations from their initial placement in
        the ins to their final extraction from the out.
        '''

    def as_truth():  # @NoSelf
        '''
        Switch to evaluation context where incoming things can be extracted and
        transformed so that the results of chainsawing them can be used to
        determine which of two potential paths should be executed. After
        they're evaluated, the ins state is automatically returned to a
        previously taken baseline snapshot of the incoming things so further
        opportunities to extract and transform them aren't lost.
        '''

    def as_view():  # @NoSelf
        '''
        Switch to query context where incoming things can be extracted and
        transformed so that the results of chainsawing them can be queried.
        After they're queried, the ins state is automatically returned to a
        previously taken baseline snapshot of the incoming things so further
        opportunities to extract and transform them aren't lost.
        '''

    ###########################################################################
    ## things in chain ########################################################
    ###########################################################################

    def as_auto():  # @NoSelf
        '''Context where ins is automatically rebalanced out.'''

    def as_manual():  # @NoSelf
        '''Context where ins must be manually rebalanced with out.'''

    def shift_in():  # @NoSelf
        '''Manually copy outgoing things to ins.'''

    def shift_out():  # @NoSelf
        '''Manually copy incoming things to out.'''

    balanced = Attribute('''Determine if ins and out are in balance''')

    ###########################################################################
    ## snapshot of things #####################################################
    ###########################################################################

    def snapshot(baseline=False, original=False):  # @NoSelf
        '''
        Take a snapshot of incoming things currently in ins.

        @param baseline: make snapshot baseline version (default: False)
        @param original: make snapshot original version (default: False)
        '''

    def undo(snapshot=0, baseline=False, original=False):  # @NoSelf
        '''
        Revert incoming things to a previous version within ins.

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
        Assign current callable and/or alternative callable.

        @param call: callable to assign
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
        Place many `things` after any incoming `things` already in current
        ins.

        @param things: wannabe incoming things
        '''

    def extendfront(things):  # @NoSelf
        '''
        Place many `things` before any incoming `things` already in current
        ins.

        @param thing: wannabe incoming things
        '''

    def append(thing):  # @NoSelf
        '''
        Place one `thing` after any incoming `things` already in current
        ins.

        @param thing: one wannabe incoming thing
        '''

    def appendfront(thing):  # @NoSelf
        '''
        Place one `thing` before any incoming `things` already in current
        ins.

        @param thing: one wannabe incoming thing
        '''

    ###########################################################################
    ## knowing things #########################################################
    ###########################################################################

    def __bool__():  # @NoSelf
        '''Return results build while in truth context or length of ins.'''

    ###########################################################################
    ## know things ############################################################
    ###########################################################################

    def __repr__():  # @NoSelf
        '''object representation'''

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
        choose current callable based on results of CONDITION mode

        @param call: external callable to use if condition is `True`
        @param alt: external callable  to use if condition if `False`
        '''

    def end():  # @NoSelf
        '''Return outgoing things and clear out everything.'''

    def results():  # @NoSelf
        '''Return outgoing things and clear out.'''

    def preview():  # @NoSelf
        '''Take a peek at the current state of outgoing things.'''

    ###########################################################################
    ## wrapping things ########################################################
    ###########################################################################

    def wrap(wrapper):  # @NoSelf
        '''
        wrapper for out

        @param wrapper: an iterator class
        '''

    ###########################################################################
    ## string wrapping things #################################################
    ###########################################################################

    def as_ascii(errors='strict'):  # @NoSelf
        '''
        encode each incoming thing as ascii string (regardless of type)

        @param errors: error handling (default: 'strict')
        '''

    def as_bytes(encoding='utf-8', errors='strict'):  # @NoSelf
        '''
        encode each incoming thing as byte string (regardless of type)

        @param encoding: encoding for things (default: 'utf-8')
        @param errors: error handling (default: 'strict')
        '''

    def as_unicode(encoding='utf-8', errors='strict'):  # @NoSelf
        '''
        decode each incoming thing as unicode string (regardless of type)

        @param encoding: encoding for things (default: 'utf-8')
        @param errors: error handling (default: 'strict')
        '''

    ###########################################################################
    ## sequence wrapping things ###############################################
    ###########################################################################

    def as_list():  # @NoSelf
        '''clear current wrapper'''

    def unwrap():  # @NoSelf
        '''clear current wrapper'''

    def as_deque():  # @NoSelf
        '''set wrapper to `deque`'''

    def as_tuple():  # @NoSelf
        '''set wrapper to `tuple`'''

    ###########################################################################
    ## map wrapping things ####################################################
    ###########################################################################

    def as_dict():  # @NoSelf
        '''set wrapper to `dict`'''

    def as_ordereddict():  # @NoSelf
        '''set wrapper to `OrderedDict`'''

    ###########################################################################
    ## stuf wrapping things ###################################################
    ###########################################################################

    def as_frozenstuf():  # @NoSelf
        '''set wrapper to `frozenstuf`'''

    def as_orderedstuf():  # @NoSelf
        '''set wrapper to `orderedstuf`'''

    def as_stuf():  # @NoSelf
        '''set wrapper to `stuf`'''

    ###########################################################################
    ## set wrapping things ####################################################
    ###########################################################################

    def as_frozenset():  # @NoSelf
        '''set wrapper to `frozenset`'''

    def as_set():  # @NoSelf
        '''set wrapper to `set`'''


class KReduce(AppspaceKey):

    '''reduce key'''

    def concat():  # @NoSelf
        '''concatenate incoming together'''

    def flatten():  # @NoSelf
        '''flatten nested incoming'''

    def join(sep='', encoding='utf-8', errors='strict'):  # @NoSelf
        '''
        join incoming into one unicode string (regardless of type)

        @param sep: join separator (default: '')
        @param encoding: encoding for things (default: 'utf-8')
        @param errors: error handling (default: 'strict')
        '''

    def reduce(initial=None, reverse=False):  # @NoSelf
        '''
        reduce incoming to one thing using current callable (from left
        side of incoming)

        @param initial: initial thing (default: None)
        @param reverse: reduce from right side of incoming things
        '''

    def weave():  # @NoSelf
        '''interleave incoming into one thing'''

    def zip():  # @NoSelf
        '''
        smash incoming into one single thing, pairing things by iterable
        position
        '''


class KSlice(AppspaceKey):

    '''slicing key'''

    def first(n=0):  # @NoSelf
        '''
        first `n` things of incoming or just the first thing

        @param n: number of things (default: 0)
        '''

    def initial():  # @NoSelf
        '''all incoming except the last thing'''

    def last(n=0):  # @NoSelf
        '''
        last `n` things of incoming or just the last thing

        @param n: number of things (default: 0)
        '''

    def nth(n, default=None):  # @NoSelf
        '''
        `nth` incoming thing in incoming or default thing

        @param n: number of things
        @param default: default thing (default: None)
        '''

    def rest():  # @NoSelf
        '''all incoming except the first thing'''

    def slice(start, stop=None, step=None):  # @NoSelf
        '''
        split incoming into sequences of length `n`, using `fill` thing
        to pad incomplete sequences

        @param n: number of things
        @param fill: fill thing (default: None)
        '''

    def split(n, fill=None):  # @NoSelf
        '''
        split incoming into sequences of length `n`, using `fill` thing
        to pad incomplete sequences

        @param n: number of things
        @param fill: fill thing (default: None)
        '''


class KRepeat(AppspaceKey):

    '''repeat key'''

    def combinations(n):  # @NoSelf
        '''
        repeat every combination for `n` of incoming

        @param n: number of repetitions
        '''

    def copy():  # @NoSelf
        '''copy each incoming thing'''

    def product(n=1):  # @NoSelf
        '''
        nested for each loops repeated `n` times

        @param n: number of repetitions (default: 1)
        '''

    def permutations(n):  # @NoSelf
        '''
        repeat every permutation for every `n` of incoming

        @param n: length of thing to permutate
        '''

    def repeat(n=None, call=False):  # @NoSelf
        '''
        repeat incoming `n` times by itself or with current callable

        @param n: repeat call n times on incoming (default: None)
        '''


class KMap(AppspaceKey):

    '''map key'''

    def invoke(name):  # @NoSelf
        '''
        invoke method `name` on each incoming thing with passed arguments,
        keywords but return incoming thing instead if method returns `None`

        @param name: name of method
        '''

    def map(args=False, kwargs=False):  # @NoSelf
        '''
        invoke call on each incoming thing

        @param args: map each incoming thing as python *args for call
        @param kwargs: map each incoming thing as python **kwargs for call
        '''


class KCollect(AppspaceKey):

    '''collecting key'''

    def attributes(*names):  # @NoSelf
        '''
        extract object attributes from incoming by their `*names`

        extract object members from incoming

        extract ancestors of things by method resolution order
        '''

    def extract(pattern, flags=0):  # @NoSelf
        '''
        extract patterns from incoming strings

        @param pattern: search pattern
        '''

    def mapping():  # @NoSelf
        '''
        invoke call on each mapping to get key, value pairs

        invoke call on each mapping to get keys
        invoke call on each mapping to get values
        '''

    def items(*keys):  # @NoSelf
        '''extract object items from incoming by item `*keys`'''


class KFilter(AppspaceKey):

    '''filtering mixin'''

    def filter(pattern=None, reverse=False, flags=0):  # @NoSelf
        '''
        incoming for which current callable returns `True`

        @param pattern: search pattern expression (default: None)
        @param reverse: reduce from right side (default: False)
        '''

    def find(pattern=None, reverse=False, flags=0):  # @NoSelf
        '''first incoming thing for which current callable returns `True`'''

    def replace(pattern, new, count=0, flags=0):  # @NoSelf
        '''
        replace incoming strings matching pattern with replacement string

        @param pattern: search pattern
        @param new: replacement string
        '''

    def difference(symmetric=False):  # @NoSelf
        '''
        difference between incoming

        @param symmetric: use symmetric difference
        '''

    def disjointed():  # @NoSelf
        '''disjoint between incoming'''

    def intersection():  # @NoSelf
        '''intersection between incoming'''

    def partition(pattern=None, flags=0):  # @NoSelf
        '''
        split incoming into `True` and `False` things based on results
        of call
        '''

    def subset():  # @NoSelf
        '''incoming that are subsets of incoming'''

    def superset():  # @NoSelf
        '''incoming that are supersets of incoming'''

    def union():  # @NoSelf
        '''union between incoming'''

    def unique():  # @NoSelf
        '''
        list unique incoming, preserving order and remember all incoming things
        ever seen
        '''


class KMath(AppspaceKey):

    '''math key'''

    def average():  # @NoSelf
        '''average value of incoming'''

    def max():  # @NoSelf
        '''
        find maximum value among incoming using current callable as key
        function
        '''

    def median():  # @NoSelf
        '''median value of incoming'''

    def min():  # @NoSelf
        '''
        find minimum value among incoming using current callable as key
        function
        '''

    def minmax():  # @NoSelf
        '''minimum and maximum values among incoming'''

    def range():  # @NoSelf
        '''statistical range of incoming'''

    def sum(start=0, floats=False):  # @NoSelf
        '''
        total incoming together

        @param start: starting number (default: 0)
        @param floats: incoming are floats (default: False)
        '''


class KTruth():

    '''truth mixin'''

    def all():  # @NoSelf
        '''if `all` incoming are `True`'''

    def any():  # @NoSelf
        '''if `any` incoming are `True`'''

    def frequency():  # @NoSelf
        '''frequency of each incoming thing'''

    def quantify():  # @NoSelf
        '''
        how many times current callable returns `True` for incoming
        '''


class KOrder(AppspaceKey):

    '''order mixin'''

    def choice():  # @NoSelf
        '''random choice of/from incoming'''

    def groupby():  # @NoSelf
        '''
        Group things together, using the current callable as the key function.
        '''

    def reverse():  # @NoSelf
        '''reverse order of incoming'''

    def sort():  # @NoSelf
        '''
        sort incoming, optionally using current call as key function
        '''

    def sample(n):  # @NoSelf
        '''
        random sampling drawn from `n` incoming things

        @param n: number of incoming
        '''

    def shuffle():  # @NoSelf
        '''randomly order incoming'''
