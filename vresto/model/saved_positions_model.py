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

from typing import List
from dataclasses import dataclass, field
from qtpy.QtCore import QSettings


@dataclass(frozen=False, slots=True)
class SavedPositionsModel:
    """Dataclass that hold of the saved values for the expert tab."""

    settings: QSettings = field(init=True, repr=False, compare=False)

    _pt_foil: str = field(init=False, repr=False, compare=False, default="0, 0, 0")
    _thick_pt: str = field(init=False, repr=False, compare=False, default="0, 0, 0")
    _lab6: str = field(init=False, repr=False, compare=False, default="0, 0, 0")
    _ceo2: str = field(init=False, repr=False, compare=False, default="0, 0, 0")
    _enstatite_au: str = field(init=False, repr=False, compare=False, default="0, 0, 0")
    _p_plate: str = field(init=False, repr=False, compare=False, default="0, 0, 0")
    _position_1: str = field(init=False, repr=False, compare=False, default="0, 0, 0")
    _position_2: str = field(init=False, repr=False, compare=False, default="0, 0, 0")

    def __post_init__(self) -> None:
        object.__setattr__(self, "_pt_foil", self._read_saved_value("pt_foil"))
        object.__setattr__(self, "_thick_pt", self._read_saved_value("thick_pt"))
        object.__setattr__(self, "_lab6", self._read_saved_value("lab6"))
        object.__setattr__(self, "_ceo2", self._read_saved_value("ceo2"))
        object.__setattr__(self, "_enstatite_au", self._read_saved_value("enstatite_au"))
        object.__setattr__(self, "_p_plate", self._read_saved_value("p_plate"))
        object.__setattr__(self, "_position_1", self._read_saved_value("position_1"))
        object.__setattr__(self, "_position_2", self._read_saved_value("position_2"))

    def _read_saved_value(self, target_value: str) -> str:
        saved_value = self.settings.value(target_value, type=str)
        if saved_value == "":
            saved_value = "0, 0, 0"
        return saved_value

    @staticmethod
    def _get_list_of_positions(positions: str) -> List[float]:
        positions = positions.split(",")
        return list(map(float, positions))

    @property
    def pt_foil(self) -> List[float]:
        return self._get_list_of_positions(self._pt_foil)

    @property
    def thick_pt(self) -> List[float]:
        return self._get_list_of_positions(self._thick_pt)

    @property
    def lab6(self) -> List[float]:
        return self._get_list_of_positions(self._lab6)

    @property
    def ceo2(self) -> List[float]:
        return self._get_list_of_positions(self._ceo2)

    @property
    def enstatite_au(self) -> List[float]:
        return self._get_list_of_positions(self._enstatite_au)

    @property
    def p_plate(self) -> List[float]:
        return self._get_list_of_positions(self._p_plate)

    @property
    def position_1(self) -> List[float]:
        return self._get_list_of_positions(self._position_1)

    @property
    def position_2(self) -> List[float]:
        return self._get_list_of_positions(self._position_2)

    @pt_foil.setter
    def pt_foil(self, value) -> None:
        if isinstance(value, float):
            object.__setattr__(self, "_pt_foil", value)
            self.settings.setValue("pt_foil", self._pt_foil)

    @thick_pt.setter
    def thick_pt(self, value) -> None:
        if isinstance(value, str):
            object.__setattr__(self, "_thick_pt", value)
            self.settings.setValue("thick_pt", self._thick_pt)

    @lab6.setter
    def lab6(self, value) -> None:
        if isinstance(value, str):
            object.__setattr__(self, "_lab6", value)
            self.settings.setValue("lab6", self._lab6)

    @ceo2.setter
    def ceo2(self, value) -> None:
        if isinstance(value, str):
            object.__setattr__(self, "_ceo2", value)
            self.settings.setValue("ceo2", self._ceo2)

    @enstatite_au.setter
    def enstatite_au(self, value) -> None:
        if isinstance(value, str):
            object.__setattr__(self, "_enstatite_au", value)
            self.settings.setValue("enstatite_au", self._enstatite_au)

    @p_plate.setter
    def p_plate(self, value) -> None:
        if isinstance(value, str):
            object.__setattr__(self, "_p_plate", value)
            self.settings.setValue("p_plate", self._p_plate)

    @position_1.setter
    def position_1(self, value) -> None:
        if isinstance(value, str):
            object.__setattr__(self, "_position_1", value)
            self.settings.setValue("position_1", self._position_1)

    @position_2.setter
    def position_2(self, value) -> None:
        if isinstance(value, str):
            object.__setattr__(self, "_position_2", value)
            self.settings.setValue("position_2", self._position_2)
