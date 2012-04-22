`knife` is a powerful `Python <http://docs.python.org/>`_ multitool
loosely inspired by `underscore.js <http://documentcloud.github.com/underscore/>`_
but remixed for maximum `pythonicity <http://docs.python.org/glossary.html#term-pythonic>`_. 

`knife` concentrates power that is normally dispersed across the entire
Python universe in one convenient shrink-wrapped package.

Vitals
======

`knife` works with Python 2.6, 2.7, and 3.2.

`knife` documentation is at http://readthedocs.org/docs/knife/en/latest/ or
http://packages.python.org/knife/

Installation
============

Install `knife` with `pip <http://www.pip-installer.org/en/latest/index.html>`_...::

  $ pip install knife
  [... possibly exciting stuff happening ...]
  Successfully installed knife
  
...or `easy_install <http://packages.python.org/distribute/>`_...::

  $ easy_install knife
  [... possibly exciting stuff happening ...]
  Finished processing dependencies for knife
  
...or old school by downloading `knife` from http://pypi.python.org/pypi/knife/::

  $ python setup.py install
  [... possibly exciting stuff happening ...]
  Finished processing dependencies for knife

Development
===========

 * Public repository: https://bitbucket.org/lcrees/knife.
 * Mirror: https://github.com/kwarterthieves/knife/
 * Issue tracker: https://bitbucket.org/lcrees/knife/issues
 * License: `BSD <http://www.opensource.org/licenses/bsd-license.php>`_ license

3 second *knife*
================

Things go in:

  >>> gauntlet = __(5, 4, 3, 2, 1)
  
Things get knifed:

  >>> gauntlet.initial().rest().slice(1, 2).last()

Things come out:

  >>> gauntlet.get()
  3

Slightly more *knife*
=====================

`knife` has 40 plus methods that can be `chained <https://en.wikipedia.org/
wiki/Fluent_interface>`_ into pipelines.

contrived example:
^^^^^^^^^^^^^^^^^^

  >>> from knife import __
  >>> __(5, 4, 3, 2, 1).initial().rest().slice(1, 2).last().get()
  3

Or used object-oriented style.

contrived example:
^^^^^^^^^^^^^^^^^^

  >>> from knife import knife
  >>> oo = knife(('a', 1), ('b', 2), ('c', 3))
  >>> oo.wrap(dict)
  >>> oo.map()
  >>> oo.get()
  {'a': 1, 'b': 2, 'c': 3}
  
A `knife` knife can rollback the state of things it has knifed back to results
of the immediately preceding steps, a baseline snapshot, or even the original
arguments.

contrived example:
^^^^^^^^^^^^^^^^^^
  
  >>> undone = __(1, 2, 3).prepend(1, 2, 3, 4, 5, 6)
  >>> undone.peek()
  [1, 2, 3, 4, 5, 6, 1, 2, 3]
  >>> undone.append(1).undo().peek()
  [1, 2, 3, 4, 5, 6, 1, 2, 3]
  >>> undone.append(1, 2).undo(2).peek()
  [1, 2, 3, 4, 5, 6, 1, 2, 3, 1]
  >>> undone.snapshot().append(1, 2).baseline().peek()
  [1, 2, 3, 4, 5, 6, 1, 2, 3, 1]
  >>> undone.original().peek()
  [1, 2, 3]
  >>> one.original().minmax().pipe(two).merge().back().max().get()
  1000
  >>> one.original().minmax().pipe(two).merge().back().sum().get()
  1002

`knife` knives come in two flavors: `active` and `lazy`. Active
knives evaluate the result of each method immediately it's called. Calling the
same method with a lazy knife only generate results when they are iterated over
or `knife.lazy.lazyknife.get` is called to get results.
  
`knife.lazy.lazyknife` combines all `knife` methods in one class:

  >>> from knife import lazyknife

It can be imported under its *dunderscore* (`knife.__`) alias.

  >>> from knife import __  
  
`knife.active.activeknife` also combines every `knife` method in one
combo `knife` class:

  >>> from knife import activeknife

It can be imported under its `knife.knife` alias:
 
  >>> from knife import knife

`knife`'s methods are available in more focused classes that group related 
methods together. These can also be chained into pipelines.

contrived example:
^^^^^^^^^^^^^^^^^^

  >>> from knife.active import mathknife, reduceknife
  >>> one = mathknife(10, 5, 100, 2, 1000)
  >>> two = reduceknife()
  >>> one.minmax().pipe(two).merge().back().min().get()
  2