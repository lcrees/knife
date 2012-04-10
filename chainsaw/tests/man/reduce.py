# -*- coding: utf-8 -*-
'''reduce test mixins'''

from inspect import ismodule

from chainsaw.compat import port


class MSliceMixin(object):

    def test_first(self):
        manchainsaw = self.qclass(5, 4, 3, 2, 1).first()
        self.assertFalse(manchainsaw.balanced)
        manchainsaw.shift_in()
        self.assertTrue(manchainsaw.balanced)
        self.assertEqual(manchainsaw.results(), 5)
        self.assertFalse(manchainsaw.balanced)
        self._false_true_false(
            self.qclass(5, 4, 3, 2, 1).first(2), self.assertEqual, [5, 4],
        )

    def test_nth(self):
        self._false_true_false(
            self.qclass(5, 4, 3, 2, 1).nth(2), self.assertEqual, 3,
        )
        self._false_true_false(
            self.qclass(5, 4, 3, 2, 1).nth(10, 11), self.assertEqual, 11,
        )

    def test_last(self):
        manchainsaw = self.qclass(5, 4, 3, 2, 1).last()
        self.assertFalse(manchainsaw.balanced)
        manchainsaw.shift_in()
        self.assertTrue(manchainsaw.balanced)
        self.assertEqual(manchainsaw.results(), 1)
        self.assertFalse(manchainsaw.balanced)
        self._false_true_false(
            self.qclass(5, 4, 3, 2).last(2), self.assertEqual, [3, 2],
        )

    def test_initial(self):
        self._false_true_false(
            self.qclass(5, 4, 3, 2, 1).initial(),
            self.assertEqual,
            [5, 4, 3, 2],
        )

    def test_rest(self):
        self._false_true_false(
            self.qclass(5, 4, 3, 2, 1).rest(), self.assertEqual, [4, 3, 2, 1],
        )

    def test_split(self):
        self._false_true_false(
            self.qclass(
                'moe', 'larry', 'curly', 30, 40, 50, True,
            ).split(2, 'x'),
            self.assertEqual,
            [('moe', 'larry'), ('curly', 30), (40, 50), (True, 'x')],
        )


class MReduceMixin(object):

    def test_concat(self):
        self._false_true_false(
            self.qclass([1, 2], [5, [3, 4]]).concat(),
            self.assertEqual,
            [1, 2, 5, [3, 4]],
        )

    def test_flatten(self):
        self._false_true_false(
            self.qclass([[1, [2], [3, [[4]]]]]).flatten(),
            self.assertEqual,
            [1, 2, 3, 4],
        )

    def test_reduce(self):
        self._false_true_false(
            self.qclass(1, 2, 3).tap(lambda x, y: x + y).reduce(),
            self.assertEqual,
            6,
        )
        self._false_true_false(
            self.qclass(1, 2, 3).tap(lambda x, y: x + y).reduce(1),
            self.assertEqual,
            7,
        )
        self._false_true_false(
            self.qclass([0, 1], [2, 3], [4, 5]).tap(
                lambda x, y: x + y
            ).reduce(reverse=True),
            self.assertEqual,
             [4, 5, 2, 3, 0, 1],
        )
        self._false_true_false(
            self.qclass([0, 1], [2, 3], [4, 5]).tap(
                lambda x, y: x + y
            ).reduce([0, 0], True),
            self.assertEqual,
            [4, 5, 2, 3, 0, 1, 0, 0],
        )

    def test_weave(self):
        self._false_true_false(
            self.qclass(
                ['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False]
            ).weave(),
            self.assertEqual,
            ['moe', 30, True, 'larry', 40, False, 'curly', 50, False],
        )

    def test_zip(self):
        self._true_true_false(
            self.qclass(
                ['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False],
            ).zip(),
            self.assertEqual,
            [('moe', 30, True), ('larry', 40, False), ('curly', 50, False)],
        )

    def test_join(self):
        from stuf.six import u, b
        self._false_true_false(
            self.qclass([1], True, b('thing'), None, (1,)).join(u(', ')),
            self.assertEqual,
            u('[1], True, thing, None, (1,)')
        )

__all__ = sorted(name for name, obj in port.items(locals()) if not any([
    name.startswith('_'), ismodule(obj), name in ['ismodule', 'port']
]))
del ismodule
