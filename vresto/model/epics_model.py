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
    sample_horizontal = "13RAMAN2:m1"
    sample_focus = "13RAMAN2:m3"
    sample_vertical = "13RAMAN2:m2"

    camera = "rpi_4:Switch11"

    light_reflected = "rpi_dac:Chan0Volt"
    light_transmitted = "rpi_dac:Chan2Volt"
    transmitted_switch = "rpi_4:Switch13"

    shutter_switch_1 = "rpi_4:Switch01"
    shutter_switch_3 = "rpi_4:Switch03"
    shutter_switch_4 = "rpi_4:Switch04"

    station_stop = "13RAMAN2:allstop"

    path = "13RamanLF1:cam1:FilePath"


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
