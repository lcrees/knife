# -*- coding: utf-8 -*-
'''manual call chain queuing test mixins'''


class MQMixin(object):

    ###########################################################################
    ## queue manipulation #####################################################
    ###########################################################################

    def test_repr(self):
        from stuf.six import strings
        self.assertIsInstance(
            self.qclass([1, 2, 3, 4, 5, 6]).__repr__(), strings,
        )

    def test_peek(self):
        initial = self.qclass(1, 2, 3, 4, 5, 6)
        self.assertListEqual(initial.peek(), [1, 2, 3, 4, 5, 6])
        self.assertEqual(len(initial), 6)
        self.assertListEqual(initial.balance(reverse=True).end(), [1, 2, 3, 4, 5, 6])
        self.assertEqual(len(initial), 0)

    def test_extend(self):
        self.assertListEqual(
            self.qclass().extend([1, 2, 3, 4, 5, 6]).balance(reverse=True).end(),
            [1, 2, 3, 4, 5, 6],
        )

    def test_outextend(self):
        self.assertListEqual(
            self.qclass().extendout([1, 2, 3, 4, 5, 6]).end(),
            [1, 2, 3, 4, 5, 6],
        )

    def test_extendleft(self):
        self.assertListEqual(
            self.qclass().extendleft([1, 2, 3, 4, 5, 6]).balance(reverse=True).end(),
            [6, 5, 4, 3, 2, 1]
        )

    def test_append(self):
        self.assertEqual(
            self.qclass().append('foo').balance(reverse=True).end(), 'foo'
        )

    def test_prepend(self):
        self.assertEqual(
            self.qclass().prepend('foo').balance(reverse=True).end(), 'foo'
        )

    def test_inclear(self):
        self.assertEqual(len(list(self.qclass([1, 2, 5, 6]).clearin())), 0)

    def test_outclear(self):
        self.assertEqual(
            len(list(self.qclass([1, 2, 5, 6]).clearout().outflow)), 0
        )

    ###########################################################################
    ## queue balancing ########################################################
    ###########################################################################

    def test_undo(self):
        queue = self.qclass(1, 2, 3).extendleft([1, 2, 3, 4, 5, 6]).balance(reverse=True)
        self.assertListEqual(queue.snapshot(), [6, 5, 4, 3, 2, 1, 1, 2, 3])
        self.assertListEqual(queue.peek(), [6, 5, 4, 3, 2, 1, 1, 2, 3])
        queue.append(1).undo().balance(reverse=True)
        self.assertListEqual(queue.snapshot(), [6, 5, 4, 3, 2, 1, 1, 2, 3])
        queue.append(1).append(2).undo().balance(reverse=True)
        self.assertListEqual(queue.snapshot(), [6, 5, 4, 3, 2, 1, 1, 2, 3, 1])
        queue.append(1).append(2).undo(2).balance(reverse=True)
        self.assertListEqual(queue.snapshot(), [6, 5, 4, 3, 2, 1, 1, 2, 3, 1])
        queue.undo(everything=True).balance(reverse=True)
        self.assertListEqual(queue.balance(reverse=True).end(), [1, 2, 3])

    def test_insync(self):
        q = self.qclass(1, 2, 3, 4, 5, 6).balance(reverse=True).clearin().balance()
        self.assertEqual(list(q.incoming), list(q.outflow))

    def test_outsync(self):
        q = self.qclass(1, 2, 3, 4, 5, 6).balance(reverse=True)
        self.assertEqual(list(q.incoming), list(q.outflow))

    ###########################################################################
    ## queue information ######################################################
    ###########################################################################

    def test_results(self):
        self.assertListEqual(
            list(self.qclass(1, 2, 3, 4, 5, 6).balance(reverse=True).results()),
            [1, 2, 3, 4, 5, 6]
        )

    def test_tuple_wrap(self):
        self.assertIsInstance(
            self.qclass(1, 2, 3, 4, 5, 6).tupleout().balance(reverse=True).out(),
            tuple,
        )
        self.assertTupleEqual(
            self.qclass(1, 2, 3, 4, 5, 6).tupleout().balance(reverse=True).out(),
            (1, 2, 3, 4, 5, 6),
        )

    def test_set_wrap(self):
        self.assertIsInstance(
            self.qclass(1, 2, 3, 4, 5, 6).setout().balance(reverse=True).out(),
            set,
        )
        self.assertSetEqual(
            self.qclass(1, 2, 3, 4, 5, 6).setout().balance(reverse=True).out(),
            set([1, 2, 3, 4, 5, 6]),
        )

    def test_deque_wrap(self):
        from collections import deque
        self.assertIsInstance(
            self.qclass(1, 2, 3, 4, 5, 6).dequeout().balance(reverse=True).out(),
            deque,
        )
        self.assertEqual(
            self.qclass(1, 2, 3, 4, 5, 6).dequeout().balance(reverse=True).out(),
            deque([1, 2, 3, 4, 5, 6]),
        )

    def test_frozenset_wrap(self):
        self.assertIsInstance(
            self.qclass(1, 2, 3, 4, 5, 6).fsetout().balance(reverse=True).out(),
            frozenset,
        )
        self.assertSetEqual(
            self.qclass(1, 2, 3, 4, 5, 6).fsetout().balance(reverse=True).out(),
            frozenset([1, 2, 3, 4, 5, 6]),
        )

    def test_dict_wrap(self):
        self.assertIsInstance(
            self.qclass(
                (1, 2), (3, 4), (5, 6)
            ).dictout().balance(reverse=True).out(),
            dict,
        )
        self.assertDictEqual(
            self.qclass(
                (1, 2), (3, 4), (5, 6)
            ).dictout().balance(reverse=True).out(),
            {1: 2, 3: 4, 5: 6},
        )

    def test_frozenstuf_wrap(self):
        from stuf import frozenstuf
        self.assertIsInstance(
            self.qclass(
                ('a1', 2), ('a3', 4), ('a5', 6)
            ).fstufout().balance(reverse=True).out(),
            frozenstuf,
        )
        self.assertEqual(
            self.qclass(
                ('a1', 2), ('a3', 4), ('a5', 6)
            ).fstufout().balance(reverse=True).out(),
           frozenstuf({'a1': 2, 'a3': 4, 'a5': 6}),
        )

    def test_ordereddict_wrap(self):
        from stuf.utils import OrderedDict
        self.assertIsInstance(
            self.qclass(
                (1, 2), (3, 4), (5, 6)
            ).odictout().balance(reverse=True).out(),
            OrderedDict,
        )
        self.assertDictEqual(
            self.qclass(
                (1, 2), (3, 4), (5, 6)
            ).odictout().balance(reverse=True).out(),
            OrderedDict({1: 2, 3: 4, 5: 6}),
        )

    def test_orderedstuf_wrap(self):
        from stuf import orderedstuf
        self.assertIsInstance(
            self.qclass(
                (1, 2), (3, 4), (5, 6)
            ).ostufout().balance(reverse=True).out(),
            orderedstuf,
        )
        self.assertEqual(
            self.qclass(
                (1, 2), (3, 4), (5, 6)
            ).ostufout().balance(reverse=True).out(),
           orderedstuf({1: 2, 3: 4, 5: 6}),
        )

    def test_stuf_wrap(self):
        from stuf import stuf
        self.assertIsInstance(
            self.qclass(
                (1, 2), (3, 4), (5, 6)
            ).stufout().balance(reverse=True).out(),
            stuf,
        )
        self.assertDictEqual(
            self.qclass(
                (1, 2), (3, 4), (5, 6)
            ).stufout().balance(reverse=True).out(),
           stuf({1: 2, 3: 4, 5: 6}),
        )
