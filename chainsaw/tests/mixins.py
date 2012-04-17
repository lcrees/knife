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

    def test_max(self):
        # auto
        from stuf import stuf
        stooges = [
            stuf(name='moe', age=40),
            stuf(name='larry', age=50),
            stuf(name='curly', age=60),
        ]
        test = self.mclass(1, 2, 4)
        self.assertEqual(test.as_query().as_auto().max().read(), 4)
        self.assertEqual(test.as_edit().as_auto().max().close(), 4)
        test = self.mclass(*stooges)
        self.assertEqual(
            stuf(test.as_query().as_auto().tap(
                lambda x: x.age
            ).max().untap().read()),
            stuf(name='curly', age=60),
        )
        self.assertEqual(
            stuf(test.as_edit().as_auto().tap(
                lambda x: x.age
            ).max().untap().close()),
            stuf(name='curly', age=60),
        )
        # man
        self._false_true_false(
            self.mclass(1, 2, 4).as_query().as_manual().max(),
            self.assertEqual,
            4,
        )
        self._false_true_false(
            self.mclass(*stooges).as_edit().as_manual().tap(
                lambda x: x.age
            ).max().untap(),
            self.assertEqual,
            stuf(name='curly', age=60)
        )

    def test_min(self):
        # auto
        self.assertEqual(
            self.mclass(10, 5, 100, 2, 1000).as_edit().as_auto().min().close(),
            2,
        )
        self.assertEqual(
            self.mclass(10, 5, 100, 2, 1000).as_edit().as_auto().tap(
                lambda x: x
            ).min().close(), 2,
        )
        # man
        self._false_true_false(
            self.mclass(10, 5, 100, 2, 1000).as_edit().as_manual().min(),
            self.assertEqual,
            2,
        )
        self._false_true_false(
            self.mclass(10, 5, 100, 2, 1000).as_edit().as_manual().tap(
                lambda x: x
            ).min(),
            self.assertEqual,
            2,
        )

    def test_minmax(self):
        # auto
        self.assertEqual(
            self.mclass(1, 2, 4).as_edit().as_auto().minmax().close(), (1, 4)
        )
        self.assertEqual(
            self.mclass(
                10, 5, 100, 2, 1000
            ).as_edit().as_auto().minmax().close(),
            (2, 1000),
        )
        # man
        self._false_true_false(
            self.mclass(1, 2, 4).as_edit().as_manual().minmax(),
            self.assertEqual,
            (1, 4),
        )
        self._false_true_false(
            self.mclass(10, 5, 100, 2, 1000).as_edit().as_manual().minmax(),
            self.assertEqual,
            (2, 1000),
        )

    def test_sum(self):
        # auto
        self.assertEqual(
            self.mclass(1, 2, 3).as_edit().as_auto().sum().close(), 6
        )
        self.assertEqual(
            self.mclass(1, 2, 3).as_edit().as_auto().sum(1).close(), 7
        )
        self.assertEqual(
            self.mclass(
                .1, .1, .1, .1, .1, .1, .1, .1, .1, .1
            ).as_edit().as_auto().sum(precision=True).close(),
            1.0,
        )
        # man
        self._false_true_false(
            self.mclass(1, 2, 3).as_edit().as_manual().sum(), self.assertEqual,
            6,
        )
        self._false_true_false(
            self.mclass(1, 2, 3).as_edit().as_manual().sum(1),
            self.assertEqual,
            7,
        )
        self._false_true_false(
            self.mclass(
                .1, .1, .1, .1, .1, .1, .1, .1, .1, .1
            ).as_edit().as_manual().sum(precision=True),
            self.assertEqual,
            1.0,
        )

    def test_median(self):
        # auto
        self.assertEqual(
            self.mclass(4, 5, 7, 2, 1).as_edit().as_auto().median().close(), 4,
        )
        self.assertEqual(
            self.mclass(4, 5, 7, 2, 1, 8).as_edit().as_auto().median().close(),
            4.5,
        )
        # man
        self._false_true_false(
            self.mclass(4, 5, 7, 2, 1).as_edit().as_manual().median(),
            self.assertEqual,
            4,
        )
        self._false_true_false(
            self.mclass(4, 5, 7, 2, 1, 8).as_edit().as_manual().median(),
            self.assertEqual,
            4.5,
        )

    def test_average(self):
        # auto
        self.assertEqual(
            self.mclass(10, 40, 45).as_edit().as_auto().average().close(),
            31.666666666666668,
        )
        # man
        self._false_true_false(
            self.mclass(10, 40, 45).as_edit().as_manual().average(),
            self.assertEqual,
            31.666666666666668,
        )

    def test_range(self):
        # auto
        self.assertEqual(
            self.mclass(3, 5, 7, 3, 11).as_edit().as_auto().range().close(), 8,
        )
        # man
        self._false_true_false(
            self.mclass(3, 5, 7, 3, 11).as_edit().as_manual().range(),
            self.assertEqual,
            8,
        )

    def test_count(self):
        # auto
        common = self.mclass(
            11, 3, 5, 11, 7, 3, 11
        ).as_edit().as_auto().count().close()
        self.assertEqual(common[2], [(11, 3), (3, 2), (5, 1), (7, 1)])
        # most common
        self.assertEqual(common[1], 11)
        # least common
        self.assertEqual(common[0], 7)
        # man
        self._false_true_false(
            self.mclass(11, 3, 5, 11, 7, 3, 11).as_edit().as_manual().count(),
            self.assertEqual,
            (7, 11, [(11, 3), (3, 2), (5, 1), (7, 1)]),
        )


