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

from qtpy.QtCore import QObject

from vresto.widget import PasswordFormWidget
from vresto.widget.custom import MsgBox
from vresto.model import PasswordModel


class PasswordFormController(QObject):

    def __init__(
        self,
        widget: PasswordFormWidget,
        model: PasswordModel,
    ) -> None:
        super(PasswordFormController, self).__init__()

        self._widget = widget
        self._model = model

        self._connect_password_form_widgets()

    def _connect_password_form_widgets(self) -> None:
        self._widget.btn_apply.clicked.connect(self._btn_apply_clicked)
        self._widget.btn_cancel.clicked.connect(self._btn_cancel_clicked)

    def _clear_password_fields(self) -> None:
        self._widget.lne_old_password.clear()
        self._widget.lne_new_password.clear()
        self._widget.lne_repeat_password.clear()

    def _check_old_password(self) -> bool:
        user_input = self._widget.lne_old_password.text()
        old_password = self._model.settings.value("password", type=str)

        if old_password == "":
            return True

        if user_input == old_password:
            return True

        return False

    def _check_match(self) -> bool:
        password = self._widget.lne_new_password.text()
        password_repeat = self._widget.lne_repeat_password.text()

        if password == password_repeat:
            return True

        return False

    def _btn_apply_clicked(self) -> None:

        if self._widget.lne_old_password.text().strip() == "":
            MsgBox(msg="Old password cannot be empty.")
            self._clear_password_fields()
            return None

        if self._widget.lne_new_password.text().strip() == "":
            MsgBox(msg="New password cannot be empty.")
            return None

        if self._widget.lne_repeat_password.text().strip() == "":
            MsgBox(msg="Password repeat cannot be empty.")
            self._clear_password_fields()
            return None

        if not self._check_old_password():
            MsgBox(msg="Old password is incorrect.")
            self._clear_password_fields()
            return None

        if not self._check_match():
            MsgBox(msg="Passwords do not match, please try again.")
            self._clear_password_fields()
            return None

        self._model.password = self._widget.lne_new_password.text()
        MsgBox(msg="Password changed!")
        self._clear_password_fields()
        self._widget.hide()

    def _btn_cancel_clicked(self) -> None:
        self._clear_password_fields()
        self._widget.hide()
