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


class CorrectionsModel:
    """Base correction model. It provides methods to get diamond thickness, position and real position."""

    _diamond_index: float = 2.4195
    _fused_silica_index: float = 1.459
    _moissanite_index: float = 2.67
    _refraction_index: float = _diamond_index

    _abort_status: bool = False

    def get_diamond_thickness(
        self, virtual_position: float, diamond_position: float
    ) -> float:
        """Calculates and returns the diamond thickness."""
        return round((diamond_position - virtual_position) * self._refraction_index, 4)

    def get_diamond_position(
        self, virtual_position: float, diamond_thickness: float
    ) -> float:
        """Calculates and returns the diamond position."""
        diamond_thickness /= self._refraction_index
        return round(virtual_position + diamond_thickness + self._refraction_index, 4)

    @staticmethod
    def get_real_position(diamond_thickness: float, diamond_position: float) -> float:
        """Calculates and returns the real position."""
        return round(diamond_position - diamond_thickness, 4)

    @property
    def refraction_index(self) -> float:
        return self._refraction_index

    @property
    def abort_status(self) -> bool:
        return self._abort_status

    @refraction_index.setter
    def refraction_index(self, value: str) -> None:
        value = value.lower()
        if value == "diamond":
            self._refraction_index = self._diamond_index
        elif value == "fused silica":
            self._refraction_index = self._fused_silica_index
        elif value == "moissanite":
            self._refraction_index = self._moissanite_index

    @abort_status.setter
    def abort_status(self, value: bool) -> None:
        self._abort_status = value
