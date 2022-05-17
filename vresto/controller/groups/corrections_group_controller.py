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

from epics import caget
from typing import Tuple, Union
from qtpy.QtWidgets import QComboBox, QLineEdit, QPushButton, QCheckBox, QStackedWidget
from qtpy.QtCore import Qt

from vresto.model import DoubleValuePV, CorrectionsModel, EpicsModel
from vresto.widget.groups import CorrectionsGroup
from vresto.widget.custom import MsgBox


class CorrectionsGroupController:

    def __init__(
        self,
        widget: CorrectionsGroup,
        corrections_model: CorrectionsModel,
        epics_model: EpicsModel,
        check_c_mirrors: QCheckBox,
        btn_reset: QPushButton,
        cmb_refraction_index: QComboBox,
        lne_virtual_position: QLineEdit,
        lne_diamond_table: QLineEdit,
        lne_real_position: QLineEdit,
        sample_focus_stage: DoubleValuePV,
        us_mirror_focus: DoubleValuePV,
        ds_mirror_focus: DoubleValuePV,
        microscope_zoom: DoubleValuePV,
        stacked_img_widget: QStackedWidget,
    ) -> None:
        self._widget = widget
        self._corrections = corrections_model
        self._epics = epics_model
        self._cmb_refraction_index = cmb_refraction_index
        self._btn_reset = btn_reset
        self._check_c_mirrors = check_c_mirrors

        self._lne_virtual_position = lne_virtual_position
        self._lne_diamond_table = lne_diamond_table
        self._lne_real_position = lne_real_position
        self._sample_focus_stage = sample_focus_stage
        self._us_mirror_focus = us_mirror_focus
        self._ds_mirror_focus = ds_mirror_focus
        self._microscope_zoom = microscope_zoom

        self._stacked_images = stacked_img_widget

        self._connect_corrections_widgets()

    def _connect_corrections_widgets(self) -> None:
        self._widget.check_focus_sample.stateChanged.connect(
            self._check_focus_sample_changed
        )
        self._widget.cmb_diamond_thickness.currentIndexChanged.connect(
            self._cmb_diamond_thickness_changed
        )
        self._widget.cmb_diamond_thickness.lineEdit().returnPressed.connect(
            self._cmb_diamond_thickness_pressed
        )
        self._widget.check_focus_diamond_table.stateChanged.connect(
            self._check_focus_diamond_changed
        )
        self._widget.btn_real_position.clicked.connect(self._btn_real_position_clicked)
        self._widget.check_diamond_thickness.clicked.connect(
            self._check_diamond_thickness_changed
        )

        self._btn_reset.clicked.connect(self._btn_reset_clicked)

        self._cmb_refraction_index.currentTextChanged.connect(
            self._cmb_refraction_index_changed
        )

    def _check_focus_sample_changed(self, state: int) -> None:
        if state:
            if self._microscope_zoom.readback != 0.0:
                self._widget.check_focus_sample.setCheckState(Qt.CheckState.Unchecked)
                MsgBox(
                    msg=f"Diamond correction must be performed with Microscope 'Zoom IN'!\n"
                    f"Make sure that this is the case and if need repeat the correction."
                )
                return None

        self._widget.cmb_diamond_thickness.lineEdit().setReadOnly(not state)

    def _cmb_diamond_thickness_changed(self) -> None:
        self._cmb_value_changed()

    def _cmb_diamond_thickness_pressed(self) -> None:
        self._cmb_value_changed()

    def _cmb_value_changed(self) -> None:
        try:
            if float(self._widget.cmb_diamond_thickness.currentText()) <= 0:
                self._widget.cmb_diamond_thickness.setCurrentText("")
                return None
        except ValueError:
            return None

        if self._widget.cmb_diamond_thickness.currentText().strip() == "":
            return None

        self._move_to_diamond_position(
            cmb_diamond_thickness=self._widget.cmb_diamond_thickness,
            lne_virtual_position=self._lne_virtual_position,
        )
        self._widget.check_diamond_thickness.setChecked(True)
        self._widget.cmb_diamond_thickness.setEnabled(False)
        self._widget.check_diamond_thickness.setEnabled(True)
        self._stacked_images.setCurrentIndex(2)

    def _check_diamond_thickness_changed(self, state: int) -> None:
        if not state:
            self._widget.cmb_diamond_thickness.setEnabled(True)
            self._widget.cmb_diamond_thickness.setCurrentText("")
            self._widget.check_diamond_thickness.setDisabled(True)
            self._stacked_images.setCurrentIndex(1)

    def _check_focus_diamond_changed(self, state: int) -> None:
        check_one = self._widget.check_focus_sample.isChecked()
        check_two = self._widget.check_diamond_thickness.isChecked()

        if not (check_one and check_two):
            self._widget.check_focus_diamond_table.setCheckState(
                Qt.CheckState.Unchecked
            )
            return None

        if state:

            try:
                virtual_position = float(self._lne_virtual_position.text())
                diamond_position = float(self._lne_diamond_table.text())
            except ValueError:
                return None

            diamond_thickness = self._corrections.get_diamond_thickness(
                virtual_position=virtual_position,
                diamond_position=diamond_position,
            )

            index = self._widget.cmb_diamond_thickness.findText(
                str(diamond_thickness).rstrip("0")
            )
            if index != -1:
                self._widget.cmb_diamond_thickness.setCurrentIndex(index)
            else:
                self._widget.cmb_diamond_thickness.addItem(str(diamond_thickness))
                self._widget.cmb_diamond_thickness.setCurrentIndex(
                    self._widget.cmb_diamond_thickness.count() - 1
                )

    def _btn_real_position_clicked(self) -> None:
        check_one = self._widget.check_focus_sample.isChecked()
        check_two = self._widget.check_diamond_thickness.isChecked()
        check_three = self._widget.check_focus_diamond_table.isChecked()

        if check_one and check_two and check_three:
            diamond_thickness = float(self._widget.cmb_diamond_thickness.currentText())
            diamond_position = float(self._lne_diamond_table.text())

            real_position = self._corrections.get_real_position(
                diamond_thickness=diamond_thickness,
                diamond_position=diamond_position,
            )

            self._sample_focus_stage.move(real_position)
            self._lne_real_position.setText("{0:.4f}".format(real_position))

            if self._check_c_mirrors.isChecked():
                self._correct_mirrors_position(
                    self._lne_virtual_position, self._lne_real_position
                )

            self._stacked_images.setCurrentIndex(3)

    def _btn_reset_clicked(self) -> None:
        self._widget.check_focus_diamond_table.setChecked(False)
        self._widget.cmb_diamond_thickness.setEnabled(True)
        self._widget.cmb_diamond_thickness.lineEdit().clear()
        self._widget.cmb_diamond_thickness.lineEdit().setReadOnly(True)
        self._widget.check_diamond_thickness.setDisabled(True)
        self._widget.check_diamond_thickness.setChecked(False)
        self._widget.check_focus_sample.setChecked(False)
        self._check_c_mirrors.setChecked(True)

        self._stacked_images.setCurrentIndex(1)

        self._lne_diamond_table.clear()
        self._lne_real_position.clear()

    def _cmb_refraction_index_changed(self) -> None:
        self._corrections.refraction_index = self._cmb_refraction_index.currentText()

    def _move_to_diamond_position(
        self, cmb_diamond_thickness: QComboBox, lne_virtual_position: QLineEdit
    ) -> None:
        try:
            virtual_position = float(lne_virtual_position.text())
            diamond_thickness = float(cmb_diamond_thickness.currentText())
        except ValueError:
            return None

        diamond_position = self._corrections.get_diamond_position(
            virtual_position=virtual_position,
            diamond_thickness=diamond_thickness
        )

        high_limit = caget(self._sample_focus_stage.pv + ".HLM")
        low_limit = caget(self._sample_focus_stage.pv + ".LLM")

        if diamond_position < low_limit or diamond_position > high_limit:
            return None

        self._sample_focus_stage.move(value=diamond_position)

    def _correct_mirrors_position(
        self, lne_virtual_position: QLineEdit, lne_real_position: QLineEdit
    ) -> None:
        try:
            virtual_position = float(lne_virtual_position.text())
            real_position = float(lne_real_position.text())
        except ValueError:
            return None
        else:
            corrected_position = (virtual_position - real_position) * -1

            self._us_mirror_focus.move(value=corrected_position)
            self._ds_mirror_focus.move(value=corrected_position)
