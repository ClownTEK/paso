#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#Author: Read AUTHORS file.
#License: Read COPYING file.



from PyQt4 import *
from ui_progressdialog import Ui_progressDialog




#t = gettext.translation(const.APP_NAME, const.APP_I18NDIR, fallback = True)
#_ = t.ugettext




class progress(QtGui.QDialog, Ui_progressDialog):


    def __init__(self):
        #
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.stop = False




    def setName(self, name):
        self.progressName.setText(name)




    def setAction(self, act):
        self.actionLabel.setText(act)




    def setValue(self, val):
        if self.stop:
            self.close()
        self.progressBar.setValue(val)



    @QtCore.pyqtSignature("void")
    def on_stopButton_clicked(self):
        self.stop = True
        self.close()




