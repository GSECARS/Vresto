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

from typing import Optional
from qtpy.QtWidgets import QCheckBox, QLineEdit
from qtpy.QtCore import QObject, Signal

from vresto.model import DoubleValuePV, EpicsModel
from vresto.widget.groups import DiamondImagesGroup


class DiamondImagesGroupController(QObject):
    _virtual_position_changed: Signal = Signal(str)
    _diamond_table_changed: Signal = Signal(str)

    def __init__(
        self,
        widget: DiamondImagesGroup,
        epics_model: EpicsModel,
        sample_focus_stage: DoubleValuePV,
        check_focus_sample: QCheckBox,
        check_focus_diamond: QCheckBox,
        check_focus_thickness: QCheckBox,
    ) -> None:
        super(DiamondImagesGroupController, self).__init__()

        self._widget = widget
        self._epics = epics_model

        self._sample_focus_stage = sample_focus_stage

        self._check_focus_sample = check_focus_sample
        self._check_focus_diamond = check_focus_diamond
        self._check_focus_thickness = check_focus_thickness

        self._focus_sample_checked: bool = False
        self._focus_diamond_checked: bool = False

        self._connect_diamond_image_widgets()

    def _connect_diamond_image_widgets(self) -> None:
        self._widget.lne_virtual_position.returnPressed.connect(
            lambda: self._move_focus(self._widget.lne_virtual_position)
        )
        self._widget.lne_diamond_table.returnPressed.connect(
            lambda: self._move_focus(self._widget.lne_diamond_table)
        )
        self._widget.btn_diamond_go.clicked.connect(
            lambda: self._move_focus(self._widget.lne_diamond_table, 1)
        )
        self._widget.btn_virtual_go.clicked.connect(
            lambda: self._move_focus(self._widget.lne_virtual_position, 0)
        )
        self._widget.btn_real_go.clicked.connect(
            lambda: self._move_focus(self._widget.lne_real_position, 2)
        )

        # Additional check state methods
        self._check_focus_sample.stateChanged.connect(self._update_focus_sample_helper)
        self._check_focus_diamond.stateChanged.connect(
            self._update_focus_diamond_helper
        )

        self._virtual_position_changed.connect(self._update_virtual_position)
        self._diamond_table_changed.connect(self._update_diamond_table)

    def _move_focus(
        self, lne_box: QLineEdit, image_index: Optional[int] = None
    ) -> None:
        lne_box.clearFocus()

        try:
            value = float(lne_box.text())
        except ValueError:
            return None

        if image_index is not None:
            self._widget.stacked_images.setCurrentIndex(image_index)

        self._sample_focus_stage.move(value=value)

    def _update_focus_sample_helper(self, state: int) -> None:
        if state:
            value = True
        else:
            value = False

        self._focus_sample_checked = value

    def _update_focus_diamond_helper(self, state: int) -> None:
        if state:
            value = True
        else:
            value = False

        self._focus_diamond_checked = value

    def _update_virtual_position(self, text: str) -> None:
        if not self._widget.lne_virtual_position.hasFocus():
            if self._widget.lne_virtual_position.text() != text:
                self._widget.lne_virtual_position.setText(text)

    def _update_diamond_table(self, text: str) -> None:
        if not self._widget.lne_diamond_table.hasFocus():
            if self._widget.lne_diamond_table.text() != text:
                self._widget.lne_diamond_table.setText(text)

    def _update_diamond_images(self, position: float) -> None:
        if -120 < position <= -60:
            current_index = 0
        else:
            if not self._check_focus_thickness.isChecked():
                current_index = 1
            else:
                current_index = 2

        self._widget.stacked_images.setCurrentIndex(current_index)

    def update_diamond_image_widgets(self) -> None:
        if self._epics.connected:

            sample_focus_rbv_string = str(
                "{0:.4f}".format(self._sample_focus_stage.readback)
            )

            # Virtual position
            if not self._focus_sample_checked:
                self._virtual_position_changed.emit(sample_focus_rbv_string)

            # Diamond table position
            if self._focus_sample_checked and not self._focus_diamond_checked:
                self._diamond_table_changed.emit(sample_focus_rbv_string)

