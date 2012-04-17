# -*- coding: utf-8 -*-
'''base chainsaw mixins'''

from threading import local

from chainsaw._compat import tounicode, tobytes


class ChainsawMixin(local):

    '''base chainsaw mixin'''

    def __init__(self, *things, **kw):
        '''
        init

        :argument `things`: incoming things
        '''
        super(ChainsawMixin, self).__init__(*things, **kw)

    ###########################################################################
    ## things in process ######################################################
    ###########################################################################

    def as_multi(self):
        '''
        Treat each incoming thing as one processing unit within a series of
        processing units.
        '''
        self._mode = self._MANY
        return self

    def as_one(self):
        '''
        Treat multiple incoming things as one processing unit.
        '''
        self._mode = self._ONE
        return self

    ###########################################################################
    ## things in session ######################################################
    ###########################################################################

    def as_edit(self):
        '''
        Work on incoming things **without** automatically reverting back to a
        baseline snapshot when :meth:`commit()` is invoked.
        '''
        self._context = self._EDIT
        self._truth = None
        return self.clear().undo(baseline=True)._unchain()

    def as_query(self):
        '''
        Work on incoming things where incoming things revert to a baseline
        snapshot when :meth:`close()` is invoked.
        '''
        self._context = self._QUERY
        self._truth = None
        return self.snapshot(baseline=True)._as_chain()

    ###########################################################################
    ## things in chains #######################################################
    ###########################################################################

    def as_auto(self):
        '''
        Let incoming things be automatically rebalanced with outgoing things.
        '''
        self._AUTO = True
        return self

    def as_manual(self):
        '''
        Disallow incoming things from being manually rebalanced with outgoing
        things.
        '''
        self._AUTO = False
        return self

    def out_in(self):
        '''
        Copy outgoing things back to incoming things for further processing.
        '''
        return self._outin()

    def in_out(self):
        '''
        Copy incoming things to outgoing things for output.
        '''
        return self._inout()

    @property
    def balanced(self):
        '''
        If outgoing and incoming things are in balance.
        '''
        return self._balanced()

    ###########################################################################
    ## snapshot of things #####################################################
    ###########################################################################

    def snapshot(self, baseline=False, original=False):
        '''
        Take a snapshot of the current state of incoming things.

        :keyword boolean baseline: make snapshot the baseline snapshot

        :keyword boolean original: make snapshot the original snapshot
        '''
        return self._snapshot(baseline, original)

    def undo(self, snapshot=0, baseline=False, original=False):
        '''
        Revert incoming things back to a previous snapshot.

        :keyword integer snapshot: number of steps ago e.g. ``1``, ``2``, ``3``

        :keyword boolean baseline: revert incoming things to baseline snapshot

        :keyword boolean original: revert incoming things to original snapshot
        '''
        return self._undo(snapshot, baseline, original)

    ###########################################################################
    ## things are called ######################################################
    ###########################################################################

    def params(self, *args, **kw):
        '''
        Assign global `positional
        <http://docs.python.org/glossary.html#term-positional-argument>`_ or
        `keyword <http://docs.python.org/glossary.html#term-keyword-argument>`_
        params used when the worker is invoked.
        '''
        # positional params
        self._args = args
        # keyword arguemnts
        self._kw = kw
        return self

    def tap(self, call):
        '''
        Assign worker.

        :argument call: a callable
        '''
        # reset stored position params
        self._args = ()
        # reset stored keyword params
        self._kw = {}
        # assign worker
        self._call = call
        return self

    def untap(self):
        '''
        Remove worker and global `positional
        <http://docs.python.org/glossary.html#term-positional-argument>`_ and
        `keyword <http://docs.python.org/glossary.html#term-keyword-argument>`_
        params.
        '''
        # reset position params
        self._args = ()
        # reset keyword params
        self._kw = {}
        # reset worker
        self._call = None
        return self

    def pattern(self, pattern, type='parse', flags=0):
        '''
        Compile a search pattern and use it as the worker.

        :argument string pattern: search pattern

        :keyword string type: engine to compile pattern with. Valid options are
          `'parse' <http://pypi.python.org/pypi/parse/>`_, `'re'
          <http://docs.python.org/library/re.html>`_, or `'glob'
          <http://docs.python.org/library/fnmatch.html>`_

        :keyword integer flags: regular expression `flags
          <http://docs.python.org/library/re.html#re.DEBUG>`_
        '''
        self._call = self._pattern(pattern, type, flags)
        return self

    ###########################################################################
    ## things coming in #######################################################
    ###########################################################################

    def extend(self, things):
        '''
        Insert `things` **after** any other incoming things.

        :argument things: incoming things
        '''
        with self._man1():
            return self._xtend(things)

    def extendfront(self, things):
        '''
        Insert `things` **before** any other incoming things.

        :argument things: incoming things
        '''
        with self._man1():
            return self._xtendfront(things)

    def append(self, thing):
        '''
        Insert `thing` **after** any other incoming things.

        :argument thing: incoming thing
        '''
        with self._man1():
            return self._append(thing)

    def prepend(self, thing):
        '''
        Insert `thing` **before** any other incoming things.

        :argument thing: incoming thing
        '''
        with self._man1():
            return self._prepend(thing)

    ###########################################################################
    ## knowing things #########################################################
    ###########################################################################

    def __len__(self):
        '''Number of incoming things.'''
        return self._len()

    def __repr__(self):
        '''Object representation.'''
        return self._repr()

    ###########################################################################
    ## cleaning up things #####################################################
    ###########################################################################

    def clear(self):
        '''
        Clear everything.
        '''
        return self._clear()

    def clear_in(self):
        '''
        Clear incoming things.
        '''
        return self._clearin()

    def clear_out(self):
        '''
        Clear outgoing things.
        '''
        return self._clearout()


