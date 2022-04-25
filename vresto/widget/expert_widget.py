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

from vresto.model import PathModel


class ExpertWidget(QWidget):
    """Creates an instance of the alignment widget."""

    def __init__(
        self,
        paths: PathModel,
    ) -> None:
        super(ExpertWidget, self).__init__()

        self._paths = paths

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

        # Set the layout
        self.setLayout(layout)
