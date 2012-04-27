# -*- coding: utf-8 -*-
'''knife mixin keys'''

from appspace.keys import AppspaceKey


class KCompare(AppspaceKey):

    '''
    comparing knife key
    '''

    def all():  # @NoSelf
        '''
        Discover if :meth:`worker` is :data:`True` for **all** incoming things.

        :rtype: :obj:`knife` :term:`object`

        >>> from knife import __
        >>> __(2, 4, 6, 8).worker(lambda x: x % 2 == 0).all().get()
        True

        .. seealso::

          :func:`~__builtins__.all`
            Python standard library

          `all <http://documentcloud.github.com/underscore/#all>`_
            Underscore.js

          `all <http://mirven.github.com/underscore.lua/#all>`_
            Underscore.lua

          `all <http://vti.github.com/underscore-perl/#all>`_
            Underscore.perl

          `all <http://brianhaveri.github.com/Underscore.php/#all>`_
            Underscore.php
        '''

    def any():  # @NoSelf
        '''
        Discover if :meth:`worker` is :data:`True` for **any** incoming thing.

        :rtype: :obj:`knife` :term:`object`

        >>> __(1, 4, 5, 9).worker(lambda x: x % 2 == 0).any().get()
        True

        .. seealso::

          :func:`~__builtins__.any`
            Python standard library

          `any <http://documentcloud.github.com/underscore/#any>`_
            Underscore.js

          `any <http://mirven.github.com/underscore.lua/#any>`_
            Underscore.lua

          `any <http://vti.github.com/underscore-perl/#ant>`_
            Underscore.perl

          `any <http://brianhaveri.github.com/Underscore.php/#any>`_
            Underscore.php
        '''

    def difference(symmetric=False):  # @NoSelf
        '''
        Discover difference within a series of :term:`iterable` incoming
        things.

        :keyword bool symmetric: return symmetric difference

        :rtype: :obj:`knife` :term:`object`

        >>> # default behavior
        >>> test = __([1, 2, 3, 4, 5], [5, 2, 10], [10, 11, 2])
        >>> test.difference().get()
        [1, 3, 4]
        >>> # symmetric difference
        >>> test.original().difference(symmetric=True).get()
        [1, 2, 3, 4, 11]

        .. seealso::

          :meth:`set.difference`
            Python standard library

          :meth:`set.symmetric_difference`
            Python standard library

          `difference <http://documentcloud.github.com/underscore/#difference>`_
            Underscore.js

          `difference <http://vti.github.com/underscore-perl/#difference>`_
            Underscore.perl

          `difference <http://brianhaveri.github.com/Underscore.php/#difference>`_
            Underscore.php
        '''

    def intersect():  # @NoSelf
        '''
        Discover intersection within a series of :term:`iterable` incoming
        things.

        :rtype: :obj:`knife` :term:`object`

        >>> __([1, 2, 3], [101, 2, 1, 10], [2, 1]).intersection().get()
        [1, 2]

        .. seealso::

          :meth:`set.intersection`
            Python standard library

          `intersection <http://documentcloud.github.com/underscore/#intersection>`_
            Underscore.js

          `intersection <http://vti.github.com/underscore-perl/#intersection>`_
            Underscore.perl

          `intersection <http://brianhaveri.github.com/Underscore.php/#intersection>`_
            Underscore.php
        '''

    def union():  # @NoSelf
        '''
        Discover union within a series of :term:`iterable` incoming things.

        :rtype: :obj:`knife` :term:`object`

        >>> __([1, 2, 3], [101, 2, 1, 10], [2, 1]).union().get()
        [1, 10, 3, 2, 101]

        .. seealso::

          :meth:`set.union`
            Python standard library

          `union <http://documentcloud.github.com/underscore/#union>`_
            Underscore.js

          `union <http://vti.github.com/underscore-perl/#union>`_
            Underscore.perl

          `union <http://brianhaveri.github.com/Underscore.php/#union>`_
            Underscore.php
        '''

    def unique():  # @NoSelf
        '''
        Discover unique incoming things.

        :rtype: :obj:`knife` :term:`object`

        >>> # default behavior
        >>> __(1, 2, 1, 3, 1, 4).unique().get()
        [1, 2, 3, 4]
        >>> # using worker as key function
        >>> __(1, 2, 1, 3, 1, 4).worker(round).unique().get()
        [1, 2, 3, 4]

        .. seealso::

          `uniq <http://documentcloud.github.com/underscore/#uniq>`_
            Underscore.js

          `uniq <http://vti.github.com/underscore-perl/#uniq>`_
            Underscore.perl

          `uniq <http://brianhaveri.github.com/Underscore.php/#uniq>`_
            Underscore.php
        '''


