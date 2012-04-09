# -*- coding: utf-8 -*-
'''manual call chain queuing test mixins'''


class MQMixin(object):

    ###########################################################################
    ## queue manipulation #####################################################
    ###########################################################################

    def test_factory(self):
        from stuf import stuf
        self.assertDictEqual(
            self.qclass(
                ('a', 1), ('b', 2), ('c', 3)
            ).reup().tap(stuf, factory=True).map().end(),
            stuf(a=1, b=2, c=3),
        )

    def test_repr(self):
        from stuf.six import strings
        self.assertIsInstance(
            self.qclass([1, 2, 3, 4, 5, 6]).__repr__(), strings,
        )

    def test_preview(self):
        initial = self.qclass(1, 2, 3, 4, 5, 6)
        self.assertListEqual(initial.preview(), [1, 2, 3, 4, 5, 6])
        self.assertEqual(len(initial), 6)
        self.assertListEqual(
            initial.rebalance(reverse=True).end(), [1, 2, 3, 4, 5, 6]
        )
        self.assertEqual(len(initial), 0)

    def test_extend(self):
        self.assertListEqual(
            self.qclass().extend(
                [1, 2, 3, 4, 5, 6]
            ).rebalance(reverse=True).end(),
            [1, 2, 3, 4, 5, 6],
        )

    def test_extendfront(self):
        self.assertListEqual(
            self.qclass().extendfront(
                [1, 2, 3, 4, 5, 6]
            ).rebalance(reverse=True).end(),
            [6, 5, 4, 3, 2, 1]
        )

    def test_append(self):
        self.assertEqual(
            self.qclass().append('foo').rebalance(reverse=True).end(), 'foo'
        )

    def test_appendfront(self):
        self.assertEqual(
            self.qclass().appendfront('foo').rebalance(reverse=True).end(),
            'foo'
        )

    def test_inclear(self):
        self.assertEqual(len(list(self.qclass([1, 2, 5, 6]).clearin())), 0)

    def test_outclear(self):
        self.assertEqual(
            len(list(self.qclass([1, 2, 5, 6]).clearvalue()._outflow)), 0
        )

    ###########################################################################
    ## queue balancing ########################################################
    ###########################################################################

    def test_undo(self):
        queue = self.qclass(1, 2, 3).extendfront(
            [1, 2, 3, 4, 5, 6]
        ).rebalance(reverse=True)
        self.assertListEqual(queue.snapshot(), [6, 5, 4, 3, 2, 1, 1, 2, 3])
        self.assertListEqual(queue.preview(), [6, 5, 4, 3, 2, 1, 1, 2, 3])
        queue.append(1).undo().rebalance(reverse=True)
        self.assertListEqual(queue.snapshot(), [6, 5, 4, 3, 2, 1, 1, 2, 3])
        queue.append(1).append(2).undo().rebalance(reverse=True)
        self.assertListEqual(queue.snapshot(), [6, 5, 4, 3, 2, 1, 1, 2, 3, 1])
        queue.append(1).append(2).undo(2).rebalance(reverse=True)
        self.assertListEqual(queue.snapshot(), [6, 5, 4, 3, 2, 1, 1, 2, 3, 1])
        queue.undo(everything=True).rebalance(reverse=True)
        self.assertListEqual(queue.rebalance(reverse=True).end(), [1, 2, 3])

    def test_insync(self):
        q = self.qclass(1, 2, 3, 4, 5, 6).rebalance(
            reverse=True
        ).clearin().rebalance()
        self.assertEqual(list(q._inflow), list(q._outflow))

    def test_outsync(self):
        q = self.qclass(1, 2, 3, 4, 5, 6).rebalance(reverse=True)
        self.assertEqual(list(q._inflow), list(q._outflow))

    ###########################################################################
    ## queue information ######################################################
    ###########################################################################

    def test_results(self):
        self.assertListEqual(
            list(self.qclass(
                1, 2, 3, 4, 5, 6
            ).rebalance(reverse=True).results()),
            [1, 2, 3, 4, 5, 6]
        )

    def test_tuple_wrap(self):
        self.assertIsInstance(
            self.qclass(
                1, 2, 3, 4, 5, 6
            ).tuplevalue().rebalance(reverse=True).results(),
            tuple,
        )
        self.assertTupleEqual(
            self.qclass(
                1, 2, 3, 4, 5, 6
            ).tuplevalue().rebalance(reverse=True).results(),
            (1, 2, 3, 4, 5, 6),
        )

    def test_set_wrap(self):
        self.assertIsInstance(
            self.qclass(
                1, 2, 3, 4, 5, 6
            ).setvalue().rebalance(reverse=True).results(),
            set,
        )
        self.assertSetEqual(
            self.qclass(
                1, 2, 3, 4, 5, 6
            ).setvalue().rebalance(reverse=True).results(),
            set([1, 2, 3, 4, 5, 6]),
        )

    def test_deque_wrap(self):
        from collections import deque
        self.assertIsInstance(
            self.qclass(
                1, 2, 3, 4, 5, 6
            ).dequevalue().rebalance(reverse=True).results(),
            deque,
        )
        self.assertEqual(
            self.qclass(
                1, 2, 3, 4, 5, 6
            ).dequevalue().rebalance(reverse=True).results(),
            deque([1, 2, 3, 4, 5, 6]),
        )

    def test_frozenset_wrap(self):
        self.assertIsInstance(
            self.qclass(
                1, 2, 3, 4, 5, 6
            ).fsetvalue().rebalance(reverse=True).results(),
            frozenset,
        )
        self.assertSetEqual(
            self.qclass(
                1, 2, 3, 4, 5, 6
            ).fsetvalue().rebalance(reverse=True).results(),
            frozenset([1, 2, 3, 4, 5, 6]),
        )

    def test_dict_wrap(self):
        self.assertIsInstance(
            self.qclass(
                (1, 2), (3, 4), (5, 6)
            ).dictvalue().rebalance(reverse=True).results(),
            dict,
        )
        self.assertDictEqual(
            self.qclass(
                (1, 2), (3, 4), (5, 6)
            ).dictvalue().rebalance(reverse=True).results(),
            {1: 2, 3: 4, 5: 6},
        )

    def test_frozenstuf_wrap(self):
        from stuf import frozenstuf
        self.assertIsInstance(
            self.qclass(
                ('a1', 2), ('a3', 4), ('a5', 6)
            ).fstufvalue().rebalance(reverse=True).results(),
            frozenstuf,
        )
        self.assertEqual(
            self.qclass(
                ('a1', 2), ('a3', 4), ('a5', 6)
            ).fstufvalue().rebalance(reverse=True).results(),
           frozenstuf({'a1': 2, 'a3': 4, 'a5': 6}),
        )

    def test_ordereddict_wrap(self):
        from stuf.utils import OrderedDict
        self.assertIsInstance(
            self.qclass(
                (1, 2), (3, 4), (5, 6)
            ).odictvalue().rebalance(reverse=True).results(),
            OrderedDict,
        )
        self.assertDictEqual(
            self.qclass(
                (1, 2), (3, 4), (5, 6)
            ).odictvalue().rebalance(reverse=True).results(),
            OrderedDict({1: 2, 3: 4, 5: 6}),
        )

    def test_orderedstuf_wrap(self):
        from stuf import orderedstuf
        self.assertIsInstance(
            self.qclass(
                (1, 2), (3, 4), (5, 6)
            ).ostufvalue().rebalance(reverse=True).results(),
            orderedstuf,
        )
        self.assertEqual(
            self.qclass(
                (1, 2), (3, 4), (5, 6)
            ).ostufvalue().rebalance(reverse=True).results(),
           orderedstuf({1: 2, 3: 4, 5: 6}),
        )

    def test_stuf_wrap(self):
        from stuf import stuf
        self.assertIsInstance(
            self.qclass(
                (1, 2), (3, 4), (5, 6)
            ).stufvalue().rebalance(reverse=True).results(),
            stuf,
        )
        self.assertDictEqual(
            self.qclass(
                (1, 2), (3, 4), (5, 6)
            ).stufvalue().rebalance(reverse=True).results(),
           stuf({1: 2, 3: 4, 5: 6}),
        )

    def test_ascii(self):
        from stuf.six import u, b
        self._true_true_false(
            self.qclass([1], True, r't', b('i'), u('g'), None, (1,)).ascii(),
            self.assertEqual,
            [b('[1]'), b('True'), b('t'), b('i'), b('g'), b('None'), b('(1,)')]
        )

    def test_bytes(self):
        from stuf.six import u, b
        self._true_true_false(
            self.qclass([1], True, r't', b('i'), u('g'), None, (1,)).bytes(),
            self.assertEqual,
            [
        b('[1]'), b('True'), b('t'), b('i'),  b('g'), b('None'), b('(1,)')
            ]
        )

    def test_unicode(self):
        from stuf.six import u, b
        self._true_true_false(
            self.qclass([1], True, r't', b('i'), u('g'), None, (1,)).unicode(),
            self.assertEqual,
            [u('[1]'), u('True'), u('t'), u('i'), u('g'), u('None'), u('(1,)')]
        )
