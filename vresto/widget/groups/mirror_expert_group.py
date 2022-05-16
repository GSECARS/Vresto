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
from qtpy.QtWidgets import QGroupBox, QPushButton, QLabel, QGridLayout, QLineEdit, QSlider, QHBoxLayout, QVBoxLayout
from qtpy.QtCore import Qt, QSize

from vresto.model import PathModel


class MirrorExpertGroup(QGroupBox):

    _title = " Laser-mirrors "
    _max_size = QSize(280, 200)

    def __init__(self, paths: PathModel) -> None:
        super(MirrorExpertGroup, self).__init__()

        self._paths = paths

        self.btn_ds_plus = QPushButton("+")
        self.btn_ds_minus = QPushButton("-")
        self.btn_us_plus = QPushButton("+")
        self.btn_us_minus = QPushButton("-")
        self.btn_step_1 = QPushButton()
        self.btn_step_2 = QPushButton()
        self.btn_ds_focus_zero = QPushButton(" DS")
        self.btn_us_focus_zero = QPushButton(" US")

        self._buttons = [
            self.btn_ds_focus_zero,
            self.btn_us_focus_zero,
        ]

        self._plus_buttons = [
            self.btn_ds_plus,
            self.btn_us_plus,
        ]

        self._minus_buttons = [
            self.btn_ds_minus,
            self.btn_us_minus,
        ]

        self._step_buttons = [
            self.btn_step_1,
            self.btn_step_2,
        ]

        self.lbl_step = QLabel("Step (mm)")
        self.lbl_ds = QLabel("Downstream")
        self.lbl_us = QLabel("Upstream")
        self.lbl_zero = QLabel("Zero Focus")
        self.lbl_ds_small = QLabel("DS")
        self.lbl_us_small = QLabel("US")

        self._labels = [
            self.lbl_ds,
            self.lbl_us,
            self.lbl_ds_small,
            self.lbl_us_small,
            self.lbl_zero,
        ]

        self.slider_ds = QSlider(Qt.Vertical)
        self.slider_us = QSlider(Qt.Vertical)

        self.lne_ds = QLineEdit()
        self.lne_us = QLineEdit()

        self.setTitle(self._title)
        self.setStyleSheet(
            open(os.path.join(self._paths.qss_path, "mirror_expert_group.qss"), "r").read()
        )

        self._configure_buttons()
        self._set_object_names()
        self._set_widget_sizes()
        self._layout_group()

    def _configure_buttons(self) -> None:
        for step_button in self._step_buttons:
            step_button.setCheckable(True)

    def _set_object_names(self) -> None:
        """Sets all the object names for the group and the group widgets."""
        self.setObjectName("group-mirrors")
        [plus_button.setObjectName("btn-plus") for plus_button in self._plus_buttons]
        [minus_button.setObjectName("btn-minus") for minus_button in self._minus_buttons]
        [step_button.setObjectName("btn-step") for step_button in self._step_buttons]
        [label.setObjectName("lbl-mirror") for label in self._labels]
        [button.setObjectName("btn-mirror") for button in self._buttons]
        self.lne_ds.setObjectName("lne-mirror")
        self.lne_us.setObjectName("lne-mirror")
        self.slider_ds.setObjectName("slider")
        self.slider_us.setObjectName("slider")
        self.lbl_step.setObjectName("lbl-step")

    def _set_widget_sizes(self) -> None:
        [button.setFixedSize(80, 30) for button in self._buttons]
        [step_button.setFixedSize(40, 20) for step_button in self._step_buttons]
        self.lne_ds.setFixedSize(60, 20)
        self.lne_us.setFixedSize(60, 20)

        self.setMaximumSize(self._max_size)

    def _layout_group(self) -> None:
        layout = QGridLayout()
        layout.setSpacing(10)

        layout_step_widgets = QHBoxLayout()
        layout_step_widgets.setContentsMargins(0, 0, 0, 0)
        layout_step_widgets.setSpacing(2)
        layout_step_widgets.addWidget(self.lbl_step, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_step_widgets.addWidget(self.btn_step_1, alignment=Qt.AlignmentFlag.AlignRight)
        layout_step_widgets.addWidget(self.btn_step_2, alignment=Qt.AlignmentFlag.AlignLeft)

        layout_ds = QHBoxLayout()
        layout_ds.setSpacing(2)
        layout_ds.addWidget(self.lbl_ds)
        layout_ds.addStretch(1)
        layout_ds.addWidget(self.btn_ds_minus)
        layout_ds.addWidget(self.lne_ds)
        layout_ds.addWidget(self.btn_ds_plus)

        layout_us = QHBoxLayout()
        layout_us.setSpacing(2)
        layout_us.addWidget(self.lbl_us)
        layout_us.addStretch(1)
        layout_us.addWidget(self.btn_us_minus)
        layout_us.addWidget(self.lne_us)
        layout_us.addWidget(self.btn_us_plus)

        layout_slider_ds = QVBoxLayout()
        layout_slider_ds.setSpacing(5)
        layout_slider_ds.addWidget(self.slider_ds)
        layout_slider_ds.addStretch(1)
        layout_slider_ds.addWidget(self.lbl_ds_small, alignment=Qt.AlignmentFlag.AlignLeft)

        layout_slider_us = QVBoxLayout()
        layout_slider_us.setSpacing(5)
        layout_slider_us.addWidget(self.slider_us)
        layout_slider_us.addStretch(1)
        layout_slider_us.addWidget(self.lbl_us_small, alignment=Qt.AlignmentFlag.AlignLeft)

        layout.addLayout(layout_ds, 0, 0, 1, 4)
        layout.addLayout(layout_us, 1, 0, 1, 4)
        layout.addLayout(layout_slider_ds, 0, 4, 3, 1)
        layout.addLayout(layout_slider_us, 0, 5, 3, 1)
        layout.addLayout(layout_step_widgets, 2, 0, 1, 4)
        layout.addWidget(self.lbl_zero, 3, 0, 1, 2)
        layout.addWidget(self.btn_ds_focus_zero, 3, 2, 1, 2, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.btn_us_focus_zero, 3, 4, 1, 2)

        self.setLayout(layout)
