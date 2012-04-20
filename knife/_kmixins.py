# -*- coding: utf-8 -*-
'''knife mixin keys'''

from appspace.keys import AppspaceKey


class KCompare(AppspaceKey):

    '''
    comparing knife key
    '''

    def all():  # @NoSelf
        '''
        Discover if :meth:`worker` returns :const:`True` for **every**
        incoming thing.

        >>> from knife import __
        >>> __(2, 4, 6, 8).worker(lambda x: x % 2 == 0).all().fetch()
        True
        '''

    def any():  # @NoSelf
        '''
        Discover if :meth:`worker` returns :const:`True` for **any** incoming
        thing.

        >>> __(1, 4, 5, 9).worker(lambda x: x % 2 == 0).any().fetch()
        True
        '''

    def difference(symmetric=False):  # @NoSelf
        '''
        Discover difference within a series of `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ incoming
        things.

        :keyword boolean symmetric: use symmetric difference

        >>> # default behavior
        >>> test = __([1, 2, 3, 4, 5], [5, 2, 10], [10, 11, 2])
        >>> test.difference().fetch()
        [1, 3, 4]
        >>> # symmetric difference
        >>> test.original().difference(symmetric=True).fetch()
        [1, 3, 4, 11]
        '''

    def intersect():  # @NoSelf
        '''
        Discover intersection within a series of `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ incoming
        things.

        >>> __([1, 2, 3], [101, 2, 1, 10], [2, 1]).intersection().fetch()
        [1, 2]
        '''

    def union():  # @NoSelf
        '''
        Discover union within a series of `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ incoming things.

        >>> __([1, 2, 3], [101, 2, 1, 10], [2, 1]).union().fetch()
        [1, 10, 3, 2, 101]
        '''

    def unique():  # @NoSelf
        '''
        Discover unique incoming things.

          >>> # default behavior
          >>> __(1, 2, 1, 3, 1, 4).unique().fetch()
          [1, 2, 3, 4]
          >>> # using worker as key function
          >>> __(1, 2, 1, 3, 1, 4).worker(round).unique().fetch()
          [1, 2, 3, 4]
        '''


class KMath(AppspaceKey):

    '''mathing knife key'''

    def average():  # @NoSelf
        '''
        Discover average incoming thing.

          >>> from knife import __
          >>> __(10, 40, 45).average().fetch()
          31.666666666666668
        '''

    def count():  # @NoSelf
        '''
        Discover how many times each incoming thing occurs.

        :returns: :class:`tuple` of (*least common thing*, *most common thing*,
          [*counts of everything* (a :class:`list` of :class:`tuple` pairs of
          (*thing*, *count*))]).

          >>> common = __(11, 3, 5, 11, 7, 3, 5, 11).count().fetch()
          >>> # least common thing
          >>> common.least_common
          7
          >>> # most common thing
          >>> common.most_common
          11
          >>> # total count for every thing
          >>> common.totals
          [(11, 3), (3, 2), (5, 2), (7, 1)]
        '''

    def max():  # @NoSelf
        '''
        Discover maximum incoming thing using :meth:`worker` as the `key
        function <http://docs.python.org/glossary.html#term-key-function>`_.

          >>> # default behavior
          >>> __(1, 2, 4).max().fetch()
          4
          >>> stooges = (
          ...    {'name': 'moe', 'age': 40},
          ...    {'name': 'larry', 'age': 50},
          ...    {'name': 'curly', 'age': 60},
          ... )
          >>> # using worker as key function
          >>> __(*stooges).worker(lambda x: x['age']).max().fetch()
          {'age': 60, 'name': 'curly'}
        '''

    def median():  # @NoSelf
        '''
        Discover median incoming thing.

        >>> __(4, 5, 7, 2, 1).median().fetch()
        4
        >>> __(4, 5, 7, 2, 1, 8).median().fetch()
        4.5
        '''

    def min():  # @NoSelf
        '''
        Discover minimum incoming thing using :meth:`worker` as the `key
        function <http://docs.python.org/glossary.html#term-key-function>`_.

        >>> test = __(10, 5, 100, 2, 1000)
        >>> test.min().fetch()
        2
        >>> test.original().worker(lambda x: x % 100 == 0).min().fetch()
        10
        '''

    def minmax():  # @NoSelf
        '''
        Discover minimum and maximum incoming things.

        :returns: :class:`namedtuple` (*minimum value*, *maximum value*).

          >>> minmax = __(1, 2, 4).minmax().fetch()
          >>> minmax.minimum
          1
          >>> minmax.maximum
          4
        '''

    def range():  # @NoSelf
        '''
        Discover length of the smallest interval that can contain every
        incoming thing.

          >>> __(3, 5, 7, 3, 11).range().fetch()
          8
        '''

    def sum(start=0, precision=False):  # @NoSelf
        '''
        Discover total by adding `start` and incoming things together.

        :keyword start: starting number
        :type start: integer or float

        :keyword boolean precision: add floats with extended precision

          >>> # default behavior
          >>> __(1, 2, 3).sum().fetch()
          6
          >>> # with a starting mumber
          >>> __(1, 2, 3).sum(start=1).fetch()
          7
          >>> # add floating points with extended precision
          >>> __(.1, .1, .1, .1, .1, .1, .1, .1).sum(precision=True).fetch()
          1.0
        '''


