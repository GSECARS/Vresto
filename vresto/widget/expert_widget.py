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
from qtpy.QtWidgets import QWidget, QGridLayout

from vresto.widget.groups import (
    CommonControlsExpertGroup,
    PinholeExpertGroup,
    MicroscopeExpertGroup,
    MirrorExpertGroup,
    SampleExpertGroup,
    ZeroExpertGroup,
    SavedPositionsExpertGroup,
)
from vresto.model import PathModel


class ExpertWidget(QWidget):
    """Creates an instance of the alignment widget."""

    def __init__(
        self,
        paths: PathModel,
        common_control_expert_group: CommonControlsExpertGroup,
        pinhole_expert_group: PinholeExpertGroup,
        microscope_expert_group: MicroscopeExpertGroup,
        mirror_expert_group: MirrorExpertGroup,
        sample_expert_group: SampleExpertGroup,
        zero_expert_group: ZeroExpertGroup,
        saved_positions_expert_group: SavedPositionsExpertGroup,
    ) -> None:
        super(ExpertWidget, self).__init__()

        self._paths = paths
        self.common_control_expert_widget = common_control_expert_group
        self.pinhole_expert_widget = pinhole_expert_group
        self.microscope_expert_widget = microscope_expert_group
        self.mirror_expert_widget = mirror_expert_group
        self.sample_expert_widget = sample_expert_group
        self.zero_expert_widget = zero_expert_group
        self.saved_positions_expert_widget = saved_positions_expert_group

        self._configure_expert_widget()
        self._layout_expert_widget()

    def _configure_expert_widget(self) -> None:
        # Load expert qss
        self.setStyleSheet(
            open(os.path.join(self._paths.qss_path, "expert.qss"), "r").read()
        )

    def _layout_expert_widget(self) -> None:
        """Creates the layout for the expert widget."""
        # Add widgets to layout
        layout = QGridLayout()
        layout.addWidget(self.common_control_expert_widget, 0, 0, 1, 4)
        layout.addWidget(self.pinhole_expert_widget, 1, 0, 1, 1)
        layout.addWidget(self.microscope_expert_widget, 1, 1, 1, 3)
        layout.addWidget(self.mirror_expert_widget, 2, 0, 1, 1)
        layout.addWidget(self.sample_expert_widget, 2, 1, 1, 3)
        layout.addWidget(self.zero_expert_widget, 3, 0, 1, 4)
        layout.addWidget(self.saved_positions_expert_widget, 4, 0, 1, 4)

        # Set the layout
        self.setLayout(layout)