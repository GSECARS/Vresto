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
    CorrectionsGroup,
    CommonControlsGroup,
    DiamondImagesGroup,
    SampleGroup,
)
from vresto.model import PathModel


class AlignmentWidget(QWidget):
    """Creates an instance of the alignment widget."""

    def __init__(
        self,
        paths: PathModel,
        corrections_group: CorrectionsGroup,
        common_controls_group: CommonControlsGroup,
        diamond_images_group: DiamondImagesGroup,
        sample_group: SampleGroup,
    ) -> None:
        super(AlignmentWidget, self).__init__()

        self._paths = paths
        self.corrections_widget = corrections_group
        self.common_controls_widget = common_controls_group
        self.diamond_images_widget = diamond_images_group
        self.sample_widget = sample_group

        self._configure_alignment_widget()
        self._layout_alignment_widget()

    def _configure_alignment_widget(self) -> None:
        # Load alignment qss
        self.setStyleSheet(
            open(os.path.join(self._paths.qss_path, "alignment.qss"), "r").read()
        )

    def _layout_alignment_widget(self) -> None:
        """Creates the layout for the alignment widget."""
        # Add widgets to layout
        layout = QGridLayout()

        layout.addWidget(self.corrections_widget, 2, 0, 1, 1)
        layout.addWidget(self.common_controls_widget, 3, 0, 1, 1)

        layout.addWidget(self.diamond_images_widget, 2, 1, 3, 2)
        layout.addWidget(self.sample_widget, 6, 1, 3, 2)

        # Set the layout
        self.setLayout(layout)
