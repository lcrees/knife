# -*- coding: utf-8 -*-
'''ordering test mixins'''

from inspect import ismodule

from chainsaw.compat import port


class MathMixin(object):

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
        self.assertEqual(self.qclass(1, 2, 4).minmax().end(), [1, 4])
        self.assertEqual(
            self.qclass(10, 5, 100, 2, 1000).minmax().end(), [2, 1000],
        )
        # man
        self._false_true_false(
            self.mclass(1, 2, 4).minmax(), self.assertEqual, [1, 4],
        )
        self._false_true_false(
            self.mclass(10, 5, 100, 2, 1000).minmax(),
            self.assertEqual,
            [2, 1000],
        )

    def test_sum(self):
        # auto
        self.assertEqual(self.qclass(1, 2, 3).sum().end(), 6)
        self.assertEqual(self.qclass(1, 2, 3).sum(1).end(), 7)
        self.assertEqual(
            self.qclass(
                .1, .1, .1, .1, .1, .1, .1, .1, .1, .1
            ).sum(floats=True).end(),
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
            ).sum(floats=True),
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


class TruthMixin(object):

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

    def test_quantify(self):
        # auto
        self.assertEqual(
            self.qclass(True, 1, None, 'yes').tap(bool).quantify().end(), 3,
        )
        self.assertEqual(
            self.qclass(None, 0, 'yes', False).tap(bool).quantify().end(), 1,
        )
        # man
        self._false_true_false(
            self.mclass(True, 1, None, 'yes').tap(bool).quantify(),
            self.assertEqual,
            3,
        )
        self._false_true_false(
            self.mclass(None, 0, 'yes', False).tap(bool).quantify(),
            self.assertEqual,
            1,
        )

    def test_frequency(self):
        # auto
        common = self.qclass(11, 3, 5, 11, 7, 3, 11).frequency().end()
        self.assertEqual(common[2], [(11, 3), (3, 2), (5, 1), (7, 1)])
        # most common
        self.assertEqual(common[1], 11)
        # least common
        self.assertEqual(common[0], 7)
        # man
        self._false_true_false(
            self.mclass(11, 3, 5, 11, 7, 3, 11).frequency(),
            self.assertEqual,
            (7, 11, [(11, 3), (3, 2), (5, 1), (7, 1)]),
        )


class OrderMixin(object):

    def test_choice(self):
        # auto
        self.assertEqual(len(list(self.qclass(1, 2, 3, 4, 5, 6).choice())), 1)
        # man
        manchainsaw = self.mclass(1, 2, 3, 4, 5, 6).choice()
        self.assertFalse(manchainsaw.balanced)
        manchainsaw.shift_in()
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
        manchainsaw.shift_in()
        self.assertTrue(manchainsaw.balanced)
        manchainsaw.end()
        self.assertTrue(manchainsaw.balanced)

    def test_shuffle(self):
        # auto
        self.assertEqual(
            len(self.qclass(1, 2, 3, 4, 5, 6).shuffle()),
            len([5, 4, 6, 3, 1, 2]),
        )
        # man
        manchainsaw = self.mclass(1, 2, 3, 4, 5, 6).shuffle()
        self.assertTrue(manchainsaw.balanced)
        manchainsaw.shift_in()
        self.assertTrue(manchainsaw.balanced)
        manchainsaw.end()
        self.assertTrue(manchainsaw.balanced)

    def test_group(self,):
        # auto
        from math import floor
        self.assertEqual(
        self.qclass(1.3, 2.1, 2.4).tap(lambda x: floor(x)).groupby().end(),
            [(1.0, (1.3,)), (2.0, (2.1, 2.4))]
        )
        self.assertEqual(
            self.qclass(1.3, 2.1, 2.4).groupby().end(),
            [(1.3, (1.3,)), (2.1, (2.1,)), (2.4, (2.4,))],
        )
        # man
        self._false_true_false(
            self.mclass(1.3, 2.1, 2.4).tap(lambda x: floor(x)).groupby(),
            self.assertListEqual,
            [(1.0, (1.3,)), (2.0, (2.1, 2.4))]
        )
        self._true_true_false(
            self.mclass(1.3, 2.1, 2.4).groupby(),
            self.assertListEqual,
            [(1.3, (1.3,)), (2.1, (2.1,)), (2.4, (2.4,))],
        )

    def test_reverse(self):
        # auto
        self.assertEqual(
            self.qclass(5, 4, 3, 2, 1).reverse().end(), [1, 2, 3, 4, 5],
        )
        # man
        self._true_true_false(
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


__all__ = sorted(name for name, obj in port.items(locals()) if not any([
    name.startswith('_'), ismodule(obj), name in ['ismodule', 'port']
]))
del ismodule