class KMath(AppspaceKey):

    '''mathing knife key'''

    def average():  # @NoSelf
        '''
        Discover average value among incoming things.

        :rtype: :obj:`knife` :term:`object`

        >>> from knife import __
        >>> __(10, 40, 45).average().get()
        31.666666666666668
        '''

    def count():  # @NoSelf
        '''
        Discover how common each incoming thing is.

        :return: Collects :func:`~collections.namedtuple` ``Count(least=int,
          most=int, overall=[(thing1, int), (thing2, int), ...])``

        :rtype: :obj:`knife` :term:`object`

        >>> common = __(11, 3, 5, 11, 7, 3, 5, 11).count().get()
        >>> # least common thing
        >>> common.least
        7
        >>> # most common thing
        >>> common.most
        11
        >>> # total count for every thing
        >>> common.overall
        [(11, 3), (3, 2), (5, 2), (7, 1)]
        '''

    def max():  # @NoSelf
        '''
        Discover the maximum value among incoming things using :meth:`worker`
        as the :term:`key function`.

        :rtype: :obj:`knife` :term:`object`

        >>> # default behavior
        >>> __(1, 2, 4).max().get()
        4
        >>> stooges = (
        ...    {'name': 'moe', 'age': 40},
        ...    {'name': 'larry', 'age': 50},
        ...    {'name': 'curly', 'age': 60},
        ... )
        >>> # using worker as key function
        >>> __(*stooges).worker(lambda x: x['age']).max().get()
        {'age': 60, 'name': 'curly'}

        .. seealso::

          :func:`~__builtins__.max`
            Python standard library

          `max <http://documentcloud.github.com/underscore/#max>`_
            Underscore.js

          `max <http://mirven.github.com/underscore.lua/#max>`_
            Underscore.lua

          `max <http://vti.github.com/underscore-perl/#max>`_
            Underscore.perl

          `max <http://brianhaveri.github.com/Underscore.php/#max>`_
            Underscore.php
        '''

    def median():  # @NoSelf
        '''
        Discover the median value among incoming things.

        :rtype: :obj:`knife` :term:`object`

        >>> __(4, 5, 7, 2, 1).median().get()
        4
        >>> __(4, 5, 7, 2, 1, 8).median().get()
        4.5
        '''

    def min():  # @NoSelf
        '''
        Discover the minimum value among incoming things using :meth:`worker`
        as the :term:`key function`.

        :rtype: :obj:`knife` :term:`object`

        >>> test = __(10, 5, 100, 2, 1000)
        >>> test.min().get()
        2
        >>> test.original().worker(lambda x: x % 100 == 0).min().get()
        10

        .. seealso::

          :func:`~__builtins__.min`
            Python standard library

          `min <http://documentcloud.github.com/underscore/#min>`_
            Underscore.js

          `min <http://mirven.github.com/underscore.lua/#min>`_
            Underscore.lua

          `min <http://vti.github.com/underscore-perl/#min>`_
            Underscore.perl

          `min <http://brianhaveri.github.com/Underscore.php/#min>`_
            Underscore.php
        '''

    def minmax():  # @NoSelf
        '''
        Discover the minimum and maximum values among incoming things.

        :return:  :func:`~collections.namedtuple` ``MinMAx(min=value,
          max=value)``.

        :rtype: :obj:`knife` :term:`object`

        >>> minmax = __(1, 2, 4).minmax().get()
        >>> minmax.min
        1
        >>> minmax.max
        4
        '''

    def range():  # @NoSelf
        '''
        Discover the length of the smallest interval that can contain the
        value of every incoming thing.

        :rtype: :obj:`knife` :term:`object`

        >>> __(3, 5, 7, 3, 11).range().get()
        8
        '''

    def sum(start=0, precision=False):  # @NoSelf
        '''
        Discover the total value of adding `start` and incoming things
        together.

        :keyword start: starting number
        :type start: :func:`int` or :func:`float`

        :keyword bool precision: add floats with extended precision

        :rtype: :obj:`knife` :term:`object`

        >>> # default behavior
        >>> __(1, 2, 3).sum().get()
        6
        >>> # with a starting mumber
        >>> __(1, 2, 3).sum(start=1).get()
        7
        >>> # add floating points with extended precision
        >>> __(.1, .1, .1, .1, .1, .1, .1, .1).sum(precision=True).get()
        0.8
        '''


