.. knife documentation master file, created by
   sphinx-quickstart on Wed Apr 11 00:32:47 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

*knife* Documentation
#####################

:mod:`knife` is a powerful `Python <http://docs.python.org/>`_ multitool
loosely inspired by `underscore.js <http://documentcloud.github.com/underscore/>`_
but remixed for maximum `pythonicity <http://docs.python.org/glossary.html#term-pythonic>`_. 

:mod:`knife` concentrates power normally dispersed across the entire Python
universe in one convenient shrink-wrapped package.

Vitals
======

:mod:`knife` works with Python 2.6, 2.7, and 3.2.

mod:`knife` documentation is at http://readthedocs.org/docs/knife/en/latest/ or
http://packages.python.org/knife/

Installation
============

Install :mod:`knife` with `pip <http://www.pip-installer.org/en/latest/index.html>`_...::

  $ pip install knife
  [... possibly exciting stuff happening ...]
  Successfully installed knife
  
...or `easy_install <http://packages.python.org/distribute/>`_...::

  $ easy_install knife
  [... possibly exciting stuff happening ...]
  Finished processing dependencies for knife
  
...or old school by downloading :mod:`knife` from http://pypi.python.org/pypi/knife/::

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

:mod:`knife` has 40 plus methods that can be `chained <https://en.wikipedia.org/
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
  
A :mod:`knife` knife can rollback the state of things it has knifed back to results
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

:mod:`knife` knives come in two flavors: :mod:`active` and :mod:`lazy`. Active
knives evaluate the result of each method immediately it's called. Calling the
same method with a lazy knife only generate results when they are iterated over
or :meth:`knife.lazy.lazyknife.get` is called to get results.
  
:class:`knife.lazy.lazyknife` combines all :mod:`knife` methods in one
:mod:`knife` class:

  >>> from knife import lazyknife

It can be imported under its *dunderscore* (:class:`knife.__`) alias.

  >>> from knife import __  
  
:class:`knife.active.activeknife` also combines every :mod:`knife` method in one
combo :mod:`knife` class:

  >>> from knife import activeknife

It can be imported under its :class:`knife.knife` alias:
 
  >>> from knife import knife

:mod:`knife`'s methods are available in more focused classes that group related 
methods together. These can also be chained into pipelines.

contrived example:
^^^^^^^^^^^^^^^^^^

  >>> from knife.active import mathknife, reduceknife
  >>> one = mathknife(10, 5, 100, 2, 1000)
  >>> two = reduceknife()
  >>> one.minmax().pipe(two).merge().back().min().get()
  2

Lazy knives
===========

.. toctree::
   :maxdepth: 2

   lazyknife
   lcmpknife
   lfilterknife
   lmapknife
   lmathknife
   lorderknife
   lreduceknife
   lrepeatknife
   lsliceknife

Active knives
=============

.. toctree::
   :maxdepth: 2

   activeknife
   acmpknife
   afilterknife
   amapknife
   amathknife
   aorderknife
   areduceknife
   arepeatknife
   asliceknife

indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

