# -*- coding: utf-8 -*-
'''manual balancing test mixins'''

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class Manning(unittest.TestCase):

    def _false_true_false(self, mantube, expr, comp=None):
        self.assertFalse(mantube.balanced)
        mantube.balance()
        self.assertTrue(mantube.balanced)
        if comp is not None:
            expr(mantube.out(), comp)
        else:
            expr(mantube.out())
        self.assertFalse(mantube.balanced)

    def _true_true_false(self, mantube, expr, comp=None):
        self.assertTrue(mantube.balanced)
        mantube.balance()
        self.assertTrue(mantube.balanced)
        if comp is not None:
            out = mantube.out()
            expr(out, comp, out)
        else:
            expr(mantube.out())
        self.assertFalse(mantube.balanced)

    def _false_true_true(self, mantube, expr, comp=None):
        self.assertFalse(mantube.balanced)
        mantube.balance()
        self.assertTrue(mantube.balanced)
        if comp is not None:
            expr(mantube.out(), comp)
        else:
            expr(mantube.out())
        self.assertTrue(mantube.balanced)
