# -*- coding: utf-8 -*-
'''tube transforming mixins'''

import re
from json import loads
from threading import local
from collections import deque
from htmlentitydefs import name2codepoint
from json.encoder import encode_basestring
from xml.sax.saxutils import escape, unescape

from stuf.six import u
from stuf.utils import OrderedDict
from stuf.core import stuf, frozenstuf, orderedstuf

from tube.compat import imap, tounicode, tobytes


class StringMixin(local):

    '''filters mixin'''

    def ascii(self, errors='strict'):
        '''
        encode each inflow thing as ascii string (regardless of type)

        @param errors: error handling (default: 'strict')
        '''
        with self._flow():
            return self._xtend(imap(
                lambda x: tobytes(x, 'ascii', errors), self._iterable,
            ))
    
    def bytes(self, encoding='utf-8', errors='strict'):
        '''
        encode each inflow thing as byte string (regardless of type)

        @param encoding: encoding for things (default: 'utf-8')
        @param errors: error handling (default: 'strict')
        '''
        with self._flow():
            return self._xtend(imap(
                lambda x: tobytes(x, encoding, errors), self._iterable,
            ))

    def htmlescape(self):
        '''escape HTML (&, <, >, ", and ')'''
        with self._flow():
            return self._xtend(imap(
                lambda x: escape(x, {'"':"&quot;", "'":'&#39;'}),
                self._iterable,
            ))

    def htmlunescape(self):
        '''
        unescape HTML
        
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
        with self._flow():
            return self._xtend(imap(unescape, self._iterable)) 

    def join(self, sep=u(''), encoding='utf-8', errors='strict'):
        '''
        join inflow into one unicode string (regardless of type)

        @param sep: join separator (default: '')
        @param encoding: encoding for things (default: 'utf-8')
        @param errors: error handling (default: 'strict')
        '''
        with self._flow():
            return self._append(tounicode(sep.join(imap(
                tounicode, self._iterable,
            )), encoding, errors))

    def jsescape(self):
        '''javascript/json escape each inflow string'''
        with self._flow():
            return self._xtend(imap(encode_basestring, self._iterable))

    def jsunescape(self):
        '''javascript/json unescape each inflow string'''
        with self._flow():
            return self._xtend(imap(loads, self._iterable))

    def unicode(self, encoding='utf-8', errors='strict'):
        '''
        decode each inflow thing as unicode string (regardless of type)

        @param encoding: encoding for things (default: 'utf-8')
        @param errors: error handling (default: 'strict')
        '''
        with self._flow():
            return self._xtend(imap(
                lambda x: tounicode(x, encoding, errors), self._iterable,
            ))

    def xmlescape(self):
        '''xml excape each inflow string'''
        with self._flow():
            return self._xtend(imap(escape, self._iterable))

    def xmlunescape(self):
        '''xml unescape each inflow string'''
        with self._flow():
            return self._xtend(imap(unescape, self._iterable))


class ExitMixin(local):

    '''tube exit mixin'''

    def reup(self):
        '''put inflow in inflow as one inflow thing'''
        with self.flow2(keep=False):
            return self._append(list(self._iterable))

    def wrap(self, wrapper):
        '''
        wrapper for outflow

        @param wrapper: an iterator class
        '''
        self._wrapper = wrapper
        return self

    def tupleout(self):
        '''set wrapper to `tuple`'''
        return self.wrap(tuple)

    def setout(self):
        '''set wrapper to `set`'''
        return self.wrap(set)

    def dequeout(self):
        '''set wrapper to `deque`'''
        return self.wrap(deque)

    def dictout(self):
        '''set wrapper to `dict`'''
        return self.wrap(dict)

    def fsetout(self):
        '''set wrapper to `frozenset`'''
        return self.wrap(frozenset)

    def fstufout(self):
        '''set wrapper to `frozenstuf`'''
        return self.wrap(frozenstuf)

    def odictout(self):
        '''set wrapper to `OrderedDict`'''
        return self.wrap(OrderedDict)

    def ostufout(self):
        '''set wrapper to `orderedstuf`'''
        return self.wrap(orderedstuf)

    def stufout(self):
        '''set wrapper to `stuf`'''
        return self.wrap(stuf)

    def listout(self):
        '''clear current wrapper'''
        return self.wrap(list)

    unwrap = listout
