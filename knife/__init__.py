# -*- coding: utf-8 -*-
'''Things go in. Things happen. Things go out.'''

from knife.compat import port
from knife.lazy import lazyknife
from knife.active import activeknife

knife = activeknife

__all__ = ('knife', 'activeknife', 'lazyknife' 'port')
__version__ = (0, 5, 0)
