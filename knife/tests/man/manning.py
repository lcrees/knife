# -*- coding: utf-8 -*-
'''manual balancing test mixins'''

from knife.compat import unittest


class Manning(unittest.TestCase):

    def _false_true_false(self, manknife, expr, comp=None):
        self.assertFalse(manknife.balanced)
        manknife.rebalance()
        self.assertTrue(manknife.balanced)
        if comp is not None:
            expr(manknife.results(), comp)
        else:
            expr(manknife.results())
        self.assertFalse(manknife.balanced)

    def _true_true_false(self, manknife, expr, comp=None):
        self.assertTrue(manknife.balanced)
        manknife.rebalance()
        self.assertTrue(manknife.balanced)
        if comp is not None:
            out = manknife.results()
            expr(out, comp, out)
        else:
            expr(manknife.results())
        self.assertFalse(manknife.balanced)

    def _false_true_true(self, manknife, expr, comp=None):
        self.assertFalse(manknife.balanced)
        manknife.rebalance()
        self.assertTrue(manknife.balanced)
        if comp is not None:
            expr(manknife.results(), comp)
        else:
            expr(manknife.results())
        self.assertTrue(manknife.balanced)
