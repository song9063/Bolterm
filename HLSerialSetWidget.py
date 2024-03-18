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
from PySide6.QtCore import Qt, QSettings, Signal
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QComboBox, QLabel, QPushButton
from PySide6.QtSerialPort import QSerialPortInfo

class HLSerialSetWidget(QWidget):
    
    openSerial = Signal()

    def __init__(self, parent=None):
        super(HLSerialSetWidget,self).__init__(parent)

        self.settings = QSettings()
        self.arPorts = []

        self.topLayout = QHBoxLayout()
        self.initUI()
        self.topLayout.addStretch()
        self.setLayout(self.topLayout)
        self.scanPorts()

    def initUI(self):
        self.setMaximumHeight(100)
        layLine1 = QHBoxLayout()
        layLine2 = QHBoxLayout()

        lblBaud = QLabel(self.tr("Baudrate"), self)
        self.comboBaudrate = QComboBox(self)
        self.comboBaudrate.addItems(["110", "300", "600", "1200", "2400", "4800", "9600", "14400", "19200", "38400", "57600", "115200", "128000", "256000"])
        self.comboBaudrate.currentTextChanged.connect(lambda: self.onSettingItemChanged("Baudrate", self.comboBaudrate.currentText()))
        lastVal = self.settings.value("Baudrate")
        if lastVal is not None:
            self.comboBaudrate.setCurrentText(lastVal)
        layLine1.addWidget(lblBaud)
        layLine1.addWidget(self.comboBaudrate)
        layLine1.addSpacing(10)

        lblBits = QLabel(self.tr("DataBits"), self)
        self.comboDataBits = QComboBox(self)
        self.comboDataBits.addItems(["5","6","7","8"])
        self.comboDataBits.currentTextChanged.connect(lambda: self.onSettingItemChanged("DataBits", self.comboDataBits.currentText()))
        lastVal = self.settings.value("DataBits")
        if lastVal is not None:
            self.comboDataBits.setCurrentText(lastVal)
        layLine1.addWidget(lblBits)
        layLine1.addWidget(self.comboDataBits)
        layLine1.addSpacing(10)

        lblParity = QLabel(self.tr("Parity"), self)
        self.comboParities = QComboBox(self)
        self.comboParities.addItems(["No", "Even", "Odd", "Space", "Mark"])
        self.comboParities.currentTextChanged.connect(lambda: self.onSettingItemChanged("Parity", self.comboParities.currentText()))
        lastVal = self.settings.value("Parity")
        if lastVal is not None:
            self.comboParities.setCurrentText(lastVal)
        layLine1.addWidget(lblParity)
        layLine1.addWidget(self.comboParities)
        layLine1.addSpacing(10)

        lblStop = QLabel(self.tr("StopBits"), self)
        self.comboStops = QComboBox(self)
        self.comboStops.addItems(["1", "1.5", "2"])
        self.comboStops.currentTextChanged.connect(lambda: self.onSettingItemChanged("StopBits", self.comboStops.currentText()))
        lastVal = self.settings.value("StopBits")
        if lastVal is not None:
            self.comboStops.setCurrentText(lastVal)
        layLine1.addWidget(lblStop)
        layLine1.addWidget(self.comboStops)
        layLine1.addSpacing(10)

        lblFlow = QLabel(self.tr("Flow"), self)
        self.comboFlows = QComboBox(self)
        self.comboFlows.addItems(["No", "H/W(RTS/CTS)", "S/W(XOnOff)"])
        self.comboFlows.currentTextChanged.connect(lambda: self.onSettingItemChanged("Flow", self.comboFlows.currentText()))
        lastVal = self.settings.value("Flow")
        if lastVal is not None:
            self.comboFlows.setCurrentText(lastVal)
        layLine1.addWidget(lblFlow)
        layLine1.addWidget(self.comboFlows)
        layLine1.addStretch()

        lblPorts = QLabel(self.tr("Port"), self)
        self.comboPorts = QComboBox(self)
        self.comboPorts.setMaximumWidth(300)
        self.comboPorts.currentTextChanged.connect(self.onPortSelected)
        self.btRefreshPorts = QPushButton(self.tr("Scan"))
        self.btRefreshPorts.clicked.connect(self.scanPorts)
        layLine2.addWidget(lblPorts)
        layLine2.addWidget(self.comboPorts)
        layLine2.addWidget(self.btRefreshPorts)
        layLine1.addSpacing(10)

        self.btConnect = QPushButton(self.tr("Open"), self)
        self.btConnect.clicked.connect(self.onConnectClicked)
        layLine2.addWidget(self.btConnect)
        self.setConnectedUI(False)

        layLine2.addStretch()
        
        hbox = QVBoxLayout()
        hbox.setSpacing(0)
        hbox.addLayout(layLine1)
        hbox.addLayout(layLine2)
        self.topLayout.addLayout(hbox)

    def setConnectedUI(self, connected):
        if connected:
            self.btConnect.setText("Close")
        else:
            self.btConnect.setText("Open")

    def scanPorts(self):
        self.arPorts.clear()
        self.comboPorts.clear()
        ports = QSerialPortInfo().availablePorts()
        for p in ports:
            if not p.portName().startswith('cu'):
                self.arPorts.append(p)
                self.comboPorts.addItem(p.portName())

        lastVal = self.settings.value("Port")
        if lastVal is not None:
            # print("port ", lastVal)
            self.comboPorts.setCurrentText(lastVal)

    def onPortSelected(self):
        nIndex = self.comboPorts.currentIndex()
        if nIndex < 0:
            return
    
        port = self.arPorts[nIndex]
        # print(f'port selected {port.portName()}')

    def onSettingItemChanged(self, strName, strVal):
        self.settings.setValue(strName, strVal)
        # print(strName, strVal)

    def onConnectClicked(self):
        self.settings.setValue("Port", self.comboPorts.currentText())
        self.openSerial.emit()
