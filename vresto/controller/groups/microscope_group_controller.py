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

from qtpy.QtCore import QObject, Signal

from vresto.model import DoubleValuePV, EpicsModel
from vresto.widget.groups import MicroscopeGroup
from vresto.widget.custom import MsgBox


class MicroscopeGroupController(QObject):
    _microscope_position_changed: Signal = Signal(str)
    _microscope_zoom_position_changed: Signal = Signal(str)
    _microscope_position: Signal = Signal(float)
    _microscope_zoom_position: Signal = Signal(float)
    _reflected_changed: Signal = Signal(int)
    _transmitted_changed: Signal = Signal(int)

    _microscope_in: float = 0.0
    _microscope_out: float = -85.0
    _microscope_zoom_in: float = 0.0
    _microscope_zoom_out: float = -12.0

    _light_transmitted_on: float = 1.0
    _light_transmitted_off: float = 0.0

    _slider_max: int = 100
    _slider_value_multiplier: int = 2

    _omega_limit: float = -90.0
    _ds_limit: float = 40.0

    def __init__(
        self,
        widget: MicroscopeGroup,
        epics_model: EpicsModel,
        microscope_stage: DoubleValuePV,
        microscope_zoom: DoubleValuePV,
        microscope_focus: DoubleValuePV,
        light_reflected: DoubleValuePV,
        light_transmitted: DoubleValuePV,
        light_transmitted_switch: DoubleValuePV,
        sample_omega_stage: DoubleValuePV,
        ds_mirror: DoubleValuePV,
    ) -> None:
        super(MicroscopeGroupController, self).__init__()

        self._widget = widget
        self._epics = epics_model

        self.microscope_stage = microscope_stage
        self.microscope_zoom = microscope_zoom
        self._microscope_focus = microscope_focus
        self.light_reflected = light_reflected
        self.light_transmitted = light_transmitted
        self.light_transmitted_switch = light_transmitted_switch
        self._sample_omega_stage = sample_omega_stage
        self._ds_mirror = ds_mirror

        self._connect_microscope_widgets()
        self._configure_microscope_widgets()

    def _connect_microscope_widgets(self) -> None:
        self._widget.btn_microscope_in.clicked.connect(self._btn_microscope_in_clicked)
        self._widget.btn_microscope_out.clicked.connect(
            self._btn_microscope_out_clicked
        )
        self._widget.btn_zoom_in.clicked.connect(self._btn_microscope_zoom_in_clicked)
        self._widget.btn_zoom_out.clicked.connect(self._btn_microscope_zoom_out_clicked)
        self._widget.slider_reflected.valueChanged.connect(
            self._slider_reflected_value_changed
        )
        self._widget.slider_transmitted.valueChanged.connect(
            self._slider_transmitted_value_changed
        )

        self._microscope_position_changed.connect(
            self._update_microscope_position_label
        )
        self._microscope_zoom_position_changed.connect(
            self._update_microscope_zoom_position_label
        )
        self._microscope_position.connect(self._microscope_at_position)
        self._microscope_zoom_position.connect(self._microscope_zoom_at_position)
        self._reflected_changed.connect(self._reflected_value_changed)
        self._transmitted_changed.connect(self._transmitted_value_changed)

    def _configure_microscope_widgets(self) -> None:
        self._widget.btn_microscope_in.setToolTip(
            f"Moves the microscope at {self._microscope_in}"
        )
        self._widget.btn_microscope_out.setToolTip(
            f"Moves the microscope at {self._microscope_out}"
        )
        self._widget.btn_zoom_in.setToolTip(
            f"The microscope zooms in at {self._microscope_zoom_in}"
        )
        self._widget.btn_zoom_out.setToolTip(
            f"The microscope zooms out at {self._microscope_zoom_out}"
        )

        self._widget.slider_reflected.setMinimum(0)
        self._widget.slider_reflected.setMaximum(self._slider_max)
        self._widget.slider_reflected.setRange(0, self._slider_max)

        self._widget.slider_transmitted.setMinimum(0)
        self._widget.slider_transmitted.setMaximum(self._slider_max)
        self._widget.slider_transmitted.setRange(0, self._slider_max)

    def _btn_microscope_in_clicked(self) -> None:
        if self._sample_omega_stage.moving:
            MsgBox(msg=f"Wait for omega to stop moving.")
            return None

        if self._ds_mirror.moving:
            MsgBox(msg=f"Wait for downstream mirror to stop moving.")
            return None

        if self._sample_omega_stage.readback != self._omega_limit:
            MsgBox(
                msg=f"First, move the omega stage at {self._omega_limit} deg."
            )
            return None

        if self._ds_mirror.readback < self._ds_limit:
            MsgBox(
                msg=f"First, move the downstream mirror up."
            )
            return None

        self.microscope_stage.move(value=self._microscope_in)
        self.light_transmitted_switch.move(value=self._light_transmitted_on)
        self._widget.slider_reflected.setValue(int(self._slider_max / 2))
        self._widget.slider_transmitted.setValue(int(self._slider_max / 2))

    def _btn_microscope_out_clicked(self) -> None:
        if self.microscope_zoom.readback != self._microscope_zoom_in:
            MsgBox(
                msg=f"Diamond correction must be performed with Microscope 'Zoom IN'!\n"
                f"Make sure that this is the case and if need repeat the correction."
            )
            return None

        self.microscope_stage.move(value=self._microscope_out)
        self._widget.slider_reflected.setValue(0)
        self._widget.slider_transmitted.setValue(0)
        self.light_transmitted_switch.move(value=self._light_transmitted_off)

    def _btn_microscope_zoom_in_clicked(self) -> None:
        self.microscope_zoom.move(value=self._microscope_zoom_in)

    def _btn_microscope_zoom_out_clicked(self) -> None:
        self.microscope_zoom.move(value=self._microscope_zoom_out)

    def _slider_reflected_value_changed(self) -> None:
        self.light_reflected.move(
            value=(
                self._widget.slider_reflected.value() / self._slider_value_multiplier
            )
        )

    def _slider_transmitted_value_changed(self) -> None:
        self.light_transmitted.move(
            value=(
                self._widget.slider_transmitted.value() / self._slider_value_multiplier
            )
        )

    def _update_microscope_position_label(self, text: str) -> None:
        self._widget.lbl_microscope_position.setText(text)

    def _update_microscope_zoom_position_label(self, text: str) -> None:
        self._widget.lbl_zoom_position.setText(text)

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

    def _microscope_zoom_at_position(self, position: float) -> None:
        if position == self._microscope_zoom_in:
            self._widget.btn_zoom_in.setEnabled(False)
            self._widget.btn_zoom_out.setEnabled(True)
        elif position == self._microscope_zoom_out:
            self._widget.btn_zoom_in.setEnabled(True)
            self._widget.btn_zoom_out.setEnabled(False)
        else:
            self._widget.btn_zoom_in.setEnabled(True)
            self._widget.btn_zoom_out.setEnabled(True)

    def _reflected_value_changed(self, value: int) -> None:
        if not self._widget.slider_reflected.hasFocus():
            self._widget.slider_reflected.valueChanged.disconnect(
                self._slider_reflected_value_changed
            )
            self._widget.slider_reflected.setValue(value)
            self._widget.slider_reflected.valueChanged.connect(
                self._slider_reflected_value_changed
            )

    def _transmitted_value_changed(self, value: int) -> None:
        if not self._widget.slider_transmitted.hasFocus():
            self._widget.slider_transmitted.valueChanged.disconnect(
                self._slider_transmitted_value_changed
            )
            self._widget.slider_transmitted.setValue(value)
            self._widget.slider_transmitted.valueChanged.connect(
                self._slider_transmitted_value_changed
            )

    def update_microscope_positions(self) -> None:
        if self._epics.connected:

            if self._microscope_focus.moving:
                self._microscope_focus.moving = False

            if self.microscope_stage.moving:
                self._microscope_position_changed.emit(
                    str("{0:.4f}".format(self.microscope_stage.readback))
                )

                self.microscope_stage.moving = False
                self._microscope_position.emit(round(self.microscope_stage.readback, 3))

            if self.microscope_zoom.moving:
                self._microscope_zoom_position_changed.emit(
                    str("{0:.4f}".format(self.microscope_zoom.readback))
                )

                self.microscope_zoom.moving = False
                self._microscope_zoom_position.emit(self.microscope_zoom.readback)

            if self.light_reflected.moving:
                self._reflected_changed.emit(
                    int(self.light_reflected.readback * self._slider_value_multiplier)
                )
                self.light_reflected.moving = False

                self._microscope_zoom_position.emit(self.microscope_zoom.readback)

            if self.light_transmitted.moving:
                self._transmitted_changed.emit(
                    int(self.light_transmitted.readback * self._slider_value_multiplier)
                )
                self.light_transmitted.moving = False

                self._microscope_zoom_position.emit(self.microscope_zoom.readback)

            if self.light_transmitted_switch.moving:
                self.light_transmitted_switch.moving = False

        if self.microscope_stage.readback is None:
            self._microscope_position_changed.emit("Unknown")

        if self.microscope_zoom.readback is None:
            self._microscope_zoom_position_changed.emit("Unknown")
