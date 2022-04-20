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
from vresto.model import MainModel, QtWorkerModel, IDDModel, ImportExportModel
from vresto.controller.groups import (
    PinholeGroupController,
    MicroscopeGroupController,
    CommonControlsGroupController,
    DiamondImagesGroupController,
    CorrectionsGroupController,
    MirrorGroupController,
    SampleGroupController,
)


class MainController(QObject):
    """Base controller, initializes sub-controllers, creates and run main app worker and checks for epics connection."""

    _epics_connection_changed: Signal = Signal(bool)

    def __init__(self) -> None:
        super(MainController, self).__init__()

        self._app = QApplication(sys.argv)
        self._model = MainModel()
        self._idd = IDDModel()
        self._import_export = ImportExportModel(
            vertical=self._idd.sample_vertical,
            horizontal=self._idd.sample_horizontal,
            focus=self._idd.sample_focus,
            us_mirror_focus=self._idd.us_mirror_focus,
            ds_mirror_focus=self._idd.ds_mirror_focus
        )
        self._widget = MainWidget(self._model.paths)

        # Init controller groups
        self.pinhole_group = PinholeGroupController(
            widget=self._widget.pinhole_widget,
            epics_model=self._model.epics,
            pinhole_stage=self._idd.pinhole,
            omega_stage=self._idd.sample_omega,
            us_mirror=self._idd.us_mirror,
        )

        self.microscope_group = MicroscopeGroupController(
            widget=self._widget.microscope_widget,
            epics_model=self._model.epics,
            microscope_stage=self._idd.microscope,
            microscope_zoom=self._idd.microscope_zoom,
            light_reflected=self._idd.microscope_light,
            sample_omega_stage=self._idd.sample_omega,
        )

        self.common_controls_group = CommonControlsGroupController(
            widget=self._widget.common_controls_widget,
            corrections_model=self._model.corrections,
            epics_model=self._model.epics,
            ie_model=self._import_export,
            path=self._idd.path,
            lne_virtual_position=self._widget.diamond_images_widget.lne_virtual_position,
            lne_real_position=self._widget.diamond_images_widget.lne_real_position,
            us_mirror=self._idd.us_mirror,
            ds_mirror=self._idd.ds_mirror,
            microscope_stage=self._idd.microscope,
            pinhole_stage=self._idd.pinhole,
            omega_stage=self._idd.sample_omega,
            xps_stop=self._idd.xps_stop,
            station_stop=self._idd.station_stop,
            mirror_stop=self._idd.mirror_stop,
        )

        self.diamond_images_group = DiamondImagesGroupController(
            widget=self._widget.diamond_images_widget,
            epics_model=self._model.epics,
            sample_focus_stage=self._idd.sample_focus,
            omega_stage=self._idd.sample_omega,
            check_focus_sample=self._widget.corrections_widget.check_focus_sample,
            check_focus_diamond=self._widget.corrections_widget.check_focus_diamond_table,
            check_focus_thickness=self._widget.corrections_widget.check_diamond_thickness,
        )

        self.corrections_group = CorrectionsGroupController(
            widget=self._widget.corrections_widget,
            corrections_model=self._model.corrections,
            epics_model=self._model.epics,
            btn_reset=self._widget.common_controls_widget.btn_reset,
            check_c_mirrors=self._widget.common_controls_widget.check_c_mirrors,
            lne_virtual_position=self._widget.diamond_images_widget.lne_virtual_position,
            lne_diamond_table=self._widget.diamond_images_widget.lne_diamond_table,
            lne_real_position=self._widget.diamond_images_widget.lne_real_position,
            cmb_refraction_index=self._widget.common_controls_widget.cmb_refraction_index,
            sample_focus_stage=self._idd.sample_focus,
            us_mirror_focus=self._idd.us_mirror_focus,
            ds_mirror_focus=self._idd.ds_mirror_focus,
            microscope_zoom=self._idd.microscope_zoom,
            stacked_img_widget=self._widget.diamond_images_widget.stacked_images,
        )

        self.mirror_group = MirrorGroupController(
            widget=self._widget.mirror_widget,
            epics_model=self._model.epics,
            us_mirror=self._idd.us_mirror,
            ds_mirror=self._idd.ds_mirror,
            omega_stage=self._idd.sample_omega,
            pinhole_stage=self._idd.pinhole,
        )

        self.sample_group = SampleGroupController(
            widget=self._widget.sample_widget,
            epics_model=self._model.epics,
            sample_vertical_stage=self._idd.sample_vertical,
            sample_horizontal_stage=self._idd.sample_horizontal,
            sample_focus_stage=self._idd.sample_focus,
            sample_omega_stage=self._idd.sample_omega,
            us_mirror=self._idd.us_mirror,
            ds_mirror=self._idd.ds_mirror,
            microscope=self._idd.microscope,
            reflected_light=self._idd.microscope_light,
            pinhole=self._idd.pinhole,
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
            self.pinhole_group.update_pinhole_position()
            self.microscope_group.update_microscope_positions()
            self.common_controls_group.update_correction_position()
            self.diamond_images_group.update_diamond_image_widgets()
            self.corrections_group.update_correction_position()
            self.mirror_group.update_mirror_positions()
            self.sample_group.update_sample_positions()
            time.sleep(0.05)

        # Clear camonitor instances after exiting the loop
        for pv in self._idd.collection:
            pv.moving = False
            del pv

        # Set as finished so UI can exit
        self._widget.worker_finished = True
