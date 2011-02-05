#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#Author: Read AUTHORS file.
#License: Read COPYING file.



from PyQt4 import *
from ui_pasoinfogroup import Ui_pasoInfoGroup
from engine.pasofile.types import header
#import gettext



#t = gettext.translation(const.APP_NAME, const.APP_I18NDIR, fallback = True)
#_ = t.ugettext




class pasoInfo(QtGui.QGroupBox, Ui_pasoInfoGroup):


    def __init__(self):
        #
        QtGui.QGroupBox.__init__(self)
        self.setupUi(self)

        self.changed = False
        self.__header = header()
        self.__processEvents = True

        QtCore.QObject.connect(self.lineEdit,  QtCore.SIGNAL("textChanged (const QString&)"),  self.__onChange)
        QtCore.QObject.connect(self.lineEdit_2,  QtCore.SIGNAL("textChanged (const QString&)"),  self.__onChange)
        QtCore.QObject.connect(self.plainTextEdit,  QtCore.SIGNAL("textChanged ()"),  self.__onChange)




    def setHeader(self, header):
        self.__header = header
        self.__processEvents = False
        self.plainTextEdit.setPlainText(self.__header.dc)
        self.lineEdit.setText(self.__header.n)
        self.lineEdit_2.setText(self.__header.hp)
        self.lineEdit_3.setText(self.__header.r)
        self.lineEdit_4.setText(self.__header.d)
        self.lineEdit_5.setText(self.__header.pn)
        self.lineEdit_6.setText(self.__header.pm)
        self.__processEvents = True
        self.changed = False




    def setTitle(self, title):
        self.label_3.setText(title)



    def getHeader(self):
        return(self.__header)




    def __onChange(self, string=""):
        if self.__processEvents:
            self.__header.n = self.lineEdit.text()
            self.__header.dc = self.plainTextEdit.toPlainText()
            self.__header.hp = self.lineEdit_2.text()
            self.changed = True





