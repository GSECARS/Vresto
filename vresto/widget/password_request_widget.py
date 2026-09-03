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
from qtpy.QtWidgets import QDialog, QGridLayout, QLineEdit, QLabel, QPushButton
from qtpy.QtCore import Qt

from vresto.model import PathModel


class PasswordRequestWidget(QDialog):
    """Creates an instance of the alignment widget."""

    def __init__(
        self,
        paths: PathModel,
    ) -> None:
        super(PasswordRequestWidget, self).__init__(flags=Qt.Dialog | Qt.FramelessWindowHint)

        self._paths = paths

        self.lne_password = QLineEdit()
        self._lbl_password = QLabel("Password")

        self.btn_cancel = QPushButton("CANCEL")
        self.btn_apply = QPushButton("APPLY")

        self._configure_password_request_widgets()
        self._layout_password_request_widgets()

    def _configure_password_request_widgets(self) -> None:
        # Set object names
        self.setObjectName("QDialog")
        self.btn_cancel.setObjectName("password-btn")
        self.btn_apply.setObjectName("password-btn")
        self.lne_password.setObjectName("password-lne")
        self._lbl_password.setObjectName("password-lbl")

        # Load password form qss
        self.setStyleSheet(
            open(os.path.join(self._paths.qss_path, "password.qss"), "r").read()
        )

        self.lne_password.setEchoMode(QLineEdit.Password)

    def _layout_password_request_widgets(self) -> None:
        """Creates the layout for the password request widgets."""
        layout = QGridLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.addWidget(self._lbl_password, 0, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.lne_password, 0, 1, 1, 4)

        layout.addWidget(self.btn_cancel, 1, 2, 1, 1)
        layout.addWidget(self.btn_apply, 1, 3, 1, 1)
        self.setLayout(layout)
