import leather


class TestBars(leather.LeatherTestCase):
    def setUp(self):
        self.shape = leather.Bars('red')
        self.linear = leather.Linear(0, 10)
        self.ordinal = leather.Ordinal(['foo', 'bar', 'bing'])
        self.palette = (color for color in ['red', 'white', 'blue'])

    def test_to_svg(self):
        series = leather.Series([
            (0, 'foo'),
            (5, 'bar'),
            (10, 'bing')
        ])

        group = self.shape.to_svg(200, 100, self.linear, self.ordinal, series, self.palette)
        rects = list(group)

        self.assertEqual(len(rects), 3)
        self.assertEqual(float(rects[2].get('x')), 0)
        self.assertEqual(float(rects[2].get('width')), 200)

    def test_nulls(self):
        series = leather.Series([
            (0, 'foo'),
            (None, None),
            (10, 'bing')
        ])

        group = self.shape.to_svg(200, 100, self.linear, self.ordinal, series, self.palette)
        rects = list(group)

        self.assertEqual(len(rects), 2)
        self.assertEqual(float(rects[1].get('x')), 0)
        self.assertEqual(float(rects[1].get('width')), 200)

    def test_zeros(self):
        series = leather.Series([
            (0, 'foo'),
            (0, None),
            (0, 'bing')
        ])

        linear = leather.Linear(0, 0)

        group = self.shape.to_svg(200, 100, linear, self.ordinal, series, self.palette)
        rects = list(group)

        self.assertEqual(len(rects), 2)
        self.assertEqual(float(rects[1].get('x')), 0)
        self.assertEqual(float(rects[1].get('width')), 0)

    def test_validate(self):
        series = leather.Series([
            (1, 'foo')
        ])

        self.shape.validate_series(series)

        series = leather.Series([
            ('foo', 1)
        ])

        with self.assertRaises(ValueError):
            self.shape.validate_series(series)


class TestColumns(leather.LeatherTestCase):
    def setUp(self):
        self.shape = leather.Columns('red')
        self.linear = leather.Linear(0, 10)
        self.ordinal = leather.Ordinal(['foo', 'bar', 'bing'])
        self.palette = (color for color in ['red', 'white', 'blue'])

    def test_to_svg(self):
        series = leather.Series([
            ('foo', 0),
            ('bar', 5),
            ('bing', 10)
        ])

        group = self.shape.to_svg(200, 100, self.ordinal, self.linear, series, self.palette)
        rects = list(group)

        self.assertEqual(len(rects), 3)
        self.assertEqual(float(rects[1].get('y')), 50)
        self.assertEqual(float(rects[1].get('height')), 50)

    def test_nulls(self):
        series = leather.Series([
            ('foo', 0),
            (None, None),
            ('bing', 10)
        ])

        group = self.shape.to_svg(200, 100, self.ordinal, self.linear, series, self.palette)
        rects = list(group)

        self.assertEqual(len(rects), 2)
        self.assertEqual(float(rects[1].get('y')), 0)
        self.assertEqual(float(rects[1].get('height')), 100)

    def test_validate(self):
        series = leather.Series([
            ('foo', 1)
        ])

        self.shape.validate_series(series)

        series = leather.Series([
            (1, 'foo')
        ])

        with self.assertRaises(ValueError):
            self.shape.validate_series(series)


class TestDots(leather.LeatherTestCase):
    def setUp(self):
        self.shape = leather.Dots('red')
        self.linear = leather.Linear(0, 10)
        self.ordinal = leather.Ordinal(['foo', 'bar', 'bing'])
        self.palette = (color for color in ['red', 'white', 'blue'])

    def test_linear(self):
        series = leather.Series([
            (0, 0),
            (5, 5),
            (10, 10)
        ])

        group = self.shape.to_svg(200, 100, self.linear, self.linear, series, self.palette)
        circles = list(group)

        self.assertEqual(len(circles), 3)
        self.assertEqual(float(circles[1].get('cx')), 100)
        self.assertEqual(float(circles[1].get('cy')), 50)

    def test_ordinal(self):
        series = leather.Series([
            ('foo', 0),
            ('bar', 5),
            ('bing', 10)
        ])

        group = self.shape.to_svg(200, 100, self.ordinal, self.linear, series, self.palette)
        circles = list(group)

        self.assertEqual(len(circles), 3)
        self.assertEqual(float(circles[1].get('cx')), 100)
        self.assertEqual(float(circles[1].get('cy')), 50)

    def test_nulls(self):
        series = leather.Series([
            (0, 0),
            (None, None),
            (10, 10)
        ])

        group = self.shape.to_svg(200, 100, self.linear, self.linear, series, self.palette)
        circles = list(group)

        self.assertEqual(len(circles), 2)
        self.assertEqual(float(circles[1].get('cx')), 200)
        self.assertEqual(float(circles[1].get('cy')), 0)

    def test_validate(self):
        series = leather.Series([
            (1, 1)
        ])

        self.shape.validate_series(series)

        series = leather.Series([
            (1, 'foo')
        ])

        with self.assertRaises(ValueError):
            self.shape.validate_series(series)


class TestLine(leather.LeatherTestCase):
    def setUp(self):
        self.shape = leather.Line('red')
        self.linear = leather.Linear(0, 10)
        self.ordinal = leather.Ordinal(['foo', 'bar', 'bing'])
        self.palette = (color for color in ['red', 'white', 'blue'])

    def test_linear(self):
        series = leather.Series([
            (0, 0),
            (5, 5),
            (10, 10)
        ])

        group = self.shape.to_svg(200, 100, self.linear, self.linear, series, self.palette)
        paths = list(group)

        self.assertEqual(len(paths), 1)

    def test_ordinal(self):
        series = leather.Series([
            ('foo', 0),
            ('bar', 5),
            ('bing', 10)
        ])

        group = self.shape.to_svg(200, 100, self.ordinal, self.linear, series, self.palette)
        paths = list(group)

        self.assertEqual(len(paths), 1)

    def test_nulls(self):
        series = leather.Series([
            (0, 0),
            (None, None),
            (10, 10)
        ])

        group = self.shape.to_svg(200, 100, self.linear, self.linear, series, self.palette)
        paths = list(group)

        self.assertEqual(len(paths), 2)

    def test_validate(self):
        series = leather.Series([
            (1, 1)
        ])

        self.shape.validate_series(series)

        series = leather.Series([
            (1, 'foo')
        ])

        with self.assertRaises(ValueError):
            self.shape.validate_series(series)
