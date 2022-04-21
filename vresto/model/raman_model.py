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
from typing import List, Optional

from vresto.model import PVModel, DoubleValuePV, StringValuePV, EpicsConfig


@dataclass(frozen=True)
class RamanModel:

    sample_horizontal: DoubleValuePV = field(init=False, repr=False, compare=False)
    sample_focus: DoubleValuePV = field(init=False, repr=False, compare=False)
    sample_vertical: DoubleValuePV = field(init=False, repr=False, compare=False)
    camera: DoubleValuePV = field(init=False, repr=False, compare=False)
    transmitted_switch: DoubleValuePV = field(init=False, repr=False, compare=False)
    shutter_switch_1: DoubleValuePV = field(init=False, repr=False, compare=False)
    shutter_switch_3: DoubleValuePV = field(init=False, repr=False, compare=False)
    shutter_switch_4: DoubleValuePV = field(init=False, repr=False, compare=False)
    light_reflected: DoubleValuePV = field(init=False, repr=False, compare=False)
    light_transmitted: DoubleValuePV = field(init=False, repr=False, compare=False)
    station_stop: DoubleValuePV = field(init=False, repr=False, compare=False)
    path: StringValuePV = field(init=False, repr=False, compare=False)

    collection: List[PVModel] = field(
        init=False, repr=False, compare=False, default_factory=lambda: []
    )

    def __post_init__(self) -> None:
        self._set_stages()

    def _add_pv(
        self,
        pv_name: str,
        movable: bool,
        limited: bool,
        rbv_extension: bool,
        monitor: bool,
        as_string: Optional[bool] = False,
    ) -> None:

        name = pv_name
        if "_" in name:
            name.replace("_", " ")

        if as_string:
            pv_type = StringValuePV
        else:
            pv_type = DoubleValuePV

        object.__setattr__(
            self,
            pv_name,
            pv_type(
                name=name,
                pv=EpicsConfig[pv_name].value,
                movable=movable,
                limited=limited,
                rbv_extension=rbv_extension,
                monitor=monitor,
            ),
        )
        self.collection.append(getattr(self, pv_name))

    def _set_stages(self) -> None:
        self._add_pv(
            pv_name="sample_horizontal",
            movable=True,
            limited=True,
            rbv_extension=True,
            monitor=True,
        )
        self._add_pv(
            pv_name="sample_focus",
            movable=True,
            limited=True,
            rbv_extension=True,
            monitor=True,
        )
        self._add_pv(
            pv_name="sample_vertical",
            movable=True,
            limited=True,
            rbv_extension=True,
            monitor=True,
        )
        self._add_pv(
            pv_name="camera",
            movable=True,
            limited=False,
            rbv_extension=False,
            monitor=True,
        )
        self._add_pv(
            pv_name="transmitted_switch",
            movable=True,
            limited=False,
            rbv_extension=False,
            monitor=True,
        )
        self._add_pv(
            pv_name="shutter_switch_1",
            movable=True,
            limited=False,
            rbv_extension=False,
            monitor=True,
        )
        self._add_pv(
            pv_name="shutter_switch_3",
            movable=True,
            limited=False,
            rbv_extension=False,
            monitor=True,
        )
        self._add_pv(
            pv_name="shutter_switch_4",
            movable=True,
            limited=False,
            rbv_extension=False,
            monitor=True,
        )
        self._add_pv(
            pv_name="light_reflected",
            movable=True,
            limited=False,
            rbv_extension=False,
            monitor=True,
        )
        self._add_pv(
            pv_name="light_transmitted",
            movable=True,
            limited=False,
            rbv_extension=False,
            monitor=True,
        )
        self._add_pv(
            pv_name="station_stop",
            movable=True,
            limited=False,
            rbv_extension=False,
            monitor=False,
        )
        self._add_pv(
            pv_name="path",
            movable=False,
            limited=False,
            rbv_extension=False,
            monitor=True,
            as_string=True,
        )
