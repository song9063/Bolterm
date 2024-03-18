# 
# This file is part of the Bolterm distribution (https://github.com/song9063/Bolterm).
# Copyright (c) 2024 Song Junwoo.
# 
# This program is free software: you can redistribute it and/or modify  
# it under the terms of the GNU General Public License as published by  
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License 
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
from PySide6.QtCore import Signal, Slot, QSettings
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableView, QHeaderView
from HLWatchTableModel import HLWatchTableModel

class HLWatchTableWidget(QWidget):
    def __init__(self, parent=None):
        super(HLWatchTableWidget, self).__init__(parent)

        self.settings = QSettings()
        self.watcheItems = {}
        self.watchKeys = []


        self.model = HLWatchTableModel()

        self.initUI()

        self.model.addWatchKey("+CREG:")
        self.model.addWatchKey("+CEREG:")
        self.model.addWatchKey("+CR")
        # self.model.removeWatchAt(2)

    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        self.setMinimumWidth(100)
        self.setMinimumHeight(100)

        self.tableView = QTableView(self)
        self.tableView.setModel(self.model)
        # self.model.dataChanged.connect(self.tableView.update)

        self.horizontal_header = self.tableView.horizontalHeader()
        self.vertical_header = self.tableView.verticalHeader()
        self.horizontal_header.setSectionResizeMode(
                               QHeaderView.ResizeToContents
                               )
        self.vertical_header.setSectionResizeMode(
                             QHeaderView.ResizeToContents
                             )
        # self.horizontal_header.setStretchLastSection(True)

        layout.addWidget(self.tableView)
        self.setLayout(layout)

    def getWatchKeys(self):
        return self.model.watchKeys
    
    def updateWatchValues(self, valueDict):
        self.model.updateWatchValues(valueDict)