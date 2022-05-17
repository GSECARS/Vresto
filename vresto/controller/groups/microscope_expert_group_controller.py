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
from qtpy.QtWidgets import QLineEdit
from qtpy.QtCore import QObject, Signal

from vresto.controller.groups import MicroscopeGroupController
from vresto.model import DoubleValuePV, EpicsModel, EventFilterModel
from vresto.widget.groups import MicroscopeExpertGroup


class MicroscopeExpertGroupController(QObject):
    _gain_changed: Signal = Signal(int)
    _microscope_vertical_changed: Signal = Signal(str)
    _microscope_horizontal_changed: Signal = Signal(str)

    _microscope_in: float = 0.0
    _microscope_out: float = -70.0

    _slider_max: int = 100
    _slider_light_multiplier: int = 20
    _slider_gain_multiplier: int = 3.3

    _step: float
    _step_1: float = 0.1
    _step_2: float = 0.01
    _step_3: float = 0.001

    def __init__(
        self,
        widget: MicroscopeExpertGroup,
        controller: MicroscopeGroupController,
        epics_model: EpicsModel,
        microscope_stage: DoubleValuePV,
        microscope_vertical: DoubleValuePV,
        microscope_horizontal: DoubleValuePV,
        microscope_light: DoubleValuePV,
        microscope_gain: DoubleValuePV,
    ) -> None:
        super(MicroscopeExpertGroupController, self).__init__()

        self._widget = widget
        self._controller = controller
        self._epics = epics_model

        self.microscope_stage = microscope_stage
        self.microscope_vertical = microscope_vertical
        self.microscope_horizontal = microscope_horizontal
        self.microscope_light = microscope_light
        self.microscope_gain = microscope_gain

        self.vertical_filter = EventFilterModel(self.microscope_vertical)
        self.horizontal_filter = EventFilterModel(self.microscope_horizontal)
        self.focus_filter = EventFilterModel(self.microscope_stage)

        self._connect_microscope_widgets()
        self._configure_microscope_widgets()

    def _connect_microscope_widgets(self) -> None:
        self._widget.btn_microscope_in.clicked.connect(self._btn_microscope_in_clicked)
        self._widget.btn_microscope_out.clicked.connect(self._btn_microscope_out_clicked)
        self._widget.slider_light.valueChanged.connect(self._slider_light_value_changed)
        self._widget.slider_gain.valueChanged.connect(self._slider_gain_value_changed)

        self._controller.microscope_position_changed.connect(self._update_microscope_position_label)

        self._widget.btn_step_1.clicked.connect(lambda: self._btn_step_clicked(value=self._step_1))
        self._widget.btn_step_2.clicked.connect(lambda: self._btn_step_clicked(value=self._step_2))
        self._widget.btn_step_3.clicked.connect(lambda: self._btn_step_clicked(value=self._step_3))

        self._widget.lne_microscope_vertical.returnPressed.connect(
            lambda: self._lne_microscope_pressed(
                stage=self.microscope_vertical,
                lne_box=self._widget.lne_microscope_vertical,
            )
        )
        self._widget.lne_microscope_horizontal.returnPressed.connect(
            lambda: self._lne_microscope_pressed(
                stage=self.microscope_horizontal,
                lne_box=self._widget.lne_microscope_horizontal,
            )
        )
        self._widget.lne_microscope_focus.returnPressed.connect(
            lambda: self._lne_microscope_pressed(
                stage=self.microscope_stage,
                lne_box=self._widget.lne_microscope_focus,
            )
        )

        self._widget.btn_microscope_vertical_plus.clicked.connect(
            lambda: self._btn_plus_minus_clicked(stage=self.microscope_vertical)
        )
        self._widget.btn_microscope_vertical_minus.clicked.connect(
            lambda: self._btn_plus_minus_clicked(
                stage=self.microscope_vertical, minus=True
            )
        )
        self._widget.btn_microscope_horizontal_plus.clicked.connect(
            lambda: self._btn_plus_minus_clicked(stage=self.microscope_horizontal)
        )
        self._widget.btn_microscope_horizontal_minus.clicked.connect(
            lambda: self._btn_plus_minus_clicked(
                stage=self.microscope_horizontal, minus=True
            )
        )
        self._widget.btn_microscope_focus_plus.clicked.connect(
            lambda: self._btn_plus_minus_clicked(stage=self.microscope_stage)
        )
        self._widget.btn_microscope_focus_minus.clicked.connect(
            lambda: self._btn_plus_minus_clicked(
                stage=self.microscope_stage, minus=True
            )
        )

        self._controller.microscope_position.connect(self._microscope_at_position)
        self._controller.reflected_changed.connect(self._light_value_changed)
        self._gain_changed.connect(self._gain_value_changed)

        self._microscope_vertical_changed.connect(self._update_microscope_vertical)
        self._microscope_horizontal_changed.connect(self._update_microscope_horizontal)
        self._controller.microscope_position_changed.connect(self._update_microscope_focus)

    def _configure_microscope_widgets(self) -> None:
        self._widget.btn_step_1.setText(str(self._step_1))
        self._widget.btn_step_2.setText(str(self._step_2))
        self._widget.btn_step_3.setText(str(self._step_3))

        # Default selection
        self._widget.btn_step_3.setChecked(True)
        self._step = self._step_3

        # Status and tool tips
        self._widget.btn_step_1.setStatusTip(f"Sets the step to {self._step_1} mm")
        self._widget.btn_step_2.setStatusTip(f"Sets the step to {self._step_2} mm")
        self._widget.btn_step_3.setStatusTip(f"Sets the step to {self._step_3} mm")
        self._widget.btn_microscope_in.setToolTip(f"Moves the microscope at {self._microscope_in}")
        self._widget.btn_microscope_out.setToolTip(f"Moves the microscope at {self._microscope_out}")

        # Set event filters
        self._widget.lne_microscope_vertical.installEventFilter(self.vertical_filter)
        self._widget.lne_microscope_horizontal.installEventFilter(self.horizontal_filter)
        self._widget.lne_microscope_focus.installEventFilter(self.focus_filter)

        # Config sliders
        self._widget.slider_light.setMinimum(0)
        self._widget.slider_light.setMaximum(self._slider_max)
        self._widget.slider_light.setRange(0, self._slider_max)

        self._widget.slider_gain.setMinimum(0)
        self._widget.slider_gain.setMaximum(self._slider_max)
        self._widget.slider_gain.setRange(0, self._slider_max)

    def _btn_microscope_in_clicked(self) -> None:
        self.microscope_stage.move(value=self._microscope_in)
        self._widget.slider_light.setValue(int(self._slider_max / 2))

    def _btn_microscope_out_clicked(self) -> None:
        self.microscope_stage.move(value=self._microscope_out)
        self._widget.slider_light.setValue(0)

    def _slider_light_value_changed(self) -> None:
        self.microscope_light.move(value=(self._widget.slider_light.value() / self._slider_light_multiplier))

    def _slider_gain_value_changed(self) -> None:
        self.microscope_gain.move(value=(self._widget.slider_gain.value() / self._slider_gain_multiplier))

    def _update_microscope_position_label(self, text: str) -> None:
        self._widget.lbl_microscope_position.setText(text)

    def _microscope_at_position(self, position: float) -> None:
        if position == self._microscope_in:
            self._widget.btn_microscope_in.setEnabled(False)
            self._widget.btn_microscope_out.setEnabled(True)
        elif position == self._microscope_out:
            self._widget.btn_microscope_in.setEnabled(True)
            self._widget.btn_microscope_out.setEnabled(False)
        else:
            self._widget.btn_microscope_in.setEnabled(True)
            self._widget.btn_microscope_out.setEnabled(True)

    def _light_value_changed(self, value: int) -> None:
        if not self._widget.slider_light.hasFocus():
            self._widget.slider_light.valueChanged.disconnect(
                self._slider_light_value_changed
            )
            self._widget.slider_light.setValue(value)
            self._widget.slider_light.valueChanged.connect(
                self._slider_light_value_changed
            )

    def _gain_value_changed(self, value: int) -> None:
        if not self._widget.slider_gain.hasFocus():
            self._widget.slider_gain.valueChanged.disconnect(
                self._slider_gain_value_changed
            )
            self._widget.slider_gain.setValue(value)
            self._widget.slider_gain.valueChanged.connect(
                self._slider_gain_value_changed
            )

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
    def _lne_microscope_pressed(stage: DoubleValuePV, lne_box: QLineEdit) -> None:
        if lne_box.text() is not None:
            value = float(lne_box.text())

            stage.move(value=value)
        lne_box.clearFocus()

    def _update_microscope_vertical(self, text: str) -> None:
        if not self._widget.lne_microscope_vertical.hasFocus():
            if self._widget.lne_microscope_vertical.text() != text:
                self._widget.lne_microscope_vertical.setText(text)

    def _update_microscope_horizontal(self, text: str) -> None:
        if not self._widget.lne_microscope_horizontal.hasFocus():
            if self._widget.lne_microscope_horizontal.text() != text:
                self._widget.lne_microscope_horizontal.setText(text)

    def _update_microscope_focus(self, text: str) -> None:
        if not self._widget.lne_microscope_focus.hasFocus():
            if self._widget.lne_microscope_focus.text() != text:
                self._widget.lne_microscope_focus.setText(text)

    def update_microscope_positions(self) -> None:
        if self._epics.connected:

            if self.microscope_gain.moving:
                self._gain_changed.emit(
                    int(self.microscope_gain.readback * self._slider_gain_multiplier)
                )
                self.microscope_gain.moving = False

            if self.microscope_vertical.moving:
                self._microscope_vertical_changed.emit(
                    str("{0:.4f}".format(self.microscope_vertical.readback))
                )

                self.microscope_vertical.moving = False

            if self.microscope_horizontal.moving:
                self._microscope_horizontal_changed.emit(
                    str("{0:.4f}".format(self.microscope_horizontal.readback))
                )

                self.microscope_horizontal.moving = False
