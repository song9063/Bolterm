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
# Reference: https://doc.qt.io/qtforpython-6/examples/example_widgets_richtext_syntaxhighlighter.html

from PySide6.QtCore import (QEvent, QObject, QEvent, Qt, Signal)
from PySide6.QtGui import (QTextCharFormat, QColor, QFont, QPalette, QTextCursor, QKeyEvent)
from PySide6.QtWidgets import (QPlainTextEdit, QVBoxLayout)
from HLATHighlighter import HLATHighlighter

class HLTermEditorWidget(QPlainTextEdit):
    
    writeCommand = Signal(str)

    def __init__(self, parent=None):
        super(HLTermEditorWidget, self).__init__(parent)

        self.highlighter = HLATHighlighter()

        self.setupHighlighter()
        self.setupEditor()

        self.bAutoScrollToEnd = False

    def showTestText(self):
        strTxt = """AT+IFC=1,23 # this is not comment
AT+IFC=1,23
AT+IFC=1,23
AT+KCNXCFG=1,"GPRS",""
AT+IFC?
CEREG=1 
RPuK:
FPuK:
RBUB: 8
RBFW: 6
OK
"""
        self.addText(strTxt)

        strTxt = """# comment
ERROR
 ERROR
 ERROR1
 ERROR 12
"""
        self.addText(strTxt)

    def showDemoCommand(self):
        strTxt = """# Request Identification Information

## Model info
ATI0

## Revision
ATI3

## Model S/W Version
ATI8

# Details
ATI9

"""
        self.addText(strTxt)

    def setupHighlighter(self):
        fATCmd = QTextCharFormat()
        fATCmd.setFontWeight(QFont.Normal)
        fATCmd.setForeground(QColor("#87AF87"))
        patternCmd = r'^\s*AT\+.*(?=[\?=])' # AT+Some=
        patternCmd = r'^\s*.*(?=[\?=:])'
        self.highlighter.addMapping(patternCmd, fATCmd)

        fATValue = QTextCharFormat()
        fATValue.setFontWeight(QFont.Bold)
        fATValue.setForeground(QColor("#FF8700"))
        fATValue.setForeground(QColor("#FFFFAF"))
        patternVal = r'(?<=\=|\:).+(?=[\#.*])*'
        self.highlighter.addMapping(patternVal, fATValue)

        fComment = QTextCharFormat()
        fComment.setFontWeight(QFont.Normal)
        fComment.setForeground(QColor("#5FAFAF"))
        patternCmt = r'^\#.*'
        self.highlighter.addMapping(patternCmt, fComment)

        fErr = QTextCharFormat()
        fErr.setFontWeight(QFont.Bold)
        fErr.setForeground(QColor("#AF5F5F"))
        patternError = r'\s*ERROR'
        self.highlighter.addMapping(patternError, fErr)

        fSend = QTextCharFormat()
        fSend.setFontWeight(QFont.Normal)
        fSend.setForeground(QColor("#FF8700"))
        patternSend = r'^SEND>'
        self.highlighter.addMapping(patternSend, fSend)

        fOK = QTextCharFormat()
        fOK.setFontWeight(QFont.Bold)
        fOK.setForeground(QColor("#8FAFD7"))
        patternOK = r'\s*OK'
        self.highlighter.addMapping(patternOK, fOK)

    def setupEditor(self):
        # self.editor = QPlainTextEdit()
        # p = self.editor.palette()
        # p.setColor(self.editor.viewport().backgroundRole(), QColor("#262626"))
        # self.editor.viewport().setPalette(p)
        # self.editor.setStyleSheet("QPlainTextEdit {background-color: #262626; color: white;}")
        # self.highlighter.setDocument(self.editor.document())
        self.installEventFilter(self)
        self.setStyleSheet("QPlainTextEdit {background-color: #262626; color: white;}")
        self.highlighter.setDocument(self.document())

    def setAutoScroll(self, bSet):
        self.bAutoScrollToEnd = bSet
        if bSet:
            self.moveCursor(QTextCursor.End)
            self.ensureCursorVisible()
        else:
            self.setCenterOnScroll(True)

    def addText(self, strText):
        # self.moveCursor(QTextCursor.End)
        self.insertPlainText(strText)
        if self.bAutoScrollToEnd:
            self.moveCursor(QTextCursor.End)

    def runCurrentLine(self):
        cursor = self.textCursor()
        # print(f'Block {cursor.blockNumber()}')
        doc = self.document()
        textBlock = doc.findBlockByLineNumber(cursor.blockNumber())
        strCmd = textBlock.text()
        if not strCmd.startswith('#') and len(strCmd.replace(" ", "")) > 0:
            print(strCmd.strip())
            self.writeCommand.emit(strCmd.strip())

    def eventFilter(self, obj: QObject, ev: QEvent) -> bool:
        
        if ev.type() == QEvent.Type.KeyRelease:
            keyEv = QKeyEvent(ev)
            keyComb = keyEv.keyCombination()
            # print(keyComb.key(), keyComb.keyboardModifiers())
            if keyComb.keyboardModifiers() == Qt.KeyboardModifier.ControlModifier and keyComb.key() == Qt.Key.Key_Return:
                self.runCurrentLine()
                return True
        return super().eventFilter(obj, ev)