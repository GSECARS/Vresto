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

from vresto.model import DoubleValuePV, EpicsModel
from vresto.widget.groups import ZeroExpertGroup


class ZeroExpertGroupController(QObject):

    def __init__(
        self,
        widget: ZeroExpertGroup,
        epics_model: EpicsModel,
        microscope: DoubleValuePV,
        sample_horizontal: DoubleValuePV,
        sample_vertical: DoubleValuePV,
        sample_focus: DoubleValuePV,
        pinhole_horizontal: DoubleValuePV,
        pinhole_vertical: DoubleValuePV,
    ):
        super(ZeroExpertGroupController, self).__init__()

        self._widget = widget
        self._epics = epics_model

        self._microscope = microscope

        self._sample_horizontal = sample_horizontal
        self._sample_vertical = sample_vertical
        self._sample_focus = sample_focus

        self._pinhole_horizontal = pinhole_horizontal
        self._pinhole_vertical = pinhole_vertical

        self._connect_zero_widgets()

    def _connect_zero_widgets(self) -> None:
        self._widget.btn_stage.clicked.connect(self._zero_stage)
        self._widget.btn_microscope_z.clicked.connect(lambda: self._zero_single_stage(stage=self._microscope))
        self._widget.btn_pinhole_horizontal.clicked.connect(
            lambda: self._zero_single_stage(stage=self._pinhole_horizontal)
        )
        self._widget.btn_pinhole_vertical.clicked.connect(
            lambda: self._zero_single_stage(stage=self._pinhole_vertical)
        )

    def _zero_stage(self) -> None:
        self._zero_single_stage(stage=self._sample_horizontal)
        self._zero_single_stage(stage=self._sample_vertical)
        self._zero_single_stage(stage=self._sample_focus)

    @staticmethod
    def _zero_single_stage(stage: DoubleValuePV) -> None:
        stage.set_as_offset()