class KOrder(AppspaceKey):

    '''ordering knife mixin'''

    def group():  # @NoSelf
        '''
        Group incoming things using :meth:`worker` as the `key function
        <http://docs.python.org/glossary.html#term-key-function>`_.

          >>> from knife import __
          >>> # default grouping
          >>> __(1.3, 2.1, 2.4).group().fetch()
          [(1.3, (1.3,)), (2.1, (2.1,)), (2.4, (2.4,))]
          >>> from math import floor
          >>> # use worker for key function
          >>> __(1.3, 2.1, 2.4).worker(floor).group().fetch()
          [(1.0, (1.3,)), (2.0, (2.1, 2.4))]
        '''

    def reverse():  # @NoSelf
        '''
        Reverse the order of incoming things.

          >>> __(5, 4, 3, 2, 1).reverse().fetch()
          [1, 2, 3, 4, 5]
        '''

    def sort():  # @NoSelf
        '''
        Randomly sort incoming things.

          >>> __(5, 4, 3, 2, 1).shuffle().fetch()
          [3, 1, 5, 4, 2]
        '''

    def shuffle():  # @NoSelf
        '''
        Reorder incoming things using :meth:`worker` as the `key function
        <http://docs.python.org/glossary.html#term-key-function>`_.

          >>> # default sort
          >>> __(4, 6, 65, 3, 63, 2, 4).sort().fetch()
          [2, 3, 4, 4, 6, 63, 65]
          >>> from math import sin
          >>> # using worker as key function
          >>> __(1, 2, 3, 4, 5, 6).worker(sin).sort().fetch()
          [5, 4, 6, 3, 1, 2]
        '''


class KRepeat(AppspaceKey):

    '''repeating knife key'''

    def combinate(n):  # @NoSelf
        '''
        Discover combinations of every `n` incoming things.

        :argument integer n: number of incoming things to generate
          combinations from

          >>> from knife import __
          >>> __(40, 50, 60).combinations(2).fetch()
          [(40, 50), (40, 60), (50, 60)]
        '''

    def copy():  # @NoSelf
        '''
        Duplicate each incoming thing.

          >>> __([[1, [2, 3]], [4, [5, 6]]]).copy().fetch()
          [[1, [2, 3]], [4, [5, 6]]]
        '''

    def permutate(n):  # @NoSelf
        '''
        Discover permutations of every `n` incoming things.

        :argument integer n: number of incoming things to generate
          permutations from

          >>> __(40, 50, 60).permutations(2).fetch()
          [(40, 50), (40, 60), (50, 40), (50, 60), (60, 40), (60, 50)]
        '''

    def repeat(n=None, call=False):  # @NoSelf
        '''
        Repeat either incoming things or invoke :meth:`worker` `n` times.

        :keyword integer n: number of times to repeat

        :keyword boolean call: repeat results of invoking :meth:`worker`

          >>> # repeat iterable
          >>> __(40, 50, 60).repeat(3).fetch()
          [(40, 50, 60), (40, 50, 60), (40, 50, 60)]
          >>> def test(*args):
          ...    return list(args)
          >>> # with worker
          >>> __(40, 50, 60).worker(test).repeat(n=3, call=True).fetch()
          [[40, 50, 60], [40, 50, 60], [40, 50, 60]]
        '''


