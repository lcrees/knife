# -*- coding: utf-8 -*-
'''auto reduce test mixins'''

from inspect import ismodule

from knife.compat import port


class AMathQMixin(object):

    def test_max(self):
        self.assertEqual(self.qclass(1, 2, 4).max().close(), 4)
        from stuf import stuf
        stooges = [
            stuf(name='moe', age=40),
            stuf(name='larry', age=50),
            stuf(name='curly', age=60),
        ]
        self.assertEqual(
            stuf(self.qclass(*stooges).tap(lambda x: x.age).max().close()),
            stuf(name='curly', age=60),
        )

    def test_min(self):
        self.assertEqual(self.qclass(10, 5, 100, 2, 1000).min().close(), 2)
        self.assertEqual(
            self.qclass(10, 5, 100, 2, 1000).tap(lambda x: x).min().close(), 2,
        )

    def test_minmax(self):
        self.assertEqual(self.qclass(1, 2, 4).minmax().close(), [1, 4])
        self.assertEqual(
            self.qclass(10, 5, 100, 2, 1000).minmax().close(), [2, 1000],
        )

    def test_median(self):
        self.assertEqual(self.qclass(4, 5, 7, 2, 1).median().close(), 4)
        self.assertEqual(self.qclass(4, 5, 7, 2, 1, 8).median().close(), 4.5)

    def test_statrange(self):
        self.assertEqual(self.qclass(3, 5, 7, 3, 11).statrange().close(), 8)

    def test_sum(self):
        self.assertEqual(self.qclass(1, 2, 3).sum().close(), 6)
        self.assertEqual(self.qclass(1, 2, 3).sum(1).close(), 7)

    def test_fsum(self):
        self.assertEqual(
            self.qclass(.1, .1, .1, .1, .1, .1, .1, .1, .1, .1).fsum().close(),
            1.0,
        )

    def test_average(self):
        self.assertEqual(
            self.qclass(10, 40, 45).average().close(), 31.666666666666668,
        )


class ATruthQMixin(object):

    def test_all(self):
        self.assertFalse(
            self.qclass(True, 1, None, 'yes').tap(bool).all().close()
        )

    def test_any(self):
        self.assertTrue(
            self.qclass(None, 0, 'yes', False).tap(bool).any().close()
        )

    def test_include(self):
        self.assertTrue(self.qclass(1, 2, 3).contains(3).close())

    def test_quantify(self):
        self.assertEqual(
            self.qclass(True, 1, None, 'yes').tap(bool).quantify().close(), 3,
        )
        self.assertEqual(
            self.qclass(None, 0, 'yes', False).tap(bool).quantify().close(), 1,
        )

    def test_common(self):
        self.assertEqual(
            self.qclass(11, 3, 5, 11, 7, 3, 11).common().close(), 11,
        )

    def test_uncommon(self):
        self.assertEqual(
            self.qclass(11, 3, 5, 11, 7, 3, 11).uncommon().close(), 7,
        )

    def test_frequency(self):
        self.assertEqual(
            self.qclass(11, 3, 5, 11, 7, 3, 11).frequency().close(),
            [(11, 3), (3, 2), (5, 1), (7, 1)]
        )


class AReduceQMixin(AMathQMixin, ATruthQMixin):
    
    def test_concat(self):
        self.assertEqual(
            self.qclass([1, 2], [5, [3, 4]]).concat().close(),
            [1, 2, 5, [3, 4]],
        )   

    def test_flatten(self):
        self.assertEqual(
            self.qclass([[1, [2], [3, [[4]]]]]).flatten().close(), [1, 2, 3, 4],
        )

    def test_pairwise(self):
        self.assertEqual(
            self.qclass(
                'moe', 30, True, 'larry', 40, False, 'curly', 50, 1, 1,
            ).pairwise().close(),
            [('moe', 30), (30, True), (True, 'larry'), ('larry', 40),
            (40, False), (False, 'curly'), ('curly', 50), (50, 1), (1, 1)]
        )

    def test_reduce(self):
        self.assertEqual(
            self.qclass(1, 2, 3).tap(lambda x, y: x + y).reduce().close(), 6,
        )
        self.assertEqual(
            self.qclass(1, 2, 3).tap(lambda x, y: x + y).reduce(1).close(), 7,
        )

    def test_reduceright(self):
        self.assertEqual(
            self.qclass([0, 1], [2, 3], [4, 5]).tap(
                lambda x, y: x + y
            ).reduceright().close(), [4, 5, 2, 3, 0, 1],
        )
        self.assertEqual(
            self.qclass([0, 1], [2, 3], [4, 5]).tap(
                lambda x, y: x + y
            ).reduceright([0, 0]).close(), [4, 5, 2, 3, 0, 1, 0, 0],
        )

    def test_roundrobin(self):
        self.assertEqual(
            self.qclass(
                ['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False]
            ).roundrobin().close(),
            ['moe', 30, True, 'larry', 40, False, 'curly', 50, False],
        )

    def test_zip(self):
        self.assertEqual(
            self.qclass(
                ['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False]
            ).zip().close(),
            [('moe', 30, True), ('larry', 40, False), ('curly', 50, False)],
        )


__all__ = sorted(name for name, obj in port.items(locals()) if not any([
    name.startswith('_'), ismodule(obj), name in ['ismodule', 'port']
]))
del ismodule
