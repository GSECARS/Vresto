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
from qtpy.QtWidgets import QGroupBox, QGridLayout, QPushButton
from qtpy.QtCore import QSize
from vresto.model import PathModel


class ZeroExpertGroup(QGroupBox):

    _title = " Zero "
    _max_size = QSize(550, 200)

    def __init__(self, paths: PathModel) -> None:
        super(ZeroExpertGroup, self).__init__()

        self._paths = paths

        self.btn_pinhole_z = QPushButton("PINHOLE-Z")
        self.btn_pinhole_vertical = QPushButton("PINHOLE-VERT")
        self.btn_pinhole_horizontal = QPushButton("PINHOLE-HORIZ")
        self.btn_objectives = QPushButton("OBJECTIVES")
        self.btn_stage = QPushButton("STAGE")
        self.btn_stage_x = QPushButton("STAGE-X")
        self.btn_us_c_mirror = QPushButton("C-MIRROR US")
        self.btn_ds_c_mirror = QPushButton("C-MIRROR DS")
        self.btn_us_focus = QPushButton("FOCUS US")
        self.btn_ds_focus = QPushButton("FOCUS DS")
        self.btn_microscope = QPushButton("MICROSCOPE")
        self.btn_microscope_z = QPushButton("MICROSCOPE-Z")

        self._buttons = [
            self.btn_pinhole_z,
            self.btn_pinhole_vertical,
            self.btn_pinhole_horizontal,
            self.btn_objectives,
            self.btn_stage,
            self.btn_stage_x,
            self.btn_us_c_mirror,
            self.btn_ds_c_mirror,
            self.btn_us_focus,
            self.btn_ds_focus,
            self.btn_microscope,
            self.btn_microscope_z,
        ]

        self.setTitle(self._title)
        self.setStyleSheet(
            open(os.path.join(self._paths.qss_path, "zero_expert_group.qss"), "r").read()
        )

        self._set_object_names()
        self._set_widget_sizes()
        self._set_tool_status_tips()
        self._layout_group()

    def _set_object_names(self) -> None:
        """Sets all the object names for the group and the group widgets."""
        self.setObjectName("group-zero")
        [button.setObjectName("btn-zero") for button in self._buttons]

    def _set_tool_status_tips(self) -> None:
        """Sets all the tool and status tips for the group."""
        pass

    def _set_widget_sizes(self) -> None:
        pass

    def _layout_group(self) -> None:
        """Creates the layout for the zero expert group."""
        layout = QGridLayout()
        layout.setSpacing(10)

        layout.addWidget(self.btn_pinhole_z, 0, 0, 1, 1)
        layout.addWidget(self.btn_pinhole_vertical, 0, 1, 1, 1)
        layout.addWidget(self.btn_pinhole_horizontal, 0, 2, 1, 1)

        layout.addWidget(self.btn_stage, 1, 0, 1, 1)
        layout.addWidget(self.btn_microscope, 1, 1, 1, 1)
        layout.addWidget(self.btn_microscope_z, 1, 2, 1, 1)

        layout.addWidget(self.btn_stage_x, 2, 0, 1, 1)
        layout.addWidget(self.btn_ds_focus, 2, 1, 1, 1)
        layout.addWidget(self.btn_ds_c_mirror, 2, 2, 1, 1)

        layout.addWidget(self.btn_objectives, 3, 0, 1, 1)
        layout.addWidget(self.btn_us_focus, 3, 1, 1, 1)
        layout.addWidget(self.btn_us_c_mirror, 3, 2, 1, 1)

        self.setLayout(layout)
