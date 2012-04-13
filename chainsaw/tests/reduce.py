# -*- coding: utf-8 -*-
'''auto reduce test mixins'''


class FilterMixin(object):

    def test_pattern(self):
        self.assertEqual(
            self.qclass(
                'This is the first test',
                'This is the second test',
                'This is the third test'
            ).pattern('{} first {}').filter().end(), 'This is the first test'
        )
        self.assertEqual(
            self.qclass(
                'This is the first test',
                'This is the second test',
                'This is the third test'
            ).pattern(
                '. third .', type='regex'
            ).filter().end(), 'This is the third test'
        )
        self.assertEqual(
            self.qclass(
                'This is the first test',
                'This is the second test',
                'This is the third test'
            ).pattern(
                '*second*', type='glob'
            ).filter().end(), 'This is the second test'
        )

    def test_traverse(self):
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
        ).tap(test, isclass).as_tuple().traverse().untap().end(),
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
            ).tap(test, isclass).as_tuple().traverse().untap().shift_in(),
            self.assertEqual,
            (('age', 40), ('name', 'moe'), ('age', 50), ('name', 'larry'),
            ('age', 60), ('name', 'curly'), ('stoog4', (('age', 969),
            ('name', 'beastly')))),
        )
        # auto
        class stooge: #@IgnorePep8
            name = 'moe'
            age = 40
        class stooge2(stooges): #@IgnorePep8
            name = 'larry'
            age = 50
        class stooge3(stoog2): #@IgnorePep8
            name = 'curly'
            age = 60
        out = self.qclass(stoog3).mro().end()
        self.assertEqual(
            out,
            [stooge3, stooge2, stooge],
            out,
        )
        # man
        self._true_true_false(
            self.mclass(stoog3).traverse(ancestors=True),
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

    def test_items(self):
        from stuf import stuf
        stooges = [
            stuf(name='moe', age=40),
            stuf(name='larry', age=50),
            stuf(name='curly', age=60)
        ]
        # auto
        self.assertEqual(
            self.qclass(*stooges).items('name').end(),
            ['moe', 'larry', 'curly'],
        )
        self.assertEqual(
            self.qclass(*stooges).items('name', 'age').end(),
            [('moe', 40), ('larry', 50), ('curly', 60)],
        )
        stooges = [['moe', 40], ['larry', 50], ['curly', 60]]
        self.assertEqual(
            self.qclass(*stooges).items(0).end(), ['moe', 'larry', 'curly'],
        )
        self.assertEqual(self.qclass(*stooges).items(1).end(), [40, 50, 60])
        self.assertEqual(self.qclass(*stooges).items('place').end(), [])
        # man
        stooges = [
            stuf(name='moe', age=40),
            stuf(name='larry', age=50),
            stuf(name='curly', age=60)
        ]
        self._true_true_false(
            self.mclass(*stooges).items('name'),
            self.assertEqual,
            ['moe', 'larry', 'curly'],
        )
        self._true_true_false(
            self.mclass(*stooges).items('name', 'age'),
            self.assertEqual,
            [('moe', 40), ('larry', 50), ('curly', 60)],
        )
        stooges = [['moe', 40], ['larry', 50], ['curly', 60]]
        self._true_true_false(
            self.mclass(*stooges).items(0),
            self.assertEqual,
            ['moe', 'larry', 'curly'],
        )
        self._true_true_false(
            self.mclass(*stooges).items(1),
            self.assertEqual,
            [40, 50, 60],
        )
        self._false_true_true(
            self.mclass(*stooges).items('place'),
            self.assertEqual,
            [],
        )

    def test_mapping(self):
        # auto
        self.assertEqual(
            self.qclass(
                dict([(1, 2), (2, 3), (3, 4)]), dict([(1, 2), (2, 3), (3, 4)])
            ).mapping(True).end(), [1, 2, 3, 1, 2, 3],
        )
        self.assertEqual(
            self.qclass(
                dict([(1, 2), (2, 3), (3, 4)]), dict([(1, 2), (2, 3), (3, 4)])
            ).mapping(values=True).end(), [2, 3, 4, 2, 3, 4],
        )
        self.assertEqual(
            self.qclass(
                dict([(1, 2), (2, 3), (3, 4)]), dict([(1, 2), (2, 3), (3, 4)])
            ).tap(lambda x, y: x * y).mapping().end(), [2, 6, 12, 2, 6, 12],
        )
        # man
        self._false_true_false(
            self.mclass(
                dict([(1, 2), (2, 3), (3, 4)]), dict([(1, 2), (2, 3), (3, 4)])
            ).mapping(True),
            self.assertEqual,
            [1, 2, 3, 1, 2, 3],
        )
        self._false_true_false(
            self.mclass(
                dict([(1, 2), (2, 3), (3, 4)]), dict([(1, 2), (2, 3), (3, 4)])
            ).mapping(values=True),
            self.assertEqual,
            [2, 3, 4, 2, 3, 4],
        )
        self._false_true_false(
            self.mclass(
                dict([(1, 2), (2, 3), (3, 4)]), dict([(1, 2), (2, 3), (3, 4)])
            ).tap(lambda x, y: x * y).mapping(),
            self.assertEqual,
            [2, 6, 12, 2, 6, 12],
        )

    def test_filter(self):
        # auto
        self.assertEqual(
            self.qclass(1, 2, 3, 4, 5, 6).tap(
                lambda x: x % 2 == 0
            ).filter(invert=True).end(), [1, 3, 5]
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
            ).filter(invert=True),
            self.assertEqual,
            [1, 3, 5],
        )

    def test_duality(self):
        # auto
        self.assertEqual(
            self.qclass(1, 2, 3, 4, 5, 6).tap(
                lambda x: x % 2 == 0
            ).duality().end(), [[2, 4, 6], [1, 3, 5]]
        )
        # man
        self._false_true_false(
            self.mclass(
                1, 2, 3, 4, 5, 6
            ).tap(lambda x: x % 2 == 0).duality(),
            self.assertEqual,
            [[2, 4, 6], [1, 3, 5]],
        )


