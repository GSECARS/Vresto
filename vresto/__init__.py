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


def _win_local_icon(src: str) -> str:
    """Copy the .ico to %PROGRAMDATA%\\Vresto so Windows can find it before network shares mount."""
    import os
    import shutil
    dest_dir = os.path.join(os.environ.get("PROGRAMDATA", r"C:\ProgramData"), "Vresto")
    try:
        os.makedirs(dest_dir, exist_ok=True)
        dest = os.path.join(dest_dir, "diamond.ico")
        shutil.copy2(src, dest)
        return dest
    except OSError:
        return src


def main():
    import argparse
    import os

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--no-epics", action="store_true")
    parser.add_argument("--make-icon", "-m", action="store_true")
    args, remaining = parser.parse_known_args()

    if args.make_icon:
        from pathlib import Path
        from pyshortcuts import make_shortcut
        icons_dir = Path(__file__).parent / "assets" / "icons"
        if sys.platform == "darwin":
            icon = str(icons_dir / "diamond.icns")
        elif sys.platform == "win32":
            icon = _win_local_icon(str(icons_dir / "diamond.ico"))
        else:
            icon = str(icons_dir / "diamond.png")
        make_shortcut(sys.argv[0], name="Vresto", icon=icon, terminal=False)
        return

    if args.no_epics:
        os.environ["VRESTO_NO_EPICS"] = "1"
        sys.argv = [sys.argv[0]] + remaining

    from vresto.controller import MainController
    MainController().run(version=_get_version())
