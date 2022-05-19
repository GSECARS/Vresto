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

from dataclasses import dataclass, field
from qtpy.QtCore import QSettings


@dataclass(frozen=False, slots=True)
class PasswordModel:

    settings: QSettings = field(init=True, repr=False, compare=False)

    _password: str = field(init=False, repr=False, compare=False, default="password")

    def __post_init__(self):
        object.__setattr__(self, "_password", self._read_password_value(target="password"))

    def _read_password_value(self, target: str) -> None:
        saved_value = self.settings.value(target, type=str)
        if saved_value == "":
            saved_value = "password"
        return saved_value

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, value):
        if isinstance(value, str):
            print("HERE")
            object.__setattr__(self, "_password", value)
            self.settings.setValue("password", self._password)
