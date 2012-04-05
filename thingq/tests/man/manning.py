# -*- coding: utf-8 -*-
'''manual balancing test mixins'''

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class Manning(unittest.TestCase):

    def _false_true_false(self, manq, expr, comp=None):
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        if comp is not None:
            expr(manq.out(), comp)
        else:
            expr(manq.out())
        self.assertFalse(manq.balanced)

    def _true_true_false(self, manq, expr, comp=None):
        self.assertTrue(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        if comp is not None:
            out = manq.out()
            expr(out, comp, out)
        else:
            expr(manq.out())
        self.assertFalse(manq.balanced)

    def _false_true_true(self, manq, expr, comp=None):
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        if comp is not None:
            expr(manq.out(), comp)
        else:
            expr(manq.out())
        self.assertTrue(manq.balanced)