class CompareMixin(object):

    def test_all(self):
        # auto
        self.assertFalse(
            self.mclass(
                True, 1, None, 'yes'
            ).as_edit().as_auto().tap(bool).all().close()
        )
        # man
        self._false_true_false(
            self.mclass(
                True, 1, None, 'yes'
            ).as_edit().as_manual().tap(bool).all(),
            self.assertFalse,
        )

    def test_any(self):
        # auto
        self.assertTrue(
            self.mclass(
                None, 0, 'yes', False
            ).as_edit().as_auto().tap(bool).any().close()
        )
        # man
        self._false_true_false(
            self.mclass(
                None, 0, 'yes', False
            ).as_edit().as_manual().tap(bool).any(),
            self.assertTrue,
        )

    def test_difference(self):
        # auto
        self.assertEqual(
            self.mclass(
                [1, 2, 3, 4, 5], [5, 2, 10]
            ).as_edit().as_auto().difference().close(),
            [1, 3, 4],
        )
        self.assertEqual(
            self.mclass(
                [1, 2, 3, 4, 5], [5, 2, 10]
            ).as_edit().as_auto().difference(True).close(),
            [1, 3, 4, 10]
        )
        # man
        self._false_true_false(
            self.mclass(
                [1, 2, 3, 4, 5], [5, 2, 10]
            ).as_edit().as_manual().difference(),
            self.assertEqual,
            [1, 3, 4]
        )
        self._false_true_false(
            self.mclass(
                [1, 2, 3, 4, 5], [5, 2, 10]
                ).as_edit().as_manual().difference(True),
            self.assertEqual,
            [1, 3, 4, 10]
        )

    def test_disjointed(self):
        # auto
        self.assertTrue(
            self.mclass(
                [1, 2, 3], [5, 4, 10]
            ).as_edit().as_auto().disjointed().close()
        )
        self.assertFalse(
            self.mclass(
                [1, 2, 3], [5, 2, 10]
            ).as_edit().as_auto().disjointed().close()
        )
        # man
        self._false_true_false(
            self.mclass(
                [1, 2, 3], [5, 4, 10]
            ).as_edit().as_manual().disjointed(),
            self.assertTrue,
        )
        self._false_true_false(
            self.mclass(
                [1, 2, 3], [5, 2, 10]
            ).as_edit().as_manual().disjointed(),
            self.assertFalse,
        )

    def test_intersection(self):
        # auto
        self.assertEqual(
            self.mclass(
                [1, 2, 3], [101, 2, 1, 10], [2, 1]
            ).as_edit().as_auto().intersection().close(), [1, 2],
        )
        # man
        self._false_true_false(
            self.mclass(
                [1, 2, 3], [101, 2, 1, 10], [2, 1]
            ).as_edit().as_manual().intersection(),
            self.assertEqual,
            [1, 2],
        )

    def test_subset(self):
        # auto
        self.assertTrue(
            self.mclass(
                [1, 2, 3], [101, 2, 1, 3]
            ).as_edit().as_auto().subset().close(),
        )
        # man
        self._false_true_false(
            self.mclass(
                [1, 2, 3], [101, 2, 1, 3]
            ).as_edit().as_manual().subset(),
            self.assertTrue,
        )

    def test_superset(self):
        # auto
        diff = self.mclass(
            [101, 2, 1, 3, 6, 34], [1, 2, 3]
        ).as_edit().as_auto().superset().close()
        self.assertTrue(diff)
        # man
        self._false_true_false(
            self.mclass(
                [101, 2, 1, 3, 6, 34], [1, 2, 3]
            ).as_edit().as_manual().superset(),
            self.assertTrue,
        )

    def test_union(self):
        # auto
        self.assertEqual(
            self.mclass(
                [1, 2, 3], [101, 2, 1, 10], [2, 1]
            ).as_edit().as_auto().union().close(),
            [1, 10, 3, 2, 101],
        )
        # man
        self._false_true_false(
            self.mclass(
                [1, 2, 3], [101, 2, 1, 10], [2, 1]
            ).as_edit().as_manual().union(),
            self.assertEqual,
            [1, 10, 3, 2, 101],
        )

    def test_unique(self):
        # auto
        self.assertEqual(
            self.mclass(
                1, 2, 1, 3, 1, 4
            ).as_edit().as_auto().unique().close(), [1, 2, 3, 4],
        )
        self.assertEqual(
            self.mclass(
                1, 2, 1, 3, 1, 4
            ).as_edit().as_auto().tap(round).unique().close(),
            [1, 2, 3, 4],
        )
        # man
        self._false_true_false(
            self.mclass(1, 2, 1, 3, 1, 4).as_edit().as_manual().unique(),
            self.assertEqual,
            [1, 2, 3, 4],
        )
        self._false_true_false(
            self.mclass(
                1, 2, 1, 3, 1, 4
            ).as_edit().as_manual().tap(round).unique(),
            self.assertEqual,
            [1, 2, 3, 4],
        )


