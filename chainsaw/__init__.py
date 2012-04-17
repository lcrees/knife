# -*- coding: utf-8 -*-
'''Things go in. Things happen. Things come out.'''

from chainsaw.lazy import lazysaw
from chainsaw.active import activesaw

chainsaw = activesaw

__all__ = ('chainsaw', 'activesaw', 'lazysaw')
