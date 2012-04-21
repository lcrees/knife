.. knife documentation master file, created by
   sphinx-quickstart on Wed Apr 11 00:32:47 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

knife Documentation
===================

:mod:`knife` is a powerful `Python <http://docs.python.org/>`_ multitool
loosely inspired by `underscore.js <http://documentcloud.github.com/underscore/>`_
but remixed for maximum `Pythonicness <http://docs.python.org/glossary.html#term-pythonic>`_. 
It delivers functionality scattered across the Python's `standard library <http://docs.
python.org/library/index.html>`_ in one convenient shrink-wrapped package.

Vitals
------

:mod:`knife`'s documentation can be found at http://readthedocs.org/docs/knife/en/latest/
or http://packages.python.org/knife/

:mod:`knife` works with Python 2.6, 2.7, and 3.2.

Installation
------------

:mod:`knife` can be installed with `pip <http://www.pip-installer.org/en/latest
/index.html>`_:

  $ pip install knife
  [... stuff happens ...]
  Successfully installed knife
  
Or `easy_install <http://packages.python.org/distribute/>`_:

  $ easy_install knife
  [... stuff happens ...]
  Finished processing dependencies for knife
  
:mod:`knife` can also be downloaded from http://pypi.python.org/knife

Development
-----------

 * :mod:`knife` public source repository is at https://bitbucket.org/lcrees/knife.
 * :mod:`knife` is mirrored on https://github.com/kwarterthieves/knife/.
 * :mod:`knife` issues can be reported at https://bitbucket.org/lcrees/knife/issues
 * :mod:`knife` is distributed under a `BSD <http://www.opensource.org/licenses/bsd-license.php>`_ license.

In Brief...
-----------

:mod:`knife` features 45 carefully curated methods that can be `chained <https:
//en.wikipedia.org/wiki/Fluent_interface>`_ together into one pipeline.

*Higly contrived introductory example:*

  >>> from knife import __
  >>> __(5, 4, 3, 2, 1).initial().rest().slice(1, 2).last().get()
  3

Or used in object-oriented style.

*Higly contrived introductory example:*

  >>> from knife import knife
  >>> oo = knife(('a', 1), ('b', 2), ('c', 3))
  >>> oo.wrap(dict)
  >>> oo.map()
  >>> oo.get()
  {'a': 1, 'b': 2, 'c': 3}
  
:mod:`knife`'s methods are also available in more modular classes that can be
chained together in pipelines.

*Higly contrived introductory example:*

  >>> from knife.active import mathknife, reduceknife
  >>> one = mathknife(10, 5, 100, 2, 1000)
  >>> two = reduceknife()
  >>> one.minmax().pipe(two).merge().back().min().get()
  2
  
:mod:`knife` can also rollback the results of previous operations, a baseline
snapshot, or its original arguments.

*Higly contrived introductory example:*
  
  >>> undone = __(1, 2, 3).prepend(1, 2, 3, 4, 5, 6)
  >>> undone.peek()
  [1, 2, 3, 4, 5, 6, 1, 2, 3]
  >>> undone.append(1).undo().peek()
  [1, 2, 3, 4, 5, 6, 1, 2, 3]
  >>> undone.append(1, 2).undo(2).peek()
  [1, 2, 3, 4, 5, 6, 1, 2, 3, 1]
  undone.snapshot().append(1, 2).baseline().peek()
  [1, 2, 3, 4, 5, 6, 1, 2, 3, 1]
  undone.original().peek()
  [1, 2, 3]
  >>> one.original().minmax().pipe(two).merge().back().max().get()
  1000
  >>> one.original().minmax().pipe(two).merge().back().sum().get()
  1002

:mod:`knife`'s knives come in two flavors: :mod:`active` and mod:`lazy`. Active
knives evaluate the result of each operation upon method invocation. Lazy knives
are more lazily evaluated when a :mod:`knife` is iterated over or :meth:`get`
method is called to fetch the results.

There is an active combo :mod:`knife` featuring all :mod:knife's method that 
can be imported as:

  >>> from knife import knife
  
Or:
 
  >>> from knife import activeknife
  
There is a lazy combo :mod:`knife` that can be imported as a "dunderscore" (two
underscores).

  >>> from knife import __
  
Or:

  >>> from knife import lazyknife
  
Specilized classes featuring a limited subset of :mod:`knife` functionality` are
available in active or lazy flavors and documented below:

Table of Contents
-----------------

lazy knives
-----------

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

active knives
-------------

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

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