class OutputMixin(ChainsawMixin):

    '''output mixin'''

    def __iter__(self):
        '''Yield outgoing things.'''
        return self._iterate()

    def close(self):
        '''
        Close current edit or query session and return outgoing things wrapped
        in the `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper.
        '''
        value = self._unchain()._output()
        # remove every thing
        self.clear()._clearsp()
        return value

    def commit(self):
        '''
        Close query session and return outgoing things wrapped with the
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper.
        '''
        value = self._unchain()._output()
        # remove outgoing things
        self.clear_out()
        return value

    def preview(self):
        '''
        Take a peek at the current state of outgoing things.
        '''
        return self._output()

    ###########################################################################
    ## wrapping things up #####################################################
    ###########################################################################

    def wrap(self, wrapper):
        '''
        Assign `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper for outgoing things.

        :argument wrapper: an `iterable
          <http://docs.python.org/glossary.html#term-iterable>`_ wrapper
        '''
        self._wrapper = wrapper
        return self

    def as_ascii(self, errors='strict'):
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to :class:`byte` encode outgoing things with the
        ``'ascii'`` codec.

        :keyword string errors: error handling for decoding issues
        '''
        self._wrapper = lambda x: tobytes(x, 'ascii', errors)
        return self

    def as_bytes(self, encoding='utf-8', errors='strict'):
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to :class:`byte` encode outgoing things.

        :keyword string encoding: Unicode encoding

        :keyword string errors: error handling for encoding issues
        '''
        self._wrapper = lambda x: tobytes(x, encoding, errors)
        return self

    def as_dict(self):
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to cast outgoing things to :class:`dict`.
        '''
        self._wrapper = dict
        return self

    def as_list(self):
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to cast outgoing things to :class:`list`.
        '''
        self._wrapper = list
        return self

    unwrap = as_list

    def as_set(self):
        '''
        Set `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ wrapper to cast
        outgoing things to :class:`set`.
        '''
        self._wrapper = set
        return self

    def as_tuple(self):
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to cast outgoing things to :class:`tuple`.
        '''
        self._wrapper = tuple
        return self

    def as_unicode(self, encoding='utf-8', errors='strict'):
        '''
        Set `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        wrapper to :class:`unicode` (:class:`str` under Python 3) decode
        outgoing things.

        :keyword string encoding: Unicode encoding

        :keyword string errors: error handling for decoding issues
        '''
        self._wrapper = lambda x: tounicode(x, encoding, errors)
        return self
