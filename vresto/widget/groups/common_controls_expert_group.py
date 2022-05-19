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
from qtpy.QtWidgets import QFrame, QPushButton, QLabel, QGridLayout
from qtpy.QtCore import QSize, Qt

from vresto.model import PathModel


class CommonControlsExpertGroup(QFrame):

    _max_size = QSize(850, 150)

    def __init__(self, paths: PathModel) -> None:
        super(CommonControlsExpertGroup, self).__init__()

        self._paths = paths

        self.btn_stop_all = QPushButton("STOP ALL")
        self.btn_change_password = QPushButton("CHANGE PASSWORD")
        self.lbl_warning = QLabel("WARNING: This tab is NOT for USERS!")

        self.setStyleSheet(
            open(
                os.path.join(self._paths.qss_path, "common_controls_expert_group.qss"), "r"
            ).read()
        )

        self._set_object_names()
        self._set_widget_sizes()
        self._set_tool_status_tips()
        self._layout_group()

    def _set_object_names(self) -> None:
        """Sets all the object names for the group and the group widgets."""
        self.setObjectName("group-common-controls-expert")
        self.btn_stop_all.setObjectName("btn-stop")
        self.lbl_warning.setObjectName("lbl-warning")

    def _set_tool_status_tips(self) -> None:
        """Sets all the tool and status tips for the group."""
        self.btn_stop_all.setToolTip("STOP ALL")
        self.btn_stop_all.setStatusTip("Stops all movements.")

    def _set_widget_sizes(self) -> None:
        self.btn_stop_all.setMinimumSize(70, 50)
        self.btn_change_password.setMinimumSize(70, 25)

        self.setMaximumSize(self._max_size)

    def _layout_group(self) -> None:
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.btn_stop_all, 0, 0, 1, 4)
        layout.addWidget(self.lbl_warning, 0, 4, 1, 10, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.btn_change_password, 1, 0, 1, 4)

        self.setLayout(layout)