class KOrder(AppspaceKey):

    '''ordering knife mixin'''

    def group():  # @NoSelf
        '''
        Group incoming things using :meth:`worker` as the :term:`key function`.

        :return: Collects :func:`~collections.namedtuple` ``Group(keys=keys,
          groups=tuple)``

        :rtype: :obj:`knife` :term:`object`

        >>> from knife import __
        >>> # default grouping
        >>> __(1.3, 2.1).group().get()
        [Group(keys=1.3, groups=(1.3,)), Group(keys=2.1, groups=(2.1,))]
        >>> from math import floor
        >>> # use worker for key function
        >>> __(1.3, 2.1, 2.4).worker(floor).group().get()
        [Group(keys=1.0, groups=(1.3,)), Group(keys=2.0, groups=(2.1, 2.4))]

        .. seealso::

          :func:`itertools.groupby`
            Python standard library

          `groupBy <http://documentcloud.github.com/underscore/#groupBy>`_
            Underscore.js

          `groupBy <http://vti.github.com/underscore-perl/#groupBy>`_
            Underscore.perl

          `groupBy <http://brianhaveri.github.com/Underscore.php/#groupBy>`_
            Underscore.php
        '''

    def reverse():  # @NoSelf
        '''
        Reverse the order of incoming things.

        :rtype: :obj:`knife` :term:`object`

        >>> __(5, 4, 3, 2, 1).reverse().get()
        [1, 2, 3, 4, 5]

        .. seealso::

          :func:`~__builtins__.reversed`
            Python standard library

          `reverse <http://mirven.github.com/underscore.lua/#reverse>`_
            Underscore.lua
        '''

    def sort():  # @NoSelf
        '''
        Randomly sort incoming things.

        :rtype: :obj:`knife` :term:`object`

          >>> __(5, 4, 3, 2, 1).shuffle().get() # doctest: +SKIP
          [3, 1, 5, 4, 2]

        .. seealso::

          :func:`ramdom.shuffle`
            Python standard library

          `shuffle <http://documentcloud.github.com/underscore/#shuffle>`_
            Underscore.js

          `shuffle <http://brianhaveri.github.com/Underscore.php/#shuffle>`_
            Underscore.php
        '''

    def shuffle():  # @NoSelf
        '''
        Reorder incoming things using :meth:`worker` as the
        :term:`key function`.

        :rtype: :obj:`knife` :term:`object`

        >>> # default sort
        >>> __(4, 6, 65, 3, 63, 2, 4).sort().get()
        [2, 3, 4, 4, 6, 63, 65]
        >>> from math import sin
        >>> # using worker as key function
        >>> __(1, 2, 3, 4, 5, 6).worker(sin).sort().get()
        [5, 4, 6, 3, 1, 2]

        .. seealso::

          :func:`~__builtins__.sorted`
            Python standard library

          `sortBy <http://documentcloud.github.com/underscore/#sortBy>`_
            Underscore.js

          `sort <http://mirven.github.com/underscore.lua/#sort>`_
            Underscore.lua

          `sortBy <http://vti.github.com/underscore-perl/#sortBy>`_
            Underscore.perl

          `sortBy <http://brianhaveri.github.com/Underscore.php/#sortBy>`_
            Underscore.php
        '''


