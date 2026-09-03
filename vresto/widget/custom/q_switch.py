#!/usr/bin/python3
# ----------------------------------------------------------------------
# vresto - Diamond Anvil Cell Corrections GUI software.
# Author: Christofanis Skordas (skordasc@uchicago.edu)
# Copyright (C) 2022  GSECARS, The University of Chicago
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

from typing import Optional
from qtpy.QtWidgets import QAbstractButton, QWidget, QSizePolicy
from qtpy.QtGui import QColor, QPalette, QPainter
from qtpy.QtCore import QSize, QEvent, Qt, QPropertyAnimation, Property


class QSwitch(QAbstractButton):
    """Custom button that acts like a toggle switch."""

    def __init__(self,
                 parent: QWidget,
                 track_radius: Optional[int] = 10,
                 thumb_radius: Optional[int] = 8,
                 active_color: Optional[QColor] = QColor("#677bc4"),
                 inactive_color: Optional[QColor] = QColor("#7b7f8a"),
                 circle_color: Optional[QColor] = QColor("#dbdcdd")
                 ) -> None:
        super(QSwitch, self).__init__(parent=parent)

        self._track_radius = track_radius
        self._thumb_radius = thumb_radius
        self._active_color = active_color
        self._inactive_color = inactive_color
        self._circle_color = circle_color

        # Helpers
        self._margin = None
        self._offset = None
        self._base_offset = None
        self._end_offset = None

        self._configure_switch()
        self._configure_colors()

    def _configure_switch(self) -> None:
        self.setCheckable(True)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self._margin = max(0, self._thumb_radius - self._track_radius)
        self._base_offset = max(self._thumb_radius, self._track_radius)
        self._end_offset = {
            True: lambda: self.width() - self._base_offset,
            False: lambda: self._base_offset,
        }
        self._offset = self._base_offset

    def _configure_colors(self) -> None:

        palette = self.palette()
        palette.setColor(QPalette.Highlight, self._active_color)
        palette.setColor(QPalette.Dark, self._inactive_color)
        palette.setColor(QPalette.Light, self._circle_color)

        if self._thumb_radius > self._track_radius:
            self._track_color = {
                True: palette.highlight(),
                False: palette.dark(),
            }
            self._thumb_color = {
                True: palette.highlight(),
                False: palette.light(),
            }
            self._track_opacity = 0.5
        else:
            self._track_color = {
                True: palette.highlight(),
                False: palette.dark(),
            }
            self._thumb_color = {
                True: palette.highlightedText(),
                False: palette.light(),
            }
            self._track_opacity = 1

    def sizeHint(self) -> QSize:
        return QSize(
            4 * self._track_radius + 2 * self._margin,
            2 * self._track_radius + 2 * self._margin,
        )

    def resizeEvent(self, event: QEvent) -> None:
        super().resizeEvent(event)
        self._offset = self._end_offset[self.isChecked()]()

    def paintEvent(self, event: QEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setPen(Qt.NoPen)
        track_opacity = self._track_opacity
        thumb_opacity = 1.0

        if self.isEnabled():
            track_brush = self._track_color[self.isChecked()]
            thumb_brush = self._thumb_color[self.isChecked()]
        else:
            track_opacity *= 0.8
            track_brush = self.palette().shadow()
            thumb_brush = self.palette().mid()

        painter.setBrush(track_brush)
        painter.setOpacity(track_opacity)
        painter.drawRoundedRect(
            self._margin,
            self._margin,
            self.width() - 2 * self._margin,
            self.height() - 2 * self._margin,
            self._track_radius,
            self._track_radius,
        )

        painter.setBrush(thumb_brush)
        painter.setOpacity(thumb_opacity)
        painter.drawEllipse(
            self._offset - self._thumb_radius,
            self._base_offset - self._thumb_radius,
            2 * self._thumb_radius,
            2 * self._thumb_radius,
        )

    def setChecked(self, status: bool) -> None:
        super().setChecked(status)
        self._offset = self._end_offset[status]()

    def mouseReleaseEvent(self, event: QEvent) -> None:
        super().mouseReleaseEvent(event)
        if event.button() == Qt.LeftButton:
            animation = QPropertyAnimation(self, b'offset', self)
            animation.setDuration(120)
            animation.setStartValue(self._offset)
            animation.setEndValue(self._end_offset[self.isChecked()]())
            animation.start()

    def enterEvent(self, event: QEvent) -> None:
        self.setCursor(Qt.PointingHandCursor)
        super().enterEvent(event)

    @Property(int)
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, value):
        self._offset = value
        self.update()
