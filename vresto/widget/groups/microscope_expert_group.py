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
from qtpy.QtWidgets import QGroupBox, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QSlider
from qtpy.QtCore import QSize, Qt

from vresto.model import PathModel


class MicroscopeExpertGroup(QGroupBox):

    _title = " Microscope "
    _max_size = QSize(650, 140)

    def __init__(self, paths: PathModel) -> None:
        super(MicroscopeExpertGroup, self).__init__()

        self._paths = paths

        self.btn_microscope_out = QPushButton("OUT")
        self.btn_microscope_in = QPushButton("IN")
        self.btn_microscope_vertical_plus = QPushButton("+")
        self.btn_microscope_vertical_minus = QPushButton("-")
        self.btn_microscope_horizontal_plus = QPushButton("+")
        self.btn_microscope_horizontal_minus = QPushButton("-")
        self.btn_microscope_focus_plus = QPushButton("+")
        self.btn_microscope_focus_minus = QPushButton("-")
        self.btn_step_1 = QPushButton()
        self.btn_step_2 = QPushButton()
        self.btn_step_3 = QPushButton()

        self.lbl_step = QLabel("Step (mm)")
        self.lbl_microscope_vertical = QLabel("Vertical")
        self.lbl_microscope_horizontal = QLabel("Horizontal")
        self.lbl_microscope_focus = QLabel("Focus")
        self.lbl_i = QLabel("I")
        self.lbl_g = QLabel("G")
        self.lbl_microscope_position = QLabel("Unknown")

        self.lne_microscope_vertical = QLineEdit()
        self.lne_microscope_horizontal = QLineEdit()
        self.lne_microscope_focus = QLineEdit()

        self.slider_light = QSlider(Qt.Vertical)
        self.slider_gain = QSlider(Qt.Vertical)

        self._buttons = [
            self.btn_microscope_out,
            self.btn_microscope_in,
        ]

        self._plus_buttons = [
            self.btn_microscope_vertical_plus,
            self.btn_microscope_horizontal_plus,
            self.btn_microscope_focus_plus,
        ]

        self._minus_buttons = [
            self.btn_microscope_vertical_minus,
            self.btn_microscope_horizontal_minus,
            self.btn_microscope_focus_minus,
        ]

        self._step_buttons = [
            self.btn_step_1,
            self.btn_step_2,
            self.btn_step_3,
        ]

        self._lne_boxes = [
            self.lne_microscope_vertical,
            self.lne_microscope_horizontal,
            self.lne_microscope_focus,
        ]

        self._labels = [
            self.lbl_microscope_vertical,
            self.lbl_microscope_horizontal,
            self.lbl_microscope_focus,
            self.lbl_i,
            self.lbl_g,
        ]

        self.setTitle(self._title)
        self.setStyleSheet(open(os.path.join(self._paths.qss_path, "microscope_expert_group.qss"), "r").read())

        self._set_object_names()
        self._set_widget_sizes()
        self._set_tool_status_tips()
        self._layout_group()

    def _set_object_names(self) -> None:
        """Sets all the object names for the microscope expert group and the widgets."""
        self.setObjectName("group-microscope")
        [button.setObjectName("btn-microscope") for button in self._buttons]
        [plus_button.setObjectName("btn-plus") for plus_button in self._plus_buttons]
        [minus_button.setObjectName("btn-minus") for minus_button in self._minus_buttons]
        [step_button.setObjectName("btn-step") for step_button in self._step_buttons]
        [lne.setObjectName("lne-microscope") for lne in self._lne_boxes]
        [label.setObjectName("lbl-microscope") for label in self._labels]
        self.lbl_step.setObjectName("lbl-step")
        self.lbl_microscope_position.setObjectName("lbl-microscope-position")
        self.slider_light.setObjectName("slider")
        self.slider_gain.setObjectName("slider")

    def _set_tool_status_tips(self) -> None:
        """Sets all the tool and status tips for the group."""
        self.lbl_microscope_position.setStatusTip(
            "The microscope is currently located at the given value"
        )
        self.slider_light.setStatusTip("Controls the light intensity")
        self.slider_gain.setStatusTip("Controls the light gain")

    def _set_widget_sizes(self) -> None:
        self.slider_light.setMaximumHeight(120)
        self.slider_gain.setMaximumHeight(120)

        [step_button.setFixedSize(40, 20) for step_button in self._step_buttons]
        [lne.setFixedSize(60, 20) for lne in self._lne_boxes]

        self.setMaximumSize(self._max_size)

    def _layout_group(self) -> None:
        layout = QGridLayout()
        layout.setSpacing(10)

        layout_quick_buttons = QVBoxLayout()
        layout_quick_buttons.addWidget(self.btn_microscope_out)
        layout_quick_buttons.addWidget(self.btn_microscope_in)
        layout_quick_buttons.addWidget(self.lbl_microscope_position)

        layout_vertical = QVBoxLayout()
        layout_vertical.setSpacing(2)
        layout_vertical.setContentsMargins(0, 0, 0, 0)
        layout_vertical.addWidget(self.btn_microscope_vertical_plus, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_vertical.addWidget(self.lne_microscope_vertical, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_vertical.addWidget(self.btn_microscope_vertical_minus, alignment=Qt.AlignmentFlag.AlignCenter)

        layout_horizontal = QHBoxLayout()
        layout_horizontal.setSpacing(2)
        layout_horizontal.setContentsMargins(0, 0, 0, 0)
        layout_horizontal.addWidget(self.btn_microscope_horizontal_minus)
        layout_horizontal.addWidget(self.lne_microscope_horizontal)
        layout_horizontal.addWidget(self.btn_microscope_horizontal_plus)

        layout_focus = QVBoxLayout()
        layout_focus.setSpacing(2)
        layout_focus.setContentsMargins(0, 0, 0, 0)
        layout_focus.addWidget(self.btn_microscope_focus_plus, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_focus.addWidget(self.lne_microscope_focus, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_focus.addWidget(self.btn_microscope_focus_minus, alignment=Qt.AlignmentFlag.AlignCenter)

        layout_step_widgets = QVBoxLayout()
        layout_step_widgets.setContentsMargins(0, 0, 0, 0)
        layout_step_widgets.setSpacing(2)
        layout_step_widgets.addWidget(self.lbl_step, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_step_widgets.addWidget(self.btn_step_1, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout_step_widgets.addWidget(self.btn_step_2, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout_step_widgets.addWidget(self.btn_step_3, alignment=Qt.AlignmentFlag.AlignHCenter)

        layout.addLayout(layout_quick_buttons, 0, 0, 5, 2)
        layout.addWidget(self.slider_light, 0, 2, 4, 1)
        layout.addWidget(self.lbl_i, 4, 2, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.slider_gain, 0, 3, 4, 1)
        layout.addWidget(self.lbl_g, 4, 3, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lbl_microscope_vertical, 0, 4, 1, 4, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(layout_vertical, 1, 4, 4, 4)
        layout.addWidget(self.lbl_microscope_horizontal, 0, 8, 1, 4, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(layout_horizontal, 1, 8, 4, 4)
        layout.addWidget(self.lbl_microscope_focus, 0, 12, 1, 4, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(layout_focus, 1, 12, 4, 4)
        layout.addLayout(layout_step_widgets, 0, 16, 5, 2)

        self.setLayout(layout)
