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
import time
from qtpy.QtWidgets import QApplication
from qtpy.QtCore import QObject, Signal

from vresto.widget import MainWidget
from vresto.model import MainModel, QtWorkerModel


class MainController(QObject):
    _epics_connection_changed: Signal = Signal(bool)

    def __init__(self) -> None:
        super(MainController, self).__init__()

        self._app = QApplication(sys.argv)
        self._model = MainModel()
        self._widget = MainWidget(self._model.paths)

        # Event helpers
        self._time_started = None

        self._epics_connection_changed.connect(self._update_epics_status_label)

        self._main_worker = QtWorkerModel(self._worker_methods, ())
        self._main_worker.start()

    def run(self, version: str) -> None:
        self._widget.display(version=version)
        sys.exit(self._app.exec())

    def _update_epics_status_label(self, status: bool) -> None:
        self._widget.lbl_epics_status.setEnabled(status)

    def _check_epics_connection(self) -> None:
        """Checks the epics connection every 5 minutes."""
        #
        if self._time_started is None:
            self._time_started = time.time()
            self._model.epics.connect()

        now = time.time()
        if now - self._time_started > 300:
            self._time_started = time.time()

            self._model.epics.connect()

        self._epics_connection_changed.emit(self._model.epics.connected)

    def _worker_methods(self) -> None:
        while not self._widget.terminated:
            self._check_epics_connection()
            time.sleep(0.05)

        self._widget.worker_finished = True