class KMap(AppspaceKey):

    '''mapping knife key'''

    def argmap(merge=False):  # @NoSelf
        '''
        Feed each incoming thing to :meth:`worker` as `wildcard
        <http://docs.python.org/reference/compound_stmts.html#function>`_
        `positional arguments
        <http://docs.python.org/glossary.html#term-positional-argument>`_.

        :keyword boolean merge: merge global positional :meth:`params` with
          positional arguments derived from an iterable

          >>> from knife import __
          >>> # default behavior
          >>> test = __((1, 2), (2, 3), (3, 4))
          >> test.worker(lambda x, y: x * y).argmap().fetch()
          [2, 6, 12]
          >>> # merge global positional arguments with iterable arguments
          >>> test.original().worker(lambda x, y, z, a, b: x * y * z * a * b)
          >>> test.params(7, 8, 9).argmap(merge=True).fetch()
          [1008, 3024, 6048]
        '''

    def invoke(name):  # @NoSelf
        '''
        Call method `name` from each incoming thing with the global
        `positional
        <http://docs.python.org/glossary.html#term-positional-argument>`_ and
        `keyword <http://docs.python.org/glossary.html#term-keyword-argument>`_
        :meth:`params` but keep the original thing if the return value of the
        method call is :const:`None`.

        :argument string name: method name

          >>> # invoke list.index()
          >>> __([5, 1, 7], [3, 2, 1]).params(1).invoke('index').fetch()
          [1, 2]
          >>> # invoke list.sort() but return sorted list instead of None
          >>> __([5, 1, 7], [3, 2, 1]).invoke('sort').fetch()
          [[1, 5, 7], [1, 2, 3]]
        '''

    def kwargmap(merge=False):  # @NoSelf
        '''
        Feed each incoming thing as a :class:`tuple` of `wildcard
        <http://docs.python.org/reference/compound_stmts.html#function>`_
        `positional
        <http://docs.python.org/glossary.html#term-positional-argument>`_ and
        `keyword <http://docs.python.org/glossary.html#term-keyword-argument>`_
        arguments to :meth:`worker`.

        :keyword boolean merge: merge global positional or keyword
          :meth:`params` with positional and keyword arguments derived from an
          iterable into a single :class:`tuple` of wildcard positional and
          keyword arguments like (*iterable_args* + *global_args*,
          *global_kwargs* + *iterable_kwargs*)

          >>> # default behavior
          >>> test = __(
          ...  ((1, 2), {'a': 2}), ((2, 3), {'a': 2}), ((3, 4), {'a': 2})
          ... )
          >>> test.worker(test).kwargmap().fetch()
          [6, 10, 14]
          >>> def tester(*args, **kw):
          ...    return sum(args) * sum(kw.values())
          >>> # merging global and iterable derived positional and keyword args
          >>> test.original().worker(tester).params(1, 2, 3, b=5, w=10, y=13)
          >>> test.kwargmap(merge=True).fetch()
          [270, 330, 390]
        '''

    def map(self):  # @NoSelf
        '''
        Feed each incoming thing to :meth:`worker`.

          >>> __(1, 2, 3).worker(lambda x: x * 3).map().fetch()
          [3, 6, 9]
        '''

    def mapping(keys=False, values=False):  # @NoSelf
        '''
        Run :meth:`worker` on incoming `mapping
        <http://docs.python.org/glossary.html#term-mapping>`_ things.

        :keyword boolean keys: collect mapping keys only

        :keyword boolean values: collect mapping values only

          >>> # filter items
          >>> __(dict([(1, 2), (2, 3), (3, 4)]), dict([(1, 2), (2, 3), (3, 4)])
          ... ).worker(lambda x, y: x * y).mapping().fetch()
          [2, 6, 12, 2, 6, 12]
          >>> # mapping keys only
          >>> __(dict([(1, 2), (2, 3), (3, 4)]), dict([(1, 2), (2, 3), (3, 4)])
          ... ).mapping(keys=True).fetch()
          [1, 2, 3, 1, 2, 3]
          >>> # mapping values only
          >>> __(dict([(1, 2), (2, 3), (3, 4)]), dict([(1, 2), (2, 3), (3, 4)])
          ... ).mapping(values=True).fetch()
          [2, 3, 4, 2, 3, 4]
        '''


