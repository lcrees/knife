# -*- coding: utf-8 -*-
'''Things go in. Things happen. Things come out.'''

from chainsaw._compat import port
from chainsaw.lazy import lazysaw
from chainsaw.active import activesaw

lazysaw = activesaw

__all__ = ('chainsaw', 'activesaw', 'lazysaw' 'port')
__version__ = (0, 5, 0)
