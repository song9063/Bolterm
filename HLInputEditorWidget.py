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
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QPushButton
from HLTermEditorWidget import HLTermEditorWidget

class HLInputEditorWidget(QWidget):
    writeCommand = Signal(str)

    def __init__(self, parent=None):
        super(HLInputEditorWidget, self).__init__(parent)
        self.settings = QSettings()

        self.initUI()

    def initUI(self):
        
        editorLayout = QVBoxLayout()
        editorLayout.setContentsMargins(0,0,0,0)
        editorLayout.setSpacing(0)

        self.setMinimumWidth(100)
        self.setMinimumHeight(100)

        self.editorView = HLTermEditorWidget(self)
        self.editorView.setMinimumHeight(50)
        self.editorView.setReadOnly(False)
        self.editorView.writeCommand.connect(self.onWriteCommand)
        self.editorView.showDemoCommand()

        layTool = QHBoxLayout()
        layTool.setSpacing(10)

        lblEnding = QLabel(self.tr("Ends with"), self)
        self.chkCR = QCheckBox(self.tr("CR"), self)
        self.chkCR.stateChanged.connect(lambda: self.settings.setValue("CR", self.chkCR.checkState()))
        lastChkCR = self.settings.value("CR")
        if lastChkCR != None:
            self.chkCR.setCheckState(lastChkCR)
        else:
            self.chkCR.setChecked(True) # Default: Checked

        self.chkLF = QCheckBox(self.tr("LF"), self)
        self.chkLF.stateChanged.connect(lambda: self.settings.setValue("LF", self.chkLF.checkState()))
        lastChkLF = self.settings.value("LF")
        if lastChkLF != None:
            self.chkLF.setCheckState(lastChkLF)

        self.btSendCur = QPushButton(self.tr("Send current line(ctrl+Enter)"), self)
        layTool.addWidget(lblEnding)
        layTool.addWidget(self.chkCR)
        layTool.addWidget(self.chkLF)
        layTool.addWidget(self.btSendCur)
        layTool.addStretch()

        editorLayout.addWidget(self.editorView)
        editorLayout.addLayout(layTool)
        self.setLayout(editorLayout)

    @Slot(str)
    def onWriteCommand(self, strCmd):
        self.writeCommand.emit(strCmd)