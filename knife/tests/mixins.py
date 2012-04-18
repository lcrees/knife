# -*- coding: utf-8 -*-
'''ordering test mixins'''


class stooges: #@IgnorePep8
    name = 'moe'
    age = 40
class stoog2: #@IgnorePep8
    name = 'larry'
    age = 50
class stoog3: #@IgnorePep8
    name = 'curly'
    age = 60
    class stoog4: #@IgnorePep8
        name = 'beastly'
        age = 969


class MathMixin(object):

    def test_average(self):
        self.assertEqual(
            self.mclass(10, 40, 45).average().fetch(), 31.666666666666668,
        )

    def test_count(self):
        common = self.mclass(11, 3, 5, 11, 7, 3, 11).count().fetch()
        self.assertEqual(common[2], [(11, 3), (3, 2), (5, 1), (7, 1)])
        # most common
        self.assertEqual(common[1], 11)
        # least common
        self.assertEqual(common[0], 7)

    def test_max(self):
        from stuf import stuf
        stooges = [
            stuf(name='moe', age=40),
            stuf(name='larry', age=50),
            stuf(name='curly', age=60),
        ]
        self.assertEqual(self.mclass(1, 2, 4).max().fetch(), 4)
        self.assertEqual(
            stuf(self.mclass(*stooges).worker(lambda x: x.age).max().fetch()),
            stuf(name='curly', age=60),
        )

    def test_median(self):
        self.assertEqual(self.mclass(4, 5, 7, 2, 1).median().fetch(), 4)
        self.assertEqual(self.mclass(4, 5, 7, 2, 1, 8).median().fetch(), 4.5)

    def test_min(self):
        self.assertEqual(self.mclass(10, 5, 100, 2, 1000).min().fetch(), 2)
        self.assertEqual(
            self.mclass(10, 5, 100, 2, 1000).worker(lambda x: x).min().fetch(),
            2,
        )

    def test_minmax(self):
        self.assertEqual(self.mclass(1, 2, 4).minmax().fetch(), (1, 4))
        self.assertEqual(
            self.mclass(10, 5, 100, 2, 1000).minmax().fetch(), (2, 1000),
        )

    def test_combo(self):
        test = self.mclass(10, 5, 100, 2, 1000).minmax().merge().min().fetch()
        self.assertEqual(test, 2, test)
        test = self.mclass(10, 5, 100, 2, 1000).minmax().merge().max().fetch()
        self.assertEqual(test, 1000, test)
        test = self.mclass(10, 5, 100, 2, 1000).minmax().merge().sum().fetch()
        self.assertEqual(test, 1002, test)

    def test_range(self):
        self.assertEqual(self.mclass(3, 5, 7, 3, 11).range().fetch(), 8)

    def test_sum(self):
        self.assertEqual(self.mclass(1, 2, 3).sum().fetch(), 6)
        self.assertEqual(self.mclass(1, 2, 3).sum(1).fetch(), 7)
        self.assertEqual(
            self.mclass(
                .1, .1, .1, .1, .1, .1, .1, .1, .1, .1
            ).sum(precision=True).fetch(),
            1.0,
        )


class CompareMixin(object):

    def test_all(self):
        self.assertFalse(
            self.mclass(True, 1, None, 'yes').worker(bool).all().fetch()
        )

    def test_any(self):
        self.assertTrue(
            self.mclass(None, 0, 'yes', False).worker(bool).any().fetch()
        )

    def test_difference(self):
        self.assertEqual(
            self.mclass([1, 2, 3, 4, 5], [5, 2, 10]).difference().fetch(),
            [1, 3, 4],
        )
        self.assertEqual(
            self.mclass([1, 2, 3, 4, 5], [5, 2, 10]).difference(True).fetch(),
            [1, 3, 4, 10]
        )

    def test_disjointed(self):
        self.assertTrue(
            self.mclass([1, 2, 3], [5, 4, 10]).disjointed().fetch()
        )

    def test_intersection(self):
        self.assertEqual(
            self.mclass(
                [1, 2, 3], [101, 2, 1, 10], [2, 1]
            ).intersection().fetch(), [1, 2],
        )

    def test_subset(self):
        self.assertTrue(
            self.mclass([1, 2, 3], [101, 2, 1, 3]).subset().fetch(),
        )

    def test_superset(self):
        self.assertTrue(
            self.mclass([101, 2, 1, 3, 6, 34], [1, 2, 3]).superset().fetch()
        )

    def test_union(self):
        self.assertEqual(
            self.mclass([1, 2, 3], [101, 2, 1, 10], [2, 1]).union().fetch(),
            [1, 10, 3, 2, 101],
        )

    def test_unique(self):
        self.assertEqual(
            self.mclass(1, 2, 1, 3, 1, 4).unique().fetch(), [1, 2, 3, 4],
        )
        self.assertEqual(
            self.mclass(1, 2, 1, 3, 1, 4).worker(round).unique().fetch(),
            [1, 2, 3, 4],
        )