class KFilter(AppspaceKey):

    '''filtering knife key'''

    def attrs(*names):  # @NoSelf
        '''
        Collect `attribute
        <http://docs.python.org/glossary.html#term-attribute>`_ values from
        incoming things that match an attribute *name* found in `names`.

        :argument string names: attribute names

          >>> from knife import __
          >>> from stuf import stuf
          >>> stooge = [
          ...    stuf(name='moe', age=40),
          ...    stuf(name='larry', age=50),
          ...    stuf(name='curly', age=60),
          ... ]
          >>> __(*stooge).attrs('name').fetch()
          ['moe', 'larry', 'curly']
          >>> # multiple attribute names
          >>> __(*stooge).attrs('name', 'age').fetch()
          [('moe', 40), ('larry', 50), ('curly', 60)]
          >>> # no attrs named 'place'
          >>> __(*stooge).attrs('place').fetch()
          []
        '''

    def duality():  # @NoSelf
        '''
        Divide incoming things into two `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_, the first being
        everything :meth:`worker` evaluates as :const:`True` and the second
        being everything :meth:`worker` evaluates as :const:`False`.

          >>> test = __(1, 2, 3, 4, 5, 6).worker(lambda x: x % 2 == 0)
          >>> divide = test.duality().fetch()
          >>> divide.true
          [2, 4, 6]
          >>> divide.false
          [1, 3, 5]
        '''

    def filter(invert=False):  # @NoSelf
        '''
        Collect incoming things matched by :meth:`worker`.

        :keyword boolean invert: collect incoming things :meth:`worker`
          evaluates as :const:`False` instead of :const:`True`

          >>> # filter for true values
          >>> test = __(1, 2, 3, 4, 5, 6).worker(lambda x: x % 2 == 0)
          >>> test.filter().fetch()
          [2, 4, 6]
          >>> # filter for false values
          >>> test.original().worker(lambda x: x % 2 == 0)
          >>> test.filter(invert=True).fetch()
          [1, 3, 5]
        '''

    def items(*keys):  # @NoSelf
        '''
        Collect values from incoming things (usually `sequences
        <http://docs.python.org/glossary.html#term-sequence>`_ or `mappings
        <http://docs.python.org/glossary.html#term-mapping>`_) that match a
        *key* found in `keys`.

        :argument string keys: keys or indices

          >>> stooge = [
          ...    dict(name='moe', age=40),
          ...    dict(name='larry', age=50),
          ...    dict(name='curly', age=60)
          ... ]
          >>> # get items from mappings like dictionaries, etc...
          >>> __(*stooge).items('name').fetch()
          ['moe', 'larry', 'curly']
          >>> __(*stooge).items('name', 'age').fetch()
          [('moe', 40), ('larry', 50), ('curly', 60)]
          >>> # get items from sequences like lists, tuples, etc...
          >>> stooge = [['moe', 40], ['larry', 50], ['curly', 60]]
          >>> __(*stooge).items(0).fetch()
          ['moe', 'larry', 'curly']
          >>> __(*stooge).items(1).fetch()
          [40, 50, 60]
          >>> __(*stooge).items('place').fetch()
          []
        '''

    def pattern(pattern, type='parse', flags=0):  # @NoSelf
        '''
        Compile search `pattern` for use as :meth:`worker`.

        :argument string pattern: search pattern

        :keyword string type: engine to compile `pattern` with. Valid options
          are `'parse' <http://pypi.python.org/pypi/parse/>`_, `'re'
          <http://docs.python.org/library/re.html>`_, or `'glob'
          <http://docs.python.org/library/fnmatch.html>`_

        :keyword integer flags: regular expression `flags
          <http://docs.python.org/library/re.html#re.DEBUG>`_

          >>> # using parse expression
          >>> test = __('first test', 'second test', 'third test')
          >>> test.pattern('first {}').filter().fetch()
          'first test'
          >>> # using regular expression
          >>> test.original().pattern('third .', type='regex').filter().fetch()
          'third test'
          >>> # using glob pattern
          >>> test.original().pattern('second*', type='glob').filter().fetch()
          'second test'
        '''

    def traverse(invert=False):  # @NoSelf
        '''
        Collect deeply nested values from incoming things matched by
        :meth:`worker`.

        :keyword boolean invert: select incoming things that :meth:`worker`
          evaluates as :const:`False` rather than :const:`True`

          >>> class stooge:
          ...    name = 'moe'
          ...    age = 40
          >>> class stooge2:
          ...    name = 'larry'
          ...    age = 50
          >>> class stooge3:
          ...    name = 'curly'
          ...    age = 60
          ...    class stooge4(object):
          ...        name = 'beastly'
          ...        age = 969
          >>> def test(x):
          ...    if x[0] == 'name':
          ...        return True
          ...    elif x[0].startswith('__'):
          ...        return True
          ...    return False
          >>> # using worker while filtering for False values
          >>> test.original().worker(test).traverse(invert=True).fetch()
          [ChainMap(OrderedDict([('classname', 'stooges'), ('age', 40)])),
          ChainMap(OrderedDict([('classname', 'stooge2'), ('age', 50)])),
          ChainMap(OrderedDict([('classname', 'stooge3'), ('age', 60)]),
          OrderedDict([('classname', 'stooge4'), ('age', 969)]))]
        '''


