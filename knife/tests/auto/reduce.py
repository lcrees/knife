# -*- coding: utf-8 -*-
'''auto reduce test mixins'''

from inspect import ismodule

from knife.compat import port


class ASliceMixin(object):

    def test_first(self):
        self.assertEqual(self.qclass(5, 4, 3, 2, 1).first().end(), 5)
        self.assertEqual(self.qclass(5, 4, 3, 2, 1).first(2).end(), [5, 4])

    def test_nth(self):
        self.assertEqual(self.qclass(5, 4, 3, 2, 1).nth(2).end(), 3)
        self.assertEqual(self.qclass(5, 4, 3, 2, 1).nth(10, 11).end(), 11)

    def test_last(self):
        self.assertEqual(self.qclass(5, 4, 3, 2, 1).last().end(), 1)
        self.assertEqual(self.qclass(5, 4, 3, 2, 1).last(2).end(), [2, 1])

    def test_initial(self):
        self.assertEqual(
            self.qclass(5, 4, 3, 2, 1).initial().end(), [5, 4, 3, 2]
        )

    def test_rest(self):
        self.assertEqual(
            self.qclass(5, 4, 3, 2, 1).rest().end(), [4, 3, 2, 1],
        )

    def test_split(self):
        self.assertEqual(
            self.qclass(
                'moe', 'larry', 'curly', 30, 40, 50, True
            ).grouper(2, 'x').end(),
             [('moe', 'larry'), ('curly', 30), (40, 50), (True, 'x')]
        )


class AReduceMixin(object):

    def test_join(self):
        from stuf.six import u, b
        self.assertEqual(
            self.qclass(
                [1], True, b('thing'), None, (1,)
            ).join(u(', ')).end(),
            u('[1], True, thing, None, (1,)')
        )

    def test_concat(self):
        self.assertEqual(
            self.qclass([1, 2], [5, [3, 4]]).concat().end(),
            [1, 2, 5, [3, 4]],
        )

    def test_flatten(self):
        self.assertEqual(
            self.qclass([[1, [2], [3, [[4]]]]]).flatten().end(),
            [1, 2, 3, 4],
        )

    def test_reduce(self):
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
            ).reduceright([0, 0], True).end(), [4, 5, 2, 3, 0, 1, 0, 0],
        )

    def test_weave(self):
        self.assertEqual(
            self.qclass(
                ['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False]
            ).weave().end(),
            ['moe', 30, True, 'larry', 40, False, 'curly', 50, False],
        )

    def test_zip(self):
        self.assertEqual(
            self.qclass(
                ['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False]
            ).zip().end(),
            [('moe', 30, True), ('larry', 40, False), ('curly', 50, False)],
        )


__all__ = sorted(name for name, obj in port.items(locals()) if not any([
    name.startswith('_'), ismodule(obj), name in ['ismodule', 'port']
]))
del ismodule
