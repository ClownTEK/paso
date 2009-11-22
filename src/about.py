#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#Author: Read AUTHORS file.
#License: Read COPYING file.


from PyQt4 import *
from ui_about import Ui_Dialog





class aboutDialog(QtGui.QDialog, Ui_Dialog):



    def __init__(self):
        #
        QtGui.QDialog.__init__(self)
        self.setupUi(self)




    #Close button
    @QtCore.pyqtSignature("void")
    def on_pushButton_clicked(self):
        #
        self.close()

