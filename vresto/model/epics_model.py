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
from enum import Enum
from epics import pv

from vresto.widget.custom import MsgBox


class EpicsConnectionError(Exception):
    """No epics connection exception."""

    def __init__(self, message) -> None:
        super(EpicsConnectionError, self).__init__(message)
        self._message = message

    @property
    def message(self) -> str:
        MsgBox(msg=self._message)
        return f"[EpicsConnectionError] - {self._message}"


class EpicsConfig(Enum):
    """Empty Enum to be populated with PVs"""
    pinhole = "13BMD:m27"

    sample_horizontal = "13BMD:m89"
    sample_focus = "13BMD:m91"
    sample_vertical = "13BMD:m90"
    sample_omega = "13BMD:m92"

    microscope = "13BMD:m23"
    microscope_zoom = "13BMD:m71"
    microscope_light_reflected = "13BMD:DAC1_7"
    microscope_light_transmitted = "13BMD:DAC1_6"

    us_mirror = "13BMD:m65"
    ds_mirror = "13BMD:m68"

    xps_stop = "13BMD_DAC_XPS:allstop"
    station_stop = "13BMD:allstop"

    path = "13BMDLF1:cam1:FilePath"


@dataclass(frozen=False, slots=True)
class EpicsModel:
    """Base epics model, used for testing the connection with all PVs given."""

    _connected: bool = field(init=False, compare=False, repr=False, default=False)

    def connect(self) -> None:
        """Check and set the connection status of all PVs included in the EpicsConfig."""
        if not len(EpicsConfig):
            return None

        for name, member in EpicsConfig.__members__.items():

            if not len(member.value) > 2:
                value = member.value[0]
            else:
                value = member.value

            try:
                pv_check = pv.get_pv(value, connect=True)
                if not pv_check.connected:
                    raise EpicsConnectionError(f"Could not connect {name} ({value})")
            except EpicsConnectionError:
                return None

        object.__setattr__(self, "_connected", True)

    @property
    def connected(self) -> bool:
        return self._connected
