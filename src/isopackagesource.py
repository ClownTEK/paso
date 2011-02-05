#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#Author: Read AUTHORS file.
#License: Read COPYING file.



from PyQt4 import *
from ui_isopackagesourcedialog import Ui_Dialog
from uicontrol_packagesource import sourceListControl
from constants import const
from os import path



#t = gettext.translation(const.APP_NAME, const.APP_I18NDIR, fallback = True)
#_ = t.ugettext




class isoPackageSource(QtGui.QDialog, Ui_Dialog):


    def __init__(self):
        #
        QtGui.QDialog.__init__(self)
        self.setupUi(self)

        self.__localSources = sourceListControl(True)
        self.__localSources.connectWindow(self)
        self.__localSources.connectListWidget(self.listWidget_1)
        self.__localSources.connectAddButton(self.addButton_1)
        self.__localSources.connectRemoveButton(self.removeButton_1)

        self.__remoteSources = sourceListControl(False)
        self.__remoteSources.connectWindow(self)
        self.__remoteSources.connectLineEdit(self.lineEdit_2)
        self.__remoteSources.connectListWidget(self.listWidget_2)
        self.__remoteSources.connectAddButton(self.addButton_2)
        self.__remoteSources.connectRemoveButton(self.removeButton_2)

        self.build = False

        QtCore.QObject.connect(self.wsEdit,  QtCore.SIGNAL("textChanged (const QString&)"),  self.onChange)
        QtCore.QObject.connect(self.pnEdit,  QtCore.SIGNAL("textChanged (const QString&)"),  self.onChange)
        QtCore.QObject.connect(self.pimEdit,  QtCore.SIGNAL("textChanged (const QString&)"),  self.onChange)





    def setRemoteSources(self, data):
        self.__remoteSources.setList(data)




    def setLocalSources(self, data):
        self.__localSources.setList(data)




    def setWorkspace(self, w):
        self.wsEdit.setText(w)




    def setProjectName(self, pn):
        self.pnEdit.setText(pn)




    def setPIMPath(self, pim):
        self.pimEdit.setText(pim)




    def getRemoteSources(self):
        return(self.__remoteSources.getList())




    def getLocalSources(self):
        return(self.__localSources.getList()+[path.join(self.getPIMPath(), const.PIM_REPO)])




    def getWorkspace(self):
        return( path.normpath(unicode(self.wsEdit.text())) )




    def getProjectName(self):
        return(unicode(self.pnEdit.text()))




    def getPIMPath(self):
        return(path.normpath(unicode(self.pimEdit.text())))




    def onChange(self):
        if self.wsEdit.text() != "" and self.pnEdit.text() != "" and self.pimEdit.text() != "":
            self.buildButton.setEnabled(True)
        else:   self.buildButton.setEnabled(False)



    @QtCore.pyqtSignature("void")
    def on_buildButton_clicked(self):
        self.accept()




    @QtCore.pyqtSignature("void")
    def on_cancelButton_clicked(self):
        self.reject()




    @QtCore.pyqtSignature("void")
    def on_wsButton_clicked(self):
        dirName = QtGui.QFileDialog.getExistingDirectory(self, "", self.wsEdit.text(), QtGui.QFileDialog.ShowDirsOnly )
        if dirName:
            self.wsEdit.setText(unicode(dirName))




    @QtCore.pyqtSignature("void")
    def on_pimButton_clicked(self):
        dirName = QtGui.QFileDialog.getExistingDirectory(self, "", self.pimEdit.text(), QtGui.QFileDialog.ShowDirsOnly )
        if dirName:
            self.pimEdit.setText(unicode(dirName))