class OrderMixin(object):

    def test_shuffle(self):
        # auto
        self.assertEqual(
            len(self.mclass(1, 2, 3, 4, 5, 6).as_edit().as_auto().shuffle()),
            len([5, 4, 6, 3, 1, 2]),
        )
        # man
        manchainsaw = self.mclass(
            1, 2, 3, 4, 5, 6
        ).as_edit().as_manual().shuffle()
        self.assertFalse(manchainsaw.balanced)
        manchainsaw.out_in()
        self.assertTrue(manchainsaw.balanced)
        manchainsaw.close()
        self.assertTrue(manchainsaw.balanced)

    def test_group(self,):
        # auto
        from math import floor
        self.assertEqual(
            self.mclass(
                1.3, 2.1, 2.4
            ).as_edit().as_auto().tap(lambda x: floor(x)).group().close(),
            [(1.0, (1.3,)), (2.0, (2.1, 2.4))]
        )
        self.assertEqual(
            self.mclass(1.3, 2.1, 2.4).as_edit().as_auto().group().close(),
            [(1.3, (1.3,)), (2.1, (2.1,)), (2.4, (2.4,))],
        )
        # man
        self._false_true_false(
            self.mclass(1.3, 2.1, 2.4).as_edit().as_manual().tap(
                lambda x: floor(x)
            ).group(),
            self.assertListEqual,
            [(1.0, (1.3,)), (2.0, (2.1, 2.4))]
        )
        self._true_true_false(
            self.mclass(1.3, 2.1, 2.4).as_edit().as_manual().group(),
            self.assertListEqual,
            [(1.3, (1.3,)), (2.1, (2.1,)), (2.4, (2.4,))],
        )

    def test_reverse(self):
        # auto
        self.assertEqual(
            self.mclass(5, 4, 3, 2, 1).as_edit().as_auto().reverse().close(),
            [1, 2, 3, 4, 5],
        )
        # man
        self._false_true_false(
            self.mclass(5, 4, 3, 2, 1).as_edit().as_manual().reverse(),
            self.assertEqual,
            [1, 2, 3, 4, 5],
        )

    def test_sort(self):
        from math import sin
        # auto
        self.assertEqual(
            self.mclass(1, 2, 3, 4, 5, 6).as_edit().as_auto().tap(
                lambda x: sin(x)
            ).sort().close(),
            [5, 4, 6, 3, 1, 2],
        )
        self.assertEqual(
            self.mclass(
                4, 6, 65, 3, 63, 2, 4
            ).as_edit().as_auto().sort().close(),
            [2, 3, 4, 4, 6, 63, 65],
        )
        # man
        self._false_true_false(
            self.mclass(1, 2, 3, 4, 5, 6).as_edit().as_manual().tap(
                lambda x: sin(x)
            ).sort(),
            self.assertListEqual,
            [5, 4, 6, 3, 1, 2],
        )
        self._false_true_false(
            self.mclass(4, 6, 65, 3, 63, 2, 4).as_edit().as_manual().sort(),
            self.assertListEqual,
            [2, 3, 4, 4, 6, 63, 65],
        )


