# -*- coding: utf-8 -*-
'''base mixins'''

import re
from json import loads
from threading import local
from collections import deque
from htmlentitydefs import name2codepoint
from json.encoder import encode_basestring
from xml.sax.saxutils import escape, unescape

from stuf.utils import OrderedDict
from stuf.core import stuf, frozenstuf, orderedstuf

from tube.compat import tounicode, tobytes


class OutflowMixin(local):

    '''tube output mixin'''

    def _html(self):
        return self.wrap(lambda x: escape(x, {'"': "&quot;", "'": '&#39;'}))

    def _js(self):
        return self.wrap(encode_basestring)

    def _unhtml(self):
        '''
        from -> John J. Lee
        http://groups.google.com/group/comp.lang.python/msg/ce3fc3330cbbac0a
        '''
        def unescape_charref(ref):
            name = ref[2:-1]
            base = 10
            if name.startswith("x"):
                name = name[1:]
                base = 16
            return unichr(int(name, base))

        def replace_entities(match):
            ent = match.group()
            if ent[1] == "#":
                return unescape_charref(ent)
            repl = name2codepoint.get(ent[1:-1])
            return unichr(repl) if repl is not None else ent

        def unescape(data):
            return re.sub(r'&#?[A-Za-z0-9]+?;', replace_entities, data)
        return self.wrap(unescape)

    @staticmethod
    def _unjs(self):
        return self.wraps(loads)

    @staticmethod
    def _unxml(self):
        return unescape

    @staticmethod
    def _xml(self):
        return escape

    def asciiout(self, errors='strict'):
        '''
        encode each inflow thing as ascii string (regardless of type)

        @param errors: error handling (default: 'strict')
        '''
        return self.wrap(lambda x: tobytes(x, 'ascii', errors))

    def bytesout(self, encoding='utf-8', errors='strict'):
        '''
        encode each inflow thing as byte string (regardless of type)

        @param encoding: encoding for things (default: 'utf-8')
        @param errors: error handling (default: 'strict')
        '''
        return self.wrap(lambda x: tobytes(x, encoding, errors))

    def dequeout(self):
        '''set wrapper to `deque`'''
        return self.wrap(deque)

    def dictout(self):
        '''set wrapper to `dict`'''
        return self.wrap(dict)

    def escapeout(self, format='html'):
        '''escape inflow'''
        return self.wrap(getattr(self, format))

    def fsetout(self):
        '''set wrapper to `frozenset`'''
        return self.wrap(frozenset)

    def fstufout(self):
        '''set wrapper to `frozenstuf`'''
        return self.wrap(frozenstuf)

    def listout(self):
        '''clear current wrapper'''
        return self.wrap(list)

    unwrap = listout

    def odictout(self):
        '''set wrapper to `OrderedDict`'''
        return self.wrap(OrderedDict)

    def ostufout(self):
        '''set wrapper to `orderedstuf`'''
        return self.wrap(orderedstuf)

    def stufout(self):
        '''set wrapper to `stuf`'''
        return self.wrap(stuf)

    def reup(self):
        '''put inflow in inflow as one inflow thing'''
        with self._flow2(keep=False):
            return self._one(list(self._iterable))

    def setout(self):
        '''set wrapper to `set`'''
        return self.wrap(set)

    def tupleout(self):
        '''set wrapper to `tuple`'''
        return self.wrap(tuple)

    def unescapeout(self, format='html'):
        '''
        unescape inflow stings
        '''
        return self.wrap(getattr(self, 'un' + format))

    def unicodeout(self, encoding='utf-8', errors='strict'):
        '''
        decode each inflow thing as unicode string (regardless of type)

        @param encoding: encoding for things (default: 'utf-8')
        @param errors: error handling (default: 'strict')
        '''
        return self.wrapper(lambda x: tounicode(x, encoding, errors))

    def wrap(self, wrapper):
        '''
        wrapper for outflow

        @param wrapper: an iterator class
        '''
        self._wrapper = wrapper
        return self
