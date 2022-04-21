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
from qtpy.QtWidgets import QGroupBox, QPushButton, QLabel, QSlider, QGridLayout
from qtpy.QtCore import Qt, QSize

from vresto.model import PathModel


class CameraGroup(QGroupBox):

    _title = " Camera "
    _max_size = QSize(650, 155)

    def __init__(self, paths: PathModel) -> None:
        super(CameraGroup, self).__init__()

        self._paths = paths

        self.btn_camera_out = QPushButton("OUT")
        self.btn_camera_in = QPushButton("IN")
        self.lbl_r = QLabel("R")
        self.lbl_t = QLabel("T")
        self.slider_reflected = QSlider(Qt.Vertical)
        self.slider_transmitted = QSlider(Qt.Vertical)

        self._buttons = [
            self.btn_camera_out,
            self.btn_camera_in,
        ]
        self._labels = [
            self.lbl_r,
            self.lbl_t,
        ]

        self.setTitle(self._title)
        self.setStyleSheet(open(os.path.join(self._paths.qss_path, "camera_group.qss"), "r").read())

        self._set_object_names()
        self._set_widget_sizes()
        self._set_tool_status_tips()
        self._layout_group()

    def _set_object_names(self) -> None:
        """Sets all the object names for the group and the group widgets."""
        self.setObjectName("group-camera")
        [button.setObjectName("btn-camera") for button in self._buttons]
        [label.setObjectName("lbl-camera") for label in self._labels]
        self.slider_reflected.setObjectName("slider")
        self.slider_transmitted.setObjectName("slider")

    def _set_tool_status_tips(self) -> None:
        """Sets all the tool and status tips for the group."""

        self.slider_reflected.setStatusTip("Controls the reflected light intensity")
        self.slider_transmitted.setStatusTip("Controls the transmitted light intensity")

    def _set_widget_sizes(self) -> None:

        for button in self._buttons:
            button.setMinimumSize(100, 30)
            button.setMaximumHeight(35)

        self.slider_reflected.setMaximumHeight(120)

        self.setMaximumSize(self._max_size)

    def _layout_group(self) -> None:
        layout = QGridLayout()
        layout.setSpacing(10)

        layout.addWidget(self.btn_camera_out, 0, 0, 1, 1)
        layout.addWidget(self.btn_camera_in, 1, 0, 1, 1)

        layout.addWidget(self.slider_reflected, 0, 1, 2, 1)
        layout.addWidget(self.slider_transmitted, 0, 2, 2, 1)

        layout.addWidget(self.lbl_r, 2, 1, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lbl_t, 2, 2, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)
