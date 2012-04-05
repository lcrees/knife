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
        self.assertListEqual(initial.syncout().end(), [1, 2, 3, 4, 5, 6])
        self.assertEqual(len(initial), 0)

    def test_extend(self):
        self.assertListEqual(
            self.qclass().extend([1, 2, 3, 4, 5, 6]).syncout().end(),
            [1, 2, 3, 4, 5, 6],
        )

    def test_outextend(self):
        self.assertListEqual(
            self.qclass().outextend([1, 2, 3, 4, 5, 6]).end(),
            [1, 2, 3, 4, 5, 6],
        )

    def test_extendleft(self):
        self.assertListEqual(
            self.qclass().extendleft([1, 2, 3, 4, 5, 6]).syncout().end(),
            [6, 5, 4, 3, 2, 1]
        )

    def test_append(self):
        self.assertEqual(
            self.qclass().append('foo').syncout().end(), 'foo'
        )

    def test_prepend(self):
        self.assertEqual(
            self.qclass().prepend('foo').syncout().end(), 'foo'
        )

    def test_inclear(self):
        self.assertEqual(len(list(self.qclass([1, 2, 5, 6]).clearin())), 0)

    def test_outclear(self):
        self.assertEqual(
            len(list(self.qclass([1, 2, 5, 6]).clearout().outgoing)), 0
        )

    ###########################################################################
    ## queue balancing ########################################################
    ###########################################################################

    def test_undo(self):
        queue = self.qclass(1, 2, 3).extendleft([1, 2, 3, 4, 5, 6]).syncout()
        self.assertListEqual(queue.snapshot(), [6, 5, 4, 3, 2, 1, 1, 2, 3])
        self.assertListEqual(queue.peek(), [6, 5, 4, 3, 2, 1, 1, 2, 3])
        queue.append(1).undo().syncout()
        self.assertListEqual(queue.snapshot(), [6, 5, 4, 3, 2, 1, 1, 2, 3])
        queue.append(1).append(2).undo().syncout()
        self.assertListEqual(queue.snapshot(), [6, 5, 4, 3, 2, 1, 1, 2, 3, 1])
        queue.append(1).append(2).undo(2).syncout()
        self.assertListEqual(queue.snapshot(), [6, 5, 4, 3, 2, 1, 1, 2, 3, 1])
        queue.undo(everything=True).syncout()
        self.assertListEqual(queue.syncout().end(), [1, 2, 3])

    def test_insync(self):
        q = self.qclass(1, 2, 3, 4, 5, 6).syncout().clearin().sync()
        self.assertEqual(list(q.incoming), list(q.outgoing))

    def test_outsync(self):
        q = self.qclass(1, 2, 3, 4, 5, 6).syncout()
        self.assertEqual(list(q.incoming), list(q.outgoing))

    ###########################################################################
    ## queue information ######################################################
    ###########################################################################

    def test_results(self):
        self.assertListEqual(
            list(self.qclass(1, 2, 3, 4, 5, 6).syncout().results()),
            [1, 2, 3, 4, 5, 6]
        )

    def test_tuple_wrap(self):
        self.assertIsInstance(
            self.qclass(1, 2, 3, 4, 5, 6).tuple_wrap().syncout().value(),
            tuple,
        )
        self.assertTupleEqual(
            self.qclass(1, 2, 3, 4, 5, 6).tuple_wrap().syncout().value(),
            (1, 2, 3, 4, 5, 6),
        )

    def test_set_wrap(self):
        self.assertIsInstance(
            self.qclass(1, 2, 3, 4, 5, 6).set_wrap().syncout().value(),
            set,
        )
        self.assertSetEqual(
            self.qclass(1, 2, 3, 4, 5, 6).set_wrap().syncout().value(),
            set([1, 2, 3, 4, 5, 6]),
        )

    def test_deque_wrap(self):
        from collections import deque
        self.assertIsInstance(
            self.qclass(1, 2, 3, 4, 5, 6).deque_wrap().syncout().value(),
            deque,
        )
        self.assertEqual(
            self.qclass(1, 2, 3, 4, 5, 6).deque_wrap().syncout().value(),
            deque([1, 2, 3, 4, 5, 6]),
        )

    def test_frozenset_wrap(self):
        self.assertIsInstance(
            self.qclass(1, 2, 3, 4, 5, 6).frozenset_wrap().syncout().value(),
            frozenset,
        )
        self.assertSetEqual(
            self.qclass(1, 2, 3, 4, 5, 6).frozenset_wrap().syncout().value(),
            frozenset([1, 2, 3, 4, 5, 6]),
        )

    def test_dict_wrap(self):
        self.assertIsInstance(
            self.qclass(
                (1, 2), (3, 4), (5, 6)
            ).dict_wrap().syncout().value(),
            dict,
        )
        self.assertDictEqual(
            self.qclass(
                (1, 2), (3, 4), (5, 6)
            ).dict_wrap().syncout().value(),
            {1: 2, 3: 4, 5: 6},
        )

    def test_frozenstuf_wrap(self):
        from stuf import frozenstuf
        self.assertIsInstance(
            self.qclass(
                ('a1', 2), ('a3', 4), ('a5', 6)
            ).frozenstuf_wrap().syncout().value(),
            frozenstuf,
        )
        self.assertEqual(
            self.qclass(
                ('a1', 2), ('a3', 4), ('a5', 6)
            ).frozenstuf_wrap().syncout().value(),
           frozenstuf({'a1': 2, 'a3': 4, 'a5': 6}),
        )

    def test_ordereddict_wrap(self):
        from stuf.utils import OrderedDict
        self.assertIsInstance(
            self.qclass(
                (1, 2), (3, 4), (5, 6)
            ).ordereddict_wrap().syncout().value(),
            OrderedDict,
        )
        self.assertDictEqual(
            self.qclass(
                (1, 2), (3, 4), (5, 6)
            ).ordereddict_wrap().syncout().value(),
            OrderedDict({1: 2, 3: 4, 5: 6}),
        )

    def test_orderedstuf_wrap(self):
        from stuf import orderedstuf
        self.assertIsInstance(
            self.qclass(
                (1, 2), (3, 4), (5, 6)
            ).orderedstuf_wrap().syncout().value(),
            orderedstuf,
        )
        self.assertEqual(
            self.qclass(
                (1, 2), (3, 4), (5, 6)
            ).orderedstuf_wrap().syncout().value(),
           orderedstuf({1: 2, 3: 4, 5: 6}),
        )

    def test_stuf_wrap(self):
        from stuf import stuf
        self.assertIsInstance(
            self.qclass(
                (1, 2), (3, 4), (5, 6)
            ).stuf_wrap().syncout().value(),
            stuf,
        )
        self.assertDictEqual(
            self.qclass(
                (1, 2), (3, 4), (5, 6)
            ).stuf_wrap().syncout().value(),
           stuf({1: 2, 3: 4, 5: 6}),
        )
