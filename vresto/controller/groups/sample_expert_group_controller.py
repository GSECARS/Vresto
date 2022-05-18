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

from vresto.controller.groups import SampleGroupController
from vresto.model import DoubleValuePV, EpicsModel, EventFilterModel
from vresto.widget.groups import SampleExpertGroup

from qtpy.QtWidgets import QLineEdit


class SampleExpertGroupController(QObject):
    _vertical_rbv_changed: Signal = Signal(str)
    _horizontal_rbv_changed: Signal = Signal(str)
    _focus_rbv_changed: Signal = Signal(str)
    _omega_rbv_changed: Signal = Signal(str)
    _xray_microscope_position: Signal = Signal(float)

    _step: float
    _step_1: float = 0.1
    _step_2: float = 0.01
    _step_3: float = 0.001
    _step_omega: float
    _step_omega_1: float = 5.0
    _step_omega_2: float = 1.0
    _step_omega_3: float = 0.1

    _crosshair_high_limit: float = 5.0
    _crosshair_low_limit: float = -185.0
    _users_high_limit: float = -45.0
    _users_low_limit: float = -135.0
    _pinhole_out_value: float = -20.0

    def __init__(
        self,
        widget: SampleExpertGroup,
        controller: SampleGroupController,
        epics_model: EpicsModel,
        sample_vertical_stage: DoubleValuePV,
        sample_horizontal_stage: DoubleValuePV,
        sample_focus_stage: DoubleValuePV,
        sample_omega_stage: DoubleValuePV,
        pinhole_stage: DoubleValuePV,
    ):
        super(SampleExpertGroupController, self).__init__()

        self._widget = widget
        self._controller = controller
        self._epics = epics_model

        self._sample_vertical_stage = sample_vertical_stage
        self._sample_horizontal_stage = sample_horizontal_stage
        self._sample_focus_stage = sample_focus_stage
        self._sample_omega_stage = sample_omega_stage
        self._pihole_stage = pinhole_stage

        self._deg_sign = "\N{DEGREE SIGN}"

        self.vertical_filter = EventFilterModel(self._sample_vertical_stage)
        self.horizontal_filter = EventFilterModel(self._sample_horizontal_stage)
        self.focus_filter = EventFilterModel(self._sample_focus_stage)
        self.omega_filter = EventFilterModel(self._sample_omega_stage)

        self._connect_sample_widgets()
        self._configure_sample_widgets()

    def _connect_sample_widgets(self) -> None:
        self._widget.btn_prepare_crosshair.clicked.connect(self._btn_prepare_for_crosshair_clicked)
        self._widget.btn_prepare_user.clicked.connect(self._btn_prepare_for_users_clicked)
        # Step buttons
        self._widget.btn_step_1.clicked.connect(lambda: self._btn_step_clicked(value=self._step_1))
        self._widget.btn_step_2.clicked.connect(lambda: self._btn_step_clicked(value=self._step_2))
        self._widget.btn_step_3.clicked.connect(lambda: self._btn_step_clicked(value=self._step_3))

        # Omega step buttons
        self._widget.btn_omega_step_1.clicked.connect(
            lambda: self._btn_step_clicked(value=self._step_omega_1, omega_steps=True)
        )
        self._widget.btn_omega_step_2.clicked.connect(
            lambda: self._btn_step_clicked(value=self._step_omega_2, omega_steps=True)
        )
        self._widget.btn_omega_step_3.clicked.connect(
            lambda: self._btn_step_clicked(value=self._step_omega_3, omega_steps=True)
        )

        # Plus/minus buttons
        self._widget.btn_plus_vertical.clicked.connect(
            lambda: self._btn_plus_minus_clicked(
                sample_stage=self._sample_vertical_stage
            )
        )

        self._widget.btn_plus_horizontal.clicked.connect(
            lambda: self._btn_plus_minus_clicked(
                sample_stage=self._sample_horizontal_stage
            )
        )

        self._widget.btn_plus_focus.clicked.connect(
            lambda: self._btn_plus_minus_clicked(sample_stage=self._sample_focus_stage)
        )

        self._widget.btn_plus_omega.clicked.connect(
            lambda: self._btn_plus_minus_clicked(
                sample_stage=self._sample_omega_stage, omega=True
            )
        )

        self._widget.btn_minus_vertical.clicked.connect(
            lambda: self._btn_plus_minus_clicked(
                sample_stage=self._sample_vertical_stage, minus=True
            )
        )
        self._widget.btn_minus_horizontal.clicked.connect(
            lambda: self._btn_plus_minus_clicked(
                sample_stage=self._sample_horizontal_stage, minus=True
            )
        )
        self._widget.btn_minus_focus.clicked.connect(
            lambda: self._btn_plus_minus_clicked(
                sample_stage=self._sample_focus_stage, minus=True
            )
        )
        self._widget.btn_minus_omega.clicked.connect(
            lambda: self._btn_plus_minus_clicked(
                sample_stage=self._sample_omega_stage, minus=True, omega=True
            )
        )

        # lne boxes
        self._widget.lne_vertical.returnPressed.connect(
            lambda: self._lne_sample_pressed(
                sample_stage=self._sample_vertical_stage,
                lne_box=self._widget.lne_vertical,
            )
        )
        self._widget.lne_horizontal.returnPressed.connect(
            lambda: self._lne_sample_pressed(
                sample_stage=self._sample_horizontal_stage,
                lne_box=self._widget.lne_horizontal,
            )
        )
        self._widget.lne_focus.returnPressed.connect(
            lambda: self._lne_sample_pressed(
                sample_stage=self._sample_focus_stage,
                lne_box=self._widget.lne_focus,
            )
        )
        self._widget.lne_omega.returnPressed.connect(
            lambda: self._lne_sample_pressed(
                sample_stage=self._sample_omega_stage,
                lne_box=self._widget.lne_omega,
                omega=True,
            )
        )

        self._controller.vertical_rbv_changed.connect(self._update_vertical)
        self._controller.horizontal_rbv_changed.connect(self._update_horizontal)
        self._controller.focus_rbv_changed.connect(self._update_focus)
        self._controller.omega_rbv_changed.connect(self._update_omega)

    def _configure_sample_widgets(self) -> None:
        self._widget.btn_step_1.setText(str(self._step_1))
        self._widget.btn_step_2.setText(str(self._step_2))
        self._widget.btn_step_3.setText(str(self._step_3))
        self._widget.btn_omega_step_1.setText(str(self._step_omega_1))
        self._widget.btn_omega_step_2.setText(str(self._step_omega_2))
        self._widget.btn_omega_step_3.setText(str(self._step_omega_3))

        # Default selection
        self._widget.btn_step_3.setChecked(True)
        self._widget.btn_omega_step_2.setChecked(True)
        self._step = self._step_3
        self._step_omega = self._step_omega_2

        # Step button status tips
        self._widget.btn_step_1.setStatusTip(f"Sets the step to {self._step_1} mm")
        self._widget.btn_step_2.setStatusTip(f"Sets the step to {self._step_2} mm")
        self._widget.btn_step_3.setStatusTip(f"Sets the step to {self._step_3} mm")
        self._widget.btn_omega_step_1.setStatusTip(
            f"Sets the omega step to {self._step_omega_1} {self._deg_sign}"
        )
        self._widget.btn_omega_step_2.setStatusTip(
            f"Sets the omega step to {self._step_omega_2} {self._deg_sign}"
        )
        self._widget.btn_omega_step_3.setStatusTip(
            f"Sets the omega step to {self._step_omega_3} {self._deg_sign}"
        )

        # Set event filters
        self._widget.lne_vertical.installEventFilter(self.vertical_filter)
        self._widget.lne_horizontal.installEventFilter(self.horizontal_filter)
        self._widget.lne_focus.installEventFilter(self.focus_filter)
        self._widget.lne_omega.installEventFilter(self.omega_filter)

    def _btn_prepare_for_crosshair_clicked(self) -> None:
        self._sample_omega_stage.set_limits(
            high=self._crosshair_high_limit, low=self._crosshair_low_limit
        )
        self._move_sample_stages_to_zero()

    def _btn_prepare_for_users_clicked(self) -> None:
        self._sample_omega_stage.set_limits(
            high=self._users_high_limit, low=self._users_low_limit
        )
        self._pihole_stage.move(value=self._pinhole_out_value)
        self._move_sample_stages_to_zero()

    def _move_sample_stages_to_zero(self) -> None:
        self._sample_horizontal_stage.move(value=0.0)
        self._sample_vertical_stage.move(value=0.0)
        self._sample_focus_stage.move(value=0.0)

    def _btn_step_clicked(
        self, value: float, omega_steps: Optional[bool] = False
    ) -> None:

        if omega_steps:
            self._step_omega = value

            if self._step_omega == self._step_omega_1:
                self._widget.btn_omega_step_1.setChecked(True)
                self._widget.btn_omega_step_2.setChecked(False)
                self._widget.btn_omega_step_3.setChecked(False)
            elif self._step_omega == self._step_omega_2:
                self._widget.btn_omega_step_1.setChecked(False)
                self._widget.btn_omega_step_2.setChecked(True)
                self._widget.btn_omega_step_3.setChecked(False)
            else:
                self._widget.btn_omega_step_1.setChecked(False)
                self._widget.btn_omega_step_2.setChecked(False)
                self._widget.btn_omega_step_3.setChecked(True)
        else:
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
        sample_stage: DoubleValuePV,
        minus: Optional[bool] = False,
        omega: Optional[bool] = False,
    ) -> None:

        value = sample_stage.readback

        if minus:
            if not omega:
                sample_stage.move(value=value - self._step)
            else:
                sample_stage.move(value=value - self._step_omega)
        else:
            if not omega:
                sample_stage.move(value=value + self._step)
            else:
                sample_stage.move(value=value + self._step_omega)

    def _lne_sample_pressed(
        self,
        sample_stage: DoubleValuePV,
        lne_box: QLineEdit,
        omega: Optional[bool] = False,
    ) -> None:

        if lne_box.text() is not None:
            value = float(lne_box.text())

            if not omega:
                sample_stage.move(value=value)
            else:
                sample_stage.move(value=value)

            lne_box.clearFocus()
        else:
            lne_box.clearFocus()
            return None

    def _update_vertical(self, text: str) -> None:
        if not self._widget.lne_vertical.hasFocus():
            if self._widget.lne_vertical.text() != text:
                self._widget.lne_vertical.setText(text)

    def _update_horizontal(self, text: str) -> None:
        if not self._widget.lne_horizontal.hasFocus():
            if self._widget.lne_horizontal.text() != text:
                self._widget.lne_horizontal.setText(text)

    def _update_focus(self, text: str) -> None:
        if not self._widget.lne_focus.hasFocus():
            if self._widget.lne_focus.text() != text:
                self._widget.lne_focus.setText(text)

    def _update_omega(self, text: str) -> None:
        if not self._widget.lne_omega.hasFocus():
            if self._widget.lne_omega.text() != text:
                self._widget.lne_omega.setText(text)
