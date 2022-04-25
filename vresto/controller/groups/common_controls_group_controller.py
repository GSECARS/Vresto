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
from qtpy.QtWidgets import QFileDialog, QLineEdit

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
        self._station_stop = station_stop

        self.correction_aborted = False
        self._latest_path: str = "Unknown"

        self._connect_common_control_widgets()

    def _connect_common_control_widgets(self) -> None:
        self._widget.btn_stop_all.clicked.connect(self._btn_stop_all_clicked)
        self._widget.btn_save.clicked.connect(self._btn_save_clicked)
        self._widget.btn_save_as.clicked.connect(self._btn_save_as_clicked)
        self._widget.btn_load_correction.clicked.connect(self._btn_load_clicked)

        self._path_changed.connect(self.current_path_changed)

    def _btn_stop_all_clicked(self) -> None:
        self._widget.btn_stop_all.clearFocus()
        self._corrections.abort_status = True
        self._station_stop.move(value=1)

    def _btn_save_clicked(self) -> None:
        try:
            virtual_position = float(self._lne_virtual_position.text())
            real_position = float(self._lne_real_position.text())
        except ValueError:
            MsgBox(msg="Real and virtual positions are required to save a correction.")
            return None

        timestamp = datetime.now().strftime("%m.%d.%Y_%H.%M.%S")

        # Check filepath permissions
        current_filepath = "\\".join(list(self._path.readback.split("\\")[0:-2]))
        if not self._ie_model.is_writable(current_filepath):
            MsgBox(msg="Unsufficient directory permission.")
            return None

        filepath = os.path.join(current_filepath, "Corrections")

        if not os.path.exists(filepath):
            os.mkdir(filepath)

        filename = os.path.join(filepath, f"correction_{timestamp}.cor")

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
        filepath = "\\".join(list(self._path.readback.split("\\")[0:-2]))
        if not self._ie_model.is_writable(current_filepath):
            MsgBox(msg="Unsufficient directory permission.")
            return None

        filename, _ = QFileDialog.getSaveFileName(
            parent=self._widget,
            caption="Save File",
            directory=filepath,
            filter="Correction File (*.cor)",
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
            "\\".join(list(self._path.readback.split("\\")[0:-2])), "Corrections"
        )
        options = QFileDialog.Options()

        filename, _ = QFileDialog.getOpenFileName(
            parent=self._widget,
            caption="Open file",
            directory=filepath,
            filter="Correction File (*.cor)",
            options=options,
        )

        if filename:

            with open(filename, "r") as correction_file:

                vertical_position: float
                horizontal_position: float
                virtual_position: float

                for line in correction_file.readlines():

                    if not line.startswith("#"):
                        if line.startswith("vertical"):
                            vertical_position = float(line.split("=")[1].strip())
                        if line.startswith("horizontal"):
                            horizontal_position = float(line.split("=")[1].strip())
                        if line.startswith("virtual"):
                            virtual_position = float(line.split("=")[1].strip())

                if (
                    vertical_position is not None
                    and horizontal_position is not None
                    and virtual_position is not None
                ):
                    self._ie_model.load_position(
                        vertical_pos=vertical_position,
                        horizontal_pos=horizontal_position,
                        virtual_position=virtual_position,
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

            if self._station_stop.moving:
                self._station_stop.moving = False

            custom_path = os.path.join(
                "\\".join(list(self._path.readback.split("\\")[0:-2]))
            )

            if custom_path != self._latest_path:
                self._latest_path = custom_path

                self._path_changed.emit(self._latest_path)

                time.sleep(1)
