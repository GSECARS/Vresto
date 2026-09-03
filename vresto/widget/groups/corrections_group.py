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
    QCheckBox,
    QComboBox,
    QLabel,
    QPushButton,
    QGridLayout,
)
from qtpy.QtCore import Qt, QSize
from qtpy.QtGui import QDoubleValidator

from vresto.model import PathModel


class CorrectionsGroup(QGroupBox):

    _title = " Diamond Correction "
    _max_size = QSize(280, 220)

    def __init__(self, paths: PathModel) -> None:
        super(CorrectionsGroup, self).__init__()

        self._paths = paths

        self.check_focus_sample = QCheckBox("STEP 1: Focus on sample")
        self.check_diamond_thickness = QCheckBox("STEP 2: Insert diamond thickness")
        self.check_focus_diamond_table = QCheckBox("STEP 3: Focus on diamond table")
        self._check_boxes = [
            self.check_focus_sample,
            self.check_diamond_thickness,
            self.check_focus_diamond_table,
        ]

        self.cmb_diamond_thickness = QComboBox()
        self._lbl_mm = QLabel("mm")

        self.btn_real_position = QPushButton("GO TO REAL POSITION")

        self.setTitle(self._title)
        self.setStyleSheet(
            open(
                os.path.join(self._paths.qss_path, "corrections_group.qss"), "r"
            ).read()
        )

        self._configure_check_boxes()
        self._configure_combo_box()
        self._set_object_names()
        self._set_widget_sizes()
        self._set_tool_status_tips()
        self._layout_group()

    def _configure_check_boxes(self) -> None:
        self.check_focus_sample.setTristate(False)
        self.check_diamond_thickness.setTristate(False)
        self.check_focus_diamond_table.setTristate(False)
        self.check_diamond_thickness.setDisabled(True)

    def _configure_combo_box(self) -> None:
        self.cmb_diamond_thickness.setEditable(True)
        self.cmb_diamond_thickness.lineEdit().setReadOnly(True)
        self.cmb_diamond_thickness.lineEdit().setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cmb_diamond_thickness.setValidator(QDoubleValidator(-200000, 200000, 4))

    def _set_object_names(self) -> None:
        """Sets all the object names for the group and the group widgets."""
        self.setObjectName("group-corrections")
        self.cmb_diamond_thickness.setObjectName("combo-corrections")
        self._lbl_mm.setObjectName("lbl-corrections")
        self.btn_real_position.setObjectName("btn-real-position")

        [checkbox.setObjectName("checkbox") for checkbox in self._check_boxes]

    def _set_tool_status_tips(self) -> None:
        """Sets all the tool and status tips for the group."""
        self.check_focus_sample.setToolTip(
            "STEP 1: First find the sample and focus while the microscope is ZOOMED "
            "IN, then check this box"
        )
        self.check_focus_sample.setStatusTip(
            "STEP 1: First find the sample and focus while the microscope is ZOOMED "
            "IN, then check this box"
        )
        self.check_diamond_thickness.setToolTip(
            "STEP 2: Insert your diamond's thickness approximately (e.g. 2)"
        )
        self.check_diamond_thickness.setStatusTip(
            "STEP 2: Insert your diamond's thickness approximately (e.g. 2)"
        )
        self.check_focus_diamond_table.setToolTip(
            "STEP 3: First focus on the diamond table as best as you can, "
            "then check this box"
        )
        self.check_focus_diamond_table.setStatusTip(
            "STEP 3: First focus on the diamond table as best as you can, "
            "then check this box"
        )
        self.cmb_diamond_thickness.setToolTip(
            "Insert the diamond thickness in mm and press ENTER"
        )
        self.cmb_diamond_thickness.setStatusTip(
            "Insert the diamond thickness in mm and press ENTER"
        )
        self.btn_real_position.setToolTip("Moves the stage to the real sample position")

    def _set_widget_sizes(self) -> None:
        self.cmb_diamond_thickness.setMaximumWidth(80)

        self.setMinimumHeight(200)
        self.setMaximumSize(self._max_size)

    def _layout_group(self) -> None:
        layout = QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(self.check_focus_sample, 0, 0, 1, 5)
        layout.addWidget(self.check_diamond_thickness, 1, 0, 1, 5)
        layout.addWidget(
            self.cmb_diamond_thickness,
            2,
            1,
            1,
            2,
            alignment=Qt.AlignmentFlag.AlignRight,
        )
        layout.addWidget(self._lbl_mm, 2, 3, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.check_focus_diamond_table, 3, 0, 1, 5)
        layout.addWidget(self.btn_real_position, 4, 0, 1, 5)

        self.setLayout(layout)
