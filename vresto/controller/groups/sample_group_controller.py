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

from typing import Optional
from qtpy.QtCore import QObject, Signal

from vresto.model import DoubleValuePV, EpicsModel, EventFilterModel
from vresto.widget.groups import SampleGroup

from qtpy.QtWidgets import QLineEdit


class SampleGroupController(QObject):
    _vertical_rbv_changed: Signal = Signal(str)
    _horizontal_rbv_changed: Signal = Signal(str)
    _focus_rbv_changed: Signal = Signal(str)

    _step: float
    _step_1: float = 0.1
    _step_2: float = 0.01
    _step_3: float = 0.001

    def __init__(
        self,
        widget: SampleGroup,
        epics_model: EpicsModel,
        sample_vertical_stage: DoubleValuePV,
        sample_horizontal_stage: DoubleValuePV,
        sample_focus_stage: DoubleValuePV,
    ):
        super(SampleGroupController, self).__init__()

        self._widget = widget
        self._epics = epics_model

        self._sample_vertical_stage = sample_vertical_stage
        self._sample_horizontal_stage = sample_horizontal_stage
        self._sample_focus_stage = sample_focus_stage

        self.vertical_filter = EventFilterModel(self._sample_vertical_stage)
        self.horizontal_filter = EventFilterModel(self._sample_horizontal_stage)
        self.focus_filter = EventFilterModel(self._sample_focus_stage)

        self._connect_sample_widgets()
        self._configure_sample_widgets()

    def _connect_sample_widgets(self) -> None:
        # Step buttons
        self._widget.btn_step_1.clicked.connect(
            lambda: self._btn_step_clicked(value=self._step_1)
        )
        self._widget.btn_step_2.clicked.connect(
            lambda: self._btn_step_clicked(value=self._step_2)
        )
        self._widget.btn_step_3.clicked.connect(
            lambda: self._btn_step_clicked(value=self._step_3)
        )

        # Plus/minus buttons
        self._widget.btn_plus_vertical.clicked.connect(
            lambda: self._btn_plus_minus_clicked(
                sample_stage=self._sample_vertical_stage
            )
        )

        self._widget.btn_plus_horizontal.clicked.connect(
            lambda: self._btn_plus_minus_clicked(
                sample_stage=self._sample_horizontal_stage
            )
        )

        self._widget.btn_plus_focus.clicked.connect(
            lambda: self._btn_plus_minus_clicked(sample_stage=self._sample_focus_stage)
        )

        self._widget.btn_minus_vertical.clicked.connect(
            lambda: self._btn_plus_minus_clicked(
                sample_stage=self._sample_vertical_stage, minus=True
            )
        )
        self._widget.btn_minus_horizontal.clicked.connect(
            lambda: self._btn_plus_minus_clicked(
                sample_stage=self._sample_horizontal_stage, minus=True
            )
        )
        self._widget.btn_minus_focus.clicked.connect(
            lambda: self._btn_plus_minus_clicked(
                sample_stage=self._sample_focus_stage, minus=True
            )
        )

        # lne boxes
        self._widget.lne_vertical.returnPressed.connect(
            lambda: self._lne_sample_pressed(
                sample_stage=self._sample_vertical_stage,
                lne_box=self._widget.lne_vertical,
            )
        )
        self._widget.lne_horizontal.returnPressed.connect(
            lambda: self._lne_sample_pressed(
                sample_stage=self._sample_horizontal_stage,
                lne_box=self._widget.lne_horizontal,
            )
        )
        self._widget.lne_focus.returnPressed.connect(
            lambda: self._lne_sample_pressed(
                sample_stage=self._sample_focus_stage,
                lne_box=self._widget.lne_focus,
            )
        )

        self._vertical_rbv_changed.connect(self._update_vertical)
        self._horizontal_rbv_changed.connect(self._update_horizontal)
        self._focus_rbv_changed.connect(self._update_focus)

    def _configure_sample_widgets(self) -> None:
        self._widget.btn_step_1.setText(str(self._step_1))
        self._widget.btn_step_2.setText(str(self._step_2))
        self._widget.btn_step_3.setText(str(self._step_3))

        # Default selection
        self._widget.btn_step_3.setChecked(True)
        self._step = self._step_3

        # Step button status tips
        self._widget.btn_step_1.setStatusTip(f"Sets the step to {self._step_1} mm")
        self._widget.btn_step_2.setStatusTip(f"Sets the step to {self._step_2} mm")
        self._widget.btn_step_3.setStatusTip(f"Sets the step to {self._step_3} mm")

        # Set event filters
        self._widget.lne_vertical.installEventFilter(self.vertical_filter)
        self._widget.lne_horizontal.installEventFilter(self.horizontal_filter)
        self._widget.lne_focus.installEventFilter(self.focus_filter)

    def _btn_step_clicked(self, value: float) -> None:
        if value == self._step_1:
            self._widget.btn_step_1.setChecked(True)
            self._widget.btn_step_2.setChecked(False)
            self._widget.btn_step_3.setChecked(False)
        elif value == self._step_2:
            self._widget.btn_step_1.setChecked(False)
            self._widget.btn_step_2.setChecked(True)
            self._widget.btn_step_3.setChecked(False)
        else:
            self._widget.btn_step_1.setChecked(False)
            self._widget.btn_step_2.setChecked(False)
            self._widget.btn_step_3.setChecked(True)

    def _btn_plus_minus_clicked(
        self,
        sample_stage: DoubleValuePV,
        minus: Optional[bool] = False,
    ) -> None:

        value = sample_stage.readback

        if minus:
            sample_stage.move(value=value - self._step)
        else:
            sample_stage.move(value=value + self._step)

    @staticmethod
    def _lne_sample_pressed(
        sample_stage: DoubleValuePV,
        lne_box: QLineEdit,
    ) -> None:

        if lne_box.text() is not None:
            sample_stage.move(value=float(lne_box.text()))

            lne_box.clearFocus()
        else:
            lne_box.clearFocus()
            return None

    def _update_vertical(self, text: str) -> None:
        if not self._widget.lne_vertical.hasFocus():
            if self._widget.lne_vertical.text() != text:
                self._widget.lne_vertical.setText(text)

    def _update_horizontal(self, text: str) -> None:
        if not self._widget.lne_horizontal.hasFocus():
            if self._widget.lne_horizontal.text() != text:
                self._widget.lne_horizontal.setText(text)

    def _update_focus(self, text: str) -> None:
        if not self._widget.lne_focus.hasFocus():
            if self._widget.lne_focus.text() != text:
                self._widget.lne_focus.setText(text)

    def update_sample_positions(self) -> None:
        """Updates the sample position lne boxes."""
        if self._epics.connected:

            # Sample vertical
            if self._sample_vertical_stage.moving:
                vertical_rbv_str = str(
                    "{0:.4f}".format(self._sample_vertical_stage.readback)
                )
                self._vertical_rbv_changed.emit(vertical_rbv_str)
                self._sample_vertical_stage.moving = False

            # Sample horizontal
            if self._sample_horizontal_stage.moving:
                horizontal_rbv_str = str(
                    "{0:.4f}".format(self._sample_horizontal_stage.readback)
                )
                self._horizontal_rbv_changed.emit(horizontal_rbv_str)
                self._sample_horizontal_stage.moving = False

            # Sample focus
            if self._sample_focus_stage.moving:
                focus_rbv_str = str("{0:.4f}".format(self._sample_focus_stage.readback))
                self._focus_rbv_changed.emit(focus_rbv_str)
                self._sample_focus_stage.moving = False
