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
from qtpy.QtWidgets import (
    QGroupBox,
    QPushButton,
    QLabel,
    QLineEdit,
    QHBoxLayout,
    QGridLayout,
)
from qtpy.QtCore import Qt, QSize
from qtpy.QtGui import QDoubleValidator

from vresto.model import PathModel


class PinholeGroup(QGroupBox):

    _title: str = " Pinhole "
    _max_size: QSize = QSize(280, 200)

    def __init__(self, paths: PathModel) -> None:
        super(PinholeGroup, self).__init__()

        self._paths = paths

        self.lbl_position = QLabel("Unknown")
        self.btn_in = QPushButton("IN")
        self.btn_15 = QPushButton("-15")
        self.btn_20 = QPushButton("-20")
        self.btn_out = QPushButton("OUT")
        self.lbl_custom = QLabel("Custom (mm):")
        self.lne_custom = QLineEdit()

        self.setTitle(self._title)
        self.setStyleSheet(
            open(os.path.join(self._paths.qss_path, "pinhole_group.qss"), "r").read()
        )

        self._configure_lne_box()
        self._set_object_names()
        self._set_tool_status_tips()
        self._set_widget_sizes()
        self._layout_group()

    def _configure_lne_box(self) -> None:
        self.lne_custom.setValidator(QDoubleValidator(-200000, 200000, 4))

    def _set_object_names(self) -> None:
        """Sets all the object names for the group and the group widgets."""
        self.setObjectName("group-pinhole")
        self.btn_in.setObjectName("btn-pinhole")
        self.btn_15.setObjectName("btn-pinhole")
        self.btn_20.setObjectName("btn-pinhole")
        self.btn_out.setObjectName("btn-pinhole")
        self.lbl_custom.setObjectName("lbl-custom")
        self.lne_custom.setObjectName("lne-custom")

        self.lbl_position.setObjectName("lbl-pinhole-positions")

    def _set_tool_status_tips(self) -> None:
        """Sets all the tool and status tips for the group."""
        self.lne_custom.setToolTip("Moves the pinhole to the given position.")
        self.lbl_position.setStatusTip(
            "The pinhole is currently located at the given position."
        )

    def _set_widget_sizes(self) -> None:
        buttons = [self.btn_in, self.btn_15, self.btn_20, self.btn_out]

        for button in buttons:
            button.setMinimumSize(60, 30)
            button.setMaximumHeight(50)

        self.lne_custom.setMinimumSize(60, 30)
        self.lne_custom.setMaximumHeight(50)
        self.lne_custom.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setMaximumSize(self._max_size)

    def _layout_group(self) -> None:
        layout_top_buttons = QHBoxLayout()
        layout_top_buttons.setContentsMargins(0, 0, 0, 0)
        layout_top_buttons.setSpacing(5)
        layout_top_buttons.addWidget(self.btn_in)
        layout_top_buttons.addWidget(self.btn_15)
        layout_top_buttons.addWidget(self.btn_20)
        layout_top_buttons.addWidget(self.btn_out)

        layout = QGridLayout()
        layout.setSpacing(10)
        layout.addLayout(layout_top_buttons, 0, 0, 1, 4)
        layout.addWidget(
            self.lbl_custom, 1, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout.addWidget(self.lne_custom, 1, 2, 1, 2)
        layout.addWidget(
            self.lbl_position, 2, 0, 1, 4, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.setLayout(layout)
