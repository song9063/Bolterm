# 
# This file is part of the Bolterm distribution (https://github.com/song9063/Bolterm).
# Copyright (c) 2015 Liviu Ionescu.
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
from PySide6.QtCore import QCoreApplication, QSettings, Signal
from PySide6.QtGui import QAction, QCloseEvent, QKeySequence, QResizeEvent
from PySide6.QtWidgets import QMainWindow

class HLMainWindow(QMainWindow):
    
    windowCloseEvent = Signal()

    def __init__(self, parent=None):
        super(HLMainWindow, self).__init__(parent)
        self.setWindowTitle("Bolterm")

        self.initSettings()
        self.initMenu()
        # geom = self.screen().availableGeometry()
        # self.setFixedSize(geom.width() * 0.5, geom.height() * 0.5)

    def closeEvent(self, event: QCloseEvent) -> None:
        self.windowCloseEvent.emit()
        return super().closeEvent(event)

    def initSettings(self):
        QCoreApplication.setOrganizationName("Busang Inc")
        QCoreApplication.setOrganizationDomain("busanginc.com")
        QCoreApplication.setApplicationName("Bolterm")

        self.settings = QSettings()
        winSize = self.settings.value("window/size")
        if winSize != None:
            self.resize(winSize)

    def initMenu(self):
        self.menu = self.menuBar()
        self.fileMenu = self.menu.addMenu("File")

        exitAction = QAction("Quit", self)
        exitAction.setShortcut(QKeySequence.Quit)
        exitAction.triggered.connect(self.close)

        self.fileMenu.addAction(exitAction)

        self.status = self.statusBar()
        self.status.showMessage("Data loaded")

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.settings.setValue("window/size", event.size())
        return super().resizeEvent(event)
    