class KRepeat(AppspaceKey):

    '''repeating knife key'''

    def combinate(n):  # @NoSelf
        '''
        Discover `combinations <https://en.wikipedia.org/wiki/Combination>`_
        for every `n` incoming things.

        :argument int n: number of incoming things to derive combinations from

        :rtype: :obj:`knife` :term:`object`

        >>> from knife import __
        >>> __(40, 50, 60).combinate(2).get()
        [(40, 50), (40, 60), (50, 60)]

        .. seealso::

          :func:`itertools.combinations`
            Python standard library
        '''

    def copy():  # @NoSelf
        '''
        Duplicate each incoming thing.

        :rtype: :obj:`knife` :term:`object`

        >>> __([[1, [2, 3]], [4, [5, 6]]]).copy().get()
        [[1, [2, 3]], [4, [5, 6]]]

        .. seealso::

          :func:`copy.deepcopy`
            Python standard library
        '''

    def permutate(n):  # @NoSelf
        '''
        Discover `permutations <https://en.wikipedia.org/wiki/Permutation>`_
        for every `n` incoming things.

        :argument int n: number of incoming things to derive permutations from

        :rtype: :obj:`knife` :term:`object`

        >>> __(40, 50, 60).permutate(2).get()
        [(40, 50), (40, 60), (50, 40), (50, 60), (60, 40), (60, 50)]

        .. seealso::

          :func:`itertools.permutations`
            Python standard library
        '''

    def repeat(n=None, call=False):  # @NoSelf
        '''
        Repeat incoming things `n` times or invoke :meth:`worker` `n` times.

        :keyword int n: number of times to repeat

        :keyword bool call: repeat results of invoking :meth:`worker`

        :rtype: :obj:`knife` :term:`object`

        >>> # repeat iterable
        >>> __(40, 50, 60).repeat(3).get()
        [(40, 50, 60), (40, 50, 60), (40, 50, 60)]
        >>> def test(*args):
        ...    return list(args)
        >>> # with worker
        >>> __(40, 50, 60).worker(test).repeat(n=3, call=True).get()
        [[40, 50, 60], [40, 50, 60], [40, 50, 60]]

        .. seealso::

          :func:`itertools.repeat`
            Python standard library

          `times <http://documentcloud.github.com/underscore/#times>`_
            Underscore.js

          `times <http://vti.github.com/underscore-perl/#times>`_
            Underscore.perl

          `times <http://brianhaveri.github.com/Underscore.php/#times>`_
            Underscore.php
        '''


class KMap(AppspaceKey):

    '''mapping knife key'''

    def argmap(merge=False):  # @NoSelf
        '''
        Feed each incoming thing to :meth:`worker` as :term:`positional
        argument`\s.

        :keyword bool merge: merge global positional :meth:`params` with
          positional arguments derived from incoming things

        :rtype: :obj:`knife` :term:`object`

        >>> from knife import __
        >>> # default behavior
        >>> test = __((1, 2), (2, 3), (3, 4))
        >>> test.worker(lambda x, y: x * y).argmap().get()
        [2, 6, 12]
        >>> # merge global positional arguments with iterable arguments
        >>> test.original().worker(
        ...   lambda x, y, z, a, b: x * y * z * a * b
        ... ).params(7, 8, 9).argmap(merge=True).get()
        [1008, 3024, 6048]

        .. seealso::

          :func:`itertools.starmap`
            Python standard library
        '''

    def invoke(name):  # @NoSelf
        '''
        Feed global :term:`positional argument`\s and :term:`keyword
        argument`\s to each incoming thing's `name` :term:`method`.

        .. note::

          The original thing is returned if the return value of :term:`method`
          `name` is :data:`None`.

        :argument str name: method name

        :rtype: :obj:`knife` :term:`object`

        >>> # invoke list.index()
        >>> __([5, 1, 7], [3, 2, 1]).params(1).invoke('index').get()
        [1, 2]
        >>> # invoke list.sort() but return sorted list instead of None
        >>> __([5, 1, 7], [3, 2, 1]).invoke('sort').get()
        [[1, 5, 7], [1, 2, 3]]

        .. seealso::

          `invoke <http://documentcloud.github.com/underscore/#invoke>`_
            Underscore.js

          `invoke <http://mirven.github.com/underscore.lua/#invoke>`_
            Underscore.lua

          `invoke <http://vti.github.com/underscore-perl/#invoke>`_
            Underscore.perl

          `invoke <http://brianhaveri.github.com/Underscore.php/#invoke>`_
            Underscore.php
        '''

    def kwargmap(merge=False):  # @NoSelf
        '''
        Feed each incoming thing as a :func:`tuple` of
        :term:`positional argument`\s and :term:`keyword argument`\s to
        :meth:`worker`.

        :keyword bool merge: merge global positional or keyword :meth:`params`
          with positional and keyword arguments derived from incoming things
          into a single :func:`tuple` of wildcard positional and keyword
          arguments like ``(*iterable_args + global_args, **global_kwargs +
          iterable_kwargs)``

        :rtype: :obj:`knife` :term:`object`

        >>> # default behavior
        >>> test = __(
        ...  ((1, 2), {'a': 2}), ((2, 3), {'a': 2}), ((3, 4), {'a': 2})
        ... )
        >>> def tester(*args, **kw):
        ...    return sum(args) * sum(kw.values())
        >>> test.worker(tester).kwargmap().get()
        [6, 10, 14]
        >>> # merging global and iterable derived positional and keyword args
        >>> test.original().worker(tester).params(
        ...   1, 2, 3, b=5, w=10, y=13
        ... ).kwargmap(merge=True).get()
        [270, 330, 390]
        '''

    def map(self):  # @NoSelf
        '''
        Feed each incoming thing to :meth:`worker`.

        :rtype: :obj:`knife` :term:`object`

        >>> __(1, 2, 3).worker(lambda x: x * 3).map().get()
        [3, 6, 9]

        .. seealso::

          :func:`itertools.imap`
            Python standard library

          `map <http://documentcloud.github.com/underscore/#map>`_
            Underscore.js

          `map <http://mirven.github.com/underscore.lua/#map>`_
            Underscore.lua

          `map <http://vti.github.com/underscore-perl/#map>`_
            Underscore.perl

          `map <http://brianhaveri.github.com/Underscore.php/#map>`_
            Underscore.php
        '''

    def mapping(keys=False, values=False):  # @NoSelf
        '''
        Run :meth:`worker` on incoming :term:`mapping` things.

        :keyword bool keys: collect mapping keys only

        :keyword bool values: collect mapping values only

        :rtype: :obj:`knife` :term:`object`

        >>> # filter items
        >>> __(dict([(1, 2), (2, 3), (3, 4)]), dict([(1, 2), (2, 3), (3, 4)])
        ... ).worker(lambda x, y: x * y).mapping().get()
        [2, 6, 12, 2, 6, 12]
        >>> # mapping keys only
        >>> __(dict([(1, 2), (2, 3), (3, 4)]), dict([(1, 2), (2, 3), (3, 4)])
        ... ).mapping(keys=True).get()
        [1, 2, 3, 1, 2, 3]
        >>> # mapping values only
        >>> __(dict([(1, 2), (2, 3), (3, 4)]), dict([(1, 2), (2, 3), (3, 4)])
        ... ).mapping(values=True).get()
        [2, 3, 4, 2, 3, 4]

        .. seealso::

          `keys <http://documentcloud.github.com/underscore/#keys>`_
            Underscore.js

          `values <http://documentcloud.github.com/underscore/#values>`_
            Underscore.js

          `keys <http://mirven.github.com/underscore.lua/#keys>`_
            Underscore.lua

          `values <http://mirven.github.com/underscore.lua/#values>`_
            Underscore.lua

          `keys <http://vti.github.com/underscore-perl/#keys>`_
            Underscore.perl

          `values <http://vti.github.com/underscore-perl/#values>`_
            Underscore.perl

          `keys <http://brianhaveri.github.com/Underscore.php/#keys>`_
            Underscore.php

           `values <http://brianhaveri.github.com/Underscore.php/#values>`_
             Underscore.php
        '''


