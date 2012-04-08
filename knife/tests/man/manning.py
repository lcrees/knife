# -*- coding: utf-8 -*-
'''manual balancing test mixins'''

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class Manning(unittest.TestCase):

    def _false_true_false(self, manknife, expr, comp=None):
        self.assertFalse(manknife.balanced)
        manknife.balance()
        self.assertTrue(manknife.balanced)
        if comp is not None:
            expr(manknife.out(), comp)
        else:
            expr(manknife.out())
        self.assertFalse(manknife.balanced)

    def _true_true_false(self, manknife, expr, comp=None):
        self.assertTrue(manknife.balanced)
        manknife.balance()
        self.assertTrue(manknife.balanced)
        if comp is not None:
            out = manknife.out()
            expr(out, comp, out)
        else:
            expr(manknife.out())
        self.assertFalse(manknife.balanced)

    def _false_true_true(self, manknife, expr, comp=None):
        self.assertFalse(manknife.balanced)
        manknife.balance()
        self.assertTrue(manknife.balanced)
        if comp is not None:
            expr(manknife.out(), comp)
        else:
            expr(manknife.out())
        self.assertTrue(manknife.balanced)
