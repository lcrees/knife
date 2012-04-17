# -*- coding: utf-8 -*-
'''ordering test mixins'''


class MathMixin(object):

    def test_max(self):
        # auto
        from stuf import stuf
        stooges = [
            stuf(name='moe', age=40),
            stuf(name='larry', age=50),
            stuf(name='curly', age=60),
        ]
        self.assertEqual(self.qclass(1, 2, 4).max().end(), 4)
        self.assertEqual(
            stuf(self.qclass(*stooges).tap(lambda x: x.age).max().end()),
            stuf(name='curly', age=60),
        )
        # man
        self._false_true_false(
            self.mclass.as_manual()(1, 2, 4).max(), self.assertEqual, 4,
        )
        self._false_true_false(
            self.mclass(*stooges).tap(lambda x: x.age).max(),
            self.assertEqual,
            stuf(name='curly', age=60)
        )

    def test_min(self):
        # auto
        self.assertEqual(self.qclass(10, 5, 100, 2, 1000).min().end(), 2)
        self.assertEqual(
            self.qclass(10, 5, 100, 2, 1000).tap(lambda x: x).min().end(), 2,
        )
        # man
        self._false_true_false(
            self.mclass(10, 5, 100, 2, 1000).min(),
            self.assertEqual,
            2,
        )
        self._false_true_false(
            self.mclass(10, 5, 100, 2, 1000).tap(lambda x: x).min(),
            self.assertEqual,
            2,
        )

    def test_minmax(self):
        # auto
        self.assertEqual(self.qclass(1, 2, 4).minmax().end(), (1, 4))
        self.assertEqual(
            self.qclass(10, 5, 100, 2, 1000).minmax().end(), (2, 1000),
        )
        achainsaw = self.qclass(
            10, 5, 100, 2, 1000
        ).as_query().minmax().min()
        self.assertEqual(achainsaw.end(), 2)
        self.assertEqual(
            achainsaw.as_edit().in_out().preview(), [10, 5, 100, 2, 1000]
        )
        # man
        self._false_true_false(
            self.mclass(1, 2, 4).minmax(), self.assertEqual, (1, 4),
        )
        self._false_true_false(
            self.mclass(10, 5, 100, 2, 1000).minmax(),
            self.assertEqual,
            (2, 1000),
        )

    def test_sum(self):
        # auto
        self.assertEqual(self.qclass(1, 2, 3).sum().end(), 6)
        self.assertEqual(self.qclass(1, 2, 3).sum(1).end(), 7)
        self.assertEqual(
            self.qclass(
                .1, .1, .1, .1, .1, .1, .1, .1, .1, .1
            ).sum(precision=True).end(),
            1.0,
        )
        # man
        self._false_true_false(
            self.mclass(1, 2, 3).sum(), self.assertEqual, 6,
        )
        self._false_true_false(
            self.mclass(1, 2, 3).sum(1), self.assertEqual, 7,
        )
        self._false_true_false(
            self.mclass(
                .1, .1, .1, .1, .1, .1, .1, .1, .1, .1
            ).sum(precision=True),
            self.assertEqual,
            1.0,
        )

    def test_median(self):
        # auto
        self.assertEqual(self.qclass(4, 5, 7, 2, 1).median().end(), 4)
        self.assertEqual(self.qclass(4, 5, 7, 2, 1, 8).median().end(), 4.5)
        # man
        self._false_true_false(
            self.mclass(4, 5, 7, 2, 1).median(), self.assertEqual, 4,
        )
        self._false_true_false(
            self.mclass(4, 5, 7, 2, 1, 8).median(), self.assertEqual, 4.5,
        )

    def test_average(self):
        # auto
        self.assertEqual(
            self.qclass(10, 40, 45).average().end(), 31.666666666666668,
        )
        # man
        self._false_true_false(
            self.mclass(10, 40, 45).average(),
            self.assertEqual,
            31.666666666666668,
        )

    def test_range(self):
        # auto
        self.assertEqual(self.qclass(3, 5, 7, 3, 11).range().end(), 8)
        # man
        self._false_true_false(
            self.mclass(3, 5, 7, 3, 11).range(), self.assertEqual, 8,
        )

    def test_count(self):
        # auto
        common = self.qclass(11, 3, 5, 11, 7, 3, 11).count().end()
        self.assertEqual(common[2], [(11, 3), (3, 2), (5, 1), (7, 1)])
        # most common
        self.assertEqual(common[1], 11)
        # least common
        self.assertEqual(common[0], 7)
        # man
        self._false_true_false(
            self.mclass(11, 3, 5, 11, 7, 3, 11).count(),
            self.assertEqual,
            (7, 11, [(11, 3), (3, 2), (5, 1), (7, 1)]),
        )


