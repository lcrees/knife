# -*- coding: utf-8 -*-
'''auto ordering call chain test mixins'''

from inspect import ismodule

from chainsaw.compat import port


class AMathMixin(object):

    def test_max(self):
        self.assertEqual(self.qclass(1, 2, 4).max().end(), 4)
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

    def test_min(self):
        self.assertEqual(self.qclass(10, 5, 100, 2, 1000).min().end(), 2)
        self.assertEqual(
            self.qclass(10, 5, 100, 2, 1000).tap(lambda x: x).min().end(), 2,
        )

    def test_minmax(self):
        self.assertEqual(self.qclass(1, 2, 4).minmax().end(), [1, 4])
        self.assertEqual(
            self.qclass(10, 5, 100, 2, 1000).minmax().end(), [2, 1000],
        )

    def test_median(self):
        self.assertEqual(self.qclass(4, 5, 7, 2, 1).median().end(), 4)
        self.assertEqual(self.qclass(4, 5, 7, 2, 1, 8).median().end(), 4.5)

    def test_range(self):
        self.assertEqual(self.qclass(3, 5, 7, 3, 11).range().end(), 8)

    def test_sum(self):
        self.assertEqual(self.qclass(1, 2, 3).sum().end(), 6)
        self.assertEqual(self.qclass(1, 2, 3).sum(1).end(), 7)
        self.assertEqual(
            self.qclass(
                .1, .1, .1, .1, .1, .1, .1, .1, .1, .1
            ).sum(floats=True).end(),
            1.0,
        )

    def test_average(self):
        self.assertEqual(
            self.qclass(10, 40, 45).average().end(), 31.666666666666668,
        )


class ATruthMixin(object):

    def test_all(self):
        self.assertFalse(
            self.qclass(True, 1, None, 'yes').tap(bool).all().end()
        )

    def test_any(self):
        self.assertTrue(
            self.qclass(None, 0, 'yes', False).tap(bool).any().end()
        )

    def test_quantify(self):
        self.assertEqual(
            self.qclass(True, 1, None, 'yes').tap(bool).quantify().end(), 3,
        )
        self.assertEqual(
            self.qclass(None, 0, 'yes', False).tap(bool).quantify().end(), 1,
        )

    def test_frequency(self):
        common = self.qclass(11, 3, 5, 11, 7, 3, 11).frequency().end()
        self.assertEqual(common[2], [(11, 3), (3, 2), (5, 1), (7, 1)])
        # most common
        self.assertEqual(common[1], 11)
        # least common
        self.assertEqual(common[0], 7)


class AOrderMixin(object):

    '''combination mixin'''

    def test_choice(self):
        self.assertEqual(len(list(self.qclass(1, 2, 3, 4, 5, 6).choice())), 1)

    def test_sample(self):
        self.assertEqual(
            len(self.qclass(1, 2, 3, 4, 5, 6).sample(3).end()), 3,
        )

    def test_shuffle(self):
        self.assertEqual(
            len(self.qclass(1, 2, 3, 4, 5, 6).shuffle()),
            len([5, 4, 6, 3, 1, 2]),
        )

    def test_group(self,):
        from math import floor
        self.assertEqual(
        self.qclass(1.3, 2.1, 2.4).tap(lambda x: floor(x)).groupby().end(),
            [(1.0, (1.3,)), (2.0, (2.1, 2.4))]
        )
        self.assertEqual(
            self.qclass(1.3, 2.1, 2.4).groupby().end(),
            [(1.3, (1.3,)), (2.1, (2.1,)), (2.4, (2.4,))],
        )

    def test_reverse(self):
        self.assertEqual(
            self.qclass(5, 4, 3, 2, 1).reverse().end(), [1, 2, 3, 4, 5],
        )

    def test_sort(self):
        from math import sin
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


__all__ = sorted(name for name, obj in port.items(locals()) if not any([
    name.startswith('_'), ismodule(obj), name in ['ismodule', 'port']
]))
del ismodule
