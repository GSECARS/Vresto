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
from qtpy.QtWidgets import QGroupBox, QPushButton, QGridLayout

from qtpy.QtCore import QSize

from vresto.model import PathModel


class SavedPositionsExpertGroup(QGroupBox):

    _title = " Saved Positions "
    _max_size = QSize(850, 350)

    def __init__(self, paths: PathModel) -> None:
        super(SavedPositionsExpertGroup, self).__init__()

        self._paths = paths

        self.btn_pt_foil = QPushButton("Pt-foil")
        self.btn_thick_pt = QPushButton("Thick-Pt")
        self.btn_lab6 = QPushButton("LaB6")
        self.btn_ceo2 = QPushButton("CeO2")
        self.btn_enstatite_au = QPushButton("Enstatite-Au")
        self.btn_p_plate = QPushButton("P-plate")
        self.btn_position_1 = QPushButton("Position 1")
        self.btn_position_2 = QPushButton("Position 2")

        self.btn_pt_foil_update = QPushButton("Update")
        self.btn_thick_pt_update = QPushButton("Update")
        self.btn_lab6_update = QPushButton("Update")
        self.btn_ceo2_update = QPushButton("Update")
        self.btn_enstatite_au_update = QPushButton("Update")
        self.btn_p_plate_update = QPushButton("Update")
        self.btn_position_1_update = QPushButton("Update")
        self.btn_position_2_update = QPushButton("Update")

        self._buttons = [
            self.btn_pt_foil,
            self.btn_thick_pt,
            self.btn_lab6,
            self.btn_ceo2,
            self.btn_enstatite_au,
            self.btn_p_plate,
            self.btn_position_1,
            self.btn_position_2,
        ]
        self._update_buttons = [
            self.btn_pt_foil_update,
            self.btn_thick_pt_update,
            self.btn_lab6_update,
            self.btn_ceo2_update,
            self.btn_enstatite_au_update,
            self.btn_p_plate_update,
            self.btn_position_1_update,
            self.btn_position_2_update,
        ]

        self.setTitle(self._title)
        self.setStyleSheet(
            open(os.path.join(self._paths.qss_path, "saved_positions_expert_group.qss"), "r").read()
        )

        self._set_object_names()
        self._set_widget_sizes()
        self._set_tool_status_tips()
        self._layout_group()

    def _set_object_names(self) -> None:
        """Sets all the object names for the group and the group widgets."""
        self.setObjectName("group-saved-positions")
        [button.setObjectName("btn-saved-positions") for button in self._buttons]
        [update_button.setObjectName("btn-update") for update_button in self._update_buttons]

    def _set_tool_status_tips(self) -> None:
        """Sets all the tool and status tips for the group."""
        pass

    def _set_widget_sizes(self) -> None:
        [button.setMinimumSize(110, 40) for button in self._buttons]
        [update_button.setFixedSize(55, 25) for update_button in self._update_buttons]

        self.setMaximumSize(self._max_size)

    def _layout_group(self) -> None:
        """Creates the layout for the sample group."""
        layout = QGridLayout()
        layout.setSpacing(10)

        layout.addWidget(self.btn_pt_foil, 0, 0, 1, 2)
        layout.addWidget(self.btn_pt_foil_update, 0, 2, 1, 1)
        layout.addWidget(self.btn_lab6, 0, 3, 1, 2)
        layout.addWidget(self.btn_lab6_update, 0, 5, 1, 1)
        layout.addWidget(self.btn_enstatite_au, 0, 6, 1, 2)
        layout.addWidget(self.btn_enstatite_au_update, 0, 8, 1, 1)
        layout.addWidget(self.btn_position_1, 0, 9, 1, 2)
        layout.addWidget(self.btn_position_1_update, 0, 11, 1, 1)

        layout.addWidget(self.btn_thick_pt, 1, 0, 1, 2)
        layout.addWidget(self.btn_thick_pt_update, 1, 2, 1, 1)
        layout.addWidget(self.btn_ceo2, 1, 3, 1, 2)
        layout.addWidget(self.btn_ceo2_update, 1, 5, 1, 1)
        layout.addWidget(self.btn_p_plate, 1, 6, 1, 2)
        layout.addWidget(self.btn_p_plate_update, 1, 8, 1, 1)
        layout.addWidget(self.btn_position_2, 1, 9, 1, 2)
        layout.addWidget(self.btn_position_2_update, 1, 11, 1, 1)

        self.setLayout(layout)
