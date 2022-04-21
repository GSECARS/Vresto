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

import sys
import time
from qtpy.QtWidgets import QApplication
from qtpy.QtCore import QObject, Signal

from vresto.widget import MainWidget
from vresto.model import MainModel, QtWorkerModel, RamanModel, ImportExportModel
from vresto.controller.groups import (
    CorrectionsGroupController,
    CommonControlsGroupController,
    DiamondImagesGroupController,
    CameraGroupController,
    SampleGroupController,
)


class MainController(QObject):
    """Base controller, initializes sub-controllers, creates and run main app worker and checks for epics connection."""

    _epics_connection_changed: Signal = Signal(bool)

    def __init__(self) -> None:
        super(MainController, self).__init__()

        self._app = QApplication(sys.argv)
        self._model = MainModel()
        self._raman = RamanModel()
        self._import_export = ImportExportModel(
            vertical=self._raman.sample_vertical,
            horizontal=self._raman.sample_horizontal,
            focus=self._raman.sample_focus,
        )
        self._widget = MainWidget(self._model.paths)

        # Init controller groups
        self.corrections_group = CorrectionsGroupController(
            widget=self._widget.corrections_widget,
            corrections_model=self._model.corrections,
            epics_model=self._model.epics,
            btn_reset=self._widget.common_controls_widget.btn_reset,
            lne_virtual_position=self._widget.diamond_images_widget.lne_virtual_position,
            lne_diamond_table=self._widget.diamond_images_widget.lne_diamond_table,
            lne_real_position=self._widget.diamond_images_widget.lne_real_position,
            cmb_refraction_index=self._widget.common_controls_widget.cmb_refraction_index,
            sample_focus_stage=self._raman.sample_focus,
            stacked_img_widget=self._widget.diamond_images_widget.stacked_images,
        )

        self.common_controls_group = CommonControlsGroupController(
            widget=self._widget.common_controls_widget,
            corrections_model=self._model.corrections,
            epics_model=self._model.epics,
            ie_model=self._import_export,
            path=self._raman.path,
            lne_virtual_position=self._widget.diamond_images_widget.lne_virtual_position,
            lne_real_position=self._widget.diamond_images_widget.lne_real_position,
            station_stop=self._raman.station_stop,
        )

        self.diamond_images_group = DiamondImagesGroupController(
            widget=self._widget.diamond_images_widget,
            epics_model=self._model.epics,
            sample_focus_stage=self._raman.sample_focus,
            check_focus_sample=self._widget.corrections_widget.check_focus_sample,
            check_focus_diamond=self._widget.corrections_widget.check_focus_diamond_table,
            check_focus_thickness=self._widget.corrections_widget.check_diamond_thickness,
        )

        self.camera_group = CameraGroupController(
            widget=self._widget.camera_widget,
            epics_model=self._model.epics,
            camera=self._raman.camera,
            reflected=self._raman.light_reflected,
            transmitted=self._raman.light_transmitted,
            transmitted_switch=self._raman.transmitted_switch,
            shutter_switch_1=self._raman.shutter_switch_1,
            shutter_switch_3=self._raman.shutter_switch_3,
            shutter_switch_4=self._raman.shutter_switch_4,
        )

        self.sample_group = SampleGroupController(
            widget=self._widget.sample_widget,
            epics_model=self._model.epics,
            sample_vertical_stage=self._raman.sample_vertical,
            sample_horizontal_stage=self._raman.sample_horizontal,
            sample_focus_stage=self._raman.sample_focus,
        )

        # Event helpers
        self._time_started = None

        # Connect epics connection signal
        self._epics_connection_changed.connect(self._update_epics_status_label)

        # Application thread worker
        self._main_worker = QtWorkerModel(self._worker_methods, ())
        self._main_worker.start()

    def run(self, version: str) -> None:
        """Starts the application."""
        self._widget.display(version=version)
        sys.exit(self._app.exec())

    def _update_epics_status_label(self, status: bool) -> None:
        """Updates the circle status label based on epics connection."""
        self._widget.lbl_epics_status.setEnabled(status)

    def _check_epics_connection(self) -> None:
        """Checks the epics connection every 5 minutes."""
        # Initialize first connection if needed
        if self._time_started is None:
            self._time_started = time.time()
            self._model.epics.connect()
            self._epics_connection_changed.emit(self._model.epics.connected)

        now = time.time()
        # If time difference is more than 5 minutes try epics connect again
        if now - self._time_started > 300:
            self._time_started = time.time()

            self._model.epics.connect()

            # Emit connection changed signal
            self._epics_connection_changed.emit(self._model.epics.connected)

    def _worker_methods(self) -> None:
        """Runs all the worker methods."""

        while not self._widget.terminated:
            self._check_epics_connection()
            self.common_controls_group.update_correction_position()
            self.diamond_images_group.update_diamond_image_widgets()
            self.camera_group.update_camera()
            self.sample_group.update_sample_positions()
            time.sleep(0.05)

        # Set as finished so UI can exit
        self._widget.worker_finished = True
