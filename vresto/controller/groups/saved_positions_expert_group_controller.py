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

from typing import List
from qtpy.QtCore import QObject, QSettings
from qtpy.QtWidgets import QMessageBox

from vresto.model import DoubleValuePV, EpicsModel, SavedPositionsModel
from vresto.widget.groups import SavedPositionsExpertGroup


class SavedPositionsExpertGroupController(QObject):

    def __init__(
        self,
        widget: SavedPositionsExpertGroup,
        settings: QSettings,
        epics_model: EpicsModel,
        sample_vertical: DoubleValuePV,
        sample_horizontal: DoubleValuePV,
        sample_focus: DoubleValuePV,
    ):
        super(SavedPositionsExpertGroupController, self).__init__()

        self._widget = widget
        self._model = SavedPositionsModel(settings=settings)
        self._epics = epics_model

        self._sample_vertical = sample_vertical
        self._sample_horizontal = sample_horizontal
        self._sample_focus = sample_focus

        self._connect_saved_positions_widgets()

    def _connect_saved_positions_widgets(self) -> None:
        self._widget.btn_pt_foil_update.clicked.connect(self._update_pt_foil)
        self._widget.btn_thick_pt_update.clicked.connect(self._update_thick_pt)
        self._widget.btn_lab6_update.clicked.connect(self._update_lab6)
        self._widget.btn_ceo2_update.clicked.connect(self._update_ceo2)
        self._widget.btn_enstatite_au_update.clicked.connect(self._update_enstatite_au)
        self._widget.btn_p_plate_update.clicked.connect(self._update_p_plate)
        self._widget.btn_position_1_update.clicked.connect(self._update_position_1)
        self._widget.btn_position_2_update.clicked.connect(self._update_position_2)

        self._widget.btn_pt_foil.clicked.connect(lambda: self._move_to_positions(self._model.pt_foil))
        self._widget.btn_thick_pt.clicked.connect(lambda: self._move_to_positions(self._model.thick_pt))
        self._widget.btn_lab6.clicked.connect(lambda: self._move_to_positions(self._model.lab6))
        self._widget.btn_ceo2.clicked.connect(lambda: self._move_to_positions(self._model.ceo2))
        self._widget.btn_enstatite_au.clicked.connect(lambda: self._move_to_positions(self._model.enstatite_au))
        self._widget.btn_p_plate.clicked.connect(lambda: self._move_to_positions(self._model.p_plate))
        self._widget.btn_position_1.clicked.connect(lambda: self._move_to_positions(self._model.position_1))
        self._widget.btn_position_2.clicked.connect(lambda: self._move_to_positions(self._model.position_2))

    def _update_pt_foil(self) -> None:
        new_values = self._get_motor_positions()
        if self._get_confirmation(target="pt_foil", current_values=self._model.pt_foil, target_values=new_values):
            self._model.pt_foil = new_values

    def _update_thick_pt(self) -> None:
        new_values = self._get_motor_positions()
        if self._get_confirmation(target="thick_pt", current_values=self._model.thick_pt, target_values=new_values):
            self._model.thick_pt = new_values

    def _update_lab6(self) -> None:
        new_values = self._get_motor_positions()
        if self._get_confirmation(target="lab6", current_values=self._model.lab6, target_values=new_values):
            self._model.lab6 = new_values

    def _update_ceo2(self) -> None:
        new_values = self._get_motor_positions()
        if self._get_confirmation(target="ceo2", current_values=self._model.ceo2, target_values=new_values):
            self._model.ceo2 = new_values

    def _update_enstatite_au(self) -> None:
        new_values = self._get_motor_positions()
        if self._get_confirmation(target="enstatite_au", current_values=self._model.enstatite_au,
                                  target_values=new_values):
            self._model.enstatite_au = new_values

    def _update_p_plate(self) -> None:
        new_values = self._get_motor_positions()
        if self._get_confirmation(target="p_plate", current_values=self._model.p_plate, target_values=new_values):
            self._model.p_plate = new_values

    def _update_position_1(self) -> None:
        new_values = self._get_motor_positions()
        if self._get_confirmation(target="position_1", current_values=self._model.position_1, target_values=new_values):
            self._model.position_1 = new_values

    def _update_position_2(self) -> None:
        new_values = self._get_motor_positions()
        if self._get_confirmation(target="position_2", current_values=self._model.position_2, target_values=new_values):
            self._model.position_2 = new_values

    def _get_motor_positions(self) -> str:
        x = self._sample_horizontal.readback
        y = self._sample_vertical.readback
        z = self._sample_focus.readback
        return f"{x}, {y}, {z}"

    def _move_to_positions(self, target_values: List[float]) -> None:
        _msg_question = QMessageBox.question(
            self._widget,
            "Move confirmation",
            f"Are you sure you want to move to \n{target_values}?"
        )
        if _msg_question == QMessageBox.Yes:
            self._sample_horizontal.move(value=target_values[0])
            self._sample_vertical.move(value=target_values[1])
            self._sample_focus.move(value=target_values[2])

    def _get_confirmation(self, target: str, current_values: List[float], target_values: str) -> bool:
        _msg_question = QMessageBox.question(
            self._widget,
            "Update values confirmation",
            f"Are you sure you want to replace \n{current_values} with \n[{target_values}] for {target}?"
        )
        if _msg_question == QMessageBox.Yes:
            return True
        return False
