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

from vresto.controller.groups import MirrorGroupController
from vresto.model import DoubleValuePV, EpicsModel, EventFilterModel
from vresto.widget.groups import MirrorExpertGroup


class MirrorExpertGroupController(QObject):
    _ds_focus_position: Signal = Signal(float)
    _us_focus_position: Signal = Signal(float)
    _ds_light_changed: Signal = Signal(int)
    _us_light_changed: Signal = Signal(int)

    _step: float
    _step_1: float = 1.0
    _step_2: float = 0.5

    _slider_max: int = 100
    _slider_value_multiplier: int = 1

    _light_switch_on: float = 1.0
    _light_switch_off: float = 0.0

    def __init__(
        self,
        widget: MirrorExpertGroup,
        controller: MirrorGroupController,
        epics_model: EpicsModel,
        us_mirror: DoubleValuePV,
        us_focus: DoubleValuePV,
        ds_mirror: DoubleValuePV,
        ds_focus: DoubleValuePV,
        ds_light: DoubleValuePV,
        us_light: DoubleValuePV,
        us_light_switch: DoubleValuePV,
        ds_light_switch: DoubleValuePV
    ) -> None:
        super(MirrorExpertGroupController, self).__init__()

        self._widget = widget
        self._controller = controller
        self._epics = epics_model

        self._ds_mirror = ds_mirror
        self._ds_focus = ds_focus
        self._us_mirror = us_mirror
        self._us_focus = us_focus
        self._ds_light = ds_light
        self._us_light = us_light
        self._us_light_switch = us_light_switch
        self._ds_light_switch = ds_light_switch

        self.ds_filter = EventFilterModel(self._ds_mirror)
        self.us_filter = EventFilterModel(self._us_mirror)

        self._connect_mirror_widgets()
        self._configure_mirror_widgets()

    def _connect_mirror_widgets(self) -> None:
        self._widget.btn_step_1.clicked.connect(lambda: self._btn_step_clicked(value=self._step_1))
        self._widget.btn_step_2.clicked.connect(lambda: self._btn_step_clicked(value=self._step_2))
        self._widget.btn_ds_focus_zero.clicked.connect(lambda: self._zero_focus_clicked(stage=self._ds_focus))
        self._widget.btn_us_focus_zero.clicked.connect(lambda: self._zero_focus_clicked(stage=self._us_focus))
        self._widget.slider_ds.valueChanged.connect(self._slider_ds_value_changed)
        self._widget.slider_us.valueChanged.connect(self._slider_us_value_changed)

        self._widget.lne_ds.returnPressed.connect(
            lambda: self._lne_mirror_pressed(stage=self._ds_mirror, lne_box=self._widget.lne_ds,)
        )
        self._widget.lne_us.returnPressed.connect(
            lambda: self._lne_mirror_pressed(stage=self._us_mirror, lne_box=self._widget.lne_us,)
        )

        self._widget.btn_ds_plus.clicked.connect(lambda: self._btn_plus_minus_clicked(stage=self._ds_mirror))
        self._widget.btn_us_plus.clicked.connect(lambda: self._btn_plus_minus_clicked(stage=self._us_mirror))
        self._widget.btn_ds_minus.clicked.connect(
            lambda: self._btn_plus_minus_clicked(stage=self._ds_mirror, minus=True)
        )
        self._widget.btn_us_minus.clicked.connect(
            lambda: self._btn_plus_minus_clicked(stage=self._us_mirror, minus=True)
        )

        self._controller.us_mirror_position_changed.connect(self._update_us_value)
        self._controller.ds_mirror_position_changed.connect(self._update_ds_value)
        self._ds_focus_position.connect(self._ds_focus_at_position)
        self._us_focus_position.connect(self._us_focus_at_position)
        self._ds_light_changed.connect(self._ds_light_value_changed)
        self._us_light_changed.connect(self._us_light_value_changed)

    def _configure_mirror_widgets(self) -> None:
        self._widget.btn_step_1.setText(str(self._step_1))
        self._widget.btn_step_2.setText(str(self._step_2))

        # Default selection
        self._widget.btn_step_2.setChecked(True)
        self._step = self._step_2

        # Status and tool tips
        self._widget.btn_step_1.setStatusTip(f"Sets the step to {self._step_1} mm")
        self._widget.btn_step_2.setStatusTip(f"Sets the step to {self._step_2} mm")

        # Set event filters
        self._widget.lne_ds.installEventFilter(self.ds_filter)
        self._widget.lne_us.installEventFilter(self.us_filter)

        # Config sliders
        self._widget.slider_ds.setMinimum(0)
        self._widget.slider_ds.setMaximum(self._slider_max)
        self._widget.slider_ds.setRange(0, self._slider_max)

        self._widget.slider_us.setMinimum(0)
        self._widget.slider_us.setMaximum(self._slider_max)
        self._widget.slider_us.setRange(0, self._slider_max)

    def _btn_step_clicked(self, value: float) -> None:
        self._step = value

        if self._step == self._step_1:
            self._widget.btn_step_1.setChecked(True)
            self._widget.btn_step_2.setChecked(False)
        else:
            self._widget.btn_step_1.setChecked(False)
            self._widget.btn_step_2.setChecked(True)

    @staticmethod
    def _zero_focus_clicked(stage: DoubleValuePV) -> None:
        stage.move(value=0.0)

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
    def _lne_mirror_pressed(stage: DoubleValuePV, lne_box: QLineEdit) -> None:
        if lne_box.text() is not None:
            value = float(lne_box.text())

            stage.move(value=value)
        lne_box.clearFocus()

    def _update_ds_value(self, text: str) -> None:
        if not self._widget.lne_ds.hasFocus():
            if self._widget.lne_ds.text() != text:
                self._widget.lne_ds.setText(text)

    def _update_us_value(self, text: str) -> None:
        if not self._widget.lne_us.hasFocus():
            if self._widget.lne_us.text() != text:
                self._widget.lne_us.setText(text)

    def _ds_focus_at_position(self, position: float) -> None:
        if position == 0:
            self._widget.btn_ds_focus_zero.setEnabled(False)
        else:
            self._widget.btn_ds_focus_zero.setEnabled(True)

    def _us_focus_at_position(self, position: float) -> None:
        if position == 0:
            self._widget.btn_us_focus_zero.setEnabled(False)
        else:
            self._widget.btn_us_focus_zero.setEnabled(True)

    def _slider_ds_value_changed(self) -> None:
        self._ds_light.move(value=(self._widget.slider_ds.value() / self._slider_value_multiplier))

        if self._widget.slider_ds.value() == 0:
            self._ds_light_switch.move(value=self._light_switch_off)
        else:
            self._ds_light_switch.move(value=self._light_switch_on)

    def _slider_us_value_changed(self) -> None:
        self._us_light.move(value=(self._widget.slider_us.value() / self._slider_value_multiplier))

        if self._widget.slider_us.value() == 0:
            self._us_light_switch.move(value=self._light_switch_off)
        else:
            self._us_light_switch.move(value=self._light_switch_on)

    def _ds_light_value_changed(self, value: int) -> None:
        if not self._widget.slider_ds.hasFocus():
            self._widget.slider_ds.valueChanged.disconnect(
                self._slider_ds_value_changed
            )
            self._widget.slider_ds.setValue(value)
            self._widget.slider_ds.valueChanged.connect(
                self._slider_ds_value_changed
            )

    def _us_light_value_changed(self, value: int) -> None:
        if not self._widget.slider_us.hasFocus():
            self._widget.slider_us.valueChanged.disconnect(
                self._slider_us_value_changed
            )
            self._widget.slider_us.setValue(value)
            self._widget.slider_us.valueChanged.connect(
                self._slider_us_value_changed
            )

    def update_mirror_positions(self) -> None:
        if self._epics.connected:

            if self._ds_focus.moving:
                self._ds_focus.moving = False
                self._ds_focus_position.emit(self._ds_focus.readback)

            if self._us_focus.moving:
                self._us_focus.moving = False
                self._us_focus_position.emit(self._us_focus.readback)

            if self._ds_light.moving:
                self._ds_light_changed.emit(
                    int(self._ds_light.readback * self._slider_value_multiplier)
                )
                self._ds_light.moving = False

            if self._us_light.moving:
                self._us_light_changed.emit(
                    int(self._us_light.readback * self._slider_value_multiplier)
                )
                self._us_light.moving = False

            if self._ds_light_switch.moving:
                self._ds_light_switch.moving = False

            if self._us_light_switch.moving:
                self._us_light_switch.moving = False
