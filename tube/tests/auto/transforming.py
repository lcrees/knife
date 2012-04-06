# -*- coding: utf-8 -*-
'''auto filtering call chain test mixins'''

from inspect import ismodule

from tube.compat import port


class AStringQMixin(object):

    def test_join(self):
        from stuf.six import u, b
        self.assertEqual(
            self.qclass([1], True, b('thing'), None, (1,)).join(u(', ')).end(),
            u('[1], True, thing, None, (1,)')
        )

    def test_ascii(self):
        from stuf.six import u, b
        self.assertEqual(
            self.qclass(
                [1], True, r't', b('i'), u('g'), None, (1,)
            ).ascii().end(),
            [b('[1]'), b('True'), b('t'), b('i'), b('g'), b('None'), b('(1,)')]
        )

    def test_bytes(self):
        from stuf.six import u, b
        self.assertEqual(
            self.qclass(
                [1], True, r't',  b('i'), u('g'), None, (1,)
            ).bytes().end(),
            [b('[1]'), b('True'), b('t'), b('i'), b('g'), b('None'), b('(1,)')]
        )

    def test_unicode(self):
        from stuf.six import u, b
        self.assertEqual(
            self.qclass(
                [1], True, r't', b('i'), u('g'), None, (1,)
            ).unicode().end(),
            [u('[1]'), u('True'), u('t'), u('i'), u('g'), u('None'), u('(1,)')]
        )

__all__ = sorted(name for name, obj in port.items(locals()) if not any([
    name.startswith('_'), ismodule(obj), name in ['ismodule', 'port']
]))
del ismodule
del port
