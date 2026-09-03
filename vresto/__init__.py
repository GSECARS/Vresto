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

import sys
from importlib.metadata import PackageNotFoundError, version


def _get_version() -> str:
    try:
        return version("vresto")
    except PackageNotFoundError:
        return "dev"


def main():
    import argparse
    import os

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--no-epics", action="store_true")
    args, remaining = parser.parse_known_args()

    if args.no_epics:
        os.environ["VRESTO_NO_EPICS"] = "1"
        sys.argv = [sys.argv[0]] + remaining

    from vresto.controller import MainController
    MainController().run(version=_get_version())
