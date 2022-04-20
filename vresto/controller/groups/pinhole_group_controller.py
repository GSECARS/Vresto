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
from vresto.widget.groups import PinholeGroup
from vresto.widget.custom import MsgBox


class PinholeGroupController(QObject):
    _pinhole_position_changed: Signal = Signal(str)
    _position: Signal = Signal(float)

    _pinhole_in: float = 0.0
    _pinhole_out: float = -20.0
    _pinhole_off: float = -30.0
    _omega_limit: float = -90
    _us_limit: float = -114.0

    def __init__(
        self,
        widget: PinholeGroup,
        epics_model: EpicsModel,
        pinhole_stage: DoubleValuePV,
        omega_stage: DoubleValuePV,
        us_mirror: DoubleValuePV,
    ) -> None:
        super(PinholeGroupController, self).__init__()

        self._widget = widget
        self._epics = epics_model

        self._pinhole_stage = pinhole_stage
        self._omega_stage = omega_stage
        self._us_mirror = us_mirror

        self._connect_pinhole_widgets()
        self._configure_pinhole_widgets()

    def _connect_pinhole_widgets(self) -> None:
        self._widget.btn_20.clicked.connect(self._btn_pinhole_20_clicked)
        self._widget.btn_in.clicked.connect(self._btn_pinhole_in_clicked)
        self._widget.btn_out.clicked.connect(self._btn_pinhole_out_clicked)
        self._widget.btn_off.clicked.connect(self._btn_pinhole_off_clicked)
        self._widget.lne_custom.returnPressed.connect(self._lne_custom_pressed)

        self._pinhole_position_changed.connect(self._update_pinhole_label)
        self._position.connect(self._pinhole_at_position)

    def _configure_pinhole_widgets(self) -> None:
        self._widget.btn_20.setToolTip(f"Moves the pinhole at 20.0")
        self._widget.btn_in.setToolTip(f"Moves the pinhole at {self._pinhole_in}")
        self._widget.btn_out.setToolTip(f"Moves the pinhole at {self._pinhole_out}")
        self._widget.btn_off.setToolTip(f"Moves the pinhole at {self._pinhole_off}")

    def _btn_pinhole_20_clicked(self) -> None:
        if self._omega_stage.moving:
            MsgBox(msg=f"Wait for omega to stop moving.")
            return None

        if self._us_mirror.moving:
            MsgBox(msg=f"Wait for the us mirror to stop moving.")
            return None
        if (
            self._omega_stage.readback != self._omega_limit
            or self._us_mirror.readback > self._us_limit
        ):
            MsgBox(
                msg=f"You forgot to remove the UPSTREAM MIRROR or you are in the MICROSCOPE position."
            )
            return None
        self._pinhole_stage.move(value=20.0)

    def _btn_pinhole_in_clicked(self) -> None:
        if self._omega_stage.moving:
            MsgBox(msg=f"Wait for omega to stop moving.")
            return None
        if self._omega_stage.readback != self._omega_limit:
            MsgBox(
                msg=f"The omega stage must be at {self._omega_limit}. Move to X-RAY position."
            )
            return None
        self._pinhole_stage.move(value=self._pinhole_in)

    def _btn_pinhole_out_clicked(self) -> None:
        self._pinhole_stage.move(value=self._pinhole_out)

    def _btn_pinhole_off_clicked(self) -> None:
        self._pinhole_stage.move(value=self._pinhole_off)

    def _lne_custom_pressed(self) -> None:
        self._widget.lne_custom.clearFocus()
        if self._widget.lne_custom.text() is not None:
            value = float(self._widget.lne_custom.text())

            if value > 0.0:
                if self._omega_stage.moving:
                    MsgBox(msg=f"Wait for omega to stop moving.")
                    return None

                if self._us_mirror.moving:
                    MsgBox(msg=f"Wait for the us mirror to stop moving.")
                    return None

                if (
                    self._omega_stage.readback != self._omega_limit
                    or self._us_mirror.readback > self._us_limit
                ):
                    MsgBox(
                        msg=f"You forgot to remove the UPSTREAM MIRROR or you are in the MICROSCOPE position."
                    )
                    return None

            self._pinhole_stage.move(value=value)

    def _update_pinhole_label(self, text: str) -> None:
        self._widget.lbl_position.setText(text)

    def _pinhole_at_position(self, position: float) -> None:
        if position == 20:
            self._widget.btn_20.setEnabled(False)
            self._widget.btn_in.setEnabled(True)
            self._widget.btn_out.setEnabled(True)
            self._widget.btn_off.setEnabled(True)
        elif position == self._pinhole_in:
            self._widget.btn_20.setEnabled(True)
            self._widget.btn_in.setEnabled(False)
            self._widget.btn_out.setEnabled(True)
            self._widget.btn_off.setEnabled(True)
        elif position == self._pinhole_out:
            self._widget.btn_20.setEnabled(True)
            self._widget.btn_in.setEnabled(True)
            self._widget.btn_out.setEnabled(False)
            self._widget.btn_off.setEnabled(True)
        elif position == self._pinhole_off:
            self._widget.btn_20.setEnabled(True)
            self._widget.btn_in.setEnabled(True)
            self._widget.btn_out.setEnabled(True)
            self._widget.btn_off.setEnabled(False)
        else:
            self._widget.btn_20.setEnabled(True)
            self._widget.btn_in.setEnabled(True)
            self._widget.btn_out.setEnabled(True)
            self._widget.btn_off.setEnabled(True)

    def update_pinhole_position(self) -> None:
        """Updates the pinhole position label and disables/enables pinhole buttons."""
        if self._epics.connected:
            if self._pinhole_stage.moving:
                self._pinhole_position_changed.emit(
                    str("{0:.4f}".format(self._pinhole_stage.readback))
                )

                self._pinhole_stage.moving = False
                self._position.emit(self._pinhole_stage.readback)

        if self._pinhole_stage.readback is None:
            self._pinhole_position_changed.emit("Unknown")