class CompareMixin(object):

    def test_all(self):
        # auto
        self.assertFalse(
            self.qclass(True, 1, None, 'yes').tap(bool).all().end()
        )
        # man
        self._false_true_false(
            self.mclass(True, 1, None, 'yes').tap(bool).all(),
            self.assertFalse,
        )

    def test_any(self):
        # auto
        self.assertTrue(
            self.qclass(None, 0, 'yes', False).tap(bool).any().end()
        )
        # man
        self._false_true_false(
            self.mclass(None, 0, 'yes', False).tap(bool).any(),
            self.assertTrue,
        )

    def test_difference(self):
        # auto
        self.assertEqual(
            self.qclass([1, 2, 3, 4, 5], [5, 2, 10]).difference().end(),
            [1, 3, 4],
        )
        self.assertEqual(
            self.qclass([1, 2, 3, 4, 5], [5, 2, 10]).difference(True).end(),
            [1, 3, 4, 10]
        )
        # man
        self._false_true_false(
            self.mclass([1, 2, 3, 4, 5], [5, 2, 10]).difference(),
            self.assertEqual,
            [1, 3, 4]
        )
        self._false_true_false(
            self.mclass([1, 2, 3, 4, 5], [5, 2, 10]).difference(True),
            self.assertEqual,
            [1, 3, 4, 10]
        )

    def test_disjointed(self):
        # auto
        self.assertTrue(
            self.qclass([1, 2, 3], [5, 4, 10]).disjointed().end()
        )
        self.assertFalse(
            self.qclass([1, 2, 3], [5, 2, 10]).disjointed().end()
        )
        # man
        self._false_true_false(
            self.mclass([1, 2, 3], [5, 4, 10]).disjointed(), self.assertTrue,
        )
        self._false_true_false(
            self.mclass([1, 2, 3], [5, 2, 10]).disjointed(), self.assertFalse,
        )

    def test_intersection(self):
        # auto
        self.assertEqual(
            self.qclass(
                [1, 2, 3], [101, 2, 1, 10], [2, 1]
            ).intersection().end(), [1, 2],
        )
        # man
        self._false_true_false(
            self.mclass([1, 2, 3], [101, 2, 1, 10], [2, 1]).intersection(),
            self.assertEqual,
            [1, 2],
        )

    def test_subset(self):
        # auto
        self.assertTrue(
            self.qclass([1, 2, 3], [101, 2, 1, 3]).subset().end(),
        )
        # man
        self._false_true_false(
            self.mclass([1, 2, 3], [101, 2, 1, 3]).subset(),
            self.assertTrue,
        )

    def test_superset(self):
        # auto
        diff = self.qclass([101, 2, 1, 3, 6, 34], [1, 2, 3]).superset().end()
        self.assertTrue(diff)
        # man
        self._false_true_false(
            self.mclass([101, 2, 1, 3, 6, 34], [1, 2, 3]).superset(),
            self.assertTrue,
        )

    def test_union(self):
        # auto
        self.assertEqual(
            self.qclass([1, 2, 3], [101, 2, 1, 10], [2, 1]).union().end(),
            [1, 10, 3, 2, 101],
        )
        # man
        self._false_true_false(
            self.mclass([1, 2, 3], [101, 2, 1, 10], [2, 1]).union(),
            self.assertEqual,
            [1, 10, 3, 2, 101],
        )

    def test_unique(self):
        # auto
        self.assertEqual(
            self.qclass(1, 2, 1, 3, 1, 4).unique().end(), [1, 2, 3, 4],
        )
        self.assertEqual(
            self.qclass(1, 2, 1, 3, 1, 4).tap(round).unique().end(),
            [1, 2, 3, 4],
        )
        # man
        self._false_true_false(
            self.mclass(1, 2, 1, 3, 1, 4).unique(),
            self.assertEqual,
            [1, 2, 3, 4],
        )
        self._false_true_false(
            self.mclass(1, 2, 1, 3, 1, 4).tap(round).unique(),
            self.assertEqual,
            [1, 2, 3, 4],
        )


class OrderMixin(object):

    def test_shuffle(self):
        # auto
        self.assertEqual(
            len(self.qclass(1, 2, 3, 4, 5, 6).shuffle()),
            len([5, 4, 6, 3, 1, 2]),
        )
        # man
        manchainsaw = self.mclass(1, 2, 3, 4, 5, 6).shuffle()
        self.assertFalse(manchainsaw.balanced)
        manchainsaw.out_in()
        self.assertTrue(manchainsaw.balanced)
        manchainsaw.end()
        self.assertTrue(manchainsaw.balanced)

    def test_group(self,):
        # auto
        from math import floor
        self.assertEqual(
        self.qclass(1.3, 2.1, 2.4).tap(lambda x: floor(x)).group().end(),
            [(1.0, (1.3,)), (2.0, (2.1, 2.4))]
        )
        self.assertEqual(
            self.qclass(1.3, 2.1, 2.4).group().end(),
            [(1.3, (1.3,)), (2.1, (2.1,)), (2.4, (2.4,))],
        )
        # man
        self._false_true_false(
            self.mclass(1.3, 2.1, 2.4).tap(lambda x: floor(x)).group(),
            self.assertListEqual,
            [(1.0, (1.3,)), (2.0, (2.1, 2.4))]
        )
        self._true_true_false(
            self.mclass(1.3, 2.1, 2.4).group(),
            self.assertListEqual,
            [(1.3, (1.3,)), (2.1, (2.1,)), (2.4, (2.4,))],
        )

    def test_reverse(self):
        # auto
        self.assertEqual(
            self.qclass(5, 4, 3, 2, 1).reverse().end(), [1, 2, 3, 4, 5],
        )
        # man
        self._false_true_false(
            self.mclass(5, 4, 3, 2, 1).reverse(),
            self.assertEqual,
            [1, 2, 3, 4, 5],
        )

    def test_sort(self):
        from math import sin
        # auto
        self.assertEqual(
            self.qclass(1, 2, 3, 4, 5, 6).tap(
                lambda x: sin(x)
            ).sort().end(),
            [5, 4, 6, 3, 1, 2],
        )
        self.assertEqual(
            self.qclass(4, 6, 65, 3, 63, 2, 4).sort().end(),
            [2, 3, 4, 4, 6, 63, 65],
        )
        # man
        self._false_true_false(
            self.mclass(1, 2, 3, 4, 5, 6).tap(lambda x: sin(x)).sort(),
           self.assertListEqual,
            [5, 4, 6, 3, 1, 2],
        )
        self._false_true_false(
            self.mclass(4, 6, 65, 3, 63, 2, 4).sort(),
          self.assertListEqual,
            [2, 3, 4, 4, 6, 63, 65],
        )