class OrderMixin(object):

    def test_shuffle(self):
        self.assertEqual(
            len(self.mclass(1, 2, 3, 4, 5, 6).shuffle()),
            len([5, 4, 6, 3, 1, 2]),
        )

    def test_group(self,):
        from math import floor
        self.assertEqual(
            self.mclass(1.3, 2.1, 2.4).worker(floor).group().fetch(),
            [(1.0, (1.3,)), (2.0, (2.1, 2.4))]
        )
        self.assertEqual(
            self.mclass(1.3, 2.1, 2.4).group().fetch(),
            [(1.3, (1.3,)), (2.1, (2.1,)), (2.4, (2.4,))],
        )

    def test_reverse(self):
        self.assertEqual(
            self.mclass(5, 4, 3, 2, 1).reverse().fetch(), [1, 2, 3, 4, 5],
        )

    def test_sort(self):
        from math import sin
        self.assertEqual(
            self.mclass(1, 2, 3, 4, 5, 6).worker(sin).sort().fetch(),
            [5, 4, 6, 3, 1, 2],
        )
        self.assertEqual(
            self.mclass(4, 6, 65, 3, 63, 2, 4).sort().fetch(),
            [2, 3, 4, 4, 6, 63, 65],
        )


class FilterMixin(object):

    def test_pattern(self):
        self.assertEqual(
            self.mclass(
                'This is the first test',
                'This is the second test',
                'This is the third test',
            ).pattern('{} first {}').filter().fetch(),
            'This is the first test'
        )
        self.assertEqual(
            self.mclass(
                'This is the first test',
                'This is the second test',
                'This is the third test',
            ).pattern(
                '. third .', type='regex'
            ).filter().fetch(), 'This is the third test'
        )
        self.assertEqual(
            self.mclass(
                'This is the first test',
                'This is the second test',
                'This is the third test',
            ).pattern(
                '*second*', type='glob'
            ).filter().fetch(), 'This is the second test'
        )

    def test_traverse(self):
        from knife._compat import ChainMap, OrderedDict
        fetch = self.mclass(stooges, stoog2, stoog3).traverse().fetch()
        self.assertEqual(
            fetch,
            [ChainMap(OrderedDict([
                ('classname', 'stooges'), ('age', 40), ('name', 'moe'),
            ])),
            ChainMap(OrderedDict([
                ('classname', 'stoog2'), ('age', 50), ('name', 'larry'),
            ])),
            ChainMap(
                OrderedDict([
                    ('classname', 'stoog3'), ('age', 60), ('name', 'curly'),
                ]),
                OrderedDict([
                    ('classname', 'stoog4'), ('age', 969), ('name', 'beastly'),
                ])
            )],
        )
        def test(x): #@IgnorePep8
            if x[0] == 'name':
                return True
            elif x[0].startswith('__'):
                return True
            return False
        self.assertEqual(
            self.mclass(
                stooges, stoog2, stoog3
            ).worker(test).traverse(True).fetch(),
            [ChainMap(OrderedDict([('classname', 'stooges'), ('age', 40)])),
            ChainMap(OrderedDict([('classname', 'stoog2'), ('age', 50)])),
            ChainMap(
                OrderedDict([('classname', 'stoog3'), ('age', 60)]),
                OrderedDict([('classname', 'stoog4'), ('age', 969)])
            )],
        )

    def test_attributes(self):
        from stuf import stuf
        stooges = [
            stuf(name='moe', age=40),
            stuf(name='larry', age=50),
            stuf(name='curly', age=60)
        ]
        self.assertEqual(
            self.mclass(*stooges).attributes('name').fetch(),
            ['moe', 'larry', 'curly'],
        )
        self.assertEqual(
            self.mclass(*stooges).attributes('name', 'age').fetch(),
            [('moe', 40), ('larry', 50), ('curly', 60)],
        )
        self.assertEqual(
            self.mclass(*stooges).attributes('place').fetch(), [],
        )

    def test_items(self):
        from stuf import stuf
        stooges = [
            stuf(name='moe', age=40),
            stuf(name='larry', age=50),
            stuf(name='curly', age=60)
        ]
        self.assertEqual(
            self.mclass(*stooges).items('name').fetch(),
            ['moe', 'larry', 'curly'],
        )
        self.assertEqual(
            self.mclass(*stooges).items('name', 'age').fetch(),
            [('moe', 40), ('larry', 50), ('curly', 60)],
        )
        stooges = [['moe', 40], ['larry', 50], ['curly', 60]]
        self.assertEqual(
            self.mclass(*stooges).items(0).fetch(), ['moe', 'larry', 'curly'],
        )
        self.assertEqual(self.mclass(*stooges).items(1).fetch(), [40, 50, 60])
        self.assertEqual(self.mclass(*stooges).items('place').fetch(), [])

    def test_mapping(self):
        self.assertEqual(
            self.mclass(
                dict([(1, 2), (2, 3), (3, 4)]), dict([(1, 2), (2, 3), (3, 4)])
            ).mapping(True).fetch(), [1, 2, 3, 1, 2, 3],
        )
        self.assertEqual(
            self.mclass(
                dict([(1, 2), (2, 3), (3, 4)]), dict([(1, 2), (2, 3), (3, 4)])
            ).mapping(values=True).fetch(),
            [2, 3, 4, 2, 3, 4],
        )
        self.assertEqual(
            self.mclass(
                dict([(1, 2), (2, 3), (3, 4)]), dict([(1, 2), (2, 3), (3, 4)])
            ).worker(lambda x, y: x * y).mapping().fetch(),
            [2, 6, 12, 2, 6, 12],
        )

    def test_filter(self):
        self.assertEqual(
            self.mclass(1, 2, 3, 4, 5, 6).worker(
                lambda x: x % 2 == 0
            ).filter(invert=True).fetch(), [1, 3, 5]
        )
        self.assertEqual(
            self.mclass(1, 2, 3, 4, 5, 6).worker(
                lambda x: x % 2 == 0
            ).filter().fetch(), [2, 4, 6]
        )

    def test_duality(self):
        self.assertEqual(
            self.mclass(1, 2, 3, 4, 5, 6).worker(
                lambda x: x % 2 == 0
            ).duality().fetch(),
            ([2, 4, 6], [1, 3, 5])
        )


