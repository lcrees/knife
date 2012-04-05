# -*- coding: utf-8 -*-
'''manual call chain queuing test mixins'''


class MQMixin(object):

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
        self.assertEqual(
            self.qclass().extend([1, 2, 3, 4, 5, 6]).syncout().end(),
            [1, 2, 3, 4, 5, 6],
        )

    def test_outextend(self):
        self.assertEqual(
            self.qclass().outextend([1, 2, 3, 4, 5, 6]).end(),
            [1, 2, 3, 4, 5, 6],
        )

    def test_extendleft(self):
        self.assertEqual(
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
        self.assertEqual(
            list(self.qclass(1, 2, 3, 4, 5, 6).syncout().results()),
            [1, 2, 3, 4, 5, 6]
        )
