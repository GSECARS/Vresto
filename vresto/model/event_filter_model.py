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

from qtpy.QtCore import QObject, QEvent
from qtpy.QtWidgets import QLineEdit

from vresto.model import DoubleValuePV


class EventFilterModel(QObject):
    """Custom event filter model to be used for focus out events."""

    def __init__(self, stage: DoubleValuePV) -> None:
        super(EventFilterModel, self).__init__()
        self.stage = stage

    def eventFilter(self, widget: QLineEdit, event: QEvent) -> bool:
        # Make available only for FocusOut events.
        if event.type() == QEvent.FocusOut:
            if not self.stage.moving:
                widget.setText(str("{0:.4f}".format(self.stage.readback)))

        return False
