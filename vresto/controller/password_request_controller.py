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
from qtpy.QtWidgets import QTabWidget

from vresto.widget import PasswordRequestWidget
from vresto.widget.custom import MsgBox
from vresto.model import PasswordModel


class PasswordRequestController(QObject):

    def __init__(
        self,
        widget: PasswordRequestWidget,
        model: PasswordModel,
        tab_widget: QTabWidget,
    ) -> None:
        super(PasswordRequestController, self).__init__()

        self._widget = widget
        self._model = model
        self._tab_widget = tab_widget

        self._connect_password_request_widgets()

    def _connect_password_request_widgets(self) -> None:
        self._tab_widget.currentChanged.connect(self._current_tab_changed)
        self._widget.btn_apply.clicked.connect(self._btn_apply_clicked)
        self._widget.btn_cancel.clicked.connect(self._btn_cancel_clicked)
        self._widget.lne_password.returnPressed.connect(self._lne_password_return_pressed)

    def _current_tab_changed(self) -> None:
        if self._tab_widget.currentIndex() == 1:
            self._tab_widget.setCurrentIndex(0)
            self._widget.show()

    def _btn_apply_clicked(self) -> None:
        self._check_password()

    def _lne_password_return_pressed(self) -> None:
        self._check_password()

    def _check_password(self) -> None:
        if self._widget.lne_password.text().strip() == "":
            MsgBox(msg="Password cannot be empty.")
            self._widget.lne_password.clear()
            return None

        user_input = self._widget.lne_password.text()
        password = self._model.settings.value("password", type=str)

        if password == "":
            password = "password"

        if user_input != password:
            MsgBox(msg="Password is incorrect.")
            self._widget.lne_password.clear()
            return None

        self._tab_widget.currentChanged.disconnect()
        self._tab_widget.setCurrentIndex(1)
        self._tab_widget.currentChanged.connect(self._current_tab_changed)

    def _btn_cancel_clicked(self) -> None:
        self._widget.lne_password.clear()
        self._widget.hide()
