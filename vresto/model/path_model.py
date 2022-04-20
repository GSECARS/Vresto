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
from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class PathModel:
    _assets_path: str = field(init=False, compare=False, repr=False)
    _qss_path: str = field(init=False, compare=False, repr=False)
    _icon_path: str = field(init=False, compare=False, repr=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "_assets_path", os.path.join(os.getcwd(), "vresto/assets"))
        object.__setattr__(self, "_qss_path", os.path.join(self._assets_path, "qss"))
        object.__setattr__(self, "_icon_path", os.path.join(self._assets_path, "icons"))

    @property
    def qss_path(self) -> str:
        return self._qss_path

    @property
    def icon_path(self) -> str:
        return self._icon_path