class FilterMixin(object):

    def test_pattern(self):
        self.assertEqual(
            self.qclass(
                'This is the first test',
                'This is the second test',
                'This is the third test'
            ).pattern('{} first {}').filter().end(), 'This is the first test'
        )
        self.assertEqual(
            self.qclass(
                'This is the first test',
                'This is the second test',
                'This is the third test'
            ).pattern(
                '. third .', type='regex'
            ).filter().end(), 'This is the third test'
        )
        self.assertEqual(
            self.qclass(
                'This is the first test',
                'This is the second test',
                'This is the third test'
            ).pattern(
                '*second*', type='glob'
            ).filter().end(), 'This is the second test'
        )

    def test_traverse(self):
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
        # auto
        out = self.qclass(stooges, stoog2, stoog3).traverse().end(),
        self.assertEqual(
            out,
            [(('age', 40), ('name', 'moe'), ('age', 50), ('name', 'larry'),
            ('age', 60), ('name', 'curly'), ('stoog4', (('age', 969),
            ('name', 'beastly'))))],
            out,
        )
        # man
        self._true_true_false(
            self.mclass(stooges, stoog2, stoog3).traverse().out_in(),
            self.assertEqual,
            [('age', 40), ('name', 'moe'), ('age', 50), ('name', 'larry'),
            ('age', 60), ('name', 'curly'), ('stoog4', (('age', 969),
            ('name', 'beastly')))],
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
            self.qclass(*stooges).attributes('name').end(),
            ['moe', 'larry', 'curly'],
        )
        self.assertEqual(
            self.qclass(*stooges).attributes('name', 'age').end(),
            [('moe', 40), ('larry', 50), ('curly', 60)],
        )
        self.assertEqual(
            self.qclass(*stooges).attributes('place').end(), [],
        )
        # man
        self._true_true_false(
            self.mclass(*stooges).attributes('name'),
            self.assertEqual,
            ['moe', 'larry', 'curly'],
        )
        self._true_true_false(
            self.mclass(*stooges).attributes('name', 'age'),
            self.assertEqual,
            [('moe', 40), ('larry', 50), ('curly', 60)],
        )
        self._false_true_true(
            self.mclass(*stooges).attributes('place'),
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
            self.qclass(*stooges).items('name').end(),
            ['moe', 'larry', 'curly'],
        )
        self.assertEqual(
            self.qclass(*stooges).items('name', 'age').end(),
            [('moe', 40), ('larry', 50), ('curly', 60)],
        )
        stooges = [['moe', 40], ['larry', 50], ['curly', 60]]
        self.assertEqual(
            self.qclass(*stooges).items(0).end(), ['moe', 'larry', 'curly'],
        )
        self.assertEqual(self.qclass(*stooges).items(1).end(), [40, 50, 60])
        self.assertEqual(self.qclass(*stooges).items('place').end(), [])
        # man
        stooges = [
            stuf(name='moe', age=40),
            stuf(name='larry', age=50),
            stuf(name='curly', age=60)
        ]
        self._true_true_false(
            self.mclass(*stooges).items('name'),
            self.assertEqual,
            ['moe', 'larry', 'curly'],
        )
        self._true_true_false(
            self.mclass(*stooges).items('name', 'age'),
            self.assertEqual,
            [('moe', 40), ('larry', 50), ('curly', 60)],
        )
        stooges = [['moe', 40], ['larry', 50], ['curly', 60]]
        self._true_true_false(
            self.mclass(*stooges).items(0),
            self.assertEqual,
            ['moe', 'larry', 'curly'],
        )
        self._true_true_false(
            self.mclass(*stooges).items(1),
            self.assertEqual,
            [40, 50, 60],
        )
        self._false_true_true(
            self.mclass(*stooges).items('place'),
            self.assertEqual,
            [],
        )

    def test_mapping(self):
        # auto
        self.assertEqual(
            self.qclass(
                dict([(1, 2), (2, 3), (3, 4)]), dict([(1, 2), (2, 3), (3, 4)])
            ).mapping(True).end(), [1, 2, 3, 1, 2, 3],
        )
        self.assertEqual(
            self.qclass(
                dict([(1, 2), (2, 3), (3, 4)]), dict([(1, 2), (2, 3), (3, 4)])
            ).mapping(values=True).end(), [2, 3, 4, 2, 3, 4],
        )
        self.assertEqual(
            self.qclass(
                dict([(1, 2), (2, 3), (3, 4)]), dict([(1, 2), (2, 3), (3, 4)])
            ).tap(lambda x, y: x * y).mapping().end(), [2, 6, 12, 2, 6, 12],
        )
        # man
        self._false_true_false(
            self.mclass(
                dict([(1, 2), (2, 3), (3, 4)]), dict([(1, 2), (2, 3), (3, 4)])
            ).mapping(True),
            self.assertEqual,
            [1, 2, 3, 1, 2, 3],
        )
        self._false_true_false(
            self.mclass(
                dict([(1, 2), (2, 3), (3, 4)]), dict([(1, 2), (2, 3), (3, 4)])
            ).mapping(values=True),
            self.assertEqual,
            [2, 3, 4, 2, 3, 4],
        )
        self._false_true_false(
            self.mclass(
                dict([(1, 2), (2, 3), (3, 4)]), dict([(1, 2), (2, 3), (3, 4)])
            ).tap(lambda x, y: x * y).mapping(),
            self.assertEqual,
            [2, 6, 12, 2, 6, 12],
        )

    def test_filter(self):
        # auto
        self.assertEqual(
            self.qclass(1, 2, 3, 4, 5, 6).tap(
                lambda x: x % 2 == 0
            ).filter(invert=True).end(), [1, 3, 5]
        )
        self.assertEqual(
            self.qclass(1, 2, 3, 4, 5, 6).tap(
                lambda x: x % 2 == 0
            ).filter().end(), [2, 4, 6]
        )
        # man
        self._false_true_false(
            self.mclass(1, 2, 3, 4, 5, 6).tap(lambda x: x % 2 == 0).filter(),
            self.assertEqual,
            [2, 4, 6],
        )
        self._false_true_false(
            self.mclass(1, 2, 3, 4, 5, 6).tap(
                lambda x: x % 2 == 0
            ).filter(invert=True),
            self.assertEqual,
            [1, 3, 5],
        )

    def test_duality(self):
        # auto
        self.assertEqual(
            self.qclass(1, 2, 3, 4, 5, 6).tap(
                lambda x: x % 2 == 0
            ).duality().end(), ([2, 4, 6], [1, 3, 5])
        )
        # man
        self._false_true_false(
            self.mclass(
                1, 2, 3, 4, 5, 6
            ).tap(lambda x: x % 2 == 0).duality(),
            self.assertEqual,
            ([2, 4, 6], [1, 3, 5]),
        )


