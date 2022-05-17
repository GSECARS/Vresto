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

from qtpy.QtCore import QObject, QSettings

from vresto.model import DoubleValuePV, EpicsModel, SavedPositionsModel
from vresto.widget.groups import SampleGroup


class SavedPositionsExpertGroupController(QObject):

    def __init__(
        self,
        widget: SampleGroup,
        settings: QSettings,
        epics_model: EpicsModel,
    ):
        super(SavedPositionsExpertGroupController, self).__init__()

        self._widget = widget
        self._model = SavedPositionsModel(settings=settings)
        self._epics = epics_model

        self._connect_saved_positions_widgets()
        self._load_saved_positions_values()

    def _connect_saved_positions_widgets(self) -> None:
        pass

    def _load_saved_positions_values(self) -> None:
        pass


