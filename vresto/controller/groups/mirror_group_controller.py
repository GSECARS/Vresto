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
from vresto.widget.groups import MirrorGroup
from vresto.widget.custom import MsgBox


class MirrorGroupController(QObject):
    _us_mirror_position_changed: Signal = Signal(str)
    _ds_mirror_position_changed: Signal = Signal(str)
    _us_mirror_position: Signal = Signal(float)
    _ds_mirror_position: Signal = Signal(float)

    _us_mirror_in: float = 0.0
    _us_mirror_out: float = -115.0
    _ds_mirror_in: float = 0.0
    _ds_mirror_out: float = -115.0

    _omega_limit: float = -90.0
    _pinhole_limit: float = 0.0

    def __init__(
        self,
        widget: MirrorGroup,
        epics_model: EpicsModel,
        us_mirror: DoubleValuePV,
        ds_mirror: DoubleValuePV,
        omega_stage: DoubleValuePV,
        pinhole_stage: DoubleValuePV,
    ) -> None:
        super(MirrorGroupController, self).__init__()

        self._widget = widget
        self._epics = epics_model

        self._ds_mirror = ds_mirror
        self._us_mirror = us_mirror
        self._omega_stage = omega_stage
        self._pinhole_stage = pinhole_stage

        self._connect_mirror_widgets()
        self._configure_mirror_widgets()

    def _connect_mirror_widgets(self) -> None:
        self._widget.btn_us_in.clicked.connect(self._btn_us_mirror_in_clicked)
        self._widget.btn_ds_in.clicked.connect(self._btn_ds_mirror_in_clicked)
        self._widget.btn_us_out.clicked.connect(self._btn_us_mirror_out_clicked)
        self._widget.btn_ds_out.clicked.connect(self._btn_ds_mirror_out_clicked)

        self._us_mirror_position_changed.connect(self._update_us_label)
        self._ds_mirror_position_changed.connect(self._update_ds_label)
        self._us_mirror_position.connect(self._us_mirror_at_position)
        self._ds_mirror_position.connect(self._ds_mirror_at_position)

    def _configure_mirror_widgets(self) -> None:
        self._widget.btn_us_in.setToolTip(
            f"Moves the us mirror at {self._us_mirror_in}"
        )
        self._widget.btn_us_out.setToolTip(
            f"Moves the us mirror at {self._us_mirror_out}"
        )
        self._widget.btn_ds_in.setToolTip(
            f"Moves the ds mirror at {self._ds_mirror_in}"
        )
        self._widget.btn_ds_out.setToolTip(
            f"Moves the ds mirror at {self._ds_mirror_out}"
        )

    def _btn_us_mirror_in_clicked(self) -> None:
        if self._omega_stage.moving:
            MsgBox(msg="Wait for omega to stop moving.")
            return None

        if self._pinhole_stage.moving:
            MsgBox(msg="Wait for pinhole to stop moving.")
            return None

        if (
            self._omega_stage.readback != self._omega_limit
            or self._pinhole_stage.readback > self._pinhole_limit
        ):
            MsgBox(msg="First move to X-Ray position and move the pinhole OUT!")
            return None

        self._us_mirror.move(value=self._us_mirror_in)

    def _btn_ds_mirror_in_clicked(self) -> None:
        if self._omega_stage.moving:
            MsgBox(msg="Wait for omega to stop moving.")
            return None

        if self._omega_stage.readback != self._omega_limit:
            MsgBox(msg="First move to X-Ray position!")
            return None

        self._ds_mirror.move(value=self._ds_mirror_in)

    def _btn_us_mirror_out_clicked(self) -> None:
        self._us_mirror.move(value=self._us_mirror_out)

    def _btn_ds_mirror_out_clicked(self) -> None:
        self._ds_mirror.move(value=self._ds_mirror_out)

    def _update_us_label(self, text: str) -> None:
        self._widget.lbl_us_position.setText(text)

    def _us_mirror_at_position(self, position: float) -> None:
        position = round(position)

        if position == self._us_mirror_in:
            self._widget.btn_us_in.setEnabled(False)
            self._widget.btn_us_out.setEnabled(True)
        elif position == self._us_mirror_out:
            self._widget.btn_us_in.setEnabled(True)
            self._widget.btn_us_out.setEnabled(False)
        else:
            self._widget.btn_us_in.setEnabled(True)
            self._widget.btn_us_out.setEnabled(True)

    def _update_ds_label(self, text: str) -> None:
        self._widget.lbl_ds_position.setText(text)

    def _ds_mirror_at_position(self, position: float) -> None:
        position = round(position)

        if position == self._ds_mirror_in:
            self._widget.btn_ds_in.setEnabled(False)
            self._widget.btn_ds_out.setEnabled(True)
        elif position == self._ds_mirror_out:
            self._widget.btn_ds_in.setEnabled(True)
            self._widget.btn_ds_out.setEnabled(False)
        else:
            self._widget.btn_ds_in.setEnabled(True)
            self._widget.btn_ds_out.setEnabled(True)

    def update_mirror_positions(self) -> None:
        """Updates the mirror position labels."""
        if self._epics.connected:

            if self._us_mirror.moving:
                self._us_mirror_position_changed.emit(
                    str("{0:.4f}".format(self._us_mirror.readback))
                )

                self._us_mirror.moving = False
                self._us_mirror_position.emit(self._us_mirror.readback)

            if self._ds_mirror.moving:
                self._ds_mirror_position_changed.emit(
                    str("{0:.4f}".format(self._ds_mirror.readback))
                )

                self._ds_mirror.moving = False
                self._ds_mirror_position.emit(self._ds_mirror.readback)

        if self._us_mirror.readback is None:
            self._us_mirror_position_changed.emit("Unknown")

        if self._ds_mirror.readback is None:
            self._ds_mirror_position_changed.emit("Unknown")
