# -*- mode: python ; coding: utf-8 -*-
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

block_cipher = None

import sys
import os
import epics
from distutils.sysconfig import get_python_lib
from vresto import __version__

root_directory = os.getcwd()

epics_lib = os.path.dirname(epics.__file__)
additional_data = [
    ("vresto\\assets\\icons\\diamond.ico", "."),
    ("vresto\\assets", "vresto\\assets"),
    ("LICENSE", "."),
    (epics_lib, "epics\\")
]

a = Analysis(
    ['vresto.py'],
    pathex=[root_directory],
    binaries=[],
    datas=additional_data,
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='vresto',
    debug=False,
    strip=False,
    upx=True,
    console=False,
    icon='vresto\\assets\\icons\\diamond.ico'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='Vresto_{}'.format(__version__)
)
