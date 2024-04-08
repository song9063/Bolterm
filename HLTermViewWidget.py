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
from PySide6.QtCore import Qt, QIODevice, Slot, QByteArray, QTimer, QSettings
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QPushButton
from HLSerialSetWidget import HLSerialSetWidget
from HLTermEditorWidget import HLTermEditorWidget

class HLTermViewWidget(QWidget):
    def __init__(self, parent=None):
        super(HLTermViewWidget, self).__init__(parent)
        self.settings = QSettings()

        self.initUI()

    def initUI(self):
        lay = QVBoxLayout()
        lay.setContentsMargins(0,0,0,0)
        lay.setSpacing(0)

        self.setMinimumWidth(100)
        self.setMinimumHeight(100)

        layTools = QHBoxLayout()
        layTools.setSpacing(10)
        self.chkAutoScroll = QCheckBox(self.tr("AutoScroll"), self)
        self.chkAutoScroll.stateChanged.connect(self.onChkAutoScrollStateChanged)
        layTools.addWidget(self.chkAutoScroll)

        btSaveOutput = QPushButton(self.tr("Save output"), self)
        layTools.addWidget(btSaveOutput)

        layTools.addStretch()
        btClear = QPushButton(self.tr("Clear"), self)
        btClear.clicked.connect(self.onClearClicked)
        layTools.addWidget(btClear)

        self.termView = HLTermEditorWidget(self)
        self.termView.setMinimumHeight(100)
        self.termView.setReadOnly(True)
        # self.termView.showTestText()
        
        lay.addLayout(layTools)
        lay.addWidget(self.termView)
        self.setLayout(lay)

        lastChk = self.settings.value("AutoScroll")
        if lastChk is not None:
            self.chkAutoScroll.setChecked(lastChk)
            self.termView.setAutoScroll(lastChk)

    def onChkAutoScrollStateChanged(self):
        self.settings.setValue("AutoScroll", self.chkAutoScroll.isChecked())
        self.termView.setAutoScroll(self.chkAutoScroll.isChecked())

    def onClearClicked(self):
        self.termView.clear()

    def addText(self, strText):
        self.termView.addText(strText)

        print(self.termView.viewportMargins())
        print(self.termView.viewportSizeHint())
        # pol = self.termView.sizeAdjustPolicy()
        # print(pol)
    
        

        # print(self.termView.toPlainText())
        # print('End of text')