class SliceMixin(object):

    def test_dice(self):
        # auto
        self.assertEqual(
            self.qclass(
                'moe', 'larry', 'curly', 30, 40, 50, True
            ).dice(2, 'x').end(),
            [('moe', 'larry'), ('curly', 30), (40, 50), (True, 'x')]
        )
        # man
        self._false_true_false(
            self.mclass(
                'moe', 'larry', 'curly', 30, 40, 50, True,
            ).dice(2, 'x'),
            self.assertEqual,
            [('moe', 'larry'), ('curly', 30), (40, 50), (True, 'x')],
        )

    def test_first(self):
        # auto
        self.assertEqual(self.qclass(5, 4, 3, 2, 1).first().end(), 5)
        self.assertEqual(self.qclass(5, 4, 3, 2, 1).first(2).end(), [5, 4])
        # man
        manchainsaw = self.mclass(5, 4, 3, 2, 1).first()
        self.assertFalse(manchainsaw.balanced)
        manchainsaw.out_in()
        self.assertTrue(manchainsaw.balanced)
        self.assertEqual(manchainsaw.results(), 5)
        self.assertFalse(manchainsaw.balanced)
        self._false_true_false(
            self.mclass(5, 4, 3, 2, 1).first(2), self.assertEqual, [5, 4],
        )

    def test_index(self):
        # auto
        self.assertEqual(self.qclass(5, 4, 3, 2, 1).at(2).end(), 3)
        self.assertEqual(self.qclass(5, 4, 3, 2, 1).at(10, 11).end(), 11)
        # man
        self._false_true_false(
            self.mclass(5, 4, 3, 2, 1).at(2), self.assertEqual, 3,
        )
        self._false_true_false(
            self.mclass(5, 4, 3, 2, 1).at(10, 11), self.assertEqual, 11,
        )

    def test_slice(self):
        # auto
        self.assertEqual(self.qclass(5, 4, 3, 2, 1).slice(2).end(), [5, 4])
        self.assertEqual(self.qclass(5, 4, 3, 2, 1).slice(2, 4).end(), [3, 2])
        self.assertEqual(self.qclass(5, 4, 3, 2, 1).slice(2, 4, 2).end(), 3)
        # man
        self._false_true_false(
            self.mclass(5, 4, 3, 2, 1).slice(2), self.assertEqual, [5, 4],
        )
        self._false_true_false(
            self.mclass(5, 4, 3, 2, 1).slice(2, 4), self.assertEqual, [3, 2]
        )
        self._false_true_false(
            self.mclass(5, 4, 3, 2, 1).slice(2, 4, 2), self.assertEqual, 3,
        )

    def test_last(self):
        # auto
        self.assertEqual(self.qclass(5, 4, 3, 2, 1).last().end(), 1)
        self.assertEqual(self.qclass(5, 4, 3, 2, 1).last(2).end(), [2, 1])
        # man
        manchainsaw = self.mclass(5, 4, 3, 2, 1).last()
        self.assertFalse(manchainsaw.balanced)
        manchainsaw.out_in()
        self.assertTrue(manchainsaw.balanced)
        self.assertEqual(manchainsaw.results(), 1)
        self.assertFalse(manchainsaw.balanced)
        self._false_true_false(
            self.mclass(5, 4, 3, 2).last(2), self.assertEqual, [3, 2],
        )

    def test_initial(self):
        # auto
        self.assertEqual(
            self.qclass(5, 4, 3, 2, 1).initial().end(), [5, 4, 3, 2]
        )
        # man
        self._false_true_false(
            self.mclass(5, 4, 3, 2, 1).initial(),
            self.assertEqual,
            [5, 4, 3, 2],
        )

    def test_rest(self):
        # auto
        self.assertEqual(
            self.qclass(5, 4, 3, 2, 1).rest().end(), [4, 3, 2, 1],
        )
        # man
        self._false_true_false(
            self.mclass(5, 4, 3, 2, 1).rest(), self.assertEqual, [4, 3, 2, 1],
        )

    def test_choice(self):
        # auto
        self.assertEqual(
            len(self.qclass(1, 2, 3, 4, 5, 6).choice().out_in()), 1
        )
        # man
        manchainsaw = self.mclass(1, 2, 3, 4, 5, 6).choice()
        self.assertFalse(manchainsaw.balanced)
        manchainsaw.out_in()
        self.assertTrue(manchainsaw.balanced)
        manchainsaw.end()
        self.assertTrue(manchainsaw.balanced)

    def test_sample(self):
        #auto
        self.assertEqual(
            len(self.qclass(1, 2, 3, 4, 5, 6).sample(3).end()), 3,
        )
        # man
        manchainsaw = self.mclass(1, 2, 3, 4, 5, 6).sample(3)
        self.assertFalse(manchainsaw.balanced)
        manchainsaw.out_in()
        self.assertTrue(manchainsaw.balanced)
        manchainsaw.end()
        self.assertTrue(manchainsaw.balanced)


