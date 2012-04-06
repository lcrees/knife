# -*- coding: utf-8 -*-
'''thingpipe transforming mixins'''

import re
from threading import local
from json import loads
from json.encoder import encode_basestring

from htmlentitydefs import name2codepoint
from xml.sax.saxutils import escape, unescape

from stuf.six import u
from thingpipe.compat import imap, tounicode, tobytes


class StringMixin(local):

    '''filters mixin'''

    def ascii(self, errors='strict'):
        '''
        encode each incoming thing as ascii string (regardless of type)

        @param errors: error handling (default: 'strict')
        '''
        with self._context():
            return self._xtend(imap(
                lambda x: tobytes(x, 'ascii', errors), self._iterable,
            ))
    
    def bytes(self, encoding='utf-8', errors='strict'):
        '''
        encode each incoming thing as byte string (regardless of type)

        @param encoding: encoding for things (default: 'utf-8')
        @param errors: error handling (default: 'strict')
        '''
        with self._context():
            return self._xtend(imap(
                lambda x: tobytes(x, encoding, errors), self._iterable,
            ))

    def htmlescape(self):
        '''escape HTML (&, <, >, ", and ')'''
        with self._context():
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
        with self._context():
            return self._xtend(imap(unescape, self._iterable)) 

    def join(self, sep=u(''), encoding='utf-8', errors='strict'):
        '''
        join incoming things into one unicode string (regardless of type)

        @param sep: join separator (default: '')
        @param encoding: encoding for things (default: 'utf-8')
        @param errors: error handling (default: 'strict')
        '''
        with self._context():
            return self._append(tounicode(sep.join(imap(
                tounicode, self._iterable,
            )), encoding, errors))

    def jsescape(self):
        '''javascript/json escape each incoming string'''
        with self._context():
            return self._xtend(imap(encode_basestring, self._iterable))

    def jsunescape(self):
        '''javascript/json unescape each incoming string'''
        with self._context():
            return self._xtend(imap(loads, self._iterable))

    def unicode(self, encoding='utf-8', errors='strict'):
        '''
        decode each incoming thing as unicode string (regardless of type)

        @param encoding: encoding for things (default: 'utf-8')
        @param errors: error handling (default: 'strict')
        '''
        with self._context():
            return self._xtend(imap(
                lambda x: tounicode(x, encoding, errors), self._iterable,
            ))

    def xmlescape(self):
        '''xml excape each incoming string'''
        with self._context():
            return self._xtend(imap(escape, self._iterable))

    def xmlunescape(self):
        '''xml unescape each incoming string'''
        with self._context():
            return self._xtend(imap(unescape, self._iterable))
