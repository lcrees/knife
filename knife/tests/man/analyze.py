# -*- coding: utf-8 -*-
'''ordering test mixins'''

from inspect import ismodule

from knife.compat import port


class MMathMixin(object):

    def test_max(self):
        self._false_true_false(
            self.qclass(1, 2, 4).max(), self.assertEqual, 4,
        )
        from stuf import stuf
        stooges = [
            stuf(name='moe', age=40),
            stuf(name='larry', age=50),
            stuf(name='curly', age=60),
        ]
        manknife = self.qclass(*stooges).tap(lambda x: x.age).max()
        self.assertFalse(manknife.balanced)
        manknife.rebalance()
        self.assertTrue(manknife.balanced)
        self.assertEqual(stuf(manknife.end()), stuf(name='curly', age=60))
        self.assertTrue(manknife.balanced)

    def test_min(self):
        self._false_true_false(
            self.qclass(10, 5, 100, 2, 1000).min(),
            self.assertEqual,
            2,
        )
        self._false_true_false(
            self.qclass(10, 5, 100, 2, 1000).tap(lambda x: x).min(),
            self.assertEqual,
            2,
        )

    def test_minmax(self):
        self._false_true_false(
            self.qclass(1, 2, 4).minmax(), self.assertEqual, [1, 4],
        )
        self._false_true_false(
            self.qclass(10, 5, 100, 2, 1000).minmax(),
            self.assertEqual,
            [2, 1000],
        )

    def test_sum(self):
        self._false_true_false(
            self.qclass(1, 2, 3).sum(), self.assertEqual, 6,
        )
        self._false_true_false(
            self.qclass(1, 2, 3).sum(1), self.assertEqual, 7,
        )
        self._false_true_false(
            self.qclass(
                .1, .1, .1, .1, .1, .1, .1, .1, .1, .1
            ).sum(floats=True),
            self.assertEqual,
            1.0,
        )

    def test_median(self):
        self._false_true_false(
            self.qclass(4, 5, 7, 2, 1).median(), self.assertEqual, 4,
        )
        self._false_true_false(
            self.qclass(4, 5, 7, 2, 1, 8).median(), self.assertEqual, 4.5,
        )

    def test_average(self):
        self._false_true_false(
            self.qclass(10, 40, 45).average(),
            self.assertEqual,
            31.666666666666668,
        )

    def test_range(self):
        self._false_true_false(
            self.qclass(3, 5, 7, 3, 11).range(), self.assertEqual, 8,
        )


class MTruthMixin(object):

    def test_all(self):
        self._false_true_false(
            self.qclass(True, 1, None, 'yes').tap(bool).all(),
            self.assertFalse,
        )

    def test_any(self):
        self._false_true_false(
            self.qclass(None, 0, 'yes', False).tap(bool).any(),
            self.assertTrue,
        )

    def test_quantify(self):
        self._false_true_false(
            self.qclass(True, 1, None, 'yes').tap(bool).quantify(),
            self.assertEqual,
            3,
        )
        self._false_true_false(
            self.qclass(None, 0, 'yes', False).tap(bool).quantify(),
            self.assertEqual,
            1,
        )

    def test_frequency(self):
        self._false_true_false(
            self.qclass(11, 3, 5, 11, 7, 3, 11).frequency(),
            self.assertEqual,
            [(11, 3), (3, 2), (5, 1), (7, 1)],
        )
        # most common
        self._false_true_false(
            self.qclass(11, 3, 5, 11, 7, 3, 11).common(),
            self.assertEqual,
            11,
        )
        # least common
        self._false_true_false(
            self.qclass(11, 3, 5, 11, 7, 3, 11).uncommon(),
            self.assertEqual,
            7,
        )


class MOrderMixin(object):

    def test_choice(self):
        manknife = self.qclass(1, 2, 3, 4, 5, 6).choice()
        self.assertFalse(manknife.balanced)
        manknife.rebalance()
        self.assertTrue(manknife.balanced)
        manknife.end()
        self.assertTrue(manknife.balanced)

    def test_sample(self):
        manknife = self.qclass(1, 2, 3, 4, 5, 6).sample(3)
        self.assertFalse(manknife.balanced)
        manknife.rebalance()
        self.assertTrue(manknife.balanced)
        manknife.end()
        self.assertTrue(manknife.balanced)

    def test_shuffle(self):
        manknife = self.qclass(1, 2, 3, 4, 5, 6).shuffle()
        self.assertTrue(manknife.balanced)
        manknife.rebalance()
        self.assertTrue(manknife.balanced)
        manknife.end()
        self.assertTrue(manknife.balanced)

    def test_group(self,):
        from math import floor
        self._false_true_false(
            self.qclass(1.3, 2.1, 2.4).tap(lambda x: floor(x)).groupby(),
            self.assertListEqual,
            [[1.0, [1.3]], [2.0, [2.1, 2.4]]]
        )
        self._true_true_false(
            self.qclass(1.3, 2.1, 2.4).groupby(),
            self.assertListEqual,
            [[1.3, [1.3]], [2.1, [2.1]], [2.4, [2.4]]],
        )

    def test_reverse(self):
        self._true_true_false(
            self.qclass(5, 4, 3, 2, 1).reverse(),
            self.assertEqual,
            [1, 2, 3, 4, 5],
        )

    def test_sort(self):
        from math import sin
        self._true_true_false(
            self.qclass(1, 2, 3, 4, 5, 6).tap(lambda x: sin(x)).sort(),
           self.assertListEqual,
            [5, 4, 6, 3, 1, 2],
        )
        self._true_true_false(
            self.qclass(4, 6, 65, 3, 63, 2, 4).sort(),
          self.assertListEqual,
            [2, 3, 4, 4, 6, 63, 65],
        )


__all__ = sorted(name for name, obj in port.items(locals()) if not any([
    name.startswith('_'), ismodule(obj), name in ['ismodule', 'port']
]))
del ismodule
