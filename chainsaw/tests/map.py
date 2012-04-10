# -*- coding: utf-8 -*-
'''auto mapping call chain test mixins'''

from inspect import ismodule

from chainsaw.compat import port


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

    def test_times(self):
        # auto
        def test(*args):
            return list(args)
        self.assertEqual(
            self.qclass(40, 50, 60).tap(test).times(3).end(),
            [[40, 50, 60], [40, 50, 60], [40, 50, 60]],
        )
        # man
        self._true_true_false(
            self.mclass(40, 50, 60).tap(test).times(3),
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
        manchainsaw.shift_in()
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

    def test_product(self):
        # auto
        foo = self.qclass('ABCD', 'xy').product().end()
        self.assertEqual(
            foo,
            [('A', 'x'), ('A', 'y'), ('B', 'x'), ('B', 'y'), ('C', 'x'),
            ('C', 'y'), ('D', 'x'), ('D', 'y')],
            foo,
        )
        # man
        self._false_true_false(
            self.mclass('ABCD', 'xy').product(),
            self.assertListEqual,
            [('A', 'x'), ('A', 'y'), ('B', 'x'), ('B', 'y'), ('C', 'x'),
            ('C', 'y'), ('D', 'x'), ('D', 'y')]
        )


class MapMixin(object):

    def test_factory(self):
        from stuf import stuf
        # auto
        thing = self.qclass(
            [('a', 1), ('b', 2), ('c', 3)], [('a', 1), ('b', 2), ('c', 3)]
        ).tap(stuf, factory=True).map().end()
        self.assertEqual(
            thing, [stuf(a=1, b=2, c=3), stuf(a=1, b=2, c=3)], thing
        )
        # man
        self.assertEqual(
            self.mclass(
                [('a', 1), ('b', 2), ('c', 3)], [('a', 1), ('b', 2), ('c', 3)]
            ).tap(stuf, factory=True).map().end(),
            [stuf(a=1, b=2, c=3), stuf(a=1, b=2, c=3)],
        )

    def test_map(self):
        # auto
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
        # man
        self._true_true_false(
            self.mclass(
                ((1, 2), {'a': 2}), ((2, 3), {'a': 2}), ((3, 4), {'a': 2})
            ).tap(test).map(kwargs=True),
            self.assertEqual,
            [6, 10, 14],
        )
        self._true_true_false(
            self.mclass(1, 2, 3).tap(lambda x: x * 3).map(),
            self.assertEqual,
            [3, 6, 9],
        )
        self._true_true_false(
            self.mclass(
                (1, 2), (2, 3), (3, 4)
            ).tap(lambda x, y: x * y).map(args=True),
            self.assertEqual,
            [2, 6, 12],
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


__all__ = sorted(name for name, obj in port.items(locals()) if not any([
    name.startswith('_'), ismodule(obj), name in ['ismodule', 'port']
]))
del ismodule
