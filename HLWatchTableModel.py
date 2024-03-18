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
from typing import Any
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide6.QtGui import QColor
from datetime import datetime

class HLWatchItem:
    def __init__(self, key="", val="", updatedAt="", name="", comment=""):
        self._key = key.strip()
        self._val = val.strip()
        self._prevValue = ""
        self.updatedAt = ""
        self.name = ""
        self.comment = ""

    def set(self, key, val):
        self._key = key.strip()
        self._val = val.strip()

    def setKey(self, key):
        self._key = key.strip()

    def setValue(self, val):
        strNewVal = val.strip()
        if self._val != strNewVal:
            self._prevValue = self._val
        self._val = strNewVal
        self.updatedAt = datetime.now().strftime("%H%M%S.%f")

    def getKey(self):
        return self._key
    
    def getValue(self):
        return self._val
    
    def getPrevValue(self):
        return self._prevValue
    
    def getUpdatedAt(self):
        return self.updatedAt
    
    def isEmpty(self):
        return self._key == "" and self._val == ""
    

class HLWatchTableModel(QAbstractTableModel):
    def __init__(self):
        QAbstractTableModel.__init__(self)
        self.watchItems = {}
        self.watchKeys = []

        self.initUI()

    def initUI(self):
        self.cols = 3
        self.rows = len(self.watchKeys)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> Any:
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == Qt.Orientation.Vertical:
            return [section]
        return ("Name", "Prefix", "Value", "Updated At", "Comment")[section]
    
    def rowCount(self, parent: QModelIndex) -> int:
        return len(self.watchKeys) + 1
    
    def columnCount(self, parent: QModelIndex) -> int:
        return 5
    
    def setData(self, index: QModelIndex, value: Any, role: int = ...) -> bool:
        col = index.column()
        row = index.row()
        if role == Qt.ItemDataRole.EditRole:
            if row >= len(self.watchKeys):
                self.addWatchKey(value)
                return True

            strKey = self.watchKeys[row]
            watchItem = self.watchItems.get(strKey, None)
            if watchItem is None:
                return False
            
            if value.strip() == "":
                value = strKey
                return True
            
            if col == 1: # prefix
                self.watchItems.pop(strKey)
                self.watchKeys[row] = value
                watchItem.setKey(value)
            elif col == 0: # Name
                watchItem.name = value
            elif col == 4: # Comment
                watchItem.comment = value

            self.watchItems[value] = watchItem
            self.dataChanged.emit(index, index)
            return True

        return False

    def data(self, index: QModelIndex, role: int = ...) -> Any:
        col = index.column()
        row = index.row()

        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
            if row >= len(self.watchKeys):
                return ""
            strKey = self.watchKeys[row]
            watchItem = self.watchItems.get(strKey, None)
            if watchItem is None:
                return "None"
            
            if col == 0: # Name
                return watchItem.name
            elif col == 1: # Prefix
                return watchItem.getKey()
            elif col == 2:
                strDispVal = ""
                strOldVal = watchItem.getPrevValue()
                strCurVal = watchItem.getValue()
                if strOldVal != "":
                    strDispVal = f'{strOldVal}->{strCurVal}'
                else:
                    strDispVal = strCurVal

                return strDispVal
            elif col == 3:
                return watchItem.getUpdatedAt()
            elif col == 4: # Comment
                return watchItem.comment

            return ""
        elif role == Qt.ItemDataRole.BackgroundRole:
            return QColor(Qt.GlobalColor.white)
        elif role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignLeading
        return None
    
    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        col = index.column()
        if col == 0 or col == 1 or col == 4:
            return Qt.ItemFlag.ItemIsEditable|Qt.ItemFlag.ItemIsEnabled|Qt.ItemFlag.ItemIsSelectable
        return Qt.ItemFlag.ItemIsEnabled|Qt.ItemFlag.ItemIsSelectable

    def updateWatchValues(self, vDict):
        if len(vDict) < 1:
            return
        for k, v in vDict.items():
            self.setWatchValue(k, v)
        self.layoutChanged.emit()

    def addWatchKey(self, strKey):
        if strKey in self.watchKeys or strKey.strip() == '':
            return
        
        # lastRow = len(self.watchKeys)
        # self.beginInsertRows(self.createIndex(lastRow, 0), lastRow, lastRow)
        watchItem = HLWatchItem(strKey)
        self.watchItems[strKey] = watchItem
        self.watchKeys.append(strKey)
        # self.endInsertRows()
        # print('added', lastRow)
        self.layoutChanged.emit()

    def setWatchValue(self, strKey, strVal):
        if strKey.strip() == '':
            return
        
        if strKey not in self.watchKeys:
            self.addWatchKey(strKey)

        watchItem = self.watchItems.get(strKey)
        watchItem.setValue(strVal)
        self.watchItems[strKey] = watchItem

    def removeWatchAt(self, nIndex):
        if nIndex < 0 or nIndex >= len(self.watchKeys):
            return
        
        strKey = self.watchKeys[nIndex]
        self.watchItems.pop(strKey)
        self.watchKeys.pop(nIndex)
        self.layoutChanged.emit()
        

