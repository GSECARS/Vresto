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


class PasswordFormWidget(QDialog):
    """Creates an instance of the alignment widget."""

    def __init__(
        self,
        paths: PathModel,
    ) -> None:
        super(PasswordFormWidget, self).__init__(flags=Qt.Dialog | Qt.FramelessWindowHint)

        self._paths = paths

        self.lne_old_password = QLineEdit()
        self.lne_new_password = QLineEdit()
        self.lne_repeat_password = QLineEdit()

        self._lbl_old_password = QLabel("Old Password")
        self._lbl_new_password = QLabel("New Password")
        self._lbl_repeat_password = QLabel("Repeat Password")

        self.btn_cancel = QPushButton("CANCEL")
        self.btn_apply = QPushButton("APPLY")

        self._configure_password_form_widgets()
        self._layout_password_form_widgets()

    def _configure_password_form_widgets(self) -> None:
        # Set object names
        self.setObjectName("QDialog")
        self.btn_cancel.setObjectName("password-btn")
        self.btn_apply.setObjectName("password-btn")
        self.lne_old_password.setObjectName("password-lne")
        self.lne_new_password.setObjectName("password-lne")
        self.lne_repeat_password.setObjectName("password-lne")
        self._lbl_old_password.setObjectName("password-lbl")
        self._lbl_new_password.setObjectName("password-lbl")
        self._lbl_repeat_password.setObjectName("password-lbl")

        # Load password form qss
        self.setStyleSheet(
            open(os.path.join(self._paths.qss_path, "password.qss"), "r").read()
        )

        self.lne_old_password.setEchoMode(QLineEdit.Password)
        self.lne_new_password.setEchoMode(QLineEdit.Password)
        self.lne_repeat_password.setEchoMode(QLineEdit.Password)

    def _layout_password_form_widgets(self) -> None:
        """Creates the layout for the password form widgets."""
        layout = QGridLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.addWidget(self._lbl_old_password, 0, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self._lbl_new_password, 1, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self._lbl_repeat_password, 2, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)

        layout.addWidget(self.lne_old_password, 0, 1, 1, 4)
        layout.addWidget(self.lne_new_password, 1, 1, 1, 4)
        layout.addWidget(self.lne_repeat_password, 2, 1, 1, 4)

        layout.addWidget(self.btn_cancel, 3, 2, 1, 1)
        layout.addWidget(self.btn_apply, 3, 3, 1, 1)
        self.setLayout(layout)
