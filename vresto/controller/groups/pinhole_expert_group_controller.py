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
from qtpy.QtCore import QObject, Signal
from qtpy.QtWidgets import QLineEdit

from vresto.controller.groups import PinholeGroupController
from vresto.model import EpicsModel, DoubleValuePV, EventFilterModel
from vresto.widget.groups import PinholeExpertGroup


class PinholeExpertGroupController(QObject):
    _pinhole_vertical_changed: Signal = Signal(str)
    _pinhole_horizontal_changed: Signal = Signal(str)

    _step: float
    _step_1: float = 5.0
    _step_2: float = 1.0
    _step_3: float = 0.5

    def __init__(
        self,
        widget: PinholeExpertGroup,
        controller: PinholeGroupController,
        epics_model: EpicsModel,
        pinhole: DoubleValuePV,
        pinhole_vertical: DoubleValuePV,
        pinhole_horizontal: DoubleValuePV
    ) -> None:
        super(PinholeExpertGroupController, self).__init__()

        self._widget = widget
        self._controller = controller
        self._epics = epics_model

        self._pinhole = pinhole
        self._pinhole_vertical = pinhole_vertical
        self._pinhole_horizontal = pinhole_horizontal

        self.position_filter = EventFilterModel(self._pinhole)
        self.vertical_filter = EventFilterModel(self._pinhole_vertical)
        self.horizontal_filter = EventFilterModel(self._pinhole_horizontal)

        self._connect_pinhole_widgets()
        self._configure_pinhole_widgets()

    def _connect_pinhole_widgets(self) -> None:
        # Step buttons
        self._widget.btn_step_1.clicked.connect(
            lambda: self._btn_step_clicked(value=self._step_1)
        )
        self._widget.btn_step_2.clicked.connect(
            lambda: self._btn_step_clicked(value=self._step_2)
        )
        self._widget.btn_step_3.clicked.connect(
            lambda: self._btn_step_clicked(value=self._step_3)
        )

        self._widget.btn_pinhole_position_plus.clicked.connect(
            lambda: self._btn_plus_minus_clicked(stage=self._pinhole)
        )
        self._widget.btn_pinhole_position_minus.clicked.connect(
            lambda: self._btn_plus_minus_clicked(
                stage=self._pinhole, minus=True
            )
        )
        self._widget.btn_pinhole_vertical_plus.clicked.connect(
            lambda: self._btn_plus_minus_clicked(stage=self._pinhole_vertical)
        )
        self._widget.btn_pinhole_vertical_minus.clicked.connect(
            lambda: self._btn_plus_minus_clicked(
                stage=self._pinhole_vertical, minus=True
            )
        )
        self._widget.btn_pinhole_horizontal_plus.clicked.connect(
            lambda: self._btn_plus_minus_clicked(stage=self._pinhole_horizontal)
        )
        self._widget.btn_pinhole_horizontal_minus.clicked.connect(
            lambda: self._btn_plus_minus_clicked(
                stage=self._pinhole_horizontal, minus=True
            )
        )

        self._widget.lne_pinhole_position.returnPressed.connect(
            lambda: self._lne_pinhole_pressed(
                stage=self._pinhole,
                lne_box=self._widget.lne_pinhole_position,
            )
        )
        self._widget.lne_pinhole_vertical.returnPressed.connect(
            lambda: self._lne_pinhole_pressed(
                stage=self._pinhole_vertical,
                lne_box=self._widget.lne_pinhole_vertical,
            )
        )
        self._widget.lne_pinhole_horizontal.returnPressed.connect(
            lambda: self._lne_pinhole_pressed(
                stage=self._pinhole_horizontal,
                lne_box=self._widget.lne_pinhole_horizontal,
            )
        )

        self._controller.pinhole_position_changed.connect(self._update_pinhole)
        self._pinhole_vertical_changed.connect(self._update_pinhole_vertical)
        self._pinhole_horizontal_changed.connect(self._update_pinhole_horizontal)

    def _configure_pinhole_widgets(self) -> None:
        self._widget.btn_step_1.setText(str(self._step_1))
        self._widget.btn_step_2.setText(str(self._step_2))
        self._widget.btn_step_3.setText(str(self._step_3))

        # Default selection
        self._widget.btn_step_3.setChecked(True)
        self._step = self._step_3

        # Step button status tips
        self._widget.btn_step_1.setStatusTip(f"Sets the step to {self._step_1} mm")
        self._widget.btn_step_2.setStatusTip(f"Sets the step to {self._step_2} mm")
        self._widget.btn_step_3.setStatusTip(f"Sets the step to {self._step_3} mm")

        # Set event filters
        self._widget.lne_pinhole_position.installEventFilter(self.position_filter)
        self._widget.lne_pinhole_vertical.installEventFilter(self.vertical_filter)
        self._widget.lne_pinhole_horizontal.installEventFilter(self.horizontal_filter)

    def _btn_step_clicked(self, value: float) -> None:
        self._step = value

        if self._step == self._step_1:
            self._widget.btn_step_1.setChecked(True)
            self._widget.btn_step_2.setChecked(False)
            self._widget.btn_step_3.setChecked(False)
        elif self._step == self._step_2:
            self._widget.btn_step_1.setChecked(False)
            self._widget.btn_step_2.setChecked(True)
            self._widget.btn_step_3.setChecked(False)
        else:
            self._widget.btn_step_1.setChecked(False)
            self._widget.btn_step_2.setChecked(False)
            self._widget.btn_step_3.setChecked(True)

    def _btn_plus_minus_clicked(
        self,
        stage: DoubleValuePV,
        minus: Optional[bool] = False,
    ) -> None:
        value = stage.readback

        if minus:
            stage.move(value=value - self._step)
        else:
            stage.move(value=value + self._step)

    @staticmethod
    def _lne_pinhole_pressed(stage: DoubleValuePV, lne_box: QLineEdit) -> None:
        if lne_box.text() is not None:
            value = float(lne_box.text())

            stage.move(value=value)

        lne_box.clearFocus()

    def _update_pinhole(self, text: str) -> None:
        if not self._widget.lne_pinhole_position.hasFocus():
            if self._widget.lne_pinhole_position.text() != text:
                self._widget.lne_pinhole_position.setText(text)

    def _update_pinhole_vertical(self, text: str) -> None:
        if not self._widget.lne_pinhole_vertical.hasFocus():
            if self._widget.lne_pinhole_vertical.text() != text:
                self._widget.lne_pinhole_vertical.setText(text)

    def _update_pinhole_horizontal(self, text: str) -> None:
        if not self._widget.lne_pinhole_horizontal.hasFocus():
            if self._widget.lne_pinhole_horizontal.text() != text:
                self._widget.lne_pinhole_horizontal.setText(text)

    def update_pinhole_position(self) -> None:
        """Updates the pinhole position label and disables/enables pinhole buttons."""
        if self._epics.connected:

            if self._pinhole_vertical.moving:
                self._pinhole_vertical_changed.emit(str("{0:.4f}".format(self._pinhole_vertical.readback)))

                self._pinhole_vertical.moving = False

            if self._pinhole_horizontal.moving:
                self._pinhole_horizontal_changed.emit(str("{0:.4f}".format(self._pinhole_horizontal.readback)))

                self._pinhole_horizontal.moving = False
