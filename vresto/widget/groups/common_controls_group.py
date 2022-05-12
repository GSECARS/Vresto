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
    QFrame,
    QPushButton,
    QCheckBox,
    QLabel,
    QComboBox,
    QGridLayout,
)
from qtpy.QtCore import Qt, QSize

from vresto.model import PathModel


class CommonControlsGroup(QFrame):

    _max_size = QSize(280, 230)

    def __init__(self, paths: PathModel) -> None:
        super(CommonControlsGroup, self).__init__()

        self._paths = paths

        self.btn_stop_all = QPushButton("STOP")
        self.btn_reset = QPushButton("RESET")
        self.btn_save = QPushButton("QUICK SAVE")
        self.btn_save_as = QPushButton("SAVE AS")
        self.btn_load_correction = QPushButton("LOAD POSITION")

        self.check_mic_focus_correction = QCheckBox("Use focus-correction for microscope.")

        self.lbl_refraction_index = QLabel("Refraction index options")
        self.lbl_path = QLabel("Unknown")

        self.cmb_refraction_index = QComboBox()

        self.setStyleSheet(
            open(
                os.path.join(self._paths.qss_path, "common_controls_group.qss"), "r"
            ).read()
        )

        self._configure_combo_box()
        self._configure_check_box()
        self._set_object_names()
        self._set_widget_sizes()
        self._set_tool_status_tips()
        self._layout_group()

    def _configure_combo_box(self) -> None:
        self.cmb_refraction_index.setEditable(True)
        self.cmb_refraction_index.lineEdit().setReadOnly(True)
        self.cmb_refraction_index.lineEdit().setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cmb_refraction_index.addItem("Diamond")
        self.cmb_refraction_index.addItem("Fused Silica")
        self.cmb_refraction_index.addItem("Moissanite")

    def _configure_check_box(self) -> None:
        self.check_mic_focus_correction.setChecked(True)

    def _set_object_names(self) -> None:
        """Sets all the object names for the group and the group widgets."""
        self.setObjectName("group-common-controls")
        self.btn_stop_all.setObjectName("btn-stop")
        self.btn_reset.setObjectName("btn-reset")
        self.btn_save.setObjectName("btn-save")
        self.btn_save_as.setObjectName("btn-save")
        self.btn_load_correction.setObjectName("btn-save")
        self.cmb_refraction_index.setObjectName("cmb-refraction")
        self.check_mic_focus_correction.setObjectName("checkbox-small")
        self.lbl_refraction_index.setObjectName("lbl-refraction")
        self.lbl_path.setObjectName("lbl-path")

    def _set_tool_status_tips(self) -> None:
        """Sets all the tool and status tips for the group."""
        self.btn_stop_all.setToolTip("STOP ALL")
        self.btn_stop_all.setStatusTip("Stops all movements.")
        self.btn_reset.setToolTip("Resets all and start from the begging")
        self.btn_save.setToolTip(
            "Saves correction values to the Corrections directory\nof the current user."
        )
        self.btn_save_as.setToolTip(
            "Opens a dialog that provides a way to save a custom correction file."
        )
        self.check_mic_focus_correction.setStatusTip(
            "(Optional) Corrects the focus of the microscope."
        )
        self.cmb_refraction_index.setStatusTip(
            "Select your material to apply the correct refraction index."
        )

    def _set_widget_sizes(self) -> None:
        self.btn_stop_all.setMinimumSize(70, 50)
        self.btn_reset.setMinimumSize(70, 50)
        self.check_mic_focus_correction.setMinimumWidth(280)

        self.setMaximumSize(self._max_size)

    def _layout_group(self) -> None:
        layout = QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(self.btn_stop_all, 0, 0, 2, 1)
        layout.addWidget(self.btn_reset, 0, 1, 2, 1)
        layout.addWidget(
            self.check_mic_focus_correction, 2, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout.addWidget(
            self.lbl_refraction_index,
            3,
            0,
            1,
            1,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )
        layout.addWidget(self.cmb_refraction_index, 3, 1, 1, 1)
        layout.addWidget(self.btn_load_correction, 4, 0, 1, 2)
        layout.addWidget(self.btn_save, 5, 0, 1, 1)
        layout.addWidget(self.btn_save_as, 5, 1, 1, 1)
        layout.addWidget(self.lbl_path, 6, 0, 1, 2)

        self.setLayout(layout)