class KFilter(AppspaceKey):

    '''filtering knife key'''

    def attrs(*names):  # @NoSelf
        '''
        Collect :term:`attribute` values from incoming things that match an
        **attribute name** found in `names`.

        :argument str names: attribute names

        :rtype: :obj:`knife` :term:`object`

        >>> from knife import __
        >>> from stuf import stuf
        >>> stooge = [
        ...    stuf(name='moe', age=40),
        ...    stuf(name='larry', age=50),
        ...    stuf(name='curly', age=60),
        ... ]
        >>> __(*stooge).attrs('name').get()
        ['moe', 'larry', 'curly']
        >>> # multiple attribute names
        >>> __(*stooge).attrs('name', 'age').get()
        [('moe', 40), ('larry', 50), ('curly', 60)]
        >>> # no attrs named 'place'
        >>> __(*stooge).attrs('place').get()
        []

        .. seealso::

          :func:`operator.attrgetter`
            Python standard library

          `pick <http://documentcloud.github.com/underscore/#pick>`_
            Underscore.js
        '''

    def duality():  # @NoSelf
        '''
        Divide incoming things into two :term:`iterable`\s, the first
        everything :meth:`worker` is :data:`True` for and the second
        everything :meth:`worker` is :data:`False` for.

        :rtype: :obj:`knife` :term:`object`

        >>> test = __(1, 2, 3, 4, 5, 6).worker(lambda x: x % 2 == 0)
        >>> divide = test.duality().get()
        >>> divide.true
        (2, 4, 6)
        >>> divide.false
        (1, 3, 5)
        '''

    def filter(invert=False):  # @NoSelf
        '''
        Collect incoming things matched by :meth:`worker`.

        :keyword bool invert: collect incoming things :meth:`worker` is
          :data:`False` rather than :data:`True` for

        :rtype: :obj:`knife` :term:`object`

        >>> # filter for true values
        >>> test = __(1, 2, 3, 4, 5, 6).worker(lambda x: x % 2 == 0)
        >>> test.filter().get()
        [2, 4, 6]
        >>> # filter for false values
        >>> test.original().worker(
        ...   lambda x: x % 2 == 0
        ... ).filter(invert=True).get()
        [1, 3, 5]

        .. seealso::

          :func:`itertools.ifilter`
            Python standard library

          :func:`itertools.ifilterfalse`
            Python standard library

          `filter <http://documentcloud.github.com/underscore/#filter>`_
            Underscore.js

          `reject <http://documentcloud.github.com/underscore/#reject>`_
            Underscore.js

          `filter <http://mirven.github.com/underscore.lua/#filter>`_
            Underscore.lua

          `reject <http://mirven.github.com/underscore.lua/#reject>`_
            Underscore.lua

          `filter <http://vti.github.com/underscore-perl/#filter>`_
            Underscore.perl

          `reject <http://vti.github.com/underscore-perl/#reject>`_
            Underscore.perl

          `filter <http://brianhaveri.github.com/Underscore.php/#filter>`_
            Underscore.php

          `reject <http://brianhaveri.github.com/Underscore.php/#reject>`_
            Underscore.php
        '''

    def items(*keys):  # @NoSelf
        '''
        Collect values from incoming things (usually a :term:`sequence` or
        :term:`mapping`) that match a **key** found in `keys`.

        :argument str keys: keys or indices

        :rtype: :obj:`knife` :term:`object`

        >>> stooge = [
        ...    dict(name='moe', age=40),
        ...    dict(name='larry', age=50),
        ...    dict(name='curly', age=60)
        ... ]
        >>> # get items from mappings like dictionaries, etc...
        >>> __(*stooge).items('name').get()
        ['moe', 'larry', 'curly']
        >>> __(*stooge).items('name', 'age').get()
        [('moe', 40), ('larry', 50), ('curly', 60)]
        >>> # get items from sequences like lists, tuples, etc...
        >>> stooge = [['moe', 40], ['larry', 50], ['curly', 60]]
        >>> __(*stooge).items(0).get()
        ['moe', 'larry', 'curly']
        >>> __(*stooge).items(1).get()
        [40, 50, 60]
        >>> __(*stooge).items('place').get()
        []

       .. seealso::

          :func:`operator.itemgetter`
            Python standard library

          `pick <http://documentcloud.github.com/underscore/#pick>`_
            Underscore.js
        '''

    def traverse(self, invert=False):
        '''
        Collect deeply nested values from incoming things matched by
        :meth:`worker`.

        :keyword bool invert: collect incoming things that :meth:`worker` is
          :data:`False` rather than :data:`True` for

        :rtype: :obj:`knife` :term:`object`

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
        >>> __(stooge, stooge2, stooge3).worker(test).traverse(
        ...   invert=True
        ... ).get() # doctest: +NORMALIZE_WHITESPACE
        [ChainMap(OrderedDict([('classname', 'stooge'), ('age', 40)])),
        ChainMap(OrderedDict([('classname', 'stooge2'), ('age', 50)])),
        ChainMap(OrderedDict([('classname', 'stooge3'), ('age', 60)]),
        OrderedDict([('age', 969), ('classname', 'stooge4')]))]
        '''


