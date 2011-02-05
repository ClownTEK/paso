#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#Author: Read AUTHORS file.
#License: Read COPYING file.



import sys
from PyQt4 import QtCore, QtGui
from paso.main import mainWindow


def run():
    app = QtGui.QApplication(sys.argv)
    locale = QtCore.QLocale.system().name()
    translator = QtCore.QTranslator()
    translator.load("/usr/share/paso/translations/%s.qm" % locale)
    app.installTranslator(translator)
    window = mainWindow()
    window.show()
    return( app.exec_())




if __name__ == "__main__":
    run()

