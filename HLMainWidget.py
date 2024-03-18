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
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSplitter
from HLSerialSetWidget import HLSerialSetWidget
from HLInputEditorWidget import HLInputEditorWidget
from HLTermViewWidget import HLTermViewWidget
from HLWatchTableWidget import HLWatchTableWidget

from PySide6.QtSerialPort import QSerialPort


class HLMainWidget(QWidget):
    def __init__(self, parent=None):
        super(HLMainWidget, self).__init__(parent)
        self.settings = QSettings()

        self.bConnected = False
        self.strTempForWatch = ""

        self.bytesToWrite = 0
        self.writeTimer = QTimer(self)
        self.writeTimer.timeout.connect(self.writeTimeout)

        topLayout = QVBoxLayout()
        topLayout.setContentsMargins(5,5,5,5)
        topLayout.setSpacing(5)

        self.initSerialWidget(topLayout)

        midLayout = QVBoxLayout()
        self.initTermWidget(midLayout)
        topLayout.addLayout(midLayout, 2)

        self.setLayout(topLayout)

        self.initDevice()

    def onMainWindowWillClose(self):
        self.closeDevice()
        self.settings.setValue("termSplitterSize", self.termSplitter.saveState())
        self.settings.setValue("watchSplitterSize", self.watchSplitter.saveState())
        

    def initDevice(self):
        self.device = QSerialPort(self)
        self.device.readyRead.connect(self.readSerialData)
        self.device.bytesWritten.connect(self.handleBytesWritten)

    def onConnectClicked(self):
        if self.bConnected:
            self.closeDevice()
        else:
            self.openDevice()

    def openDevice(self):
        if self.device.isOpen():
            print('Already opened')
            return
        
        portName = self.settings.value("Port")
        if portName == None:
            print('No Port selected')
            return
        
        baudRate = self.settings.value("Baudrate")
        if portName == None:
            print('No Baudrate selected')
            return
        
        dataBits = self.settings.value("DataBits")
        if dataBits == None:
            print('No DataBits selected')
            return
        qDataBits = QSerialPort.DataBits.Data8
        if dataBits == "5":
            qDataBits = QSerialPort.DataBits.Data5
        elif dataBits == "6":
            qDataBits = QSerialPort.DataBits.Data6
        elif dataBits == "7":
            qDataBits = QSerialPort.DataBits.Data7

        parity = self.settings.value("Parity")
        if parity == None:
            print('No Parity selected')
            return
        qParity = QSerialPort.Parity.NoParity
        if parity == "Even":
            qParity = QSerialPort.Parity.EvenParity
        elif parity == "Odd":
            qParity = QSerialPort.Parity.OddParity
        elif parity == "Space":
            qParity = QSerialPort.Parity.SpaceParity
        elif parity == "Mark":
            qParity = QSerialPort.Parity.MarkParity

        stopBits = self.settings.value("StopBits")
        if stopBits == None:
            print('No StopBits selected')
            return
        qStopBits = QSerialPort.StopBits.OneStop
        if stopBits == "1.5":
            qStopBits = QSerialPort.StopBits.OneAndHalfStop
        elif stopBits == "2":
            qStopBits = QSerialPort.StopBits.TwoStop

        flow = self.settings.value("Flow")
        if flow == None:
            print('No FlowControl selected')
            return
        qFlow = QSerialPort.FlowControl.NoFlowControl
        if flow.startswith("H/W"):
            qFlow = QSerialPort.FlowControl.HardwareControl
        elif flow.startswith("S/W"):
            qFlow = QSerialPort.FlowControl.SoftwareControl
        self.device.setPortName(portName)
        self.device.setBaudRate(int(baudRate))
        self.device.setDataBits(qDataBits)
        self.device.setParity(qParity)
        self.device.setStopBits(qStopBits)
        self.device.setFlowControl(qFlow)
        if self.device.open(QIODevice.OpenModeFlag.ReadWrite):
            print('opened!!')
            self.bConnected = True
            self.serialSetWidget.setConnectedUI(True)
        else:
            self.bConnected = False
            print(self.device.errorString())

    def closeDevice(self):
        if self.device.isOpen():
            self.device.close()
            self.bConnected = False
            self.serialSetWidget.setConnectedUI(False)

    def initSerialWidget(self, layout):
        self.serialSetWidget = HLSerialSetWidget(self)
        self.serialSetWidget.openSerial.connect(self.onConnectClicked)
        layout.addWidget(self.serialSetWidget, 1)

    def initTermWidget(self, layout):
        self.termSplitter = QSplitter(self)
        self.termSplitter.setChildrenCollapsible(False)
        self.termSplitter.setOrientation(Qt.Orientation.Vertical)
        self.termView = HLTermViewWidget(self)
        self.editorWidget = HLInputEditorWidget(self)
        self.editorWidget.writeCommand.connect(self.writeCommand)
        self.termSplitter.addWidget(self.termView)
        self.termSplitter.addWidget(self.editorWidget)
        self.termSplitter.setCollapsible(self.termSplitter.indexOf(self.termView), False)
        self.termSplitter.setCollapsible(self.termSplitter.indexOf(self.editorWidget), False)

        self.watchSplitter = QSplitter(self)
        self.watchSplitter.setOrientation(Qt.Orientation.Horizontal)
        self.watchSplitter.setChildrenCollapsible(False)

        self.watchWidget = HLWatchTableWidget(self)

        self.watchSplitter.addWidget(self.watchWidget)
        self.watchSplitter.addWidget(self.termSplitter)
        self.watchSplitter.setCollapsible(self.watchSplitter.indexOf(self.watchWidget), False)
        self.watchSplitter.setCollapsible(self.watchSplitter.indexOf(self.termSplitter), False)

        lastSplitterState = self.settings.value("termSplitterSize")
        if lastSplitterState != None:
            self.termSplitter.restoreState(lastSplitterState)

        lastWSplitterState = self.settings.value("watchSplitterSize")
        if lastWSplitterState != None:
            self.watchSplitter.restoreState(lastWSplitterState)

        layout.addWidget(self.watchSplitter, 3)


    def readSerialData(self):
        data = self.device.readAll()
        strData = data.data().decode('utf8')
        
        self.termView.addText(strData)
        self.parseDataForWatch(strData)
        print(strData)

    def parseDataForWatch(self, strNewData):
        watchKeys = self.watchWidget.getWatchKeys()
        if len(watchKeys) < 1:
            print("no watch keys")
            return
        
        strNewData = strNewData.replace("\r","\n")
        strNewData = strNewData.replace("\n\n","\n")
        self.strTempForWatch += strNewData.replace("\n\n\n","\n")
        arTemp = self.strTempForWatch.split("\n")
        print("received ", len(arTemp), "lines")
        print(arTemp)
        
        if not strNewData.endswith("\n"):
            self.strTempForWatch = arTemp[-1]
        else:
            self.strTempForWatch = ""

        newWatchVal = {}
        for strLine in arTemp:
            strLineVal = strLine.strip()
            if strLineVal == "":
                continue
            for strKey in watchKeys:
                if strLineVal.startswith(strKey):
                    print("Find!", strLineVal)
                    strVal = strLineVal.replace(strKey, "").strip()
                    newWatchVal[strKey] = strVal
                    break
        if len(newWatchVal) > 0:
            self.watchWidget.updateWatchValues(newWatchVal)


    def handleBytesWritten(self, bytes):
        self.bytesToWrite -= bytes
        if self.bytesToWrite == 0:
            self.writeTimer.stop()
        
    @Slot(str)
    def writeCommand(self, strCmd):
        strCmdWithCRLF = strCmd
        if self.settings.value("CR") == Qt.CheckState.Checked:
            strCmdWithCRLF = strCmdWithCRLF + "\r"
        if self.settings.value("LF") == Qt.CheckState.Checked:
            strCmdWithCRLF = strCmdWithCRLF + "\n"

        data = QByteArray(strCmdWithCRLF)
        written = self.device.write(data)
        if written == data.size():
            self.termView.addText("SEND> " + strCmd + "\n")
            self.bytesToWrite += written
            self.writeTimer.start(1000)
        else:
            print(f'Failed to write all data: {self.device.errorString()}')

    def writeTimeout(self):
        print("timeout!!")
