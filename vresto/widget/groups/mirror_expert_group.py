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
from qtpy.QtWidgets import QGroupBox, QPushButton, QLabel, QGridLayout
from qtpy.QtCore import Qt, QSize

from vresto.model import PathModel


class MirrorExpertGroup(QGroupBox):

    _title = " Laser-mirrors "
    _max_size = QSize(280, 200)

    def __init__(self, paths: PathModel) -> None:
        super(MirrorExpertGroup, self).__init__()

        self._paths = paths

        self._lbl_ds = QLabel("DOWNSTREAM")
        self._lbl_us = QLabel("UPSTREAM")
        self.lbl_ds_position = QLabel("Unknown")
        self.lbl_us_position = QLabel("Unknown")

        self.btn_ds_out = QPushButton("OUT")
        self.btn_ds_in = QPushButton("IN")
        self.btn_us_out = QPushButton("OUT")
        self.btn_us_in = QPushButton("IN")

        self._buttons = [
            self.btn_ds_out,
            self.btn_ds_in,
            self.btn_us_out,
            self.btn_us_in,
        ]

        self.setTitle(self._title)
        self.setStyleSheet(
            open(os.path.join(self._paths.qss_path, "mirror_expert_group.qss"), "r").read()
        )

        self._set_object_names()
        self._set_widget_sizes()
        self._set_tool_status_tips()
        self._layout_group()

    def _set_object_names(self) -> None:
        """Sets all the object names for the group and the group widgets."""
        self.setObjectName("group-mirrors")
        [button.setObjectName("btn-mirrors") for button in self._buttons]
        self._lbl_ds.setObjectName("lbl-mirror")
        self._lbl_us.setObjectName("lbl-mirror")
        self.lbl_ds_position.setObjectName("lbl-mirror-position")
        self.lbl_us_position.setObjectName("lbl-mirror-position")

    def _set_tool_status_tips(self) -> None:
        """Sets all the tool and status tips for the group."""
        self.lbl_ds_position.setStatusTip(
            "The downstream mirror is currently located at the given value."
        )
        self.lbl_us_position.setStatusTip(
            "The upstream mirror is currently located at the given value."
        )

    def _set_widget_sizes(self) -> None:

        for button in self._buttons:
            button.setMinimumSize(100, 30)
            button.setMaximumHeight(50)

        self.setMaximumSize(self._max_size)

    def _layout_group(self) -> None:
        layout = QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(self._lbl_ds, 0, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._lbl_us, 0, 2, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.btn_ds_out, 1, 0, 1, 2)
        layout.addWidget(self.btn_ds_in, 2, 0, 1, 2)
        layout.addWidget(self.btn_us_out, 1, 2, 1, 2)
        layout.addWidget(self.btn_us_in, 2, 2, 1, 2)
        layout.addWidget(self.lbl_ds_position, 3, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lbl_us_position, 3, 2, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)
