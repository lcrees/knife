# -*- coding: utf-8 -*-
'''auto queuing call chain test mixins'''


class AQMixin(object):

    ###########################################################################
    ## queue manipulation #####################################################
    ###########################################################################

    def test_repr(self):
        from stuf.six import strings
        self.assertTrue(isinstance(
            self.qclass([1, 2, 3, 4, 5, 6]).__repr__(), strings,
        ))

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
            self.qclass().extendout([1, 2, 3, 4, 5, 6]).end(),
            [1, 2, 3, 4, 5, 6],
        )

    def test_extendleft(self):
        self.assertListEqual(
            self.qclass().extendleft([1, 2, 3, 4, 5, 6]).syncout().end(),
            [6, 5, 4, 3, 2, 1]
        )

    def test_append(self):
        autoq = self.qclass().append('foo').syncout()
        self.assertEqual(autoq.end(), 'foo')

    def test_prepend(self):
        autoq = self.qclass().prepend('foo').syncout()
        self.assertEqual(autoq.end(), 'foo')

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
        queue.undo(everything=True).syncout()
        self.assertListEqual(queue.syncout().end(), [1, 2, 3])

    def test_insync(self):
        q = self.qclass([1, 2, 3, 4, 5, 6]).syncout().clearin().sync()
        self.assertListEqual(list(q.incoming), list(q.outgoing))

    def test_outsync(self):
        q = self.qclass([1, 2, 3, 4, 5, 6]).syncout()
        self.assertListEqual(list(q.incoming), list(q.outgoing))

    ##########################################################################
    # queue information ######################################################
    ##########################################################################

    def test_results(self):
        self.assertListEqual(
            list(self.qclass(1, 2, 3, 4, 5, 6).syncout().results()),
            [1, 2, 3, 4, 5, 6],
        )

    def test_tuple_wrap(self):
        self.assertIsInstance(
            self.qclass(1, 2, 3, 4, 5, 6).tupleout().syncout().out(),
            tuple,
        )
        self.assertTupleEqual(
            self.qclass(1, 2, 3, 4, 5, 6).tupleout().syncout().out(),
            (1, 2, 3, 4, 5, 6),
        )

    def test_set_wrap(self):
        self.assertIsInstance(
            self.qclass(1, 2, 3, 4, 5, 6).setout().syncout().out(),
            set,
        )
        self.assertSetEqual(
            self.qclass(1, 2, 3, 4, 5, 6).setout().syncout().out(),
            set([1, 2, 3, 4, 5, 6]),
        )

    def test_deque_wrap(self):
        from collections import deque
        self.assertIsInstance(
            self.qclass(1, 2, 3, 4, 5, 6).dequeout().syncout().out(),
            deque,
        )
        self.assertEqual(
            self.qclass(1, 2, 3, 4, 5, 6).dequeout().syncout().out(),
            deque([1, 2, 3, 4, 5, 6]),
        )

    def test_frozenset_wrap(self):
        self.assertIsInstance(
            self.qclass(1, 2, 3, 4, 5, 6).fsetout().syncout().out(),
            frozenset,
        )
        self.assertSetEqual(
            self.qclass(1, 2, 3, 4, 5, 6).fsetout().syncout().out(),
            frozenset([1, 2, 3, 4, 5, 6]),
        )

    def test_dict_wrap(self):
        self.assertIsInstance(
            self.qclass(
                (1, 2), (3, 4), (5, 6)
            ).dictout().syncout().out(),
            dict,
        )
        self.assertDictEqual(
            self.qclass(
                (1, 2), (3, 4), (5, 6)
            ).dictout().syncout().out(),
            {1: 2, 3: 4, 5: 6},
        )

    def test_frozenstuf_wrap(self):
        from stuf import frozenstuf
        self.assertIsInstance(
            self.qclass(
                ('a1', 2), ('a3', 4), ('a5', 6)
            ).fstufout().syncout().out(),
            frozenstuf,
        )
        self.assertEqual(
            self.qclass(
                ('a1', 2), ('a3', 4), ('a5', 6)
            ).fstufout().syncout().out(),
           frozenstuf({'a1': 2, 'a3': 4, 'a5': 6}),
        )

    def test_ordereddict_wrap(self):
        from stuf.utils import OrderedDict
        self.assertIsInstance(
            self.qclass(
                (1, 2), (3, 4), (5, 6)
            ).odictout().syncout().out(),
            OrderedDict,
        )
        self.assertDictEqual(
            self.qclass(
                (1, 2), (3, 4), (5, 6)
            ).odictout().syncout().out(),
            OrderedDict({1: 2, 3: 4, 5: 6}),
        )

    def test_orderedstuf_wrap(self):
        from stuf import orderedstuf
        self.assertIsInstance(
            self.qclass(
                (1, 2), (3, 4), (5, 6)
            ).ostufout().syncout().out(),
            orderedstuf,
        )
        self.assertEqual(
            self.qclass(
                (1, 2), (3, 4), (5, 6)
            ).ostufout().syncout().out(),
           orderedstuf({1: 2, 3: 4, 5: 6}),
        )

    def test_stuf_wrap(self):
        from stuf import stuf
        self.assertIsInstance(
            self.qclass(
                (1, 2), (3, 4), (5, 6)
            ).stufout().syncout().out(),
            stuf,
        )
        self.assertDictEqual(
            self.qclass(
                (1, 2), (3, 4), (5, 6)
            ).stufout().syncout().out(),
           stuf({1: 2, 3: 4, 5: 6}),
        )