class KReduce(AppspaceKey):

    '''reducing knife key'''

    def flatten():  # @NoSelf
        '''
        Reduce nested incoming things to flattened incoming things.

          >>> from knife import __
          >>> __([[1, [2], [3, [[4]]]], 'here']).flatten().fetch()
          [1, 2, 3, 4, 'here']
        '''

    def merge(self):  # @NoSelf
        '''
        Reduce multiple `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ incoming
        things into one iterable incoming thing.

          >>> test = __(['moe', 'larry'], [30, 40], [True, False])
          test.merge().fetch()
          ['moe', 'larry', 30, 40, True, False]
        '''

    def reduce(initial=None, reverse=False):  # @NoSelf
        '''
        Reduce `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        incoming things down to one incoming thing using :meth:`worker`.

        :keyword initial: starting value

        :keyword boolean reverse: reduce from `the right side
          <http://www.zvon.org/other/haskell/Outputprelude/foldr_f.html>`_
          of incoming things

          >>> # reduce from left side
          >>> __(1, 2, 3).worker(lambda x, y: x + y).reduce().fetch(),
          6
          >>> # reduce from left side with initial value
          >>> __(1, 2, 3).worker(lambda x, y: x + y).reduce(1).fetch()
          7
          >>> # reduce from right side
          >>> test = __([0, 1], [2, 3], [4, 5]).worker(lambda x, y: x + y)
          >>> test.reduce(reverse=True).fetch()
          [4, 5, 2, 3, 0, 1]
          >>> # reduce from right side with initial value
          >>> test.original().worker(lambda x, y: x + y)
          >>> test.reduce(initial=[0, 0], reverse=True).fetch()
          [4, 5, 2, 3, 0, 1, 0, 0]
        '''

    def zip():  # @NoSelf
        '''
        Convert multiple `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ incoming
        things to :class:`tuples` composed of things found at the same index
        position within those iterables.

          >>> test = __(['moe', 'larry'], [30, 40], [True, False])
          >>> test.zip().fetch()
          [('moe', 30, True), ('larry', 40, False)]
        '''


