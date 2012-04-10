# -*- coding: utf-8 -*-
'''manual balancing test mixins'''

from chainsaw.compat import unittest


class Manning(unittest.TestCase):

    def _false_true_false(self, manchainsaw, expr, comp=None):
        self.assertFalse(manchainsaw.balanced)
        manchainsaw.shift_in()
        self.assertTrue(manchainsaw.balanced)
        if comp is not None:
            expr(manchainsaw.results(), comp)
        else:
            expr(manchainsaw.results())
        self.assertFalse(manchainsaw.balanced)

    def _true_true_false(self, manchainsaw, expr, comp=None):
        self.assertTrue(manchainsaw.balanced)
        manchainsaw.shift_in()
        self.assertTrue(manchainsaw.balanced)
        if comp is not None:
            out = manchainsaw.results()
            expr(out, comp, out)
        else:
            expr(manchainsaw.results(), comp)
        self.assertFalse(manchainsaw.balanced)

    def _false_true_true(self, manchainsaw, expr, comp=None):
        self.assertFalse(manchainsaw.balanced)
        manchainsaw.shift_in()
        self.assertTrue(manchainsaw.balanced)
        if comp is not None:
            expr(manchainsaw.results(), comp)
        else:
            expr(manchainsaw.results(), comp)
        self.assertTrue(manchainsaw.balanced)
