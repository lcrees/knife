# -*- coding: utf-8 -*-
'''auto mapping call chain test mixins'''

from inspect import ismodule

from knife.compat import port


class ARepeatMixin(object):

    def test_repeat(self):
        self.assertEqual(
            self.qclass(40, 50, 60).repeat(3).end(),
            [(40, 50, 60), (40, 50, 60), (40, 50, 60)],
        )

    def test_times(self):
        def test(*args):
            return list(args)
        self.assertEqual(
            self.qclass(40, 50, 60).tap(test).times(3).end(),
            [[40, 50, 60], [40, 50, 60], [40, 50, 60]],
        )

    def test_copy(self):
        testlist = [[1, [2, 3]], [4, [5, 6]]]
        newlist = self.qclass(testlist).copy().end()
        self.assertFalse(newlist is testlist)
        self.assertListEqual(newlist, testlist)
        self.assertFalse(newlist[0] is testlist[0])
        self.assertListEqual(newlist[0], testlist[0])
        self.assertFalse(newlist[1] is testlist[1])
        self.assertListEqual(newlist[1], testlist[1])

    def test_permutations(self):
        self.assertEqual(
            self.qclass(40, 50, 60).permutations(2).end(),
            [(40, 50), (40, 60), (50, 40), (50, 60), (60, 40), (60, 50)],
        )

    def test_combination(self):
        self.assertEqual(
            self.qclass(40, 50, 60).combinations(2).end(),
            [(40, 50), (40, 60), (50, 60)],
        )

    def test_product(self):
        foo = self.qclass('ABCD', 'xy').product().end()
        self.assertEqual(
            foo,
            [('A', 'x'), ('A', 'y'), ('B', 'x'), ('B', 'y'), ('C', 'x'),
            ('C', 'y'), ('D', 'x'), ('D', 'y')],
            foo,
        )


class AMapMixin(object):

    def test_factory(self):
        from stuf import stuf
        thing = self.qclass(
            ('a', 1), ('b', 2), ('c', 3)
        ).tap(stuf, factory=True).reup().map().shift_in().end()
        self.assertEqual(thing, stuf(a=1, b=2, c=3), thing)

    def test_map(self):
        def test(*args, **kw):
            return sum(args) * kw['a']
        self.assertEqual(
            self.qclass(
                ((1, 2), {'a': 2}), ((2, 3), {'a': 2}), ((3, 4), {'a': 2})
            ).tap(test).map(kwargs=True).end(),
            [6, 10, 14],
        )
        self.assertEqual(
            self.qclass(1, 2, 3).tap(lambda x: x * 3).map().end(), [3, 6, 9],
        )
        self.assertEqual(
            self.qclass(
                (1, 2), (2, 3), (3, 4)
            ).tap(lambda x, y: x * y).map(args=True).end(), [2, 6, 12],
        )

    def test_invoke(self):
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
        self.assertEqual(
            self.qclass([5, 1, 7], [3, 2, 1])
            .arguments(1).invoke('index').end(),
            [1, 2],
        )
        self.assertEqual(
            self.qclass([5, 1, 7], [3, 2, 1]).invoke('sort').end(),
            [[1, 5, 7], [1, 2, 3]],
        )

__all__ = sorted(name for name, obj in port.items(locals()) if not any([
    name.startswith('_'), ismodule(obj), name in ['ismodule', 'port']
]))
del ismodule
