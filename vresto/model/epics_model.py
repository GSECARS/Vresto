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
    pinhole = "13BMC:m73"
    pinhole_vertical = "13BMC:m72"
    pinhole_horizontal = "13BMC:m71"

    sample_horizontal = "13BMC:m46"
    sample_focus = "13BMC:m44"
    sample_vertical = "13BMC:m45"
    sample_omega = "13BMC:m33"

    microscope = "13BMC:m77"
    microscope_zoom = "13BMC:m74"
    microscope_light = "13BMC:USB3104:Ao2"
    microscope_gain = "13BMCPG2:cam1:Gain"

    station_stop = "13BMC:allstop"  # 0: Release, 1: Stop
    xps_stop = "13BMC_GPD_XPS:allstop"  # 0: Release, 1: Stop

    path = "13BMCLF1:cam1:FilePath"


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
