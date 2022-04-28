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
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
)
from qtpy.QtCore import Qt, QSize
from qtpy.QtGui import QDoubleValidator

from vresto.widget.custom import QLine
from vresto.model import PathModel


class SampleExpertGroup(QGroupBox):

    _title = " Sample "
    _max_size = QSize(550, 200)

    def __init__(self, paths: PathModel) -> None:
        super(SampleExpertGroup, self).__init__()

        self._paths = paths

        self.lbl_step = QLabel("Step (mm)")
        self.lbl_omega_step = QLabel("Step (\N{DEGREE SIGN})")
        self.lbl_vertical = QLabel("Vertical")
        self.lbl_horizontal = QLabel("Horizontal")
        self.lbl_focus = QLabel("Focus")
        self.lbl_omega = QLabel("Omega")

        self._labels = [
            self.lbl_vertical,
            self.lbl_horizontal,
            self.lbl_focus,
            self.lbl_omega,
        ]

        self.line_vertical = QLine()

        self.lne_vertical = QLineEdit()
        self.lne_horizontal = QLineEdit()
        self.lne_focus = QLineEdit()
        self.lne_omega = QLineEdit()
        self._lne_boxes = [
            self.lne_vertical,
            self.lne_horizontal,
            self.lne_focus,
            self.lne_omega,
        ]

        self.btn_prepare_crosshair = QPushButton("PREPARE FOR CROSSHAIR")
        self.btn_prepare_user = QPushButton("PREPARE FOR USER")
        self.btn_step_1 = QPushButton()
        self.btn_step_2 = QPushButton()
        self.btn_step_3 = QPushButton()
        self.btn_omega_step_1 = QPushButton()
        self.btn_omega_step_2 = QPushButton()
        self.btn_omega_step_3 = QPushButton()
        self.btn_plus_vertical = QPushButton("+")
        self.btn_plus_horizontal = QPushButton("+")
        self.btn_plus_focus = QPushButton("+")
        self.btn_plus_omega = QPushButton("+")
        self.btn_minus_vertical = QPushButton("-")
        self.btn_minus_horizontal = QPushButton("-")
        self.btn_minus_focus = QPushButton("-")
        self.btn_minus_omega = QPushButton("-")

        self._buttons = [
            self.btn_step_1,
            self.btn_step_2,
            self.btn_step_3,
            self.btn_omega_step_1,
            self.btn_omega_step_2,
            self.btn_omega_step_3,
        ]
        self._plus_buttons = [
            self.btn_plus_vertical,
            self.btn_plus_horizontal,
            self.btn_plus_focus,
            self.btn_plus_omega,
        ]

        self._minus_buttons = [
            self.btn_minus_vertical,
            self.btn_minus_horizontal,
            self.btn_minus_focus,
            self.btn_minus_omega,
        ]

        self.setTitle(self._title)
        self.setStyleSheet(
            open(os.path.join(self._paths.qss_path, "sample_group.qss"), "r").read()
        )

        self._configure_buttons()
        self._configure_lne_boxes()
        self._set_object_names()
        self._set_widget_sizes()
        self._set_tool_status_tips()
        self._layout_group()

    def _configure_buttons(self) -> None:
        for button in self._buttons:
            button.setCheckable(True)

    def _configure_lne_boxes(self) -> None:
        for lne_box in self._lne_boxes:
            lne_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lne_box.setValidator(QDoubleValidator(-200000, 200000, 4))

    def _set_object_names(self) -> None:
        """Sets all the object names for the group and the group widgets."""
        self.setObjectName("group-sample")
        self.lbl_step.setObjectName("lbl-step")
        self.lbl_omega_step.setObjectName("lbl-step")
        self.line_vertical.setObjectName("line-vertical")
        [label.setObjectName("lbl-sample") for label in self._labels]
        [lne.setObjectName("lne-sample") for lne in self._lne_boxes]
        [button.setObjectName("btn-sample") for button in self._buttons]
        [button.setObjectName("btn-plus") for button in self._plus_buttons]
        [button.setObjectName("btn-minus") for button in self._minus_buttons]
        self.btn_prepare_crosshair.setObjectName("btn-main")
        self.btn_prepare_user.setObjectName("btn-main")

    def _set_tool_status_tips(self) -> None:
        """Sets all the tool and status tips for the group."""
        self.lne_vertical.setStatusTip("Read/input the position of the vertical motor.")
        self.lne_horizontal.setStatusTip(
            "Read/input the position of the horizontal motor."
        )
        self.lne_focus.setStatusTip("Read/input the position of the focus motor.")
        self.lne_omega.setStatusTip("Read/input the position of the omega motor.")

        self.btn_plus_vertical.setToolTip("Positive values")
        self.btn_plus_horizontal.setToolTip("Positive values")
        self.btn_plus_focus.setToolTip("Positive values")
        self.btn_plus_omega.setToolTip("Positive values")

        self.btn_minus_vertical.setToolTip("Negative values")
        self.btn_minus_horizontal.setToolTip("Negative values")
        self.btn_minus_focus.setToolTip("Negative values")
        self.btn_minus_omega.setToolTip("Negative values")

    def _set_widget_sizes(self) -> None:
        for button in self._buttons:
            button.setFixedSize(40, 20)

    def _layout_group(self) -> None:
        """Creates the layout for the sample group."""
        layout_left_step_widgets = QVBoxLayout()
        layout_left_step_widgets.setContentsMargins(0, 0, 0, 0)
        layout_left_step_widgets.setSpacing(2)
        layout_left_step_widgets.addWidget(
            self.lbl_step, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout_left_step_widgets.addWidget(self.btn_step_1)
        layout_left_step_widgets.addWidget(self.btn_step_2)
        layout_left_step_widgets.addWidget(self.btn_step_3)

        layout_right_step_widgets = QVBoxLayout()
        layout_right_step_widgets.setSpacing(2)
        layout_right_step_widgets.setContentsMargins(0, 0, 0, 0)
        layout_right_step_widgets.addWidget(
            self.lbl_omega_step, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout_right_step_widgets.addWidget(self.btn_omega_step_1)
        layout_right_step_widgets.addWidget(self.btn_omega_step_2)
        layout_right_step_widgets.addWidget(self.btn_omega_step_3)

        layout_vertical = QVBoxLayout()
        layout_vertical.setSpacing(2)
        layout_vertical.setContentsMargins(0, 0, 0, 0)
        layout_vertical.addWidget(
            self.btn_plus_vertical, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout_vertical.addWidget(
            self.lne_vertical, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout_vertical.addWidget(
            self.btn_minus_vertical, alignment=Qt.AlignmentFlag.AlignCenter
        )

        layout_horizontal = QHBoxLayout()
        layout_horizontal.setSpacing(2)
        layout_horizontal.setContentsMargins(0, 0, 0, 0)
        layout_horizontal.addWidget(self.btn_minus_horizontal)
        layout_horizontal.addWidget(self.lne_horizontal)
        layout_horizontal.addWidget(self.btn_plus_horizontal)

        layout_omega = QVBoxLayout()
        layout_omega.setSpacing(2)
        layout_omega.setContentsMargins(0, 0, 0, 0)
        layout_omega.addWidget(
            self.btn_plus_omega, alignment=Qt.AlignmentFlag.AlignBottom
        )
        layout_omega.addWidget(self.lne_omega)
        layout_omega.addWidget(
            self.btn_minus_omega, alignment=Qt.AlignmentFlag.AlignTop
        )

        layout_focus = QVBoxLayout()
        layout_focus.setSpacing(2)
        layout_focus.setContentsMargins(0, 0, 0, 0)
        layout_focus.addWidget(
            self.btn_plus_focus, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout_focus.addWidget(self.lne_focus, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_focus.addWidget(
            self.btn_minus_focus, alignment=Qt.AlignmentFlag.AlignCenter
        )

        layout = QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(self.btn_prepare_crosshair, 0, 0, 1, 5)
        layout.addWidget(self.btn_prepare_user, 0, 5, 1, 7)
        layout.addLayout(
            layout_left_step_widgets, 2, 0, 3, 1, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout.addWidget(
            self.lbl_vertical, 1, 1, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout.addLayout(
            layout_vertical, 2, 1, 3, 2, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout.addWidget(
            self.lbl_horizontal, 1, 3, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout.addLayout(
            layout_horizontal, 2, 3, 3, 2, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout.addWidget(
            self.lbl_focus, 1, 5, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout.addLayout(
            layout_focus, 2, 5, 3, 2, alignment=Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(
            self.line_vertical, 1, 7, 4, 2, alignment=Qt.AlignmentFlag.AlignHCenter
        )
        layout.addWidget(
            self.lbl_omega, 1, 9, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout.addLayout(
            layout_omega, 2, 9, 3, 2, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout.addLayout(
            layout_right_step_widgets,
            2,
            11,
            3,
            1,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )

        self.setLayout(layout)