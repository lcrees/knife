# -*- coding: utf-8 -*-
'''auto filtering call chain test mixins'''

from inspect import ismodule

from knife.compat import port


class ACollectMixin(object):

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
        test = lambda x: not x[0].startswith('__')
        out = self.qclass(
            stoog3
        ).tap(test, isclass).as_tuple().mro().members().untap().end()
        self.assertEqual(
            out,
            (('age', 60), ('name', 'curly'), ('age', 50), ('name', 'larry'),
            ('age', 40), ('name', 'moe')),
            out,
        )

    def test_pick(self):
        from stuf import stuf
        stooges = [
            stuf(name='moe', age=40),
            stuf(name='larry', age=50),
            stuf(name='curly', age=60)
        ]
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

    def test_pluck(self):
        from stuf import stuf
        stooges = [
            stuf(name='moe', age=40),
            stuf(name='larry', age=50),
            stuf(name='curly', age=60)
        ]
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

    def test_items(self):
        self.assertEqual(
            self.qclass(
                dict([(1, 2), (2, 3), (3, 4)]), dict([(1, 2), (2, 3), (3, 4)])
            ).tap(lambda x, y: x * y).items().end(), [2, 6, 12, 2, 6, 12],
        )


class AFilterMixin(object):

    def test_filter(self):
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

    def test_find(self):
        self.assertEqual(
            self.qclass(1, 2, 3, 4, 5, 6).tap(
                lambda x: x % 2 == 0
            ).find().end(), 2,
        )

    def test_partition(self):
        self.assertEqual(
            self.qclass(1, 2, 3, 4, 5, 6).tap(
                lambda x: x % 2 == 0
            ).partition().end(), [[1, 3, 5], [2, 4, 6]]
        )

    def test_difference(self):
        self.assertEqual(
            self.qclass([1, 2, 3, 4, 5], [5, 2, 10]).difference().end(),
            [1, 3, 4],
        )

    def test_disjointed(self):
        self.assertTrue(
            self.qclass([1, 2, 3], [5, 4, 10]).disjointed().end()
        )
        self.assertFalse(
            self.qclass([1, 2, 3], [5, 2, 10]).disjointed().end()
        )

    def test_intersection(self):
        self.assertEqual(
            self.qclass(
                [1, 2, 3], [101, 2, 1, 10], [2, 1]
            ).intersection().end(), [1, 2],
        )

    def test_union(self):
        self.assertEqual(
            self.qclass([1, 2, 3], [101, 2, 1, 10], [2, 1]).union().end(),
            [1, 10, 3, 2, 101],
        )

    def test_unique(self):
        self.assertEqual(
            self.qclass(1, 2, 1, 3, 1, 4).unique().end(), [1, 2, 3, 4],
        )
        self.assertEqual(
            self.qclass(1, 2, 1, 3, 1, 4).tap(round).unique().end(),
            [1, 2, 3, 4],
        )

__all__ = sorted(name for name, obj in port.items(locals()) if not any([
    name.startswith('_'), ismodule(obj), name in ['ismodule', 'port']
]))
del ismodule
del port