class ReduceMixin(object):

    def test_flatten(self):
        # auto
        self.assertEqual(
            self.qclass([[1, [2], [3, [[4]]]], 'here']).flatten().end(),
            [1, 2, 3, 4, 'here'],
        )
        # man
        self._false_true_false(
            self.mclass([[1, [2], [3, [[4]]]], 'here']).flatten(),
            self.assertEqual,
            [1, 2, 3, 4, 'here'],
        )

    def test_merge(self):
        # auto
        self.assertEqual(
            self.qclass(
                ['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False]
            ).merge().end(),
            ['moe', 'larry', 'curly', 30, 40, 50, True, False, False],
        )
        # man
        self._false_true_false(
            self.mclass(
                ['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False],
            ).merge(),
            self.assertEqual,
            ['moe', 'larry', 'curly', 30, 40, 50, True, False, False],
        )

    def test_reduce(self):
        # auto
        self.assertEqual(
            self.qclass(1, 2, 3).tap(lambda x, y: x + y).reduce().end(), 6,
        )
        self.assertEqual(
            self.qclass(1, 2, 3).tap(lambda x, y: x + y).reduce(1).end(), 7,
        )
        self.assertEqual(
            self.qclass([0, 1], [2, 3], [4, 5]).tap(
                lambda x, y: x + y
            ).reduce(reverse=True).end(), [4, 5, 2, 3, 0, 1],
        )
        self.assertEqual(
            self.qclass([0, 1], [2, 3], [4, 5]).tap(
                lambda x, y: x + y
            ).reduce([0, 0], True).end(), [4, 5, 2, 3, 0, 1, 0, 0],
        )
        # man
        self._false_true_false(
            self.mclass(1, 2, 3).tap(lambda x, y: x + y).reduce(),
            self.assertEqual,
            6,
        )
        self._false_true_false(
            self.mclass(1, 2, 3).tap(lambda x, y: x + y).reduce(1),
            self.assertEqual,
            7,
        )
        self._false_true_false(
            self.mclass([0, 1], [2, 3], [4, 5]).tap(
                lambda x, y: x + y
            ).reduce(reverse=True),
            self.assertEqual,
             [4, 5, 2, 3, 0, 1],
        )
        self._false_true_false(
            self.mclass([0, 1], [2, 3], [4, 5]).tap(
                lambda x, y: x + y
            ).reduce([0, 0], True),
            self.assertEqual,
            [4, 5, 2, 3, 0, 1, 0, 0],
        )

    def test_weave(self):
        # auto
        self.assertEqual(
            self.qclass(
                ['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False]
            ).as_one().weave().end(),
            ['moe', 30, True, 'larry', 40, False, 'curly', 50, False],
        )
        # man
        self._false_true_false(
            self.mclass(
                ['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False]
            ).as_one().weave(),
            self.assertEqual,
            ['moe', 30, True, 'larry', 40, False, 'curly', 50, False],
        )

    def test_zip(self):
        # auto
        self.assertEqual(
            self.qclass(
                ['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False]
            ).as_one().zip().end(),
            [('moe', 30, True), ('larry', 40, False), ('curly', 50, False)],
        )
        # man
        self._true_true_false(
            self.mclass(
                ['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False],
            ).as_one().zip(),
            self.assertEqual,
            [('moe', 30, True), ('larry', 40, False), ('curly', 50, False)],
        )


class RepeatMixin(object):

    def test_repeat(self):
        # auto
        self.assertEqual(
            self.qclass(40, 50, 60).repeat(3).end(),
            [(40, 50, 60), (40, 50, 60), (40, 50, 60)],
        )
        # man
        self._true_true_false(
            self.mclass(40, 50, 60).repeat(3),
            self.assertEqual,
            [(40, 50, 60), (40, 50, 60), (40, 50, 60)],
        )
        # auto
        def test(*args): #@IgnorePep8
            return list(args)
        self.assertEqual(
            self.qclass(40, 50, 60).tap(test).repeat(3, True).end(),
            [[40, 50, 60], [40, 50, 60], [40, 50, 60]],
        )
        # man
        self._true_true_false(
            self.mclass(40, 50, 60).tap(test).repeat(3, True),
            self.assertEqual,
            [[40, 50, 60], [40, 50, 60], [40, 50, 60]],
        )

    def test_copy(self):
        # auto
        testlist = [[1, [2, 3]], [4, [5, 6]]]
        newlist = self.qclass(testlist).copy().end()
        self.assertFalse(newlist is testlist)
        self.assertListEqual(newlist, testlist)
        self.assertFalse(newlist[0] is testlist[0])
        self.assertListEqual(newlist[0], testlist[0])
        self.assertFalse(newlist[1] is testlist[1])
        self.assertListEqual(newlist[1], testlist[1])
        # man
        testlist = [[1, [2, 3]], [4, [5, 6]]]
        manchainsaw = self.mclass(testlist).copy()
        self.assertTrue(manchainsaw.balanced)
        manchainsaw.out_in()
        self.assertTrue(manchainsaw.balanced)
        newlist = manchainsaw.end()
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
            self.qclass(40, 50, 60).permutations(2).end(),
            [(40, 50), (40, 60), (50, 40), (50, 60), (60, 40), (60, 50)],
        )
        # man
        self._false_true_false(
            self.mclass(40, 50, 60).permutations(2),
            self.assertEqual,
            [(40, 50), (40, 60), (50, 40), (50, 60), (60, 40), (60, 50)],
        )

    def test_combination(self):
        # auto
        self.assertEqual(
            self.qclass(40, 50, 60).combinations(2).end(),
            [(40, 50), (40, 60), (50, 60)],
        )
        # man
        self._true_true_false(
            self.mclass(40, 50, 60).combinations(2),
            self.assertEqual,
            [(40, 50), (40, 60), (50, 60)],
        )


class MapMixin(object):

    def test_factory(self):
        from stuf import stuf
        # auto
        thing = self.qclass(
            [('a', 1), ('b', 2), ('c', 3)], [('a', 1), ('b', 2), ('c', 3)]
        ).tap(stuf).map().end()
        self.assertEqual(
            thing, [stuf(a=1, b=2, c=3), stuf(a=1, b=2, c=3)], thing
        )
        # man
        self.assertEqual(
            self.mclass(
                [('a', 1), ('b', 2), ('c', 3)], [('a', 1), ('b', 2), ('c', 3)]
            ).tap(stuf).map().end(),
            [stuf(a=1, b=2, c=3), stuf(a=1, b=2, c=3)],
        )

    def test_kwargmap(self):
        # auto
        def test(*args, **kw):
            return sum(args) * sum(kw.values())
        self.assertEqual(
            self.qclass(
                ((1, 2), {'a': 2}), ((2, 3), {'a': 2}), ((3, 4), {'a': 2})
            ).tap(test).kwargmap().end(),
            [6, 10, 14],
        )
        self.assertEqual(
            self.qclass(
                ((1, 2), {'a': 2}), ((2, 3), {'a': 2}), ((3, 4), {'a': 2})
            ).tap(test).arguments(
                1, 2, 3, b=5, w=10, y=13
            ).kwargmap(True).end(),
            [270, 330, 390],
        )
        # man
        self._true_true_false(
            self.mclass(
                ((1, 2), {'a': 2}), ((2, 3), {'a': 2}), ((3, 4), {'a': 2})
            ).tap(test).kwargmap(),
            self.assertEqual,
            [6, 10, 14],
        )
        self._true_true_false(
            self.mclass(
                ((1, 2), {'a': 2}), ((2, 3), {'a': 2}), ((3, 4), {'a': 2})
            ).tap(test).arguments(1, 2, 3, b=5, w=10, y=13).kwargmap(True),
            self.assertEqual,
            [270, 330, 390],
        )

    def test_argmap(self):
        # auto
        self.assertEqual(
            self.qclass(
                (1, 2), (2, 3), (3, 4)
            ).tap(lambda x, y: x * y).argmap().end(), [2, 6, 12],
        )
        self.assertEqual(
            self.mclass(
                (1, 2), (2, 3), (3, 4)
            ).tap(
                lambda x, y, z, a, b: x * y * z * a * b
            ).arguments(7, 8, 9).argmap(True).end(),
            [1008, 3024, 6048],
        )
        # man
        self._true_true_false(
            self.mclass(
                (1, 2), (2, 3), (3, 4)
            ).tap(lambda x, y: x * y).arguments(7, 8, 9).argmap(),
            self.assertEqual,
            [2, 6, 12],
        )
        self._true_true_false(
            self.mclass(
                (1, 2), (2, 3), (3, 4)
            ).tap(
                lambda x, y, z, a, b: x * y * z * a * b
            ).arguments(7, 8, 9).argmap(True),
            self.assertEqual,
            [1008, 3024, 6048],
        )

    def test_map(self):
        # auto
        self.assertEqual(
            self.qclass(1, 2, 3).tap(lambda x: x * 3).map().end(), [3, 6, 9],
        )
        # man
        self._true_true_false(
            self.mclass(1, 2, 3).tap(lambda x: x * 3).map(),
            self.assertEqual,
            [3, 6, 9],
        )

    def test_invoke(self):
        # auto
        self.assertEqual(
            self.qclass(
                [5, 1, 7], [3, 2, 1]
            ).arguments(1).invoke('index').end(),
            [1, 2],
        )
        self.assertEqual(
            self.qclass([5, 1, 7], [3, 2, 1]).invoke('sort').end(),
            [[1, 5, 7], [1, 2, 3]],
        )
        # man
        self._true_true_false(
            self.mclass([5, 1, 7], [3, 2, 1]).arguments(1).invoke('index'),
            self.assertEqual,
            [1, 2],
        )
        self._true_true_false(
            self.mclass([5, 1, 7], [3, 2, 1]).invoke('sort'),
            self.assertEqual,
            [[1, 5, 7], [1, 2, 3]]
        )


class Mixin(object):

    def _false_true_false(self, manchainsaw, expr, comp=None):
        self.assertFalse(manchainsaw.balanced)
        manchainsaw.out_in()
        self.assertTrue(manchainsaw.balanced)
        if comp is not None:
            expr(manchainsaw.results(), comp)
        else:
            expr(manchainsaw.results())
        self.assertFalse(manchainsaw.balanced)

    def _true_true_false(self, manchainsaw, expr, comp=None):
        self.assertTrue(manchainsaw.balanced)
        manchainsaw.out_in()
        self.assertTrue(manchainsaw.balanced)
        if comp is not None:
            out = manchainsaw.results()
            expr(out, comp, out)
        else:
            expr(manchainsaw.results(), comp)
        self.assertFalse(manchainsaw.balanced)

    def _false_true_true(self, manchainsaw, expr, comp=None):
        self.assertFalse(manchainsaw.balanced)
        manchainsaw.out_in()
        self.assertTrue(manchainsaw.balanced)
        if comp is not None:
            expr(manchainsaw.results(), comp)
        else:
            expr(manchainsaw.results(), comp)
        self.assertTrue(manchainsaw.balanced)

    def test_repr(self):
        from stuf.six import strings
        self.assertIsInstance(
            self.qclass([1, 2, 3, 4, 5, 6]).__repr__(), strings,
        )

    def test_preview(self):
        initial = self.qclass(1, 2, 3, 4, 5, 6).in_out()
        self.assertListEqual(initial.preview(), [1, 2, 3, 4, 5, 6])
        self.assertEqual(len(initial), 6)
        self.assertListEqual(initial.in_out().end(), [1, 2, 3, 4, 5, 6])
        self.assertEqual(len(initial), 0)

    def test_extend(self):
        self.assertListEqual(
            self.qclass().extend(
                [1, 2, 3, 4, 5, 6]
            ).in_out().end(),
            [1, 2, 3, 4, 5, 6],
        )

    def test_extendfront(self):
        self.assertListEqual(
            self.qclass().extendstart(
                [1, 2, 3, 4, 5, 6]
            ).in_out().end(),
            [6, 5, 4, 3, 2, 1]
        )

    def test_append(self):
        self.assertEqual(
            self.qclass().append('foo').in_out().end(), 'foo'
        )

    def test_appendfront(self):
        self.assertEqual(
            self.qclass().appendstart('foo').in_out().end(),
            'foo'
        )

    def test_clearin(self):
        self.assertEqual(len(list(self.qclass([1, 2, 5, 6]).clear_in())), 0)

    def test_clearout(self):
        self.assertEqual(
            len(list(self.qclass([1, 2, 5, 6]).clear_out()._out)), 0
        )

    def test_undo(self):
        queue = self.qclass(1, 2, 3).extendstart(
            [1, 2, 3, 4, 5, 6]
        ).in_out()
        self.assertListEqual(queue.preview(), [6, 5, 4, 3, 2, 1, 1, 2, 3])
        queue.append(1).undo().in_out()
        self.assertListEqual(queue.preview(), [6, 5, 4, 3, 2, 1, 1, 2, 3])
        queue.append(1).append(2).undo().in_out()
        self.assertListEqual(queue.preview(), [6, 5, 4, 3, 2, 1, 1, 2, 3, 1])
        queue.append(1).append(2).undo(2).in_out()
        self.assertListEqual(queue.preview(), [6, 5, 4, 3, 2, 1, 1, 2, 3, 1])
        queue.append(1).append(2).undo(baseline=True).in_out()
        self.assertListEqual(
            queue.preview(), [6, 5, 4, 3, 2, 1, 1, 2, 3, 1, 1]
        )
        queue.undo(original=True).in_out()
        self.assertListEqual(queue.end(), [1, 2, 3])

    def test_insync(self):
        q = self.qclass(1, 2, 3, 4, 5, 6).out_in().clear_in().out_in()
        self.assertEqual(list(q._in), list(q._out))

    def test_outsync(self):
        q = self.qclass(1, 2, 3, 4, 5, 6).in_out()
        self.assertEqual(list(q._in), list(q._out))

    def test_results(self):
        self.assertListEqual(
            list(self.qclass(
                1, 2, 3, 4, 5, 6
            ).in_out().results()),
            [1, 2, 3, 4, 5, 6]
        )

    def test_tuple_wrap(self):
        self.assertIsInstance(
            self.qclass(
                1, 2, 3, 4, 5, 6
            ).as_tuple().in_out().results(),
            tuple,
        )
        self.assertTupleEqual(
            self.qclass(
                1, 2, 3, 4, 5, 6
            ).as_tuple().in_out().results(),
            (1, 2, 3, 4, 5, 6),
        )

    def test_set_wrap(self):
        self.assertIsInstance(
            self.qclass(
                1, 2, 3, 4, 5, 6
            ).as_set().in_out().results(),
            set,
        )
        self.assertSetEqual(
            self.qclass(
                1, 2, 3, 4, 5, 6
            ).as_set().in_out().results(),
            set([1, 2, 3, 4, 5, 6]),
        )

    def test_dict_wrap(self):
        self.assertIsInstance(
            self.qclass(
                (1, 2), (3, 4), (5, 6)
            ).as_dict().in_out().results(),
            dict,
        )
        self.assertDictEqual(
            self.qclass(
                (1, 2), (3, 4), (5, 6)
            ).as_dict().in_out().results(),
            {1: 2, 3: 4, 5: 6},
        )

    def test_ascii(self):
        from stuf.six import u, b
        # auto
        self.assertEqual(
            self.qclass(
                [1], True, r't', b('i'), u('g'), None, (1,)
            ).as_many().as_ascii().in_out().end(),
            (b('[1]'), b('True'), b('t'), b('i'), b('g'), b('None'), b('(1,)'))
        )
        # man
        self._true_true_false(
            self.mclass(
                [1], True, r't', b('i'), u('g'), None, (1,)
            ).as_many().as_ascii().in_out(),
            self.assertEqual,
            (b('[1]'), b('True'), b('t'), b('i'), b('g'), b('None'), b('(1,)'))
        )

    def test_bytes(self):
        from stuf.six import u, b
        # auto
        self.assertEqual(
            self.qclass(
                [1], True, r't', b('i'), u('g'), None, (1,)
            ).as_many().as_bytes().in_out().end(),
            (b('[1]'), b('True'), b('t'), b('i'), b('g'), b('None'), b('(1,)'))
        )
        # man
        self._true_true_false(
            self.mclass(
                [1], True, r't', b('i'), u('g'), None, (1,)
            ).as_many().as_bytes().in_out(),
            self.assertEqual,
            (
        b('[1]'), b('True'), b('t'), b('i'), b('g'), b('None'), b('(1,)')
            )
        )

    def test_unicode(self):
        from stuf.six import u, b
        # auto
        self.assertEqual(
            self.qclass(
                [1], True, r't', b('i'), u('g'), None, (1,)
            ).as_many().as_unicode().in_out().end(),
            (u('[1]'), u('True'), u('t'), u('i'), u('g'), u('None'), u('(1,)'))
        )
        # man
        self._true_true_false(
            self.mclass(
                [1], True, r't', b('i'), u('g'), None, (1,)
            ).as_many().as_unicode().in_out(),
            self.assertEqual,
            (u('[1]'), u('True'), u('t'), u('i'), u('g'), u('None'), u('(1,)'))
        )
