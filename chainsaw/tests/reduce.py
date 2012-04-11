# -*- coding: utf-8 -*-
'''auto reduce test mixins'''


class SliceMixin(object):

    def test_first(self):
        # auto
        self.assertEqual(self.qclass(5, 4, 3, 2, 1).first().end(), 5)
        self.assertEqual(self.qclass(5, 4, 3, 2, 1).first(2).end(), [5, 4])
        # man
        manchainsaw = self.mclass(5, 4, 3, 2, 1).first()
        self.assertFalse(manchainsaw.balanced)
        manchainsaw.shift_in()
        self.assertTrue(manchainsaw.balanced)
        self.assertEqual(manchainsaw.results(), 5)
        self.assertFalse(manchainsaw.balanced)
        self._false_true_false(
            self.mclass(5, 4, 3, 2, 1).first(2), self.assertEqual, [5, 4],
        )

    def test_nth(self):
        # auto
        self.assertEqual(self.qclass(5, 4, 3, 2, 1).nth(2).end(), 3)
        self.assertEqual(self.qclass(5, 4, 3, 2, 1).nth(10, 11).end(), 11)
        # man
        self._false_true_false(
            self.mclass(5, 4, 3, 2, 1).nth(2), self.assertEqual, 3,
        )
        self._false_true_false(
            self.mclass(5, 4, 3, 2, 1).nth(10, 11), self.assertEqual, 11,
        )

    def test_last(self):
        # auto
        self.assertEqual(self.qclass(5, 4, 3, 2, 1).last().end(), 1)
        self.assertEqual(self.qclass(5, 4, 3, 2, 1).last(2).end(), [2, 1])
        # man
        manchainsaw = self.mclass(5, 4, 3, 2, 1).last()
        self.assertFalse(manchainsaw.balanced)
        manchainsaw.shift_in()
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

    def test_split(self):
        # auto
        self.assertEqual(
            self.qclass(
                'moe', 'larry', 'curly', 30, 40, 50, True
            ).split(2, 'x').end(),
             [('moe', 'larry'), ('curly', 30), (40, 50), (True, 'x')]
        )
        # man
        self._false_true_false(
            self.mclass(
                'moe', 'larry', 'curly', 30, 40, 50, True,
            ).split(2, 'x'),
            self.assertEqual,
            [('moe', 'larry'), ('curly', 30), (40, 50), (True, 'x')],
        )


class ReduceMixin(object):

    def test_join(self):
        from stuf.six import u, b
        # auto
        self.assertEqual(
            self.qclass(
                [1], True, b('thing'), None, (1,)
            ).join(u(', ')).end(),
            u('[1], True, thing, None, (1,)')
        )
        # auto
        self._false_true_false(
            self.mclass([1], True, b('thing'), None, (1,)).join(u(', ')),
            self.assertEqual,
            u('[1], True, thing, None, (1,)')
        )

    def test_concat(self):
        self.assertEqual(
            self.qclass([1, 2], [5, [3, 4]]).concat().end(),
            [1, 2, 5, [3, 4]],
        )
        # man
        self._false_true_false(
            self.mclass([1, 2], [5, [3, 4]]).concat(),
            self.assertEqual,
            [1, 2, 5, [3, 4]],
        )

    def test_flatten(self):
        # auto
        self.assertEqual(
            self.qclass([[1, [2], [3, [[4]]]]]).flatten().end(),
            [1, 2, 3, 4],
        )
        # man
        self._false_true_false(
            self.mclass([[1, [2], [3, [[4]]]]]).flatten(),
            self.assertEqual,
            [1, 2, 3, 4],
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
        # auto
        self.assertEqual(
            self.qclass(
                ['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False]
            ).as_many().weave().end(),
            ['moe', 30, True, 'larry', 40, False, 'curly', 50, False],
        )
        # man
        self._false_true_false(
            self.mclass(
                ['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False]
            ).as_many().weave(),
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
        # auto
        self.assertEqual(
            self.qclass(
                ['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False]
            ).as_many().zip().end(),
            [('moe', 30, True), ('larry', 40, False), ('curly', 50, False)],
        )
        # man
        self._true_true_false(
            self.mclass(
                ['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False],
            ).as_many().zip(),
            self.assertEqual,
            [('moe', 30, True), ('larry', 40, False), ('curly', 50, False)],
        )
