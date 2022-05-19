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

from qtpy.QtCore import QObject

from vresto.model import (
    CorrectionsModel,
    DoubleValuePV,
    EpicsModel,
)
from vresto.widget.groups import CommonControlsExpertGroup
from vresto.widget import PasswordFormWidget


class CommonControlsExpertGroupController(QObject):

    def __init__(
        self,
        widget: CommonControlsExpertGroup,
        password_widget: PasswordFormWidget,
        corrections_model: CorrectionsModel,
        epics_model: EpicsModel,
        xps_stop: DoubleValuePV,
        station_stop: DoubleValuePV,
        mirror_stop: DoubleValuePV,
    ) -> None:
        super(CommonControlsExpertGroupController, self).__init__()

        self._widget = widget
        self._password_widget = password_widget
        self._corrections = corrections_model
        self._epics = epics_model

        self._xps_stop = xps_stop
        self._station_stop = station_stop
        self._mirror_stop = mirror_stop

        self._connect_common_control_widgets()

    def _connect_common_control_widgets(self) -> None:
        self._widget.btn_stop_all.clicked.connect(self._btn_stop_all_clicked)
        self._widget.btn_change_password.clicked.connect(self._btn_changed_password_clicked)

    def _btn_stop_all_clicked(self) -> None:
        self._widget.btn_stop_all.clearFocus()

        self._corrections.abort_status = True

        self._xps_stop.move(value=1)
        self._station_stop.move(value=1)
        self._mirror_stop.move(value=1)

    def _btn_changed_password_clicked(self) -> None:
        self._password_widget.hide()
        self._password_widget.showNormal()
