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

import os
from qtpy.QtWidgets import QMainWindow, QTabWidget, QMessageBox, QLabel, QFrame, QGridLayout, QHBoxLayout, QVBoxLayout
from qtpy.QtCore import QSize
from qtpy.QtGui import QIcon, QCloseEvent

from vresto.model import PathModel


class MainWidget(QMainWindow):
    """The main application widget."""

    _size: QSize = QSize(780, 860)
    _hutch: str = ""

    def __init__(self, paths: PathModel) -> None:
        super(MainWidget, self).__init__()

        self._paths = paths

        # Groups - Define groups below

        self._main_frame = QFrame()
        self._tab_widget = QTabWidget()
        self.alignment_widget = None
        self.lbl_epics_status = QLabel()
        self._lbl_hutch = QLabel(self._hutch)

        # Enable the status bar
        self.statusBar()

        # Event helpers
        self._terminated: bool = False
        self._worker_finished: bool = False

        self._configure_tab_widget()
        self._configure_epics_status_widgets()
        self._configure_main_frame()
        self._configure_widget()

    def _configure_widget(self) -> None:
        """Basic window configuration."""
        # Set the object name
        self.setObjectName("QMainWindow")

        # Set the icon
        self.setWindowIcon(QIcon(os.path.join(self._paths.icon_path, "diamond.png")))

        # Load qss
        self.setStyleSheet(open(os.path.join(self._paths.qss_path, "main.qss"), "r").read())

        # Set maximum size
        self.setMaximumSize(self._size)

        # Set central widget
        self.setCentralWidget(self._main_frame)

    def _configure_tab_widget(self) -> None:
        """Configures the main tab widget (central widget)."""
        # Add tabs
        self._tab_widget.addTab(self.alignment_widget, "ALIGNMENT")

    def _configure_epics_status_widgets(self) -> None:
        # Circle indicator
        self.lbl_epics_status.setEnabled(False)
        self.lbl_epics_status.setObjectName("lbl-epics")

        # Hutch label
        self._lbl_hutch.setObjectName("lbl-hutch")

    def _configure_main_frame(self) -> None:

        horiz_layout = QHBoxLayout()
        horiz_layout.setSpacing(0)
        horiz_layout.addStretch(1)
        horiz_layout.addWidget(self.lbl_epics_status)
        horiz_layout.addWidget(self._lbl_hutch)

        vert_layout = QVBoxLayout()
        vert_layout.addLayout(horiz_layout)
        vert_layout.addStretch(1)

        layout = QGridLayout()
        layout.addWidget(self._tab_widget, 0, 0, 1, 1)
        layout.addLayout(vert_layout, 0, 0, 1, 1)

        self._main_frame.setLayout(layout)

    def display(self, version: str) -> None:
        """Sets the window title and the window visibility to normal."""
        # Set the title
        self.setWindowTitle(f"Vresto {version}")

        self.showNormal()

    def closeEvent(self, event: QCloseEvent) -> None:
        """Creates a message box for exit confirmation if closeEvent is triggered."""
        _msg_question = QMessageBox.question(
            self, "Exit confirmation", "Are you sure you want to close the application?"
        )

        if _msg_question == QMessageBox.Yes:

            self._terminated = True

            while not self._worker_finished:
                continue

            event.accept()
        else:
            event.ignore()

    @property
    def terminated(self) -> bool:
        return self._terminated

    @property
    def worker_finished(self) -> bool:
        return self._worker_finished

    @worker_finished.setter
    def worker_finished(self, value: bool) -> None:
        self._worker_finished = value
