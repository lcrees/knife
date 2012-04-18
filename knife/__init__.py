# -*- coding: utf-8 -*-
'''Things go in. Things happen. Things come out.'''

from knife.lazy import lazyknife
from knife.active import activeknife

knife = activeknife

__all__ = ('knife', 'activeknife', 'lazyknife')