class KReduce(AppspaceKey):

    '''reducing knife key'''

    def flatten():  # @NoSelf
        '''
        Reduce nested incoming things to flattened incoming things.

        :rtype: :obj:`knife` :term:`object`

        >>> from knife import __
        >>> __([[1, [2], [3, [[4]]]], 'here']).flatten().get()
        [1, 2, 3, 4, 'here']

        .. seealso::

          `flatten <http://documentcloud.github.com/underscore/#flatten>`_
            Underscore.js

          `flatten <http://mirven.github.com/underscore.lua/#flatten>`_
            Underscore.lua

          `flatten <http://vti.github.com/underscore-perl/#flatten>`_
            Underscore.perl

          `flatten <http://brianhaveri.github.com/Underscore.php/#flatten>`_
            Underscore.php
        '''

    def merge():  # @NoSelf
        '''
        Reduce multiple :term:`iterable` incoming things into one iterable
        incoming thing.

        :rtype: :obj:`knife` :term:`object`

        >>> __(['moe', 'larry'], [30, 40], [True, False]).merge().get()
        ['moe', 'larry', 30, 40, True, False]

        .. seealso::

          :classmethod:`itertools.chain.from_iterable`
            Python standard library
        '''

    def reduce(initial=None, reverse=False):  # @NoSelf
        '''
        Reduce :term:`iterable` incoming things down to one incoming thing
        using :meth:`worker`.

        :keyword initial: starting value

        :keyword bool reverse: reduce from `the right side <http://www.zvon.
          org/other/haskell/Outputprelude/foldr_f.html>`_ of incoming things

        :rtype: :obj:`knife` :term:`object`

        >>> # reduce from left side
        >>> __(1, 2, 3).worker(lambda x, y: x + y).reduce().get()
        6
        >>> # reduce from left side with initial value
        >>> __(1, 2, 3).worker(lambda x, y: x + y).reduce(initial=1).get()
        7
        >>> # reduce from right side
        >>> test = __([0, 1], [2, 3], [4, 5]).worker(lambda x, y: x + y)
        >>> test.reduce(reverse=True).get()
        [4, 5, 2, 3, 0, 1]
        >>> # reduce from right side with initial value
        >>> test.original().worker(
        ... lambda x, y: x + y
        ... ).reduce([0, 0], True).get()
        [4, 5, 2, 3, 0, 1, 0, 0]

        .. seealso::

          :func:`functools.reduce`
            Python standard library

          `reduce <http://documentcloud.github.com/underscore/#reduce>`_
            Underscore.js

          `reduceRight <http://documentcloud.github.com/underscore/#reduceRight>`_
            Underscore.js

          `reduce <http://mirven.github.com/underscore.lua/#reduce>`_
            Underscore.lua

          `reduce <http://vti.github.com/underscore-perl/#reduce>`_
            Underscore.perl

          `reduceRight <http://vti.github.com/underscore-perl/#reduceRight>`_
            Underscore.perl

          `reduce <http://brianhaveri.github.com/Underscore.php/#reduce>`_
            Underscore.php

          `reduceRight <http://brianhaveri.github.com/Underscore.php/#reduceRight>`_
            Underscore.php
        '''

    def zip():  # @NoSelf
        '''
        Convert multiple :term:`iterable` incoming things to a series of
        :func:`tuple`\s composed of things found at the same index position
        within the original iterables.

        :rtype: :obj:`knife` :term:`object`

        >>> test = __(['moe', 'larry'], [30, 40], [True, False])
        >>> test.zip().get()
        [('moe', 30, True), ('larry', 40, False)]

        .. seealso::

          :func:`itertools.izip`
            Python standard library

          `zip <http://documentcloud.github.com/underscore/#zip>`_
            Underscore.js

          `zip <http://vti.github.com/underscore-perl/#zip>`_
            Underscore.perl

          `zip <http://brianhaveri.github.com/Underscore.php/#zip>`_
            Underscore.php
        '''


