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

import os
import time
from datetime import datetime
from qtpy.QtCore import QObject, Signal
from qtpy.QtWidgets import QFileDialog, QLineEdit, QMessageBox

from vresto.model import (
    CorrectionsModel,
    StringValuePV,
    DoubleValuePV,
    ImportExportModel,
    EpicsModel,
)
from vresto.widget.groups import CommonControlsGroup
from vresto.widget.custom import MsgBox


class CommonControlsGroupController(QObject):

    _us_mirror_out: float = 40.0
    _ds_mirror_out: float = 40.0
    _pinhole_limit: float = -20.0
    _omega_limit: float = -90.0

    _path_changed: Signal = Signal(str)

    def __init__(
        self,
        widget: CommonControlsGroup,
        corrections_model: CorrectionsModel,
        epics_model: EpicsModel,
        ie_model: ImportExportModel,
        path: StringValuePV,
        lne_virtual_position: QLineEdit,
        lne_real_position: QLineEdit,
        us_mirror: DoubleValuePV,
        ds_mirror: DoubleValuePV,
        pinhole_stage: DoubleValuePV,
        omega_stage: DoubleValuePV,
        microscope_focus: DoubleValuePV,
        xps_stop: DoubleValuePV,
        station_stop: DoubleValuePV,
    ) -> None:
        super(CommonControlsGroupController, self).__init__()

        self._widget = widget
        self._corrections = corrections_model
        self._epics = epics_model

        self._ie_model = ie_model
        self._path = path
        self._lne_virtual_position = lne_virtual_position
        self._lne_real_position = lne_real_position
        self._us_mirror = us_mirror
        self._ds_mirror = ds_mirror
        self._pinhole_stage = pinhole_stage
        self._omega_stage = omega_stage
        self._microscope_focus = microscope_focus
        self._xps_stop = xps_stop
        self._station_stop = station_stop

        self.correction_aborted = False
        self._latest_path: str = "Unknown"

        self._connect_common_control_widgets()

    def _connect_common_control_widgets(self) -> None:
        self._widget.btn_stop_all.clicked.connect(self._btn_stop_all_clicked)
        self._widget.btn_save.clicked.connect(self._btn_save_clicked)
        self._widget.btn_save_as.clicked.connect(self._btn_save_as_clicked)
        self._widget.btn_load_correction.clicked.connect(self._btn_load_clicked)
        self._widget.btn_microscope_focus_zero.clicked.connect(self._btn_zero_clicked)

        self._path_changed.connect(self.current_path_changed)

    def _btn_stop_all_clicked(self) -> None:
        self._widget.btn_stop_all.clearFocus()

        self._corrections.abort_status = True

        self._xps_stop.move(value=1)
        self._station_stop.move(value=1)

    def _btn_zero_clicked(self) -> None:
        self._microscope_focus.move(value=0.0)

    def _btn_save_clicked(self) -> None:
        try:
            virtual_position = float(self._lne_virtual_position.text())
            real_position = float(self._lne_real_position.text())
        except ValueError:
            MsgBox(msg="Real and virtual positions are required to save a correction.")
            return None

        timestamp = datetime.now().strftime("%m.%d.%Y_%H.%M.%S")

        # Check filepath permissions
        current_filepath = "\\".join(list(self._path.readback.split("\\")[0:-1]))
        if not self._ie_model.is_writable(current_filepath):
            MsgBox(msg="Insufficient directory permission.")
            return None

        filepath = os.path.join(current_filepath, "Corrections")

        if not os.path.exists(filepath):
            os.mkdir(filepath)

        filename = os.path.join(filepath, f"correction_{timestamp}.txt")

        self._ie_model.save_correction(
            filename=filename,
            virtual_position=virtual_position,
            real_position=real_position,
            timestamp=timestamp,
        )

    def _btn_save_as_clicked(self) -> None:
        try:
            virtual_position = float(self._lne_virtual_position.text())
            real_position = float(self._lne_real_position.text())
        except ValueError:
            MsgBox(msg="Real and virtual positions are required to save a correction.")
            return None

        timestamp = datetime.now().strftime("%m.%d.%Y_%H.%M.%S")
        options = QFileDialog.Options()

        # Check filepath permissions
        filepath = "\\".join(list(self._path.readback.split("\\")[0:-1]))
        if not self._ie_model.is_writable(filepath):
            MsgBox(msg="Insufficient directory permission.")
            return None

        filename, _ = QFileDialog.getSaveFileName(
            parent=self._widget,
            caption="Save File",
            directory=filepath,
            filter="Text File (*.txt)",
            options=options,
        )

        if filename:
            self._ie_model.save_correction(
                filename=filename,
                virtual_position=virtual_position,
                real_position=real_position,
                timestamp=timestamp,
            )
        else:
            return None

    def _btn_load_clicked(self) -> None:

        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFile)

        filepath = os.path.join(
            "\\".join(list(self._path.readback.split("\\")[0:-1])), "Corrections"
        )
        options = QFileDialog.Options()

        filename, _ = QFileDialog.getOpenFileName(
            parent=self._widget,
            caption="Open file",
            directory=filepath,
            filter="Text File (*.txt)",
            options=options,
        )

        if filename:

            with open(filename, "r") as correction_file:

                vertical_position: float
                horizontal_position: float
                virtual_position: float
                real_position: float
                objective_focus: float

                for line in correction_file.readlines():

                    if not line.startswith("#"):
                        if line.startswith("vertical"):
                            vertical_position = float(line.split("=")[1].strip())
                        if line.startswith("horizontal"):
                            horizontal_position = float(line.split("=")[1].strip())
                        if line.startswith("real"):
                            real_position = float(line.split("=")[1].strip())
                        if line.startswith("objective_focus"):
                            objective_focus = float(line.split("=")[1].strip())

                if (
                    vertical_position is not None
                    and horizontal_position is not None
                    and real_position is not None
                    and objective_focus is not None
                ):

                    # Check mirrors
                    if self._us_mirror.moving or self._ds_mirror.moving:
                        MsgBox(msg="Wait until the mirrors stop moving.")
                        return None

                    if (
                        round(self._us_mirror.readback) < self._us_mirror_out
                        or round(self._ds_mirror.readback) < self._ds_mirror_out
                    ):
                        MsgBox(msg="First move the mirrors out.")
                        return None

                    # Check pinhole
                    if self._pinhole_stage.moving:
                        MsgBox(msg="Wait for the pinhole to stop moving.")
                        return None

                    if self._pinhole_stage.readback > self._pinhole_limit:
                        MsgBox(
                            msg="First move the PINHOLE to the -20 or OUT position."
                        )
                        return None

                    if self._omega_stage.moving:
                        MsgBox(msg=f"Wait for omega to stop moving.")
                        return None

                    if self._omega_stage.readback != self._omega_limit:
                        MsgBox(
                            msg=f"First, move omega at {self._omega_limit} deg."
                        )
                        return None

                    user_response = QMessageBox.question(
                        self._widget, "Move confirmation",
                        f"Are you sure you want to move to the following positions?\n"
                        f"Vertical: {vertical_position}\n"
                        f"Horizontal: {horizontal_position}\n"
                        f"Focus: {real_position}\n"
                        f"Objective focus: {objective_focus}"
                    )

                    if user_response == QMessageBox.Yes:
                        self._ie_model.load_position(
                            vertical_pos=vertical_position,
                            horizontal_pos=horizontal_position,
                            real_pos=real_position,
                            objective_focus=objective_focus,
                        )
                else:
                    MsgBox(
                        msg="Loading the file failed. Please make sure that the file format is correct."
                    )

    def current_path_changed(self, path: str) -> None:
        """Updates the label text for the target directory."""
        self._widget.lbl_path.setText(path)

    def update_correction_position(self) -> None:
        """Updates the US and DS mirror focus moving status."""
        if self._epics.connected:

            if self._xps_stop.moving:
                self._xps_stop.moving = False

            if self._station_stop.moving:
                self._station_stop.moving = False

            if self._us_mirror.moving:
                self._us_mirror.moving = False

            if self._ds_mirror.moving:
                self._ds_mirror.moving = False

            custom_path = os.path.join(
                "\\".join(list(self._path.readback.split("\\")[0:-1]))
            )

            if custom_path != self._latest_path:
                self._latest_path = custom_path

                self._path_changed.emit(self._latest_path)

                time.sleep(1)