class FilterMixin(object):

    def test_pattern(self):
        self.assertEqual(
            self.mclass(
                'This is the first test',
                'This is the second test',
                'This is the third test'
            ).pattern('{} first {}').filter().close(), 'This is the first test'
        )
        self.assertEqual(
            self.mclass(
                'This is the first test',
                'This is the second test',
                'This is the third test'
            ).pattern(
                '. third .', type='regex'
            ).filter().close(), 'This is the third test'
        )
        self.assertEqual(
            self.mclass(
                'This is the first test',
                'This is the second test',
                'This is the third test'
            ).pattern(
                '*second*', type='glob'
            ).filter().close(), 'This is the second test'
        )

    def test_traverse(self):
        from chainsaw._compat import ChainMap, OrderedDict
        self.maxDiff = None
        # auto
        out = self.mclass(
            stooges, stoog2, stoog3
        ).as_edit().as_auto().traverse().close()
        self.assertEqual(
            out,
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
            out,
        )
        def test(x): #@IgnorePep8
            if x[0] == 'name':
                return True
            elif x[0].startswith('__'):
                return True
            return False
        self.assertEqual(
            self.mclass(stooges, stoog2, stoog3).as_edit().as_auto().tap(
                test
            ).traverse(True).close(),
            [ChainMap(OrderedDict([('classname', 'stooges'), ('age', 40)])),
            ChainMap(OrderedDict([('classname', 'stoog2'), ('age', 50)])),
            ChainMap(
                OrderedDict([('classname', 'stoog3'), ('age', 60)]),
                OrderedDict([('classname', 'stoog4'), ('age', 969)])
            )],
            out,
        )
        # man
        self._true_true_false(
            self.mclass(
                stooges, stoog2, stoog3
            ).as_edit().as_manual().traverse(),
            self.assertEqual,
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
        self._true_true_false(
            self.mclass(stooges, stoog2, stoog3).as_edit().as_manual().tap(
                test
            ).traverse(True),
            self.assertEqual,
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
        # auto
        self.assertEqual(
            self.mclass(
                *stooges
            ).as_edit().as_auto().attributes('name').close(),
            ['moe', 'larry', 'curly'],
        )
        self.assertEqual(
            self.mclass(
                *stooges
            ).as_edit().as_auto().attributes('name', 'age').close(),
            [('moe', 40), ('larry', 50), ('curly', 60)],
        )
        self.assertEqual(
            self.mclass(
                *stooges
            ).as_edit().as_auto().attributes('place').close(), [],
        )
        # man
        self._true_true_false(
            self.mclass(*stooges).as_edit().as_manual().attributes('name'),
            self.assertEqual,
            ['moe', 'larry', 'curly'],
        )
        self._true_true_false(
            self.mclass(
                *stooges
            ).as_edit().as_manual().attributes('name', 'age'),
            self.assertEqual,
            [('moe', 40), ('larry', 50), ('curly', 60)],
        )
        self._false_true_true(
            self.mclass(*stooges).as_edit().as_manual().attributes('place'),
            self.assertEqual,
            [],
        )

    def test_items(self):
        from stuf import stuf
        stooges = [
            stuf(name='moe', age=40),
            stuf(name='larry', age=50),
            stuf(name='curly', age=60)
        ]
        # auto
        self.assertEqual(
            self.mclass(*stooges).as_edit().as_auto().items('name').close(),
            ['moe', 'larry', 'curly'],
        )
        self.assertEqual(
            self.mclass(
                *stooges
            ).as_edit().as_auto().items('name', 'age').close(),
            [('moe', 40), ('larry', 50), ('curly', 60)],
        )
        stooges = [['moe', 40], ['larry', 50], ['curly', 60]]
        self.assertEqual(
            self.mclass(*stooges).as_edit().as_auto().items(0).close(),
            ['moe', 'larry', 'curly'],
        )
        self.assertEqual(
            self.mclass(*stooges).as_edit().as_auto().items(1).close(),
            [40, 50, 60]
        )
        self.assertEqual(
            self.mclass(*stooges).as_edit().as_auto().items('place').close(),
            []
        )
        # man
        stooges = [
            stuf(name='moe', age=40),
            stuf(name='larry', age=50),
            stuf(name='curly', age=60)
        ]
        self._true_true_false(
            self.mclass(*stooges).as_edit().as_manual().items('name'),
            self.assertEqual,
            ['moe', 'larry', 'curly'],
        )
        self._true_true_false(
            self.mclass(*stooges).as_edit().as_manual().items('name', 'age'),
            self.assertEqual,
            [('moe', 40), ('larry', 50), ('curly', 60)],
        )
        stooges = [['moe', 40], ['larry', 50], ['curly', 60]]
        self._true_true_false(
            self.mclass(*stooges).as_edit().as_manual().items(0),
            self.assertEqual,
            ['moe', 'larry', 'curly'],
        )
        self._true_true_false(
            self.mclass(*stooges).as_edit().as_manual().items(1),
            self.assertEqual,
            [40, 50, 60],
        )
        self._false_true_true(
            self.mclass(*stooges).as_edit().as_manual().items('place'),
            self.assertEqual,
            [],
        )

    def test_mapping(self):
        # auto
        self.assertEqual(
            self.mclass(
                dict([(1, 2), (2, 3), (3, 4)]), dict([(1, 2), (2, 3), (3, 4)])
            ).as_edit().as_auto().mapping(True).close(), [1, 2, 3, 1, 2, 3],
        )
        self.assertEqual(
            self.mclass(
                dict([(1, 2), (2, 3), (3, 4)]), dict([(1, 2), (2, 3), (3, 4)])
            ).as_edit().as_auto().mapping(values=True).close(),
            [2, 3, 4, 2, 3, 4],
        )
        self.assertEqual(
            self.mclass(
                dict([(1, 2), (2, 3), (3, 4)]), dict([(1, 2), (2, 3), (3, 4)])
            ).as_edit().as_auto().tap(lambda x, y: x * y).mapping().close(),
            [2, 6, 12, 2, 6, 12],
        )
        # man
        self._false_true_false(
            self.mclass(
                dict([(1, 2), (2, 3), (3, 4)]), dict([(1, 2), (2, 3), (3, 4)])
            ).as_edit().as_manual().mapping(True),
            self.assertEqual,
            [1, 2, 3, 1, 2, 3],
        )
        self._false_true_false(
            self.mclass(
                dict([(1, 2), (2, 3), (3, 4)]), dict([(1, 2), (2, 3), (3, 4)])
            ).as_edit().as_manual().mapping(values=True),
            self.assertEqual,
            [2, 3, 4, 2, 3, 4],
        )
        self._false_true_false(
            self.mclass(
                dict([(1, 2), (2, 3), (3, 4)]), dict([(1, 2), (2, 3), (3, 4)])
            ).as_edit().as_manual().tap(lambda x, y: x * y).mapping(),
            self.assertEqual,
            [2, 6, 12, 2, 6, 12],
        )

    def test_filter(self):
        # auto
        self.assertEqual(
            self.mclass(1, 2, 3, 4, 5, 6).tap(
                lambda x: x % 2 == 0
            ).as_edit().as_auto().filter(invert=True).close(), [1, 3, 5]
        )
        self.assertEqual(
            self.mclass(1, 2, 3, 4, 5, 6).tap(
                lambda x: x % 2 == 0
            ).as_edit().as_auto().filter().close(), [2, 4, 6]
        )
        # man
        self._false_true_false(
            self.mclass(1, 2, 3, 4, 5, 6).as_edit().as_manual().tap(
                lambda x: x % 2 == 0
            ).filter(),
            self.assertEqual,
            [2, 4, 6],
        )
        self._false_true_false(
            self.mclass(1, 2, 3, 4, 5, 6).as_edit().as_manual().tap(
                lambda x: x % 2 == 0
            ).filter(invert=True),
            self.assertEqual,
            [1, 3, 5],
        )

    def test_duality(self):
        # auto
        self.assertEqual(
            self.mclass(1, 2, 3, 4, 5, 6).as_edit().tap(
                lambda x: x % 2 == 0
            ).as_auto().duality().close(), ([2, 4, 6], [1, 3, 5])
        )
        # man
        self._false_true_false(
            self.mclass(
                1, 2, 3, 4, 5, 6
            ).as_edit().as_auto().as_manual().tap(
                lambda x: x % 2 == 0
            ).duality(),
            self.assertEqual,
            ([2, 4, 6], [1, 3, 5]),
        )


class SliceMixin(object):

    def test_dice(self):
        # auto
        self.assertEqual(
            self.mclass(
                'moe', 'larry', 'curly', 30, 40, 50, True
            ).as_edit().as_auto().dice(2, 'x').close(),
            [('moe', 'larry'), ('curly', 30), (40, 50), (True, 'x')]
        )
        # man
        self._false_true_false(
            self.mclass(
                'moe', 'larry', 'curly', 30, 40, 50, True,
            ).as_edit().as_manual().dice(2, 'x'),
            self.assertEqual,
            [('moe', 'larry'), ('curly', 30), (40, 50), (True, 'x')],
        )

    def test_first(self):
        # auto
        self.assertEqual(
            self.mclass(5, 4, 3, 2, 1).as_edit().as_auto().first().close(), 5
        )
        self.assertEqual(
            self.mclass(5, 4, 3, 2, 1).as_edit().as_auto().first(2).close(),
            [5, 4]
        )
        # man
        self._false_true_false(
             self.mclass(5, 4, 3, 2, 1).as_edit().as_manual().first(),
             self.assertEqual,
             5,
        )
        self._false_true_false(
            self.mclass(5, 4, 3, 2, 1).as_edit().as_manual().first(2),
            self.assertEqual,
            [5, 4],
        )

    def test_index(self):
        # auto
        self.assertEqual(self.mclass(
            5, 4, 3, 2, 1
        ).as_edit().as_auto().at(2).close(), 3)
        self.assertEqual(
            self.mclass(
                5, 4, 3, 2, 1
            ).as_edit().as_auto().at(10, 11).close(), 11,
        )
        # man
        self._false_true_false(
            self.mclass(
                5, 4, 3, 2, 1
            ).as_edit().as_manual().at(2), self.assertEqual, 3,
        )
        self._false_true_false(
            self.mclass(5, 4, 3, 2, 1).as_edit().as_manual().at(10, 11),
            self.assertEqual,
            11,
        )

    def test_slice(self):
        # auto
        self.assertEqual(
            self.mclass(5, 4, 3, 2, 1).as_edit().as_auto().slice(2).close(),
            [5, 4]
        )
        self.assertEqual(
            self.mclass(5, 4, 3, 2, 1).as_edit().slice(2, 4).as_auto().close(),
            [3, 2]
        )
        self.assertEqual(
            self.mclass(
                5, 4, 3, 2, 1
            ).as_edit().as_auto().slice(2, 4, 2).close(), 3
        )
        # man
        self._false_true_false(
            self.mclass(5, 4, 3, 2, 1).as_edit().as_manual().slice(2),
            self.assertEqual,
            [5, 4],
        )
        self._false_true_false(
            self.mclass(5, 4, 3, 2, 1).as_edit().as_manual().slice(2, 4),
            self.assertEqual,
            [3, 2]
        )
        self._false_true_false(
            self.mclass(5, 4, 3, 2, 1).as_edit().as_manual().slice(2, 4, 2),
            self.assertEqual,
            3,
        )

    def test_last(self):
        # auto
        self.assertEqual(
            self.mclass(5, 4, 3, 2, 1).as_edit().as_auto().last().close(), 1
        )
        self.assertEqual(
            self.mclass(5, 4, 3, 2, 1).as_edit().as_auto().last(2).close(),
            [2, 1]
        )
        # man
        self._false_true_false(
            self.mclass(5, 4, 3, 2, 1).as_edit().as_manual().last(),
            self.assertEqual,
            1
        )
        self._false_true_false(
            self.mclass(5, 4, 3, 2).as_edit().as_manual().last(2),
            self.assertEqual,
            [3, 2],
        )

    def test_initial(self):
        # auto
        self.assertEqual(
            self.mclass(5, 4, 3, 2, 1).as_edit().initial().close(),
            [5, 4, 3, 2]
        )
        # man
        self._false_true_false(
            self.mclass(5, 4, 3, 2, 1).as_edit().as_manual().initial(),
            self.assertEqual,
            [5, 4, 3, 2],
        )

    def test_rest(self):
        # auto
        self.assertEqual(
            self.mclass(5, 4, 3, 2, 1).as_edit().as_auto().rest().close(),
            [4, 3, 2, 1],
        )
        # man
        self._false_true_false(
            self.mclass(5, 4, 3, 2, 1).as_edit().as_manual().rest(),
            self.assertEqual,
            [4, 3, 2, 1],
        )

    def test_choice(self):
        # auto
        self.assertEqual(
            len(self.mclass(
                1, 2, 3, 4, 5, 6
            ).as_edit().as_auto().choice().out_in()), 1
        )
        # man
        manchainsaw = self.mclass(
            1, 2, 3, 4, 5, 6
        ).as_edit().as_manual().choice()
        self.assertFalse(manchainsaw.balanced)
        manchainsaw.out_in()
        self.assertTrue(manchainsaw.balanced)
        manchainsaw.close()
        self.assertTrue(manchainsaw.balanced)

    def test_sample(self):
        #auto
        self.assertEqual(
            len(self.mclass(
                1, 2, 3, 4, 5, 6
            ).as_edit().as_auto().sample(3).close()), 3,
        )
        # man
        manchainsaw = self.mclass(
            1, 2, 3, 4, 5, 6
        ).as_edit().as_manual().sample(3)
        self.assertFalse(manchainsaw.balanced)
        manchainsaw.out_in()
        self.assertTrue(manchainsaw.balanced)
        manchainsaw.close()
        self.assertTrue(manchainsaw.balanced)


class ReduceMixin(object):

    def test_flatten(self):
        # auto
        self.assertEqual(
            self.mclass(
                [[1, [2], [3, [[4]]]], 'here']
            ).as_edit().as_auto().flatten().close(),
            [1, 2, 3, 4, 'here'],
        )
        # man
        self._false_true_false(
            self.mclass(
                [[1, [2], [3, [[4]]]], 'here']
            ).as_edit().as_manual().flatten(),
            self.assertEqual,
            [1, 2, 3, 4, 'here'],
        )

    def test_merge(self):
        # auto
        self.assertEqual(
            self.mclass(
                ['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False]
            ).as_edit().as_auto().merge().close(),
            ['moe', 'larry', 'curly', 30, 40, 50, True, False, False],
        )
        # man
        self._false_true_false(
            self.mclass(
                ['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False],
            ).as_edit().as_manual().merge(),
            self.assertEqual,
            ['moe', 'larry', 'curly', 30, 40, 50, True, False, False],
        )

    def test_reduce(self):
        # auto
        self.assertEqual(
            self.mclass(1, 2, 3).as_edit().as_auto().tap(
                lambda x, y: x + y
            ).reduce().close(), 6,
        )
        self.assertEqual(
            self.mclass(1, 2, 3).as_edit().as_auto().tap(
                lambda x, y: x + y
            ).reduce(1).close(), 7,
        )
        self.assertEqual(
            self.mclass([0, 1], [2, 3], [4, 5]).as_edit().as_auto().tap(
                lambda x, y: x + y
            ).reduce(reverse=True).close(), [4, 5, 2, 3, 0, 1],
        )
        self.assertEqual(
            self.mclass([0, 1], [2, 3], [4, 5]).as_edit().as_auto().tap(
                lambda x, y: x + y
            ).reduce([0, 0], True).close(), [4, 5, 2, 3, 0, 1, 0, 0],
        )
        # man
        self._false_true_false(
            self.mclass(1, 2, 3).as_edit().as_manual().tap(
                lambda x, y: x + y
            ).reduce(),
            self.assertEqual,
            6,
        )
        self._false_true_false(
            self.mclass(1, 2, 3).as_edit().as_manual().tap(
                lambda x, y: x + y
            ).reduce(1),
            self.assertEqual,
            7,
        )
        self._false_true_false(
            self.mclass([0, 1], [2, 3], [4, 5]).as_edit().tap(
                lambda x, y: x + y
            ).as_manual().reduce(reverse=True),
            self.assertEqual,
             [4, 5, 2, 3, 0, 1],
        )
        self._false_true_false(
            self.mclass([0, 1], [2, 3], [4, 5]).as_edit().tap(
                lambda x, y: x + y
            ).as_manual().reduce([0, 0], True),
            self.assertEqual,
            [4, 5, 2, 3, 0, 1, 0, 0],
        )

    def test_weave(self):
        # auto
        self.assertEqual(
            self.mclass(
                ['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False]
            ).as_edit().as_auto().as_one().weave().close(),
            ['moe', 30, True, 'larry', 40, False, 'curly', 50, False],
        )
        # man
        self._false_true_false(
            self.mclass(
                ['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False]
            ).as_edit().as_manual().as_one().weave(),
            self.assertEqual,
            ['moe', 30, True, 'larry', 40, False, 'curly', 50, False],
        )

    def test_zip(self):
        # auto
        self.assertEqual(
            self.mclass(
                ['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False]
            ).as_edit().as_auto().as_one().zip().close(),
            [('moe', 30, True), ('larry', 40, False), ('curly', 50, False)],
        )
        # man
        self._true_true_false(
            self.mclass(
                ['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False],
            ).as_edit().as_manual().as_one().zip(),
            self.assertEqual,
            [('moe', 30, True), ('larry', 40, False), ('curly', 50, False)],
        )


class RepeatMixin(object):

    def test_repeat(self):
        def test(*args): #@IgnorePep8
            return list(args)
        # auto
        self.assertEqual(
            self.mclass(40, 50, 60).as_edit().as_auto().repeat(3).close(),
            [(40, 50, 60), (40, 50, 60), (40, 50, 60)],
        )
        self.assertEqual(
            self.mclass(
                40, 50, 60
            ).as_edit().as_auto().tap(test).repeat(3, True).close(),
            [[40, 50, 60], [40, 50, 60], [40, 50, 60]],
        )
        # man
        self._true_true_false(
            self.mclass(
                40, 50, 60
            ).as_edit().as_manual().tap(test).repeat(3, True),
            self.assertEqual,
            [[40, 50, 60], [40, 50, 60], [40, 50, 60]],
        )
        self._true_true_false(
            self.mclass(40, 50, 60).as_edit().as_manual().repeat(3),
            self.assertEqual,
            [(40, 50, 60), (40, 50, 60), (40, 50, 60)],
        )

    def test_copy(self):
        # auto
        testlist = [[1, [2, 3]], [4, [5, 6]]]
        newlist = self.mclass(testlist).as_edit().as_auto().copy().close()
        self.assertFalse(newlist is testlist)
        self.assertListEqual(newlist, testlist)
        self.assertFalse(newlist[0] is testlist[0])
        self.assertListEqual(newlist[0], testlist[0])
        self.assertFalse(newlist[1] is testlist[1])
        self.assertListEqual(newlist[1], testlist[1])
        # man
        testlist = [[1, [2, 3]], [4, [5, 6]]]
        manchainsaw = self.mclass(testlist).as_edit().as_manual().copy()
        self.assertTrue(manchainsaw.balanced)
        manchainsaw.out_in()
        self.assertTrue(manchainsaw.balanced)
        newlist = manchainsaw.close()
        self.assertFalse(newlist is testlist)
        self.assertListEqual(newlist, testlist)
        self.assertFalse(newlist[0] is testlist[0])
        self.assertListEqual(newlist[0], testlist[0])
        self.assertFalse(newlist[1] is testlist[1])
        self.assertListEqual(newlist[1], testlist[1])
        self.assertTrue(manchainsaw.balanced)

    def test_permutations(self):
        # auto
        self.assertEqual(
            self.mclass(
                40, 50, 60
            ).as_edit().as_auto().permutations(2).close(),
            [(40, 50), (40, 60), (50, 40), (50, 60), (60, 40), (60, 50)],
        )
        # man
        self._false_true_false(
            self.mclass(40, 50, 60).as_edit().as_manual().permutations(2),
            self.assertEqual,
            [(40, 50), (40, 60), (50, 40), (50, 60), (60, 40), (60, 50)],
        )

    def test_combination(self):
        # auto
        self.assertEqual(
            self.mclass(
                40, 50, 60
            ).as_edit().as_auto().combinations(2).close(),
            [(40, 50), (40, 60), (50, 60)],
        )
        # man
        self._true_true_false(
            self.mclass(40, 50, 60).as_edit().as_manual().combinations(2),
            self.assertEqual,
            [(40, 50), (40, 60), (50, 60)],
        )


class MapMixin(object):

    def test_factory(self):
        from stuf import stuf
        # auto
        thing = self.mclass(
            [('a', 1), ('b', 2), ('c', 3)], [('a', 1), ('b', 2), ('c', 3)]
        ).as_edit().as_auto().tap(stuf).map().close()
        self.assertEqual(
            thing, [stuf(a=1, b=2, c=3), stuf(a=1, b=2, c=3)], thing
        )
        # man
        self.assertEqual(
            self.mclass(
                [('a', 1), ('b', 2), ('c', 3)], [('a', 1), ('b', 2), ('c', 3)]
            ).as_edit().as_manual().tap(stuf).map().close(),
            [stuf(a=1, b=2, c=3), stuf(a=1, b=2, c=3)],
        )

    def test_kwargmap(self):
        # auto
        def test(*args, **kw):
            return sum(args) * sum(kw.values())
        self.assertEqual(
            self.mclass(
                ((1, 2), {'a': 2}), ((2, 3), {'a': 2}), ((3, 4), {'a': 2})
            ).as_edit().as_auto().tap(test).kwargmap().close(),
            [6, 10, 14],
        )
        self.assertEqual(
            self.mclass(
                ((1, 2), {'a': 2}), ((2, 3), {'a': 2}), ((3, 4), {'a': 2})
            ).as_edit().as_auto().tap(test).params(
                1, 2, 3, b=5, w=10, y=13
            ).kwargmap(True).close(),
            [270, 330, 390],
        )
        # man
        self._true_true_false(
            self.mclass(
                ((1, 2), {'a': 2}), ((2, 3), {'a': 2}), ((3, 4), {'a': 2})
            ).as_edit().as_manual().tap(test).kwargmap(),
            self.assertEqual,
            [6, 10, 14],
        )
        self._true_true_false(
            self.mclass(
                ((1, 2), {'a': 2}), ((2, 3), {'a': 2}), ((3, 4), {'a': 2})
            ).as_edit().as_manual().tap(test).params(
                1, 2, 3, b=5, w=10, y=13
            ).kwargmap(True),
            self.assertEqual,
            [270, 330, 390],
        )

    def test_argmap(self):
        # auto
        self.assertEqual(
            self.mclass(
                (1, 2), (2, 3), (3, 4)
            ).as_edit().as_auto().tap(lambda x, y: x * y).argmap().close(),
            [2, 6, 12],
        )
        self.assertEqual(
            self.mclass((1, 2), (2, 3), (3, 4)).tap(
                lambda x, y, z, a, b: x * y * z * a * b
            ).as_edit().as_auto().params(7, 8, 9).argmap(True).close(),
            [1008, 3024, 6048],
        )
        # man
        self._true_true_false(
            self.mclass((1, 2), (2, 3), (3, 4)).tap(
                lambda x, y: x * y
            ).as_edit().as_manual().params(7, 8, 9).argmap(),
            self.assertEqual,
            [2, 6, 12],
        )
        self._true_true_false(
            self.mclass((1, 2), (2, 3), (3, 4)).tap(
                lambda x, y, z, a, b: x * y * z * a * b
            ).as_edit().params(7, 8, 9).as_manual().argmap(True),
            self.assertEqual,
            [1008, 3024, 6048],
        )

    def test_map(self):
        # auto
        self.assertEqual(
            self.mclass(1, 2, 3).as_edit().as_auto().tap(
                lambda x: x * 3
            ).map().close(),
            [3, 6, 9],
        )
        # man
        self._true_true_false(
            self.mclass(1, 2, 3).as_edit().as_manual().tap(
                lambda x: x * 3
            ).map(),
            self.assertEqual,
            [3, 6, 9],
        )

    def test_invoke(self):
        # auto
        self.assertEqual(
            self.mclass(
                [5, 1, 7], [3, 2, 1]
            ).as_edit().as_auto().params(1).invoke('index').close(),
            [1, 2],
        )
        self.assertEqual(
            self.mclass(
                [5, 1, 7], [3, 2, 1]
            ).as_edit().as_auto().invoke('sort').close(),
            [[1, 5, 7], [1, 2, 3]],
        )
        # man
        self._true_true_false(
            self.mclass(
                [5, 1, 7], [3, 2, 1]
            ).as_edit().as_manual().params(1).invoke('index'),
            self.assertEqual,
            [1, 2],
        )
        self._true_true_false(
            self.mclass([5, 1, 7], [3, 2, 1]).as_edit().as_manual().invoke(
                'sort'
            ),
            self.assertEqual,
            [[1, 5, 7], [1, 2, 3]]
        )


class Mixin(object):

    def _false_true_false(self, manchainsaw, expr, comp=None):
        self.assertFalse(manchainsaw.balanced)
        manchainsaw.out_in()
        self.assertTrue(manchainsaw.balanced)
        if comp is not None:
            expr(manchainsaw.read(), comp)
        else:
            expr(manchainsaw.read())
        self.assertFalse(manchainsaw.balanced)

    def _true_true_false(self, manchainsaw, expr, comp=None):
        self.assertTrue(manchainsaw.balanced)
        manchainsaw.out_in()
        self.assertTrue(manchainsaw.balanced)
        if comp is not None:
            out = manchainsaw.read()
            expr(out, comp, out)
        else:
            expr(manchainsaw.read(), comp)
        self.assertFalse(manchainsaw.balanced)

    def _false_true_true(self, manchainsaw, expr, comp=None):
        self.assertFalse(manchainsaw.balanced)
        manchainsaw.out_in()
        self.assertTrue(manchainsaw.balanced)
        if comp is not None:
            expr(manchainsaw.read(), comp)
        else:
            expr(manchainsaw.read(), comp)
        self.assertTrue(manchainsaw.balanced)

    def test_repr(self):
        from stuf.six import strings
        self.assertIsInstance(
            self.mclass([1, 2, 3, 4, 5, 6]).__repr__(), strings,
        )

    def test_preview(self):
        initial = self.mclass(1, 2, 3, 4, 5, 6).in_out()
        self.assertListEqual(initial.tell(), [1, 2, 3, 4, 5, 6])
        self.assertEqual(len(initial), 6)
        self.assertListEqual(initial.in_out().close(), [1, 2, 3, 4, 5, 6])
        self.assertEqual(len(initial), 0)

    def test_extend(self):
        self.assertListEqual(
            self.mclass().extend([1, 2, 3, 4, 5, 6]).in_out().close(),
            [1, 2, 3, 4, 5, 6],
        )

    def test_extendfront(self):
        self.assertListEqual(
            self.mclass().extendfront([1, 2, 3, 4, 5, 6]).in_out().close(),
            [6, 5, 4, 3, 2, 1]
        )

    def test_append(self):
        self.assertEqual(self.mclass().append('foo').in_out().close(), 'foo')

    def test_appendfront(self):
        self.assertEqual(
            self.mclass().prepend('foo').in_out().close(), 'foo'
        )

    def test_clearin(self):
        self.assertEqual(len(list(self.mclass([1, 2, 5, 6]).clear_in())), 0)

    def test_clearout(self):
        self.assertEqual(
            len(list(self.mclass([1, 2, 5, 6]).clear_out()._out)), 0
        )

    def test_undo(self):
        queue = self.mclass(1, 2, 3).as_manual().extendfront(
            [1, 2, 3, 4, 5, 6]
        ).in_out()
        self.assertEqual(queue.tell(), [6, 5, 4, 3, 2, 1, 1, 2, 3])
        queue.append(1).undo().in_out()
        self.assertEqual(queue.tell(), [6, 5, 4, 3, 2, 1, 1, 2, 3])
        queue.append(1).append(2).undo().in_out()
        self.assertEqual(queue.tell(), [6, 5, 4, 3, 2, 1, 1, 2, 3, 1])
        queue.append(1).append(2).undo(2).in_out()
        self.assertEqual(queue.tell(), [6, 5, 4, 3, 2, 1, 1, 2, 3, 1])
        queue.append(1).append(2).undo(baseline=True).in_out()
        self.assertEqual(
            queue.tell(), [6, 5, 4, 3, 2, 1, 1, 2, 3, 1, 1]
        )
        queue.undo(original=True).in_out()
        self.assertEqual(queue.close(), [1, 2, 3])

    def test_insync(self):
        q = self.mclass(1, 2, 3, 4, 5, 6).out_in().clear_in().out_in()
        self.assertEqual(list(q._in), list(q._out))

    def test_outsync(self):
        q = self.mclass(1, 2, 3, 4, 5, 6).in_out()
        self.assertEqual(list(q._in), list(q._out))

    def test_results(self):
        self.assertListEqual(
            list(self.mclass(1, 2, 3, 4, 5, 6).in_out().read()),
            [1, 2, 3, 4, 5, 6]
        )

    def test_wrap(self):
        self.assertIsInstance(
            self.mclass(1, 2, 3, 4, 5, 6).wrap(tuple).in_out().read(),
            tuple,
        )
        self.assertTupleEqual(
            self.mclass(1, 2, 3, 4, 5, 6).wrap(tuple).in_out().read(),
            (1, 2, 3, 4, 5, 6),
        )

    def test_list_wrap(self):
        self.assertIsInstance(
            self.mclass(1, 2, 3, 4, 5, 6).as_list().in_out().read(), list,
        )
        self.assertIsInstance(
            self.mclass(1, 2, 3, 4, 5, 6).unwrap().in_out().read(), list,
        )
        self.assertListEqual(
            self.mclass(1, 2, 3, 4, 5, 6).as_list().in_out().read(),
            [1, 2, 3, 4, 5, 6],
        )
        self.assertListEqual(
            self.mclass(1, 2, 3, 4, 5, 6).unwrap().in_out().read(),
            [1, 2, 3, 4, 5, 6],
        )

    def test_tuple_wrap(self):
        self.assertIsInstance(
            self.mclass(1, 2, 3, 4, 5, 6).as_tuple().in_out().read(),
            tuple,
        )
        self.assertTupleEqual(
            self.mclass(
                1, 2, 3, 4, 5, 6
            ).as_manual().as_tuple().in_out().read(),
            (1, 2, 3, 4, 5, 6),
        )

    def test_set_wrap(self):
        self.assertIsInstance(
            self.mclass(1, 2, 3, 4, 5, 6).as_set().in_out().read(),
            set,
        )
        self.assertSetEqual(
            self.mclass(
                1, 2, 3, 4, 5, 6
            ).as_manual().as_set().in_out().read(),
            set([1, 2, 3, 4, 5, 6]),
        )

    def test_dict_wrap(self):
        self.assertIsInstance(
            self.mclass((1, 2), (3, 4), (5, 6)).as_dict().in_out().read(),
            dict,
        )
        self.assertDictEqual(
            self.mclass(
                (1, 2), (3, 4), (5, 6)
            ).as_manual().as_dict().in_out().read(),
            {1: 2, 3: 4, 5: 6},
        )

    def test_ascii(self):
        from stuf.six import u, b
        # auto
        self.assertEqual(
            self.mclass(
                [1], True, r't', b('i'), u('g'), None, (1,)
            ).as_multi().as_ascii().in_out().close(),
            (b('[1]'), b('True'), b('t'), b('i'), b('g'), b('None'), b('(1,)'))
        )
        # man
        self._true_true_false(
            self.mclass(
                [1], True, r't', b('i'), u('g'), None, (1,)
            ).as_manual().as_multi().as_ascii().in_out(),
            self.assertEqual,
            (b('[1]'), b('True'), b('t'), b('i'), b('g'), b('None'), b('(1,)'))
        )

    def test_bytes(self):
        from stuf.six import u, b
        # auto
        self.assertEqual(
            self.mclass(
                [1], True, r't', b('i'), u('g'), None, (1,)
            ).as_multi().as_bytes().in_out().close(),
            (b('[1]'), b('True'), b('t'), b('i'), b('g'), b('None'), b('(1,)'))
        )
        # man
        self._true_true_false(
            self.mclass(
                [1], True, r't', b('i'), u('g'), None, (1,)
            ).as_manual().as_multi().as_bytes().in_out(),
            self.assertEqual,
            (b('[1]'), b('True'), b('t'), b('i'), b('g'), b('None'), b('(1,)'))
        )

    def test_unicode(self):
        from stuf.six import u, b
        # auto
        self.assertEqual(
            self.mclass(
                [1], True, r't', b('i'), u('g'), None, (1,)
            ).as_multi().as_unicode().in_out().close(),
            (u('[1]'), u('True'), u('t'), u('i'), u('g'), u('None'), u('(1,)'))
        )
        # man
        self._true_true_false(
            self.mclass(
                [1], True, r't', b('i'), u('g'), None, (1,)
            ).as_manual().as_multi().as_unicode().in_out(),
            self.assertEqual,
            (u('[1]'), u('True'), u('t'), u('i'), u('g'), u('None'), u('(1,)'))
        )
