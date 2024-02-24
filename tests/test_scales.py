from datetime import date, datetime
from decimal import Decimal

import leather


class TestLinear(leather.LeatherTestCase):
    def test_project(self):
        scale = leather.Linear(0, 10)

        self.assertEqual(scale.project(2, 0, 20), 4)
        self.assertEqual(scale.project(10, 0, 40), 40)
        self.assertEqual(scale.project(5, 10, 40), 25)
        self.assertEqual(scale.project(5, 10, 41), 25.5)

        scale = leather.Linear(10, 40)

        self.assertEqual(scale.project(25, 0, 10), 5)
        self.assertEqual(scale.project(4, 0, 20), -4)

        scale = leather.Linear(-10, 10)

        self.assertEqual(scale.project(0, 0, 10), 5)
        self.assertEqual(scale.project(-10, -5, 10), -5)

        scale = leather.Linear(-20, -10)

        self.assertEqual(scale.project(-15, 0, 10), 5)
        self.assertEqual(scale.project(-10, -5, 10), 10)

        with self.assertRaises(ValueError):
            leather.Linear(10, 0)

    def test_no_spread(self):
        scale = leather.Linear(0, 0)

        self.assertEqual(scale.project(0, 0, 10), 0)
        self.assertEqual(scale.project(1, 0, 10), 10)

    def test_ticks(self):
        scale = leather.Linear(0, 10)

        self.assertEqual(scale.ticks(), [0, 2.5, 5, 7.5, 10])

    def test_decimal(self):
        scale = leather.Linear(Decimal(0), Decimal(10))

        self.assertEqual(scale.project(Decimal(2), Decimal(0), Decimal(20)), Decimal(4))
        self.assertEqual(scale.project(Decimal(10), Decimal(0), Decimal(40)), Decimal(40))
        self.assertEqual(scale.project(Decimal(5), Decimal(10), Decimal(40)), Decimal(25))
        self.assertEqual(scale.project(Decimal(5), Decimal(10), Decimal(41)), Decimal(25.5))

        self.assertEqual(scale.ticks()[1], Decimal(2.5))

    def test_contains(self):
        scale = leather.Linear(-5, 5)

        self.assertTrue(scale.contains(-5))
        self.assertTrue(scale.contains(0))
        self.assertTrue(scale.contains(5))
        self.assertFalse(scale.contains(-6))
        self.assertFalse(scale.contains(6))


class TestOrdinal(leather.LeatherTestCase):
    def test_project(self):
        scale = leather.Ordinal(['a', 'b', 'c', 'd'])

        self.assertEqual(scale.project('b', 0, 20), 7.5)

        scale = leather.Ordinal(['a', 'd', 'c', 'b'])

        self.assertEqual(scale.project('b', 0, 20), 17.5)

    def test_project_interval(self):
        scale = leather.Ordinal(['a', 'b', 'c', 'd'])

        self.assertEqual(scale.project_interval('b', 0, 20), (5.25, 9.75))

        scale = leather.Ordinal(['a', 'd', 'c', 'b'])

        self.assertEqual(scale.project_interval('b', 0, 20), (15.25, 19.75))

    def test_ticks(self):
        scale = leather.Ordinal(['a', 'b', 'c', 'd'])

        self.assertEqual(scale.ticks(), ['a', 'b', 'c', 'd'])

    def test_contains(self):
        scale = leather.Ordinal(['a', 'b', 'c', 'd'])

        self.assertTrue(scale.contains('a'))
        self.assertFalse(scale.contains('aa'))
        self.assertFalse(scale.contains('e'))
        self.assertFalse(scale.contains(5))


class TestTemporal(leather.LeatherTestCase):
    """
    Note: due to leap-year calculations, it's almost impossible to write
    exact tests for this scale which are not trivial.
    """
    def test_project(self):
        scale = leather.Temporal(date(2010, 1, 1), date(2014, 1, 1))

        self.assertAlmostEqual(scale.project(date(2011, 1, 1), 0, 20), 5, 1)
        self.assertAlmostEqual(scale.project(date(2012, 1, 1), 0, 20), 10, 1)
        self.assertAlmostEqual(scale.project(date(2009, 1, 1), 0, 20), -5, 1)

        scale = leather.Temporal(datetime(2010, 1, 1), datetime(2014, 1, 1))

        self.assertAlmostEqual(scale.project(datetime(2011, 1, 1), 0, 20), 5, 1)
        self.assertAlmostEqual(scale.project(datetime(2012, 1, 1), 0, 20), 10, 1)
        self.assertAlmostEqual(scale.project(datetime(2009, 1, 1), 0, 20), -5, 1)

    def test_project_interval(self):
        scale = leather.Temporal(date(2010, 1, 1), date(2014, 1, 1))

        with self.assertRaises(NotImplementedError):
            scale.project_interval(date(2011, 1, 1), 0, 20)

    def test_ticks(self):
        scale = leather.Temporal(date(2010, 1, 1), date(2014, 1, 1))

        ticks = scale.ticks()
        self.assertEqual(ticks[0], date(2010, 1, 1))
        self.assertEqual(ticks[-1], date(2014, 1, 1))

    def test_contains(self):
        scale = leather.Temporal(date(2010, 1, 1), date(2014, 1, 1))

        self.assertTrue(scale.contains(date(2010, 1, 1)))
        self.assertTrue(scale.contains(date(2012, 6, 3)))
        self.assertTrue(scale.contains(date(2014, 1, 1)))
        self.assertFalse(scale.contains(date(2009, 12, 31)))
        self.assertFalse(scale.contains(date(2014, 1, 2)))
