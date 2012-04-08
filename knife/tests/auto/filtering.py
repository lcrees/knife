# -*- coding: utf-8 -*-
'''auto filtering call chain test mixins'''

from inspect import ismodule

from knife.compat import port


class ASliceQMixin(object):

    def test_first(self):
        self.assertEqual(self.qclass(5, 4, 3, 2, 1).first().close(), 5)
        self.assertEqual(self.qclass(5, 4, 3, 2, 1).first(2).close(), [5, 4])

    def test_nth(self):
        self.assertEqual(self.qclass(5, 4, 3, 2, 1).nth(2).close(), 3)
        self.assertEqual(self.qclass(5, 4, 3, 2, 1).nth(10, 11).close(), 11)

    def test_last(self):
        self.assertEqual(self.qclass(5, 4, 3, 2, 1).last().close(), 1)
        self.assertEqual(self.qclass(5, 4, 3, 2, 1).last(2).close(), [2, 1])

    def test_initial(self):
        self.assertEqual(
            self.qclass(5, 4, 3, 2, 1).initial().close(), [5, 4, 3, 2]
        )

    def test_rest(self):
        self.assertEqual(self.qclass(5, 4, 3, 2, 1).rest().close(), [4, 3, 2, 1])

    def test_partition(self):
        self.assertEqual(
            self.qclass(1, 2, 3, 4, 5, 6).tap(
                lambda x: x % 2 == 0
            ).partition().close(), [[1, 3, 5], [2, 4, 6]]
        )


class ACollectQMixin(object):

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
        ).tap(test, isclass).tupleout().members().untap().close(),
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
        ).tap(test, isclass).tupleout().mro().members().untap().close()
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
            self.qclass(*stooges).pick('name').close(),
            ['moe', 'larry', 'curly'],
        )
        self.assertEqual(
            self.qclass(*stooges).pick('name', 'age').close(),
            [('moe', 40), ('larry', 50), ('curly', 60)],
        )
        self.assertEqual(
            self.qclass(*stooges).pick('place').close(), [],
        )

    def test_pluck(self):
        from stuf import stuf
        stooges = [
            stuf(name='moe', age=40),
            stuf(name='larry', age=50),
            stuf(name='curly', age=60)
        ]
        self.assertEqual(
            self.qclass(*stooges).pluck('name').close(),
            ['moe', 'larry', 'curly'],
        )
        self.assertEqual(
            self.qclass(*stooges).pluck('name', 'age').close(),
            [('moe', 40), ('larry', 50), ('curly', 60)],
        )
        stooges = [['moe', 40], ['larry', 50], ['curly', 60]]
        self.assertEqual(
            self.qclass(*stooges).pluck(0).close(), ['moe', 'larry', 'curly'],
        )
        self.assertEqual(self.qclass(*stooges).pluck(1).close(), [40, 50, 60])
        self.assertEqual(self.qclass(*stooges).pluck('place').close(), [])


class ASetQMixin(object):

    def test_difference(self):
        self.assertEqual(
            self.qclass([1, 2, 3, 4, 5], [5, 2, 10]).difference().close(),
            [1, 3, 4],
        )

    def test_disjointed(self):
        self.assertTrue(self.qclass([1, 2, 3], [5, 4, 10]).disjointed().close())
        self.assertFalse(self.qclass([1, 2, 3], [5, 2, 10]).disjointed().close())

    def test_intersection(self):
        self.assertEqual(
            self.qclass(
                [1, 2, 3], [101, 2, 1, 10], [2, 1]
            ).intersection().close(), [1, 2],
        )

    def test_union(self):
        self.assertEqual(
            self.qclass([1, 2, 3], [101, 2, 1, 10], [2, 1]).union().close(),
            [1, 10, 3, 2, 101],
        )

    def test_unique(self):
        self.assertEqual(
            self.qclass(1, 2, 1, 3, 1, 4).unique().close(), [1, 2, 3, 4],
        )
        self.assertEqual(
            self.qclass(1, 2, 1, 3, 1, 4).tap(round).unique().close(),
            [1, 2, 3, 4],
        )


class AFilterQMixin(ACollectQMixin, ASetQMixin, ASliceQMixin):

    '''combination mixin'''

    def test_filter(self):
        self.assertEqual(
            self.qclass(1, 2, 3, 4, 5, 6).tap(
                lambda x: x % 2 == 0
            ).filter().close(), [2, 4, 6]
        )

    def test_find(self):
        self.assertEqual(
            self.qclass(1, 2, 3, 4, 5, 6).tap(
                lambda x: x % 2 == 0
            ).find().close(), 2,
        )

    def test_reject(self):
        self.assertEqual(
            self.qclass(1, 2, 3, 4, 5, 6).tap(
                lambda x: x % 2 == 0
            ).reject().close(), [1, 3, 5]
        )

    def test_compact(self):
        self.assertEqual(
            self.qclass(0, 1, False, 2, '', 3).compact().close(), [1, 2, 3],
        )

    def test_without(self):
        self.assertEqual(
            self.qclass(1, 2, 1, 0, 3, 1, 4).without(0, 1).close(), [2, 3, 4],
        )

__all__ = sorted(name for name, obj in port.items(locals()) if not any([
    name.startswith('_'), ismodule(obj), name in ['ismodule', 'port']
]))
del ismodule
del port
