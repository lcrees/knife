# -*- coding: utf-8 -*-
'''chainsaw base test mixins'''


class Mixin(object):

    def _false_true_false(self, manchainsaw, expr, comp=None):
        self.assertFalse(manchainsaw.balanced)
        manchainsaw.out_in()
        self.assertTrue(manchainsaw.balanced)
        if comp is not None:
            expr(manchainsaw.results(), comp)
        else:
            expr(manchainsaw.results())
        self.assertFalse(manchainsaw.balanced)

    def _true_true_false(self, manchainsaw, expr, comp=None):
        self.assertTrue(manchainsaw.balanced)
        manchainsaw.out_in()
        self.assertTrue(manchainsaw.balanced)
        if comp is not None:
            out = manchainsaw.results()
            expr(out, comp, out)
        else:
            expr(manchainsaw.results(), comp)
        self.assertFalse(manchainsaw.balanced)

    def _false_true_true(self, manchainsaw, expr, comp=None):
        self.assertFalse(manchainsaw.balanced)
        manchainsaw.out_in()
        self.assertTrue(manchainsaw.balanced)
        if comp is not None:
            expr(manchainsaw.results(), comp)
        else:
            expr(manchainsaw.results(), comp)
        self.assertTrue(manchainsaw.balanced)

    def test_repr(self):
        from stuf.six import strings
        self.assertIsInstance(
            self.qclass([1, 2, 3, 4, 5, 6]).__repr__(), strings,
        )

    def test_preview(self):
        initial = self.qclass(1, 2, 3, 4, 5, 6).in_out()
        self.assertListEqual(initial.preview(), [1, 2, 3, 4, 5, 6])
        self.assertEqual(len(initial), 6)
        self.assertListEqual(initial.in_out().end(), [1, 2, 3, 4, 5, 6])
        self.assertEqual(len(initial), 0)

    def test_extend(self):
        self.assertListEqual(
            self.qclass().extend(
                [1, 2, 3, 4, 5, 6]
            ).in_out().end(),
            [1, 2, 3, 4, 5, 6],
        )

    def test_extendfront(self):
        self.assertListEqual(
            self.qclass().extendstart(
                [1, 2, 3, 4, 5, 6]
            ).in_out().end(),
            [6, 5, 4, 3, 2, 1]
        )

    def test_append(self):
        self.assertEqual(
            self.qclass().append('foo').in_out().end(), 'foo'
        )

    def test_appendfront(self):
        self.assertEqual(
            self.qclass().appendstart('foo').in_out().end(),
            'foo'
        )

    def test_clearin(self):
        self.assertEqual(len(list(self.qclass([1, 2, 5, 6]).clear_in())), 0)

    def test_clearout(self):
        self.assertEqual(
            len(list(self.qclass([1, 2, 5, 6]).clear_out()._out)), 0
        )

    def test_undo(self):
        queue = self.qclass(1, 2, 3).extendstart(
            [1, 2, 3, 4, 5, 6]
        ).in_out()
        self.assertListEqual(queue.preview(), [6, 5, 4, 3, 2, 1, 1, 2, 3])
        queue.append(1).undo().in_out()
        self.assertListEqual(queue.preview(), [6, 5, 4, 3, 2, 1, 1, 2, 3])
        queue.append(1).append(2).undo().in_out()
        self.assertListEqual(queue.preview(), [6, 5, 4, 3, 2, 1, 1, 2, 3, 1])
        queue.append(1).append(2).undo(2).in_out()
        self.assertListEqual(queue.preview(), [6, 5, 4, 3, 2, 1, 1, 2, 3, 1])
        queue.append(1).append(2).undo(baseline=True).in_out()
        self.assertListEqual(
            queue.preview(), [6, 5, 4, 3, 2, 1, 1, 2, 3, 1, 1]
        )
        queue.undo(original=True).in_out()
        self.assertListEqual(queue.end(), [1, 2, 3])

    def test_insync(self):
        q = self.qclass(1, 2, 3, 4, 5, 6).out_in().clear_in().out_in()
        self.assertEqual(list(q._in), list(q._out))

    def test_outsync(self):
        q = self.qclass(1, 2, 3, 4, 5, 6).in_out()
        self.assertEqual(list(q._in), list(q._out))

    def test_results(self):
        self.assertListEqual(
            list(self.qclass(
                1, 2, 3, 4, 5, 6
            ).in_out().results()),
            [1, 2, 3, 4, 5, 6]
        )

    def test_tuple_wrap(self):
        self.assertIsInstance(
            self.qclass(
                1, 2, 3, 4, 5, 6
            ).as_tuple().in_out().results(),
            tuple,
        )
        self.assertTupleEqual(
            self.qclass(
                1, 2, 3, 4, 5, 6
            ).as_tuple().in_out().results(),
            (1, 2, 3, 4, 5, 6),
        )

    def test_set_wrap(self):
        self.assertIsInstance(
            self.qclass(
                1, 2, 3, 4, 5, 6
            ).as_set().in_out().results(),
            set,
        )
        self.assertSetEqual(
            self.qclass(
                1, 2, 3, 4, 5, 6
            ).as_set().in_out().results(),
            set([1, 2, 3, 4, 5, 6]),
        )

    def test_dict_wrap(self):
        self.assertIsInstance(
            self.qclass(
                (1, 2), (3, 4), (5, 6)
            ).as_dict().in_out().results(),
            dict,
        )
        self.assertDictEqual(
            self.qclass(
                (1, 2), (3, 4), (5, 6)
            ).as_dict().in_out().results(),
            {1: 2, 3: 4, 5: 6},
        )

    def test_ascii(self):
        from stuf.six import u, b
        # auto
        self.assertEqual(
            self.qclass(
                [1], True, r't', b('i'), u('g'), None, (1,)
            ).as_many().as_ascii().in_out().end(),
            (b('[1]'), b('True'), b('t'), b('i'), b('g'), b('None'), b('(1,)'))
        )
        # man
        self._true_true_false(
            self.mclass(
                [1], True, r't', b('i'), u('g'), None, (1,)
            ).as_many().as_ascii().in_out(),
            self.assertEqual,
            (b('[1]'), b('True'), b('t'), b('i'), b('g'), b('None'), b('(1,)'))
        )

    def test_bytes(self):
        from stuf.six import u, b
        # auto
        self.assertEqual(
            self.qclass(
                [1], True, r't',  b('i'), u('g'), None, (1,)
            ).as_many().as_bytes().in_out().end(),
            (b('[1]'), b('True'), b('t'), b('i'), b('g'), b('None'), b('(1,)'))
        )
        # man
        self._true_true_false(
            self.mclass(
                [1], True, r't', b('i'), u('g'), None, (1,)
            ).as_many().as_bytes().in_out(),
            self.assertEqual,
            (
        b('[1]'), b('True'), b('t'), b('i'),  b('g'), b('None'), b('(1,)')
            )
        )

    def test_unicode(self):
        from stuf.six import u, b
        # auto
        self.assertEqual(
            self.qclass(
                [1], True, r't', b('i'), u('g'), None, (1,)
            ).as_many().as_unicode().in_out().end(),
            (u('[1]'), u('True'), u('t'), u('i'), u('g'), u('None'), u('(1,)'))
        )
        # man
        self._true_true_false(
            self.mclass(
                [1], True, r't', b('i'), u('g'), None, (1,)
            ).as_many().as_unicode().in_out(),
            self.assertEqual,
            (u('[1]'), u('True'), u('t'), u('i'), u('g'), u('None'), u('(1,)'))
        )
