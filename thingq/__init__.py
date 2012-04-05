# -*- coding: utf-8 -*-
'''iterator chaining, underscored by a two-headed queue'''

from thingq.support import port
from thingq.active.core import manq, autoq
from thingq.lazy.core import autoq as lazyq

thingq = autoq

__all__ = ('thingq', 'manq', 'autoq', 'lazyq' 'port')
__version__ = (0, 5, 0)
