# -*- coding: utf-8 -*-
'''Things go in. Things happen. Things go out.'''

from thingpipe.compat import port
from thingpipe.lazy import lazypipe
from thingpipe.active import activepipe

thingpipe = activepipe

__all__ = ('thingpipe', 'activepipe', 'lazypipe' 'port')
__version__ = (0, 5, 0)
