# -*- coding: utf-8 -*-
'''manual balancing test mixins'''

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class Manning(unittest.TestCase):

    def _false_true_false(self, manpipe, expr, comp=None):
        self.assertFalse(manpipe.balanced)
        manpipe.sync()
        self.assertTrue(manpipe.balanced)
        if comp is not None:
            expr(manpipe.out(), comp)
        else:
            expr(manpipe.out())
        self.assertFalse(manpipe.balanced)

    def _true_true_false(self, manpipe, expr, comp=None):
        self.assertTrue(manpipe.balanced)
        manpipe.sync()
        self.assertTrue(manpipe.balanced)
        if comp is not None:
            out = manpipe.out()
            expr(out, comp, out)
        else:
            expr(manpipe.out())
        self.assertFalse(manpipe.balanced)

    def _false_true_true(self, manpipe, expr, comp=None):
        self.assertFalse(manpipe.balanced)
        manpipe.sync()
        self.assertTrue(manpipe.balanced)
        if comp is not None:
            expr(manpipe.out(), comp)
        else:
            expr(manpipe.out())
        self.assertTrue(manpipe.balanced)
