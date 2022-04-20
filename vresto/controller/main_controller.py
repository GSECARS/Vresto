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

import sys
from qtpy.QtWidgets import QApplication

from vresto.widget import MainWidget
from vresto.model import MainModel


class MainController:
    def __init__(self) -> None:
        self._app = QApplication(sys.argv)
        self._model = MainModel()
        self._widget = MainWidget(self._model.paths)

    def run(self, version: str) -> None:
        self._widget.display(version=version)
        sys.exit(self._app.exec())
