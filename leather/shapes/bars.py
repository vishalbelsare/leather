#!/usr/bin/env python

import xml.etree.ElementTree as ET

import six

from leather.series import CategorySeries
from leather.shapes.base import Shape


class Bars(Shape):
    """
    Render a series of data as bars.

    :param color:
        The color to fill the bars. You may also specify a
        :func:`.style_function`.
    """
    def __init__(self, fill_color):
        self._fill_color = fill_color

    def validate_series(self, series):
        """
        Verify this shape can be used to render a given series.
        """
        if isinstance(series, CategorySeries):
            raise ValueError('Bars can not be used to render CategorySeries.')

    def to_svg(self, width, height, x_scale, y_scale, series, palette):
        """
        Render bars to SVG elements.
        """
        group = ET.Element('g')
        group.set('class', 'series bars')

        zero_x = x_scale.project(0, 0, width)

        if self._fill_color:
            fill_color = self._fill_color
        else:
            fill_color = next(palette)

        # Bars display "top-down"
        for d in series.data(reverse=True):
            if d.x is None or d.y is None:
                continue

            y1, y2 = y_scale.project_interval(d.y, height, 0)
            proj_x = x_scale.project(d.x, 0, width)

            if d.x < 0:
                bar_x = proj_x
                bar_width = zero_x - proj_x
            else:
                bar_x = zero_x
                bar_width = proj_x - zero_x

            if callable(self._fill_color):
                color = self._fill_color(d.x, d.y, d.row, d.i)
            else:
                color = self._fill_color

            group.append(ET.Element('rect',
                x=six.text_type(bar_x),
                y=six.text_type(y2),
                width=six.text_type(bar_width),
                height=six.text_type(y1 - y2),
                fill=color
            ))

        return group