class KSlice(AppspaceKey):

    '''slicing knife key'''

    def at(n, default=None):  # @NoSelf
        '''
        :term:`Slice` off incoming thing found at index `n`.

        :argument int n: index of some incoming thing

        :keyword default: default returned if nothing is found at `n`

        :rtype: :obj:`knife` :term:`object`

        >>> from knife import __
        >>> # default behavior
        >>> __(5, 4, 3, 2, 1).at(2).get()
        3
        >>> # return default value if nothing found at index
        >>> __(5, 4, 3, 2, 1).at(10, 11).get()
        11

        .. seealso::

          `"nth" <http://docs.python.org/library/itertools.html#recipes>`
            Itertools Recipes
        '''

    def choice():  # @NoSelf
        '''
        Randomly :term:`slice` off **one** incoming thing.

        :rtype: :obj:`knife` :term:`object`

        >>> __(1, 2, 3, 4, 5, 6).choice().get() # doctest: +SKIP
        3

        .. seealso::

          :func:`random.choice`
            Python standard library
        '''

    def dice(n, fill=None):  # @NoSelf
        '''
        :term:`Slice` one :term:`iterable` incoming thing into `n` iterable
        incoming things.

        :argument int n: number of incoming things per slice

        :keyword fill: value to pad out incomplete iterables

        :rtype: :obj:`knife` :term:`object`

        >>> __('moe', 'larry', 'curly', 30, 40, 50, True).dice(2, 'x').get()
        [('moe', 'larry'), ('curly', 30), (40, 50), (True, 'x')]

        .. seealso::

          `"grouper" <http://docs.python.org/library/itertools.html#recipes>`
            Itertools Recipes
        '''

    def first(n=0):  # @NoSelf
        '''
        :term:`Slice`  off `n` things from the **starting** end of incoming
        things or just the **first** incoming thing.

        :keyword int n: number of incoming things

        :rtype: :obj:`knife` :term:`object`

        >>> # default behavior
        >>> __(5, 4, 3, 2, 1).first().get()
        5
        >>> # first things from index 0 to 2
        >>> __(5, 4, 3, 2, 1).first(2).get()
        [5, 4]

        .. seealso::

          `first <http://documentcloud.github.com/underscore/#first>`_
            Underscore.js

          `first <http://mirven.github.com/underscore.lua/#first>`_
            Underscore.lua

          `first <http://vti.github.com/underscore-perl/#first>`_
            Underscore.perl

          `first <http://brianhaveri.github.com/Underscore.php/#first>`_
            Underscore.php
        '''

    def initial():  # @NoSelf
        '''
        :term:`Slice` off every incoming thing except the **last** incoming
        thing.

        :rtype: :obj:`knife` :term:`object`

        >>> __(5, 4, 3, 2, 1).initial().get()
        [5, 4, 3, 2]

        .. seealso::

          `initial <http://documentcloud.github.com/underscore/#initial>`_
            Underscore.js

          `initial <http://mirven.github.com/underscore.lua/#initial>`_
            Underscore.lua

          `initial <http://vti.github.com/underscore-perl/#initial>`_
            Underscore.perl

          `initial <http://brianhaveri.github.com/Underscore.php/#initial>`_
            Underscore.php
        '''

    def last(n=0):  # @NoSelf
        '''
        :term:`Slice` off `n` things from the **tail** end of incoming things
        or just the **last** incoming thing.

        :keyword int n: number of incoming things

        :rtype: :obj:`knife` :term:`object`

        >>> # default behavior
        >>> __(5, 4, 3, 2, 1).last().get()
        1
        >>> # fetch last two things
        >>> __(5, 4, 3, 2, 1).last(2).get()
        [2, 1]

        .. seealso::

          `last <http://documentcloud.github.com/underscore/#last>`_
            Underscore.js

          `last <http://mirven.github.com/underscore.lua/#last>`_
            Underscore.lua

          `last <http://vti.github.com/underscore-perl/#last>`_
            Underscore.perl

          `last <http://brianhaveri.github.com/Underscore.php/#last>`_
            Underscore.php
        '''

    def rest():  # @NoSelf
        '''
        :term:`Slice` off every incoming thing except the **first** incoming
        thing.

        :rtype: :mod:`knife` :term:`object`

        >>> __(5, 4, 3, 2, 1).rest().get()
        [4, 3, 2, 1]

        .. seealso::

          `rest <http://documentcloud.github.com/underscore/#rest>`_
            Underscore.js

          `rest <http://mirven.github.com/underscore.lua/#rest>`_
            Underscore.lua

          `rest <http://vti.github.com/underscore-perl/#rest>`_
            Underscore.perl

          `rest <http://brianhaveri.github.com/Underscore.php/#rest>`_
            Underscore.php
        '''

    def sample(n):  # @NoSelf
        '''
        Randomly :term:`slice` off `n` incoming things.

        :argument int n: sample size

        :rtype: :mod:`knife` :term:`object`

        >>> __(1, 2, 3, 4, 5, 6).sample(3).get() # doctest: +SKIP
        [2, 4, 5]

        .. seealso::

          :func:`random.sample`
            Python standard library
        '''

    def slice(start, stop=False, step=False):  # @NoSelf
        '''
        Take :term:`slice` out of incoming things.

        :argument int start: starting index of slice

        :keyword int stop: stopping index of slice

        :keyword int step: size of step in slice

        :rtype: :mod:`knife` :term:`object`

        >>> # slice from index 0 to 3
        >>> __(5, 4, 3, 2, 1).slice(2).get()
        [5, 4]
        >>> # slice from index 2 to 4
        >>> __(5, 4, 3, 2, 1).slice(2, 4).get()
        [3, 2]
        >>> # slice from index 2 to 4 with 2 steps
        >>> __(5, 4, 3, 2, 1).slice(2, 4, 2).get()
        3

        .. seealso::

          :func:`itertools.islice`
            Python standard library

          `slice <http://mirven.github.com/underscore.lua/#slice>`_
            Underscore.lua
        '''
