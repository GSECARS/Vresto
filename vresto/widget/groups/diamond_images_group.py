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
from qtpy.QtWidgets import (
    QGroupBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QStackedWidget,
    QGridLayout,
)
from qtpy.QtCore import Qt, QSize
from qtpy.QtGui import QPixmap, QDoubleValidator

from vresto.model import PathModel


class DiamondImagesGroup(QGroupBox):

    _max_size: QSize = QSize(600, 400)

    def __init__(self, paths: PathModel) -> None:
        super(DiamondImagesGroup, self).__init__()

        self._paths = paths

        self._pic_sample_focus = os.path.join(
            self._paths.icon_path, "diamond_sample.png"
        )
        self._pic_table_focus = os.path.join(self._paths.icon_path, "diamond_table.png")
        self._pic_real_focus = os.path.join(self._paths.icon_path, "diamond_real.png")

        self.lbl_diamond_table = QLabel("Diamond Table")
        self.lbl_virtual_position = QLabel("Virtual Position")
        self.lbl_real_position = QLabel("Real Position")
        self._labels = [
            self.lbl_diamond_table,
            self.lbl_virtual_position,
            self.lbl_real_position,
        ]

        self.lne_diamond_table = QLineEdit()
        self.lne_virtual_position = QLineEdit()
        self.lne_real_position = QLineEdit()
        self.lne_boxes = [
            self.lne_diamond_table,
            self.lne_virtual_position,
            self.lne_real_position,
        ]

        self.btn_diamond_go = QPushButton("GO")
        self.btn_virtual_go = QPushButton("GO")
        self.btn_real_go = QPushButton("GO")
        self._buttons = [self.btn_diamond_go, self.btn_virtual_go, self.btn_real_go]

        self.stacked_images = QStackedWidget()
        self.label_pic_sample_focus = QLabel()
        self.label_pic_table_focus = QLabel()
        self.label_pic_real_focus = QLabel()
        self.label_pic_xray_focus = QLabel()
        self.pix_sample_focus = QPixmap(self._pic_sample_focus)
        self.pix_table_focus = QPixmap(self._pic_table_focus)
        self.pix_real_focus = QPixmap(self._pic_real_focus)

        self.setStyleSheet(
            open(
                os.path.join(self._paths.qss_path, "diamond_images_group.qss"), "r"
            ).read()
        )

        self._configure_image_labels()
        self._configure_stacked_widget()
        self._configure_lne_boxes()
        self._set_object_names()
        self._set_tool_status_tips()
        self._set_widget_sizes()
        self._layout_group()

    def _configure_image_labels(self) -> None:
        self.label_pic_sample_focus.setPixmap(self.pix_sample_focus)
        self.label_pic_table_focus.setPixmap(self.pix_table_focus)
        self.label_pic_real_focus.setPixmap(self.pix_real_focus)
        self.pix_sample_focus.scaled(
            self.label_pic_sample_focus.width(), self.label_pic_sample_focus.height()
        )
        self.pix_table_focus.scaled(
            self.label_pic_table_focus.width(), self.label_pic_table_focus.height()
        )
        self.pix_real_focus.scaled(
            self.label_pic_real_focus.width(), self.label_pic_real_focus.height()
        )
        self.label_pic_sample_focus.setScaledContents(True)
        self.label_pic_table_focus.setScaledContents(True)
        self.label_pic_real_focus.setScaledContents(True)
        self.label_pic_xray_focus.setScaledContents(True)

    def _configure_stacked_widget(self) -> None:
        self.stacked_images.addWidget(self.label_pic_sample_focus)  # Index: 0
        self.stacked_images.addWidget(self.label_pic_table_focus)  # Index: 1
        self.stacked_images.addWidget(self.label_pic_real_focus)  # Index: 2

    def _configure_lne_boxes(self) -> None:
        self.lne_diamond_table.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lne_virtual_position.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lne_real_position.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lne_diamond_table.setValidator(QDoubleValidator(-200000, 200000, 4))
        self.lne_virtual_position.setValidator(QDoubleValidator(-200000, 200000, 4))
        self.lne_real_position.setValidator(QDoubleValidator(-200000, 200000, 4))
        self.lne_real_position.setEnabled(False)

    def _set_object_names(self) -> None:
        """Sets all the object names for the group and the group widgets."""
        self.setObjectName("group-diamond-image")
        [label.setObjectName("lbl-diamond") for label in self._labels]
        [lne.setObjectName("lne-diamond") for lne in self.lne_boxes]
        [btn.setObjectName("btn-go") for btn in self._buttons]
        self.stacked_images.setObjectName("stacked-images")

    def _set_tool_status_tips(self) -> None:
        """Sets all the tool and status tips for the group."""
        self.btn_diamond_go.setToolTip("Moves the stage to the diamond table position")
        self.btn_virtual_go.setToolTip("Moves the stage to the virtual sample position")
        self.btn_real_go.setToolTip("Moves the stage to the real sample position")
        self.lne_diamond_table.setStatusTip(
            "Reads the value of the diamond table position"
        )
        self.lne_virtual_position.setStatusTip(
            "Reads the value of the virtual sample position"
        )
        self.lne_real_position.setStatusTip("Reads the real position of the sample")

    def _set_widget_sizes(self) -> None:
        [lne.setMaximumWidth(95) for lne in self.lne_boxes]
        [btn.setFixedSize(40, 32) for btn in self._buttons]

        self.setMaximumSize(self._max_size)

    def _layout_group(self) -> None:
        layout_diamond_table = QGridLayout()
        layout_diamond_table.setSpacing(2)
        layout_diamond_table.addWidget(self.lbl_diamond_table, 0, 0, 1, 1)
        layout_diamond_table.addWidget(self.lne_diamond_table, 1, 0, 1, 1)
        layout_diamond_table.addWidget(self.btn_diamond_go, 1, 1, 1, 1)
        layout_virtual_position = QGridLayout()
        layout_virtual_position.setSpacing(2)
        layout_virtual_position.addWidget(self.lbl_virtual_position, 0, 0, 1, 1)
        layout_virtual_position.addWidget(self.lne_virtual_position, 1, 0, 1, 1)
        layout_virtual_position.addWidget(self.btn_virtual_go, 1, 1, 1, 1)
        layout_real_position = QGridLayout()
        layout_real_position.setSpacing(2)
        layout_real_position.addWidget(self.lbl_real_position, 0, 0, 1, 1)
        layout_real_position.addWidget(self.lne_real_position, 1, 0, 1, 1)
        layout_real_position.addWidget(self.btn_real_go, 1, 1, 1, 1)

        layout = QGridLayout()
        layout.setSpacing(10)
        layout.addLayout(layout_diamond_table, 0, 0, 1, 1)
        layout.addLayout(layout_virtual_position, 0, 1, 1, 1)
        layout.addLayout(layout_real_position, 0, 2, 1, 1)
        layout.addWidget(self.stacked_images, 1, 0, 4, 3)

        self.setLayout(layout)