class SliceMixin(object):

    def test_dice(self):
        # auto
        self.assertEqual(
            self.qclass(
                'moe', 'larry', 'curly', 30, 40, 50, True
            ).dice(2, 'x').end(),
            [('moe', 'larry'), ('curly', 30), (40, 50), (True, 'x')]
        )
        # man
        self._false_true_false(
            self.mclass(
                'moe', 'larry', 'curly', 30, 40, 50, True,
            ).dice(2, 'x'),
            self.assertEqual,
            [('moe', 'larry'), ('curly', 30), (40, 50), (True, 'x')],
        )

    def test_first(self):
        # auto
        self.assertEqual(self.qclass(5, 4, 3, 2, 1).first().end(), 5)
        self.assertEqual(self.qclass(5, 4, 3, 2, 1).first(2).end(), [5, 4])
        # man
        manchainsaw = self.mclass(5, 4, 3, 2, 1).first()
        self.assertFalse(manchainsaw.balanced)
        manchainsaw.shift_in()
        self.assertTrue(manchainsaw.balanced)
        self.assertEqual(manchainsaw.results(), 5)
        self.assertFalse(manchainsaw.balanced)
        self._false_true_false(
            self.mclass(5, 4, 3, 2, 1).first(2), self.assertEqual, [5, 4],
        )

    def test_index(self):
        # auto
        self.assertEqual(self.qclass(5, 4, 3, 2, 1).at(2).end(), 3)
        self.assertEqual(self.qclass(5, 4, 3, 2, 1).at(10, 11).end(), 11)
        # man
        self._false_true_false(
            self.mclass(5, 4, 3, 2, 1).at(2), self.assertEqual, 3,
        )
        self._false_true_false(
            self.mclass(5, 4, 3, 2, 1).at(10, 11), self.assertEqual, 11,
        )

    def test_slice(self):
        # auto
        self.assertEqual(self.qclass(5, 4, 3, 2, 1).slice(2).end(), [5, 4])
        self.assertEqual(self.qclass(5, 4, 3, 2, 1).slice(2, 4).end(), [3, 2])
        self.assertEqual(self.qclass(5, 4, 3, 2, 1).slice(2, 4, 2).end(), 3)
        # man
        self._false_true_false(
            self.mclass(5, 4, 3, 2, 1).slice(2), self.assertEqual, [5, 4],
        )
        self._false_true_false(
            self.mclass(5, 4, 3, 2, 1).slice(2, 4), self.assertEqual, [3, 2]
        )
        self._false_true_false(
            self.mclass(5, 4, 3, 2, 1).slice(2, 4, 2), self.assertEqual, 3,
        )

    def test_last(self):
        # auto
        self.assertEqual(self.qclass(5, 4, 3, 2, 1).last().end(), 1)
        self.assertEqual(self.qclass(5, 4, 3, 2, 1).last(2).end(), [2, 1])
        # man
        manchainsaw = self.mclass(5, 4, 3, 2, 1).last()
        self.assertFalse(manchainsaw.balanced)
        manchainsaw.shift_in()
        self.assertTrue(manchainsaw.balanced)
        self.assertEqual(manchainsaw.results(), 1)
        self.assertFalse(manchainsaw.balanced)
        self._false_true_false(
            self.mclass(5, 4, 3, 2).last(2), self.assertEqual, [3, 2],
        )

    def test_initial(self):
        # auto
        self.assertEqual(
            self.qclass(5, 4, 3, 2, 1).initial().end(), [5, 4, 3, 2]
        )
        # man
        self._false_true_false(
            self.mclass(5, 4, 3, 2, 1).initial(),
            self.assertEqual,
            [5, 4, 3, 2],
        )

    def test_rest(self):
        # auto
        self.assertEqual(
            self.qclass(5, 4, 3, 2, 1).rest().end(), [4, 3, 2, 1],
        )
        # man
        self._false_true_false(
            self.mclass(5, 4, 3, 2, 1).rest(), self.assertEqual, [4, 3, 2, 1],
        )

    def test_choice(self):
        # auto
        self.assertEqual(len(list(self.qclass(1, 2, 3, 4, 5, 6).choice())), 1)
        # man
        manchainsaw = self.mclass(1, 2, 3, 4, 5, 6).choice()
        self.assertFalse(manchainsaw.balanced)
        manchainsaw.shift_in()
        self.assertTrue(manchainsaw.balanced)
        manchainsaw.end()
        self.assertTrue(manchainsaw.balanced)

    def test_sample(self):
        #auto
        self.assertEqual(
            len(self.qclass(1, 2, 3, 4, 5, 6).sample(3).end()), 3,
        )
        # man
        manchainsaw = self.mclass(1, 2, 3, 4, 5, 6).sample(3)
        self.assertFalse(manchainsaw.balanced)
        manchainsaw.shift_in()
        self.assertTrue(manchainsaw.balanced)
        manchainsaw.end()
        self.assertTrue(manchainsaw.balanced)


