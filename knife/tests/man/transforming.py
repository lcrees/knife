# -*- coding: utf-8 -*-
'''filtering test mixins'''

from inspect import ismodule

from knife.compat import port


class MStringQMixin(object):

    def test_join(self):
        from stuf.six import u, b
        self._true_true_false(
            self.qclass([1], True, b('thing'), None, (1,)).join(u(', ')),
            self.assertEqual,
            u('[1], True, thing, None, (1,)')
        )

    def test_ascii(self):
        from stuf.six import u, b
        self._true_true_false(
            self.qclass([1], True, r't', b('i'), u('g'), None, (1,)).ascii(),
            self.assertEqual,
            [b('[1]'), b('True'), b('t'), b('i'), b('g'), b('None'), b('(1,)')]
        )

    def test_bytes(self):
        from stuf.six import u, b
        self._true_true_false(
            self.qclass([1], True, r't', b('i'), u('g'), None, (1,)).bytes(),
            self.assertEqual,
            [
        b('[1]'), b('True'), b('t'), b('i'),  b('g'), b('None'), b('(1,)')
            ]
        )

    def test_unicode(self):
        from stuf.six import u, b
        self._true_true_false(
            self.qclass([1], True, r't', b('i'), u('g'), None, (1,)).unicode(),
            self.assertEqual,
            [u('[1]'), u('True'), u('t'), u('i'), u('g'), u('None'), u('(1,)')]
        )


__all__ = sorted(name for name, obj in port.items(locals()) if not any([
    name.startswith('_'), ismodule(obj), name in ['ismodule', 'port']
]))
del ismodule