class SliceMixin(object):

    def test_dice(self):
        self.assertEqual(
            self.mclass(
                'moe', 'larry', 'curly', 30, 40, 50, True
            ).dice(2, 'x').fetch(),
            [('moe', 'larry'), ('curly', 30), (40, 50), (True, 'x')]
        )

    def test_first(self):
        self.assertEqual(self.mclass(5, 4, 3, 2, 1).first().fetch(), 5)
        self.assertEqual(self.mclass(5, 4, 3, 2, 1).first(2).fetch(), [5, 4])

    def test_index(self):
        self.assertEqual(self.mclass(5, 4, 3, 2, 1).at(2).fetch(), 3)
        self.assertEqual(self.mclass(5, 4, 3, 2, 1).at(10, 11).fetch(), 11)

    def test_slice(self):
        self.assertEqual(self.mclass(5, 4, 3, 2, 1).slice(2).fetch(), [5, 4])
        self.assertEqual(
            self.mclass(5, 4, 3, 2, 1).slice(2, 4).fetch(), [3, 2]
        )
        self.assertEqual(
            self.mclass(5, 4, 3, 2, 1).slice(2, 4, 2).fetch(), 3
        )

    def test_last(self):
        self.assertEqual(self.mclass(5, 4, 3, 2, 1).last().fetch(), 1)
        self.assertEqual(self.mclass(5, 4, 3, 2, 1).last(2).fetch(), [2, 1])

    def test_initial(self):
        self.assertEqual(
            self.mclass(5, 4, 3, 2, 1).initial().fetch(), [5, 4, 3, 2]
        )

    def test_rest(self):
        self.assertEqual(
            self.mclass(5, 4, 3, 2, 1).rest().fetch(), [4, 3, 2, 1],
        )

    def test_choice(self):
        self.assertEqual(
            len(list(self.mclass(1, 2, 3, 4, 5, 6).choice())), 1,
        )

    def test_sample(self):
        self.assertEqual(
            len(self.mclass(1, 2, 3, 4, 5, 6).sample(3).fetch()), 3,
        )