class ReduceMixin(object):

    def test_flatten(self):
        # auto
        self.assertEqual(
            self.qclass([[1, [2], [3, [[4]]]], 'here']).flatten().end(),
            [1, 2, 3, 4, 'here'],
        )
        # man
        self._false_true_false(
            self.mclass([[1, [2], [3, [[4]]]], 'here']).flatten(),
            self.assertEqual,
            [1, 2, 3, 4, 'here'],
        )

    def test_merge(self):
        # auto
        self.assertEqual(
            self.qclass(
                ['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False]
            ).merge().end(),
            ['moe', 'larry', 'curly', 30, 40, 50, True, False, False],
        )
        # man
        self._false_true_false(
            self.mclass(
                ['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False],
            ).merge(),
            self.assertEqual,
            ['moe', 'larry', 'curly', 30, 40, 50, True, False, False],
        )

    def test_reduce(self):
        # auto
        self.assertEqual(
            self.qclass(1, 2, 3).tap(lambda x, y: x + y).reduce().end(), 6,
        )
        self.assertEqual(
            self.qclass(1, 2, 3).tap(lambda x, y: x + y).reduce(1).end(), 7,
        )
        self.assertEqual(
            self.qclass([0, 1], [2, 3], [4, 5]).tap(
                lambda x, y: x + y
            ).reduce(reverse=True).end(), [4, 5, 2, 3, 0, 1],
        )
        self.assertEqual(
            self.qclass([0, 1], [2, 3], [4, 5]).tap(
                lambda x, y: x + y
            ).reduce([0, 0], True).end(), [4, 5, 2, 3, 0, 1, 0, 0],
        )
        # man
        self._false_true_false(
            self.mclass(1, 2, 3).tap(lambda x, y: x + y).reduce(),
            self.assertEqual,
            6,
        )
        self._false_true_false(
            self.mclass(1, 2, 3).tap(lambda x, y: x + y).reduce(1),
            self.assertEqual,
            7,
        )
        self._false_true_false(
            self.mclass([0, 1], [2, 3], [4, 5]).tap(
                lambda x, y: x + y
            ).reduce(reverse=True),
            self.assertEqual,
             [4, 5, 2, 3, 0, 1],
        )
        self._false_true_false(
            self.mclass([0, 1], [2, 3], [4, 5]).tap(
                lambda x, y: x + y
            ).reduce([0, 0], True),
            self.assertEqual,
            [4, 5, 2, 3, 0, 1, 0, 0],
        )

    def test_weave(self):
        # auto
        self.assertEqual(
            self.qclass(
                ['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False]
            ).as_one().weave().end(),
            ['moe', 30, True, 'larry', 40, False, 'curly', 50, False],
        )
        # man
        self._false_true_false(
            self.mclass(
                ['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False]
            ).as_one().weave(),
            self.assertEqual,
            ['moe', 30, True, 'larry', 40, False, 'curly', 50, False],
        )

    def test_zip(self):
        # auto
        self.assertEqual(
            self.qclass(
                ['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False]
            ).as_one().zip().end(),
            [('moe', 30, True), ('larry', 40, False), ('curly', 50, False)],
        )
        # man
        self._true_true_false(
            self.mclass(
                ['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False],
            ).as_one().zip(),
            self.assertEqual,
            [('moe', 30, True), ('larry', 40, False), ('curly', 50, False)],
        )
