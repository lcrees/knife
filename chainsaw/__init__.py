# -*- coding: utf-8 -*-
'''Things go in. Things happen. Things go out.'''

from chainsaw.compat import port
from chainsaw.lazy import lazychainsaw
from chainsaw.active import activechainsaw

chainsaw = activechainsaw

__all__ = ('chainsaw', 'activechainsaw', 'lazychainsaw' 'port')
__version__ = (0, 5, 0)
