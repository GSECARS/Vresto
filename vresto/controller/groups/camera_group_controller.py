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
from vresto.widget.groups import CameraGroup
from vresto.widget.custom import MsgBox


class CameraGroupController(QObject):
    _camera_position_changed: Signal = Signal(int)
    _reflected_changed: Signal = Signal(int)
    _transmitted_changed: Signal = Signal(int)

    _slider_max: int = 100
    _slider_value_multiplier: int = 22.22

    def __init__(
        self,
        widget: CameraGroup,
        epics_model: EpicsModel,
        camera: DoubleValuePV,
        reflected: DoubleValuePV,
        transmitted: DoubleValuePV,
        transmitted_switch: DoubleValuePV,
        shutter_switch_1: DoubleValuePV,
        shutter_switch_3: DoubleValuePV,
        shutter_switch_4: DoubleValuePV,
    ) -> None:
        super(CameraGroupController, self).__init__()

        self._widget = widget
        self._epics = epics_model
        self._camera = camera
        self._reflected = reflected
        self._transmitted = transmitted
        self._transmitted_switch = transmitted_switch
        self._shutter_switch_1 = shutter_switch_1
        self._shutter_switch_3 = shutter_switch_3
        self._shutter_switch_4 = shutter_switch_4

        self._connect_camera_group_widgets()
        self._configure_camera_group_widgets()

    def _connect_camera_group_widgets(self) -> None:
        self._widget.btn_camera_in.clicked.connect(lambda: self._btn_camera_clicked(target_value=1))
        self._widget.btn_camera_out.clicked.connect(lambda: self._btn_camera_clicked(target_value=0))

        self._widget.slider_reflected.valueChanged.connect(self._reflected_slider_value_changed)
        self._widget.slider_transmitted.valueChanged.connect(self._transmitted_slider_value_changed)

        self._camera_position_changed.connect(self._update_camera_buttons)
        self._reflected_changed.connect(self._reflected_value_changed)
        self._transmitted_changed.connect(self._transmitted_value_changed)

    def _configure_camera_group_widgets(self) -> None:
        pass

    def _btn_camera_clicked(self, target_value: int) -> None:
        if target_value == 1:

            check_1 = self._shutter_switch_1.readback
            check_2 = self._shutter_switch_3.readback
            check_3 = self._shutter_switch_4.readback

            if check_1 == 1 or check_2 == 1 or check_3 == 1:
                MsgBox(msg="First close the laser shutters.")
                return None

            self._reflected.move(50 / self._slider_value_multiplier)
            self._transmitted.move(90 / self._slider_value_multiplier)
            self._transmitted_switch.move(1)
        else:
            self._reflected.move(0)
            self._transmitted.move(0)
            self._transmitted_switch.move(0)

        self._camera.move(value=target_value)

    def _reflected_slider_value_changed(self) -> None:
        self._reflected.move(value=(self._widget.slider_reflected.value() / self._slider_value_multiplier))

    def _transmitted_slider_value_changed(self) -> None:
        self._transmitted.move(value=(self._widget.slider_transmitted.value() / self._slider_value_multiplier))

    def _update_camera_buttons(self, current_value: int) -> None:
        """Enables and disables the camera IN and OUT buttons."""
        if current_value == 1:
            self._widget.btn_camera_in.setEnabled(False)
            self._widget.btn_camera_out.setEnabled(True)
        else:
            self._widget.btn_camera_in.setEnabled(True)
            self._widget.btn_camera_out.setEnabled(False)

    def _reflected_value_changed(self, value: int) -> None:
        if not self._widget.slider_reflected.hasFocus():
            self._widget.slider_reflected.valueChanged.disconnect(self._reflected_slider_value_changed)
            self._widget.slider_reflected.setValue(value)
            self._widget.slider_reflected.valueChanged.connect(self._reflected_slider_value_changed)

    def _transmitted_value_changed(self, value: int) -> None:
        if not self._widget.slider_transmitted.hasFocus():
            self._widget.slider_transmitted.valueChanged.disconnect(self._transmitted_slider_value_changed)
            self._widget.slider_transmitted.setValue(value)
            self._widget.slider_transmitted.valueChanged.connect(self._transmitted_slider_value_changed)

    def update_camera(self) -> None:
        """Updates the pinhole position label and disables/enables pinhole buttons."""
        if self._epics.connected:
            if self._camera.moving:
                self._camera_position_changed.emit(self._camera.readback)

                self._camera.moving = False

            if self._reflected.moving:
                self._reflected_changed.emit(
                    int(self._reflected.readback * self._slider_value_multiplier)
                )
                self._reflected.moving = False

            if self._transmitted.moving:
                self._transmitted_changed.emit(
                    int(self._transmitted.readback * self._slider_value_multiplier)
                )
                self._transmitted.moving = False

            if self._transmitted_switch.moving:
                self._transmitted_switch.moving = False

            if self._shutter_switch_1.moving:
                self._shutter_switch_1.moving = False

            if self._shutter_switch_3.moving:
                self._shutter_switch_3.moving = False

            if self._shutter_switch_4.moving:
                self._shutter_switch_4.moving = False
