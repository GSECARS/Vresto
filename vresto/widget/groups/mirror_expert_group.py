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
from qtpy.QtWidgets import QGroupBox, QHBoxLayout, QPushButton, QLabel, QGridLayout, QLineEdit
from qtpy.QtCore import Qt, QSize

from vresto.model import PathModel


class MirrorExpertGroup(QGroupBox):

    _title = " Laser-mirrors "
    _max_size = QSize(280, 250)

    def __init__(self, paths: PathModel) -> None:
        super(MirrorExpertGroup, self).__init__()

        self._paths = paths

        self._lbl_ds = QLabel("DOWNSTREAM")
        self._lbl_us = QLabel("UPSTREAM")

        self.btn_ds_out = QPushButton("OUT")
        self.btn_ds_in = QPushButton("IN")
        self.btn_us_out = QPushButton("OUT")
        self.btn_us_in = QPushButton("IN")
        self.btn_us_plus = QPushButton("+")
        self.btn_us_minus = QPushButton("-")
        self.btn_ds_plus = QPushButton("+")
        self.btn_ds_minus = QPushButton("-")
        self.btn_step_1 = QPushButton()
        self.btn_step_2 = QPushButton()
        self.btn_step_3 = QPushButton()

        self.lne_us = QLineEdit()
        self.lne_ds = QLineEdit()

        self.lbl_step = QLabel("Step (mm)")

        self._buttons = [
            self.btn_ds_out,
            self.btn_ds_in,
            self.btn_us_out,
            self.btn_us_in,
        ]

        self._plus_buttons = [
            self.btn_us_plus,
            self.btn_ds_plus,
        ]

        self._minus_buttons = [
            self.btn_us_minus,
            self.btn_ds_minus,
        ]

        self._step_buttons = [
            self.btn_step_1,
            self.btn_step_2,
            self.btn_step_3,
        ]

        self._lne_boxes = [
            self.lne_us,
            self.lne_ds,
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
        [plus_button.setObjectName("btn-plus") for plus_button in self._plus_buttons]
        [minus_button.setObjectName("btn-minus") for minus_button in self._minus_buttons]
        [step_button.setObjectName("btn-step") for step_button in self._step_buttons]
        [lne.setObjectName("lne-mirror") for lne in self._lne_boxes]
        self._lbl_ds.setObjectName("lbl-mirror")
        self._lbl_us.setObjectName("lbl-mirror")
        self.lbl_step.setObjectName("lbl-step")

    def _set_tool_status_tips(self) -> None:
        """Sets all the tool and status tips for the group."""
        pass

    def _set_widget_sizes(self) -> None:

        for button in self._buttons:
            button.setMinimumSize(100, 30)
            button.setMaximumHeight(50)

        [step_button.setFixedSize(40, 20) for step_button in self._step_buttons]
        [lne.setFixedHeight(20) for lne in self._lne_boxes]

        self.setMaximumSize(self._max_size)

    def _layout_group(self) -> None:
        layout_step_widgets = QHBoxLayout()
        layout_step_widgets.setContentsMargins(0, 0, 0, 0)
        layout_step_widgets.setSpacing(2)
        layout_step_widgets.addWidget(self.lbl_step, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_step_widgets.addStretch(1)
        layout_step_widgets.addWidget(self.btn_step_1, alignment=Qt.AlignmentFlag.AlignRight)
        layout_step_widgets.addWidget(self.btn_step_2, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout_step_widgets.addWidget(self.btn_step_3, alignment=Qt.AlignmentFlag.AlignLeft)

        layout = QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(self._lbl_ds, 0, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._lbl_us, 0, 2, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.btn_ds_out, 1, 0, 1, 2)
        layout.addWidget(self.btn_ds_in, 2, 0, 1, 2)
        layout.addWidget(self.btn_us_out, 1, 2, 1, 2)
        layout.addWidget(self.btn_us_in, 2, 2, 1, 2)
        layout.addWidget(self.btn_ds_plus, 3, 0, 1, 2)
        layout.addWidget(self.lne_ds, 4, 0, 1, 2)
        layout.addWidget(self.btn_ds_minus, 5, 0, 1, 2)
        layout.addWidget(self.btn_us_plus, 3, 2, 1, 2)
        layout.addWidget(self.lne_us, 4, 2, 1, 2)
        layout.addWidget(self.btn_us_minus, 5, 2, 1, 2)
        layout.addLayout(layout_step_widgets, 6, 0, 1, 4)

        self.setLayout(layout)
