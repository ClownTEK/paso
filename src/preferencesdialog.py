#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#Author: Read AUTHORS file.
#License: Read COPYING file.



from PyQt4 import *
from ui_preferencesdialog import Ui_Dialog
from uicontrol_packagesource import sourceListControl
from config import config




#t = gettext.translation(const.APP_NAME, const.APP_I18NDIR, fallback = True)
#_ = t.ugettext




class preferences(QtGui.QDialog, Ui_Dialog):


    def __init__(self):
        #
        QtGui.QDialog.__init__(self)
        self.setupUi(self)

        self.__localSources = sourceListControl(True)
        self.__localSources.connectWindow(self)
        self.__localSources.connectListWidget(self.listWidget_4)
        self.__localSources.connectAddButton(self.addButton_4)
        self.__localSources.connectRemoveButton(self.removeButton_4)

        self.__remoteSources = sourceListControl(False)
        self.__remoteSources.connectWindow(self)
        self.__remoteSources.connectLineEdit(self.lineEdit_7)
        self.__remoteSources.connectListWidget(self.listWidget_3)
        self.__remoteSources.connectAddButton(self.addButton_3)
        self.__remoteSources.connectRemoveButton(self.removeButton_3)

        self.config = config()
        self.lineEdit_3.setText(self.config.workspace)

        QtCore.QObject.connect(self.lineEdit,  QtCore.SIGNAL("textChanged (const QString&)"),  self.onChange)
        QtCore.QObject.connect(self.lineEdit_2,  QtCore.SIGNAL("textChanged (const QString&)"),  self.onChange)
        QtCore.QObject.connect(self.lineEdit_3,  QtCore.SIGNAL("textChanged (const QString&)"),  self.onChange)




    def load(self):
        if not self.config.load():  return(False)
        self.update()
        return(True)




    def update(self):
        self.lineEdit.setText(self.config.name)
        self.lineEdit_2.setText(self.config.email)
        self.lineEdit_3.setText(self.config.workspace)
        self.__localSources.setList(self.config.localDirs)
        self.__remoteSources.setList(self.config.remoteUrls)



    def save(self):
        self.config.name = self.lineEdit.text()
        self.config.email = self.lineEdit_2.text()
        self.config.workspace = self.lineEdit_3.text()
        self.config.localDirs = self.__localSources.getList()
        self.config.remoteUrls = self.__remoteSources.getList()
        if self.config.name != "" and self.config.email != "" and self.config.workspace != "":
            if not self.config.isExist():
                if not self.config.create():    return(False)
            else:
                if not self.config.save():  return(False)
        else:
            return(False)
        return(True)





    @QtCore.pyqtSignature("void")
    def on_saveButton_clicked(self):
        if self.save():
            self.close()




    @QtCore.pyqtSignature("void")
    def on_cancelButton_clicked(self):
        self.update()
        self.close()





    @QtCore.pyqtSignature("void")
    def on_wsButton_clicked(self):
        dirName = QtGui.QFileDialog.getExistingDirectory(self, "", self.lineEdit_3.text(), QtGui.QFileDialog.ShowDirsOnly )
        if dirName:
            self.lineEdit_3.setText(unicode(dirName))





    def onChange(self):
        if self.lineEdit.text() != "" and self.lineEdit_2.text() != "" and self.lineEdit_3.text() != "":
            self.saveButton.setEnabled(True)
        else:
            self.saveButton.setEnabled(False)




    def getLocalSources(self):
        return(self.__localSources.getList())




    def getRemoteSources(self):
        return(self.__remoteSources.getList())



