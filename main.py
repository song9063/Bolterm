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
import sys
from PySide6.QtWidgets import QApplication
from HLMainWindow import HLMainWindow
from HLMainWidget import HLMainWidget
from PySide6.QtGui import (QFont, QFontDatabase)

def main():
    app = QApplication(sys.argv)
    QFontDatabase.addApplicationFont('./assets/Hack-Bold.ttf')
    QFontDatabase.addApplicationFont('./assets/Hack-BoldItalic.ttf')
    QFontDatabase.addApplicationFont('./assets/Hack-Italic.ttf')
    QFontDatabase.addApplicationFont('./assets/Hack-Regular.ttf')
    app.setFont(QFont('Hack'))

    win = HLMainWindow()

    mainWidget = HLMainWidget(win)
    win.windowCloseEvent.connect(mainWidget.onMainWindowWillClose)
    win.setCentralWidget(mainWidget)
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
