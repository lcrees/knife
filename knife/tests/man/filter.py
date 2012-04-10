# -*- coding: utf-8 -*-
'''filtering test mixins'''

from inspect import ismodule

from knife.compat import port


class MCollectMixin(object):

    def test_members(self):
        from inspect import isclass
        class stooges: #@IgnorePep8
            name = 'moe'
            age = 40
        class stoog2: #@IgnorePep8
            name = 'larry'
            age = 50
        class stoog3: #@IgnorePep8
            name = 'curly'
            age = 60
            class stoog4: #@IgnorePep8
                name = 'beastly'
                age = 969
        self._true_true_false(
            self.qclass(
                stooges, stoog2, stoog3
            ).tap(
                lambda x: not x[0].startswith('__'), isclass
            ).tuplevalue().members().untap().rebalance(),
            self.assertEqual,
            (('age', 40), ('name', 'moe'), ('age', 50), ('name', 'larry'),
            ('age', 60), ('name', 'curly'), ('stoog4', (('age', 969),
            ('name', 'beastly')))),
        )

    def test_mro(self):
        from inspect import isclass
        class stooges: #@IgnorePep8
            name = 'moe'
            age = 40
        class stoog2(stooges): #@IgnorePep8
            name = 'larry'
            age = 50
        class stoog3(stoog2): #@IgnorePep8
            name = 'curly'
            age = 60
        self._true_true_false(
            self.qclass(stoog3).tap(
                lambda x: x, isclass
            ).tuplevalue().mro().rebalance().members().untap().rebalance(),
            self.assertEqual,
            (('age', 60), ('name', 'curly'), ('age', 50), ('name', 'larry'),
            ('age', 40), ('name', 'moe'))
        )

    def test_attributes(self):
        from stuf import stuf
        stooges = [
            stuf(name='moe', age=40),
            stuf(name='larry', age=50),
            stuf(name='curly', age=60)
        ]
        self._true_true_false(
            self.qclass(*stooges).attributes('name'),
            self.assertEqual,
            ['moe', 'larry', 'curly'],
        )
        self._true_true_false(
            self.qclass(*stooges).attributes('name', 'age'),
            self.assertEqual,
            [('moe', 40), ('larry', 50), ('curly', 60)],
        )
        self._false_true_true(
            self.qclass(*stooges).attributes('place'),
            self.assertEqual,
            [],
        )

    def test_pluck(self):
        from stuf import stuf
        stooges = [
            stuf(name='moe', age=40),
            stuf(name='larry', age=50),
            stuf(name='curly', age=60)
        ]
        self._true_true_false(
            self.qclass(*stooges).pluck('name'),
            self.assertEqual,
            ['moe', 'larry', 'curly'],
        )
        self._true_true_false(
            self.qclass(*stooges).pluck('name', 'age'),
            self.assertEqual,
            [('moe', 40), ('larry', 50), ('curly', 60)],
        )
        stooges = [['moe', 40], ['larry', 50], ['curly', 60]]
        self._true_true_false(
            self.qclass(*stooges).pluck(0),
            self.assertEqual,
            ['moe', 'larry', 'curly'],
        )
        self._true_true_false(
            self.qclass(*stooges).pluck(1),
            self.assertEqual,
            [40, 50, 60],
        )
        self._false_true_true(
            self.qclass(*stooges).pluck('place'),
            self.assertEqual,
            [],
        )

    def test_items(self):
        self._false_true_false(
            self.qclass(
                dict([(1, 2), (2, 3), (3, 4)]), dict([(1, 2), (2, 3), (3, 4)])
            ).tap(lambda x, y: x * y).items(),
            self.assertEqual,
            [2, 6, 12, 2, 6, 12],
        )


class MFilterMixin(object):

    def test_partition(self):
        self._false_true_false(
            self.qclass(
                1, 2, 3, 4, 5, 6
            ).tap(lambda x: x % 2 == 0).partition(),
            self.assertEqual,
            [[1, 3, 5], [2, 4, 6]],
        )

    def test_filter(self):
        self._false_true_false(
            self.qclass(1, 2, 3, 4, 5, 6).tap(lambda x: x % 2 == 0).filter(),
            self.assertEqual,
            [2, 4, 6],
        )
        self._false_true_false(
            self.qclass(1, 2, 3, 4, 5, 6).tap(
                lambda x: x % 2 == 0
            ).filter(invert=True),
            self.assertEqual,
            [1, 3, 5],
        )

    def test_find(self):
        self._false_true_false(
            self.qclass(1, 2, 3, 4, 5, 6).tap(lambda x: x % 2 == 0).find(),
            self.assertEqual,
            2,
        )

    def test_difference(self):
        self._false_true_false(
            self.qclass([1, 2, 3, 4, 5], [5, 2, 10]).difference(),
            self.assertEqual,
            [1, 3, 4]
        )

    def test_symmetric_difference(self):
        self._false_true_false(
            self.qclass([1, 2, 3, 4, 5], [5, 2, 10]).symmetric_difference(),
            self.assertEqual,
            [1, 3, 4, 10]
        )

    def test_disjointed(self):
        self._false_true_false(
            self.qclass([1, 2, 3], [5, 4, 10]).disjointed(), self.assertTrue,
        )
        self._false_true_false(
            self.qclass([1, 2, 3], [5, 2, 10]).disjointed(), self.assertFalse,
        )

    def test_intersection(self):
        self._false_true_false(
            self.qclass([1, 2, 3], [101, 2, 1, 10], [2, 1]).intersection(),
            self.assertEqual,
            [1, 2],
        )

    def test_union(self):
        self._false_true_false(
            self.qclass([1, 2, 3], [101, 2, 1, 10], [2, 1]).union(),
            self.assertEqual,
            [1, 10, 3, 2, 101],
        )

    def test_subset(self):
        self._false_true_false(
            self.qclass([1, 2, 3], [101, 2, 1, 3]).subset(),
            self.assertTrue,
        )

    def test_superset(self):
        self._false_true_false(
            self.qclass([1, 2, 3], [101, 2, 1, 3, 6, 34]).superset(),
            self.assertTrue,
        )

    def test_unique(self):
        self._false_true_false(
            self.qclass(1, 2, 1, 3, 1, 4).unique(),
            self.assertEqual,
            [1, 2, 3, 4],
        )
        self._false_true_false(
            self.qclass(1, 2, 1, 3, 1, 4).tap(round).unique(),
            self.assertEqual,
            [1, 2, 3, 4],
        )


__all__ = sorted(name for name, obj in port.items(locals()) if not any([
    name.startswith('_'), ismodule(obj), name in ['ismodule', 'port']
]))
del ismodule
