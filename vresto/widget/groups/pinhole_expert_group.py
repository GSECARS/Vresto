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
    QVBoxLayout,
    QGridLayout,
)
from qtpy.QtCore import Qt, QSize
from qtpy.QtGui import QDoubleValidator

from vresto.model import PathModel


class PinholeExpertGroup(QGroupBox):

    _title: str = " Pinhole "
    _max_size: QSize = QSize(280, 140)

    def __init__(self, paths: PathModel) -> None:
        super(PinholeExpertGroup, self).__init__()

        self._paths = paths

        self.btn_pinhole_position_plus = QPushButton("+")
        self.btn_pinhole_position_minus = QPushButton("-")
        self.btn_pinhole_vertical_plus = QPushButton("+")
        self.btn_pinhole_vertical_minus = QPushButton("-")
        self.btn_pinhole_horizontal_plus = QPushButton("+")
        self.btn_pinhole_horizontal_minus = QPushButton("-")
        self.btn_step_1 = QPushButton()
        self.btn_step_2 = QPushButton()
        self.btn_step_3 = QPushButton()

        self._plus_buttons = [
            self.btn_pinhole_position_plus,
            self.btn_pinhole_vertical_plus,
            self.btn_pinhole_horizontal_plus,
        ]

        self._minus_buttons = [
            self.btn_pinhole_position_minus,
            self.btn_pinhole_vertical_minus,
            self.btn_pinhole_horizontal_minus,
        ]

        self._step_buttons = [
            self.btn_step_1,
            self.btn_step_2,
            self.btn_step_3,
        ]

        self.lbl_step = QLabel("Step (mm)")
        self.lbl_pinhole_position = QLabel("Position")
        self.lbl_pinhole_vertical = QLabel("Vertical")
        self.lbl_pinhole_horizontal = QLabel("Horizontal")

        self._labels = [
            self.lbl_pinhole_position,
            self.lbl_pinhole_vertical,
            self.lbl_pinhole_horizontal,
        ]

        self.lne_pinhole_position = QLineEdit()
        self.lne_pinhole_vertical = QLineEdit()
        self.lne_pinhole_horizontal = QLineEdit()
        self._lne_boxes = [
            self.lne_pinhole_position,
            self.lne_pinhole_vertical,
            self.lne_pinhole_horizontal,
        ]

        self.setTitle(self._title)
        self.setStyleSheet(
            open(os.path.join(self._paths.qss_path, "pinhole_expert_group.qss"), "r").read()
        )

        self._configure_lne_box()
        self._set_object_names()
        self._set_tool_status_tips()
        self._set_widget_sizes()
        self._layout_group()

    def _configure_lne_box(self) -> None:
        for lne_box in self._lne_boxes:
            lne_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lne_box.setValidator(QDoubleValidator(-200000, 200000, 4))

    def _set_object_names(self) -> None:
        """Sets all the object names for the group and the group widgets."""
        self.setObjectName("group-pinhole")
        [plus_button.setObjectName("btn-plus") for plus_button in self._plus_buttons]
        [minus_button.setObjectName("btn-minus") for minus_button in self._minus_buttons]
        [step_button.setObjectName("btn-step") for step_button in self._step_buttons]
        [lne.setObjectName("lne-pinhole") for lne in self._lne_boxes]
        [label.setObjectName("lbl-pinhole") for label in self._labels]
        self.lbl_step.setObjectName("lbl-step")

    def _set_tool_status_tips(self) -> None:
        """Sets all the tool and status tips for the group."""
        self.lne_pinhole_vertical.setStatusTip("Read/input the position of the vertical pinhole motor.")
        self.lne_pinhole_horizontal.setStatusTip("Read/input the position of the horizontal pinhole motor.")

        [plus_button.setToolTip("Positive values") for plus_button in self._plus_buttons]
        [minus_button.setToolTip("Negative values") for minus_button in self._minus_buttons]
        [step_button.setToolTip("Step value") for step_button in self._step_buttons]

    def _set_widget_sizes(self) -> None:
        [step_button.setFixedSize(40, 20) for step_button in self._step_buttons]
        [lne.setFixedSize(60, 20) for lne in self._lne_boxes]

        self.setMaximumSize(self._max_size)

    def _layout_group(self) -> None:

        layout_step_widgets = QVBoxLayout()
        layout_step_widgets.setContentsMargins(0, 0, 0, 0)
        layout_step_widgets.setSpacing(2)
        layout_step_widgets.addWidget(self.lbl_step, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_step_widgets.addWidget(self.btn_step_1, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout_step_widgets.addWidget(self.btn_step_2, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout_step_widgets.addWidget(self.btn_step_3, alignment=Qt.AlignmentFlag.AlignHCenter)

        layout_pinhole_position = QHBoxLayout()
        layout_pinhole_position.setSpacing(2)
        layout_pinhole_position.addWidget(self.lbl_pinhole_position)
        layout_pinhole_position.addStretch(1)
        layout_pinhole_position.addWidget(self.btn_pinhole_position_minus)
        layout_pinhole_position.addWidget(self.lne_pinhole_position)
        layout_pinhole_position.addWidget(self.btn_pinhole_position_plus)

        layout_pinhole_vertical = QHBoxLayout()
        layout_pinhole_vertical.setSpacing(2)
        layout_pinhole_vertical.addWidget(self.lbl_pinhole_vertical)
        layout_pinhole_vertical.addStretch(1)
        layout_pinhole_vertical.addWidget(self.btn_pinhole_vertical_minus)
        layout_pinhole_vertical.addWidget(self.lne_pinhole_vertical)
        layout_pinhole_vertical.addWidget(self.btn_pinhole_vertical_plus)

        layout_pinhole_horizontal = QHBoxLayout()
        layout_pinhole_horizontal.setSpacing(2)
        layout_pinhole_horizontal.addWidget(self.lbl_pinhole_horizontal)
        layout_pinhole_horizontal.addStretch(1)
        layout_pinhole_horizontal.addWidget(self.btn_pinhole_horizontal_minus)
        layout_pinhole_horizontal.addWidget(self.lne_pinhole_horizontal)
        layout_pinhole_horizontal.addWidget(self.btn_pinhole_horizontal_plus)

        layout = QGridLayout()
        layout.setSpacing(0)
        layout.addLayout(layout_pinhole_position, 0, 0, 1, 4)
        layout.addLayout(layout_pinhole_vertical, 1, 0, 1, 4)
        layout.addLayout(layout_pinhole_horizontal, 2, 0, 1, 4)
        layout.addLayout(layout_step_widgets, 0, 4, 3, 1)

        self.setLayout(layout)
