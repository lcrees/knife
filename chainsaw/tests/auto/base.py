# -*- coding: utf-8 -*-
'''auto queuing call chain test mixins'''


class AMixin(object):

    def test_repr(self):
        from stuf.six import strings
        self.assertTrue(isinstance(
            self.qclass([1, 2, 3, 4, 5, 6]).__repr__(), strings,
        ))

    def test_extend(self):
        self.assertListEqual(
            self.qclass().extend(
                [1, 2, 3, 4, 5, 6]
            ).shift_out().end(),
            [1, 2, 3, 4, 5, 6],
        )

    def test_extendfront(self):
        self.assertListEqual(
            self.qclass().extendfront(
                [1, 2, 3, 4, 5, 6]
            ).shift_out().end(),
            [6, 5, 4, 3, 2, 1]
        )

    def test_append(self):
        autochainsaw = self.qclass().append('foo').shift_out()
        self.assertEqual(autochainsaw.end(), 'foo')

    def test_appendfront(self):
        autochainsaw = self.qclass().appendfront('foo').shift_out()
        self.assertEqual(autochainsaw.end(), 'foo')

    def test_clearin(self):
        self.assertEqual(len(list(self.qclass([1, 2, 5, 6]).clear_in())), 0)

    def test_clearout(self):
        self.assertEqual(
            len(list(self.qclass([1, 2, 5, 6]).clear_out()._outs)), 0
        )

    def test_undo(self):
        queue = self.qclass(1, 2, 3).extendfront(
            [1, 2, 3, 4, 5, 6]
        ).shift_out()
        self.assertListEqual(queue.preview(), [6, 5, 4, 3, 2, 1, 1, 2, 3])
        queue.append(1).undo().shift_out()
        self.assertListEqual(queue.preview(), [6, 5, 4, 3, 2, 1, 1, 2, 3])
        queue.append(1).append(2).undo().shift_out()
        self.assertListEqual(queue.preview(), [6, 5, 4, 3, 2, 1, 1, 2, 3, 1])
        queue.append(1).append(2).undo(2).shift_out()
        self.assertListEqual(queue.preview(), [6, 5, 4, 3, 2, 1, 1, 2, 3, 1])
        queue.undo(original=True).shift_out()
        self.assertListEqual(queue.end(), [1, 2, 3])

    def test_insync(self):
        q = self.qclass([1, 2, 3, 4, 5, 6]).shift_out()
        self.assertListEqual(list(q._ins), list(q._outs))
        q = self.qclass([1, 2, 3, 4, 5, 6]).shift_out()
        q.clear_in()
        q.shift_in()
        self.assertListEqual(list(q._ins), list(q._outs))

    def test_results(self):
        self.assertListEqual(
            list(self.qclass(
                1, 2, 3, 4, 5, 6
            ).shift_out().results()),
            [1, 2, 3, 4, 5, 6],
        )

    def test_tuple_wrap(self):
        self.assertIsInstance(
            self.qclass(
                1, 2, 3, 4, 5, 6
            ).as_tuple().shift_out().results(),
            tuple,
        )
        self.assertTupleEqual(
            self.qclass(
                1, 2, 3, 4, 5, 6
            ).as_tuple().shift_out().results(),
            (1, 2, 3, 4, 5, 6),
        )

    def test_set_wrap(self):
        self.assertIsInstance(
            self.qclass(
                1, 2, 3, 4, 5, 6
            ).as_set().shift_out().results(),
            set,
        )
        self.assertSetEqual(
            self.qclass(
                1, 2, 3, 4, 5, 6
            ).as_set().shift_out().results(),
            set([1, 2, 3, 4, 5, 6]),
        )

    def test_deque_wrap(self):
        from collections import deque
        self.assertIsInstance(
            self.qclass(
                1, 2, 3, 4, 5, 6
            ).as_deque().shift_out().results(),
            deque,
        )
        self.assertEqual(
            self.qclass(
                1, 2, 3, 4, 5, 6
            ).as_deque().shift_out().results(),
            deque([1, 2, 3, 4, 5, 6]),
        )

    def test_frozenset_wrap(self):
        self.assertIsInstance(
            self.qclass(
                1, 2, 3, 4, 5, 6
            ).as_frozenset().shift_out().results(),
            frozenset,
        )
        self.assertSetEqual(
            self.qclass(
                1, 2, 3, 4, 5, 6
            ).as_frozenset().shift_out().results(),
            frozenset([1, 2, 3, 4, 5, 6]),
        )

    def test_dict_wrap(self):
        self.assertIsInstance(
            self.qclass(
                (1, 2), (3, 4), (5, 6)
            ).as_dict().shift_out().results(),
            dict,
        )
        self.assertDictEqual(
            self.qclass(
                (1, 2), (3, 4), (5, 6)
            ).as_dict().shift_out().results(),
            {1: 2, 3: 4, 5: 6},
        )

    def test_frozenstuf_wrap(self):
        from stuf import frozenstuf
        self.assertIsInstance(
            self.qclass(
                ('a1', 2), ('a3', 4), ('a5', 6)
            ).as_frozenstuf().shift_out().results(),
            frozenstuf,
        )
        self.assertEqual(
            self.qclass(
                ('a1', 2), ('a3', 4), ('a5', 6)
            ).as_frozenstuf().shift_out().results(),
           frozenstuf({'a1': 2, 'a3': 4, 'a5': 6}),
        )

    def test_ordereddict_wrap(self):
        from stuf.utils import OrderedDict
        self.assertIsInstance(
            self.qclass(
                (1, 2), (3, 4), (5, 6)
            ).as_ordereddict().shift_out().results(),
            OrderedDict,
        )
        self.assertDictEqual(
            self.qclass(
                (1, 2), (3, 4), (5, 6)
            ).as_ordereddict().shift_out().results(),
            OrderedDict({1: 2, 3: 4, 5: 6}),
        )

    def test_orderedstuf_wrap(self):
        from stuf import orderedstuf
        self.assertIsInstance(
            self.qclass(
                (1, 2), (3, 4), (5, 6)
            ).as_orderedstuf().shift_out().results(),
            orderedstuf,
        )
        self.assertEqual(
            self.qclass(
                (1, 2), (3, 4), (5, 6)
            ).as_orderedstuf().shift_out().results(),
           orderedstuf({1: 2, 3: 4, 5: 6}),
        )

    def test_stuf_wrap(self):
        from stuf import stuf
        self.assertIsInstance(
            self.qclass(
                (1, 2), (3, 4), (5, 6)
            ).as_stuf().shift_out().results(),
            stuf,
        )
        self.assertDictEqual(
            self.qclass(
                (1, 2), (3, 4), (5, 6)
            ).as_stuf().shift_out().results(),
           stuf({1: 2, 3: 4, 5: 6}),
        )

    def test_ascii(self):
        from stuf.six import u, b
        self.assertEqual(
            self.qclass(
                [1], True, r't', b('i'), u('g'), None, (1,)
            ).as_many().as_ascii().shift_out().end(),
            [b('[1]'), b('True'), b('t'), b('i'), b('g'), b('None'), b('(1,)')]
        )

    def test_bytes(self):
        from stuf.six import u, b
        self.assertEqual(
            self.qclass(
                [1], True, r't',  b('i'), u('g'), None, (1,)
            ).as_many().as_bytes().shift_out().end(),
            [b('[1]'), b('True'), b('t'), b('i'), b('g'), b('None'), b('(1,)')]
        )

    def test_unicode(self):
        from stuf.six import u, b
        self.assertEqual(
            self.qclass(
                [1], True, r't', b('i'), u('g'), None, (1,)
            ).as_many().as_unicode().shift_out().end(),
            [u('[1]'), u('True'), u('t'), u('i'), u('g'), u('None'), u('(1,)')]
        )
