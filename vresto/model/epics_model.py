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
    pinhole = "13IDD:m22"
    pinhole_vertical = "13IDD:m93"
    pinhole_horizontal = "13IDD:m94"

    sample_horizontal = "13IDD:m81"
    sample_focus = "13IDD:m82"
    sample_vertical = "13IDD:m83"
    sample_omega = "13IDD:m84"

    microscope = "13IDD:m67"
    microscope_vertical = "13IDD:m68"
    microscope_horizontal = "13IDD:m69"
    microscope_zoom = "13IDD:m14"
    microscope_light = "13IDD:DAC2_7"
    microscope_gain = "13IDD_PG3:cam1:Gain"

    us_mirror = "13IDD:m23"
    ds_mirror = "13IDD:m24"
    us_mirror_focus = "13IDD:m65"
    ds_mirror_focus = "13IDD:m66"
    us_light = "13IDD:DAC2_1"
    ds_light = "13IDD:DAC2_2"
    us_light_switch = "13IDD:Unidig1Bo20"
    ds_light_switch = "13IDD:Unidig1Bo22"

    stage_x = "13IDD:m1"

    ds_carbon_horizontal = "13Mirror:m1"
    ds_carbon_vertical = "13Mirror:m2"
    us_carbon_horizontal = "13Mirror:m3"
    us_carbon_vertical = "13Mirror:m4"

    xps_stop = "13IDD_DAC_XPS16:allstop"
    station_stop = "13IDD:allstop"
    mirror_stop = "13Mirror:allstop"

    path = "13IDDLF1:cam1:FilePath"


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