class KSlice(AppspaceKey):

    '''slicing key'''

    def at(n, default=None):  # @NoSelf
        '''
        `Slice <http://docs.python.org/glossary.html#term-slice>`_ off
        incoming thing found at index `n`.

        :argument integer n: index of some incoming thing

        :keyword default: default returned if nothing is found at `n`

          >>> from knife import __
          >>> # default behavior
          >>> __(5, 4, 3, 2, 1).at(2).fetch()
          3
          >>> # return default value if nothing found at index
          >>> __(5, 4, 3, 2, 1).at(10, 11).fetch()
          11
        '''

    def choice():  # @NoSelf
        '''
        `Randomly slice <http://docs.python.org/glossary.html#term-slice>`_ off
        **one** incoming thing.

          >>> __(1, 2, 3, 4, 5, 6).choice().fetch()
          3
        '''

    def dice(n, fill=None):  # @NoSelf
        '''
        `Slice <http://docs.python.org/glossary.html#term-slice>`_ one
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        incoming thing into `n` iterable incoming things.

        :argument integer n: number of incoming things per slice

        :keyword fill: value to pad out incomplete iterables

        >>> __('moe', 'larry', 'curly', 30, 40, 50, True).dice(2, 'x').fetch()
        [('moe', 'larry'), ('curly', 30), (40, 50), (True, 'x')]
        '''

    def first(n=0):  # @NoSelf
        '''
        Slice off `n` things from the **starting** end of incoming things or
        just the **first** incoming thing.

        :keyword integer n: number of incoming things

          >>> # default behavior
          >>> __(5, 4, 3, 2, 1).first().fetch()
          5
          >>> # first things from index 0 to 2
          >>> __(5, 4, 3, 2, 1).first(2).fetch()
          [5, 4]
        '''

    def initial():  # @NoSelf
        '''
        `Slice <http://docs.python.org/glossary.html#term-slice>`_ off
        everything except the **last** incoming thing.

          >>> __(5, 4, 3, 2, 1).initial().fetch()
          [5, 4, 3, 2]
        '''

    def last(n=0):  # @NoSelf
        '''
        `Slice <http://docs.python.org/glossary.html#term-slice>`_ off `n`
        things from the **tail** end of incoming things or just the **last**
        incoming thing.

        :keyword integer n: number of incoming things

          >>> # default behavior
          >>> __(5, 4, 3, 2, 1).last().fetch()
          1
          >>> # fetch last two things
          >>> __(5, 4, 3, 2, 1).last(2).fetch()
          [2, 1]
        '''

    def rest():  # @NoSelf
        '''
        `Slice <http://docs.python.org/glossary.html#term-slice>`_ off
        everything except the **first** incoming thing.

          >>> __(5, 4, 3, 2, 1).rest().fetch()
          [4, 3, 2, 1]
        '''

    def sample(n):  # @NoSelf
        '''
        Randomly `slice <http://docs.python.org/glossary.html#term-slice>`_ off
        `n` incoming things.

        :argument integer n: sample size

          >>> __(1, 2, 3, 4, 5, 6).sample(3).fetch()
          [2, 4, 5]
        '''

    def slice(start, stop=False, step=False):  # @NoSelf
        '''
        `Take a slice <http://docs.python.org/glossary.html#term-slice>`_ out
        of incoming things.

        :argument integer start: starting index of slice

        :keyword integer stop: stopping index of slice

        :keyword integer step: size of step in slice

          >>> # slice from index 0 to 3
          >>> __(5, 4, 3, 2, 1).slice(2).fetch()
          [5, 4]
          >>> # slice from index 2 to 4
          >>> __(5, 4, 3, 2, 1).slice(2, 4).fetch()
          [3, 2]
          >>> # slice from index 2 to 4 with 2 steps
          >>> __(5, 4, 3, 2, 1).slice(2, 4, 2).fetch()
          3
        '''
