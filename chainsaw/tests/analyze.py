# -*- coding: utf-8 -*-
'''ordering test mixins'''


class NumberMixin(object):

    def test_max(self):
        # auto
        self.assertEqual(self.qclass.as_auto()(1, 2, 4).max().end(), 4)
        from stuf import stuf
        stooges = [
            stuf(name='moe', age=40),
            stuf(name='larry', age=50),
            stuf(name='curly', age=60),
        ]
        self.assertEqual(
            stuf(self.qclass(*stooges).tap(lambda x: x.age).max().end()),
            stuf(name='curly', age=60),
        )
        # man
        self._false_true_false(
            self.mclass.as_manual()(1, 2, 4).max(), self.assertEqual, 4,
        )
        stooges = [
            stuf(name='moe', age=40),
            stuf(name='larry', age=50),
            stuf(name='curly', age=60),
        ]
        manchainsaw = self.mclass(*stooges).tap(lambda x: x.age).max()
        self.assertFalse(manchainsaw.balanced)
        manchainsaw.shift_in()
        self.assertTrue(manchainsaw.balanced)
        self.assertEqual(stuf(manchainsaw.end()), stuf(name='curly', age=60))
        self.assertTrue(manchainsaw.balanced)

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
        manchainsaw.shift_in()
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
        self._true_true_false(
            self.mclass(1, 2, 3, 4, 5, 6).tap(lambda x: sin(x)).sort(),
           self.assertListEqual,
            [5, 4, 6, 3, 1, 2],
        )
        self._true_true_false(
            self.mclass(4, 6, 65, 3, 63, 2, 4).sort(),
          self.assertListEqual,
            [2, 3, 4, 4, 6, 63, 65],
        )
