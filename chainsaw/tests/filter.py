# -*- coding: utf-8 -*-
'''auto filtering call chain test mixins'''

from inspect import ismodule

from chainsaw.compat import port


class CollectMixin(object):

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
        # auto
        test = lambda x: not x[0].startswith('__')
        out = self.qclass(
            stooges, stoog2, stoog3
        ).tap(test, isclass).as_tuple().members().untap().end(),
        self.assertEqual(
            out,
            ((('age', 40), ('name', 'moe'), ('age', 50), ('name', 'larry'),
            ('age', 60), ('name', 'curly'), ('stoog4', (('age', 969),
            ('name', 'beastly')))),),
            out,
        )
        # man
        self._true_true_false(
            self.mclass(
                stooges, stoog2, stoog3
            ).tap(test, isclass).as_tuple().members().untap().shift_in(),
            self.assertEqual,
            (('age', 40), ('name', 'moe'), ('age', 50), ('name', 'larry'),
            ('age', 60), ('name', 'curly'), ('stoog4', (('age', 969),
            ('name', 'beastly')))),
        )

    def test_mro(self):
        # auto
        class stooges: #@IgnorePep8
            name = 'moe'
            age = 40
        class stoog2(stooges): #@IgnorePep8
            name = 'larry'
            age = 50
        class stoog3(stoog2): #@IgnorePep8
            name = 'curly'
            age = 60
        out = self.qclass(stoog3).mro().end()
        self.assertEqual(
            out,
            [stoog3, stoog2, stooges],
            out,
        )
        # man
        self._true_true_false(
            self.mclass(stoog3).mro(),
            self.assertEqual,
            [stoog3, stoog2, stooges],
        )

    def test_attributes(self):
        from stuf import stuf
        stooges = [
            stuf(name='moe', age=40),
            stuf(name='larry', age=50),
            stuf(name='curly', age=60)
        ]
        # auto
        self.assertEqual(
            self.qclass(*stooges).attributes('name').end(),
            ['moe', 'larry', 'curly'],
        )
        self.assertEqual(
            self.qclass(*stooges).attributes('name', 'age').end(),
            [('moe', 40), ('larry', 50), ('curly', 60)],
        )
        self.assertEqual(
            self.qclass(*stooges).attributes('place').end(), [],
        )
        # man
        self._true_true_false(
            self.mclass(*stooges).attributes('name'),
            self.assertEqual,
            ['moe', 'larry', 'curly'],
        )
        self._true_true_false(
            self.mclass(*stooges).attributes('name', 'age'),
            self.assertEqual,
            [('moe', 40), ('larry', 50), ('curly', 60)],
        )
        self._false_true_true(
            self.mclass(*stooges).attributes('place'),
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
        # auto
        self.assertEqual(
            self.qclass(*stooges).pluck('name').end(),
            ['moe', 'larry', 'curly'],
        )
        self.assertEqual(
            self.qclass(*stooges).pluck('name', 'age').end(),
            [('moe', 40), ('larry', 50), ('curly', 60)],
        )
        stooges = [['moe', 40], ['larry', 50], ['curly', 60]]
        self.assertEqual(
            self.qclass(*stooges).pluck(0).end(), ['moe', 'larry', 'curly'],
        )
        self.assertEqual(self.qclass(*stooges).pluck(1).end(), [40, 50, 60])
        self.assertEqual(self.qclass(*stooges).pluck('place').end(), [])
        # man
        self._true_true_false(
            self.mclass(*stooges).pluck('name'),
            self.assertEqual,
            ['moe', 'larry', 'curly'],
        )
        self._true_true_false(
            self.mclass(*stooges).pluck('name', 'age'),
            self.assertEqual,
            [('moe', 40), ('larry', 50), ('curly', 60)],
        )
        stooges = [['moe', 40], ['larry', 50], ['curly', 60]]
        self._true_true_false(
            self.mclass(*stooges).pluck(0),
            self.assertEqual,
            ['moe', 'larry', 'curly'],
        )
        self._true_true_false(
            self.mclass(*stooges).pluck(1),
            self.assertEqual,
            [40, 50, 60],
        )
        self._false_true_true(
            self.mclass(*stooges).pluck('place'),
            self.assertEqual,
            [],
        )

    def test_items(self):
        # auto
        self.assertEqual(
            self.qclass(
                dict([(1, 2), (2, 3), (3, 4)]), dict([(1, 2), (2, 3), (3, 4)])
            ).tap(lambda x, y: x * y).items().end(), [2, 6, 12, 2, 6, 12],
        )
        # man
        self._false_true_false(
            self.mclass(
                dict([(1, 2), (2, 3), (3, 4)]), dict([(1, 2), (2, 3), (3, 4)])
            ).tap(lambda x, y: x * y).items(),
            self.assertEqual,
            [2, 6, 12, 2, 6, 12],
        )


class FilterMixin(object):

    def test_filter(self):
        # auto
        self.assertEqual(
            self.qclass(1, 2, 3, 4, 5, 6).tap(
                lambda x: x % 2 == 0
            ).filter(reverse=True).end(), [1, 3, 5]
        )
        self.assertEqual(
            self.qclass(1, 2, 3, 4, 5, 6).tap(
                lambda x: x % 2 == 0
            ).filter().end(), [2, 4, 6]
        )
        # man
        self._false_true_false(
            self.mclass(1, 2, 3, 4, 5, 6).tap(lambda x: x % 2 == 0).filter(),
            self.assertEqual,
            [2, 4, 6],
        )
        self._false_true_false(
            self.mclass(1, 2, 3, 4, 5, 6).tap(
                lambda x: x % 2 == 0
            ).filter(reverse=True),
            self.assertEqual,
            [1, 3, 5],
        )

    def test_find(self):
        # auto
        self.assertEqual(
            self.qclass(1, 2, 3, 4, 5, 6).tap(
                lambda x: x % 2 == 0
            ).find().end(), 2,
        )
        # man
        self._false_true_false(
            self.mclass(1, 2, 3, 4, 5, 6).tap(lambda x: x % 2 == 0).find(),
            self.assertEqual,
            2,
        )

    def test_partition(self):
        # auto
        self.assertEqual(
            self.qclass(1, 2, 3, 4, 5, 6).tap(
                lambda x: x % 2 == 0
            ).partition().end(), [[2, 4, 6], [1, 3, 5]]
        )
        # man
        self._false_true_false(
            self.mclass(
                1, 2, 3, 4, 5, 6
            ).tap(lambda x: x % 2 == 0).partition(),
            self.assertEqual,
            [[2, 4, 6], [1, 3, 5]],
        )

    def test_difference(self):
        # auto
        self.assertEqual(
            self.qclass([1, 2, 3, 4, 5], [5, 2, 10]).difference().end(),
            [1, 3, 4],
        )
        self.assertEqual(
            self.qclass([1, 2, 3, 4, 5], [5, 2, 10]).difference(True).end(),
            [1, 3, 4, 10]
        )
        # man
        self._false_true_false(
            self.mclass([1, 2, 3, 4, 5], [5, 2, 10]).difference(),
            self.assertEqual,
            [1, 3, 4]
        )
        self._false_true_false(
            self.mclass([1, 2, 3, 4, 5], [5, 2, 10]).difference(True),
            self.assertEqual,
            [1, 3, 4, 10]
        )

    def test_disjointed(self):
        # auto
        self.assertTrue(
            self.qclass([1, 2, 3], [5, 4, 10]).disjointed().end()
        )
        self.assertFalse(
            self.qclass([1, 2, 3], [5, 2, 10]).disjointed().end()
        )
        # man
        self._false_true_false(
            self.mclass([1, 2, 3], [5, 4, 10]).disjointed(), self.assertTrue,
        )
        self._false_true_false(
            self.mclass([1, 2, 3], [5, 2, 10]).disjointed(), self.assertFalse,
        )

    def test_intersection(self):
        # auto
        self.assertEqual(
            self.qclass(
                [1, 2, 3], [101, 2, 1, 10], [2, 1]
            ).intersection().end(), [1, 2],
        )
        # man
        self._false_true_false(
            self.mclass([1, 2, 3], [101, 2, 1, 10], [2, 1]).intersection(),
            self.assertEqual,
            [1, 2],
        )

    def test_subset(self):
        # auto
        self.assertTrue(
            self.qclass([1, 2, 3], [101, 2, 1, 3]).subset().end(),
        )
        # man
        self._false_true_false(
            self.mclass([1, 2, 3], [101, 2, 1, 3]).subset(),
            self.assertTrue,
        )

    def test_superset(self):
        # auto
        diff = self.qclass([101, 2, 1, 3, 6, 34], [1, 2, 3]).superset().end()
        self.assertTrue(diff)
        # man
        self._false_true_false(
            self.mclass([101, 2, 1, 3, 6, 34], [1, 2, 3]).superset(),
            self.assertTrue,
        )

    def test_union(self):
        # auto
        self.assertEqual(
            self.qclass([1, 2, 3], [101, 2, 1, 10], [2, 1]).union().end(),
            [1, 10, 3, 2, 101],
        )
        # man
        self._false_true_false(
            self.mclass([1, 2, 3], [101, 2, 1, 10], [2, 1]).union(),
            self.assertEqual,
            [1, 10, 3, 2, 101],
        )

    def test_unique(self):
        # auto
        self.assertEqual(
            self.qclass(1, 2, 1, 3, 1, 4).unique().end(), [1, 2, 3, 4],
        )
        self.assertEqual(
            self.qclass(1, 2, 1, 3, 1, 4).tap(round).unique().end(),
            [1, 2, 3, 4],
        )
        # man
        self._false_true_false(
            self.mclass(1, 2, 1, 3, 1, 4).unique(),
            self.assertEqual,
            [1, 2, 3, 4],
        )
        self._false_true_false(
            self.mclass(1, 2, 1, 3, 1, 4).tap(round).unique(),
            self.assertEqual,
            [1, 2, 3, 4],
        )

__all__ = sorted(name for name, obj in port.items(locals()) if not any([
    name.startswith('_'), ismodule(obj), name in ['ismodule', 'port']
]))
del ismodule
del port
