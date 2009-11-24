#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#Author: Read AUTHORS file.
#License: Read COPYING file.


from PyQt4 import *
from ui_options import Ui_Dialog
from config import config
from lib import eventHandler
from constants import const
import os





class optionsDialog(QtGui.QDialog, Ui_Dialog):



    def __init__(self):
        #
        self.__data = config()
        self.onError = eventHandler()
        QtGui.QDialog.__init__(self)
        self.setupUi(self)

        #aliases
        self.__fullname = self.lineEdit
        self.__email = self.lineEdit_2





    def load(self):
        if not self.__data.load():
            if self.__data.onFirstTime:
                self.onError.raiseEvent(const.JOB_CONF_ID, const.ERR_11_ID, "")
                self.pushButton.setEnabled(False)
                self.action()
                self.pushButton.setEnabled(True)
            else:
                self.onError.raiseEvent(const.JOB_CONF_ID, const.ERR_10_ID, "")
                return(False)
        else:
            return(True)





    def save(self):
        if not self.__data.save():
            self.onError.raiseEvent(const.JOB_CONF_ID, const.ERR_11_ID, "")
            return(False)
        return(True)





    #Close button
    @QtCore.pyqtSignature("void")
    def on_pushButton_clicked(self):
        #
        self.close()




    #Ok button
    @QtCore.pyqtSignature("void")
    def on_pushButton_2_clicked(self):
        #
        self.__data.data[const.OPT_USER_KEY][const.OPT_USERNAME_KEY] = self.__fullname.text()
        self.__data.data[const.OPT_USER_KEY][const.OPT_USEREMAIL_KEY] = self.__email.text()
        if self.__data.save():
            #self.onAction.raiseEvent(100, 10, 100, 100, const.JOB_CONFS_ID,"")
            self.close()
        else:
            self.onError.raiseEvent(const.JOB_CONFS_ID, const.ERR_12_ID, "")



    def __sync(self):
        self.__fullname.setText( self.__data.data[const.OPT_USER_KEY][const.OPT_USERNAME_KEY])
        self.__email.setText( self.__data.data[const.OPT_USER_KEY][const.OPT_USEREMAIL_KEY])



    def action(self):
        self.__sync()
        self.exec_()



    def setDir(self, key, val):
        self.__data.data[const.OPT_DIRS_KEY][key] = val


    def getDir(self, key):
        return(self.__data.data[const.OPT_DIRS_KEY][key])



    def getUser(self, key):
        return(self.__data.data[const.OPT_USER_KEY][key])