class ReduceMixin(object):

    def test_flatten(self):
        self.assertEqual(
            self.mclass([[1, [2], [3, [[4]]]], 'here']).flatten().fetch(),
            [1, 2, 3, 4, 'here'],
        )

    def test_merge(self):
        self.assertEqual(
            self.mclass(
                ['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False]
            ).merge().fetch(),
            ['moe', 'larry', 'curly', 30, 40, 50, True, False, False],
        )

    def test_reduce(self):
        self.assertEqual(
            self.mclass(1, 2, 3).worker(lambda x, y: x + y).reduce().fetch(),
            6,
        )
        self.assertEqual(
            self.mclass(1, 2, 3).worker(lambda x, y: x + y).reduce(1).fetch(),
            7,
        )
        self.assertEqual(
            self.mclass([0, 1], [2, 3], [4, 5]).worker(
                lambda x, y: x + y
            ).reduce(reverse=True).fetch(), [4, 5, 2, 3, 0, 1],
        )
        self.assertEqual(
            self.mclass([0, 1], [2, 3], [4, 5]).worker(
                lambda x, y: x + y
            ).reduce([0, 0], True).fetch(), [4, 5, 2, 3, 0, 1, 0, 0],
        )

    def test_weave(self):
        self.assertEqual(
            self.mclass(
                ['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False]
            ).weave().fetch(),
            ['moe', 30, True, 'larry', 40, False, 'curly', 50, False],
        )

    def test_zip(self):
        # auto
        self.assertEqual(
            self.mclass(
                ['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False]
            ).zip().fetch(),
            [('moe', 30, True), ('larry', 40, False), ('curly', 50, False)],
        )


class RepeatMixin(object):

    def test_repeat(self):
        def test(*args): #@IgnorePep8
            return list(args)
        self.assertEqual(
            self.mclass(40, 50, 60).repeat(3).fetch(),
            [(40, 50, 60), (40, 50, 60), (40, 50, 60)],
        )
        self.assertEqual(
            self.mclass(40, 50, 60).worker(test).repeat(3, True).fetch(),
            [[40, 50, 60], [40, 50, 60], [40, 50, 60]],
        )

    def test_copy(self):
        testlist = [[1, [2, 3]], [4, [5, 6]]]
        newlist = self.mclass(testlist).copy().fetch()
        self.assertFalse(newlist is testlist)
        self.assertListEqual(newlist, testlist)
        self.assertFalse(newlist[0] is testlist[0])
        self.assertListEqual(newlist[0], testlist[0])
        self.assertFalse(newlist[1] is testlist[1])
        self.assertListEqual(newlist[1], testlist[1])

    def test_permutations(self):
        self.assertEqual(
            self.mclass(40, 50, 60).permutations(2).fetch(),
            [(40, 50), (40, 60), (50, 40), (50, 60), (60, 40), (60, 50)],
        )

    def test_combination(self):
        self.assertEqual(
            self.mclass(40, 50, 60).combinations(2).fetch(),
            [(40, 50), (40, 60), (50, 60)],
        )


class MapMixin(object):

    def test_factory(self):
        from stuf import stuf
        thing = self.mclass(
            [('a', 1), ('b', 2), ('c', 3)], [('a', 1), ('b', 2), ('c', 3)]
        ).worker(stuf).map().fetch()
        self.assertEqual(
            thing, [stuf(a=1, b=2, c=3), stuf(a=1, b=2, c=3)]
        )

    def test_kwargmap(self):
        def test(*args, **kw):
            return sum(args) * sum(kw.values())
        self.assertEqual(
            self.mclass(
                ((1, 2), {'a': 2}), ((2, 3), {'a': 2}), ((3, 4), {'a': 2})
            ).worker(test).kwargmap().fetch(),
            [6, 10, 14],
        )
        self.assertEqual(
            self.mclass(
                ((1, 2), {'a': 2}), ((2, 3), {'a': 2}), ((3, 4), {'a': 2})
            ).worker(test).params(
                1, 2, 3, b=5, w=10, y=13
            ).kwargmap(True).fetch(),
            [270, 330, 390],
        )

    def test_argmap(self):
        self.assertEqual(
            self.mclass(
                (1, 2), (2, 3), (3, 4)
            ).worker(lambda x, y: x * y).argmap().fetch(),
            [2, 6, 12],
        )
        self.assertEqual(
            self.mclass((1, 2), (2, 3), (3, 4)).worker(
                lambda x, y, z, a, b: x * y * z * a * b
            ).params(7, 8, 9).argmap(True).fetch(),
            [1008, 3024, 6048],
        )

    def test_map(self):
        self.assertEqual(
            self.mclass(1, 2, 3).worker(lambda x: x * 3).map().fetch(),
            [3, 6, 9],
        )

    def test_invoke(self):
        self.assertEqual(
            self.mclass(
                [5, 1, 7], [3, 2, 1]
            ).params(1).invoke('index').fetch(),
            [1, 2],
        )
        self.assertEqual(
            self.mclass([5, 1, 7], [3, 2, 1]).invoke('sort').fetch(),
            [[1, 5, 7], [1, 2, 3]],
        )


class Mixin(object):

    def test_repr(self):
        from stuf.six import strings
        self.assertIsInstance(
            self.mclass([1, 2, 3, 4, 5, 6]).__repr__(), strings,
        )

    def test_append(self):
        self.assertEqual(self.mclass().append('foo').peek(), 'foo')
        self.assertListEqual(
            self.mclass().append(1, 2, 3, 4, 5, 6).peek(),
            [1, 2, 3, 4, 5, 6],
        )

    def test_prepend(self):
        self.assertEqual(self.mclass().prepend('foo').peek(), 'foo')
        self.assertListEqual(
            self.mclass().prepend(1, 2, 3, 4, 5, 6).peek(), [6, 5, 4, 3, 2, 1]
        )

    def test_undo(self):
        queue = self.mclass(1, 2, 3).prepend(1, 2, 3, 4, 5, 6)
        self.assertEqual(queue.peek(), [6, 5, 4, 3, 2, 1, 1, 2, 3])
        queue.append(1).undo()
        self.assertEqual(queue.peek(), [6, 5, 4, 3, 2, 1, 1, 2, 3])
        queue.append(1).append(2).undo()
        self.assertEqual(queue.peek(), [6, 5, 4, 3, 2, 1, 1, 2, 3, 1])
        queue.append(1).append(2).undo(2)
        self.assertEqual(queue.peek(), [6, 5, 4, 3, 2, 1, 1, 2, 3, 1])
        queue.snapshot().append(1).append(2).stepback()
        self.assertEqual(queue.peek(), [6, 5, 4, 3, 2, 1, 1, 2, 3, 1])
        queue.original()
        self.assertEqual(queue.peek(), [1, 2, 3])

    def test_wrap(self):
        self.assertIsInstance(
            self.mclass(1, 2, 3, 4, 5, 6).as_type(tuple).peek(), tuple,
        )
        self.assertTupleEqual(
            self.mclass(1, 2, 3, 4, 5, 6).as_type(tuple).peek(),
            (1, 2, 3, 4, 5, 6),
        )

    def test_list(self):
        self.assertIsInstance(
            self.mclass(1, 2, 3, 4, 5, 6).as_list().peek(), list,
        )
        self.assertListEqual(
            self.mclass(1, 2, 3, 4, 5, 6).as_list().peek(),
            [1, 2, 3, 4, 5, 6],
        )

    def test_tuple(self):
        self.assertIsInstance(
            self.mclass(1, 2, 3, 4, 5, 6).as_tuple().peek(), tuple,
        )
        self.assertTupleEqual(
            self.mclass(1, 2, 3, 4, 5, 6).as_tuple().peek(),
            (1, 2, 3, 4, 5, 6),
        )

    def test_set(self):
        self.assertIsInstance(
            self.mclass(1, 2, 3, 4, 5, 6).as_set().peek(), set,
        )
        self.assertSetEqual(
            self.mclass(1, 2, 3, 4, 5, 6).as_set().peek(),
            set([1, 2, 3, 4, 5, 6]),
        )

    def test_dict(self):
        self.assertIsInstance(
            self.mclass((1, 2), (3, 4), (5, 6)).as_dict().peek(), dict,
        )
        self.assertDictEqual(
            self.mclass((1, 2), (3, 4), (5, 6)).as_dict().peek(),
            {1: 2, 3: 4, 5: 6},
        )

    def test_ascii(self):
        from stuf.six import u, b
        self.assertEqual(
            self.mclass(
                [1], True, r't', b('i'), u('g'), None, (1,)
            ).as_ascii().cast_each().peek(),
            (b('[1]'), b('True'), b('t'), b('i'), b('g'), b('None'), b('(1,)'))
        )

    def test_bytes(self):
        from stuf.six import u, b
        self.assertEqual(
            self.mclass(
                [1], True, r't', b('i'), u('g'), None, (1,)
            ).as_bytes().cast_each().peek(),
            (b('[1]'), b('True'), b('t'), b('i'), b('g'), b('None'), b('(1,)'))
        )

    def test_unicode(self):
        from stuf.six import u, b
        self.assertEqual(
            self.mclass(
                [1], True, r't', b('i'), u('g'), None, (1,)
            ).as_unicode().cast_each().peek(),
            (u('[1]'), u('True'), u('t'), u('i'), u('g'), u('None'), u('(1,)'))
        )
