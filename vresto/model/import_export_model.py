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
import errno
from dataclasses import dataclass, field

from vresto.model import DoubleValuePV


@dataclass(frozen=True)
class ImportExportModel:

    vertical: DoubleValuePV = field(init=True, compare=False, repr=False)
    horizontal: DoubleValuePV = field(init=True, compare=False, repr=False)
    focus: DoubleValuePV = field(init=True, compare=False, repr=False)
    microscope_focus: DoubleValuePV = field(init=True, compare=False, repr=False)

    def save_correction(
        self,
        filename: str,
        real_position: float,
        virtual_position: float,
        timestamp: str,
    ) -> None:
        """Saves the correction positions to a .txt file."""

        # BMD Position
        vertical_position = self.vertical.readback
        horizontal_position = self.horizontal.readback

        with open(filename, "w") as correction_file:

            timestamp = timestamp.split("_")

            correction_file.write(
                f"# Vresto\n"
                f"# Automatically generated correction file, {timestamp[0]} {timestamp[1]}\n"
                f"\n"
                f"Hutch=13BMD\n\n"
                f"# Below are the relative positions of the vertical, horizontal, virtual\n"
                f"# focus and real focus positions.\n"
                f"vertical={vertical_position}\n"
                f"horizontal={horizontal_position}\n"
                f"virtual={virtual_position}\n"
                f"real={real_position}\n"
                f"objective_focus={(virtual_position - real_position) * -1}"
                f"\n"
            )

    def load_position(
        self, vertical_pos: float, horizontal_pos: float, real_pos: float, objective_focus: float
    ) -> None:
        self.vertical.move(value=vertical_pos)
        self.horizontal.move(value=horizontal_pos)
        self.focus.move(value=real_pos)
        self.microscope_focus.move(value=objective_focus)

    @staticmethod
    def is_writable(filepath: str) -> bool:
        """Checks if there are sufficient permission to write to the specified directory."""
        filepath += "\\permissions.txt"
        try:
            with open(filepath, "w") as permissions_file:
                permissions_file.write("Write test")
            os.remove(filepath)
        except OSError as error:
            if error.errno == errno.EACCES:
                return False
        return True
