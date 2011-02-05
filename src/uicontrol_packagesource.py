#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#Author: Read AUTHORS file.
#License: Read COPYING file.



from PyQt4 import *
from constants import const






class sourceListControl():

    def __init__(self, local):
        self.__behaviorIsLocal = local
        self.window = ""
        self.lineEdit = QtGui.QLineEdit()
        self.listWidget = QtGui.QListWidget()
        self.addButton = QtGui.QPushButton()
        self.removeButton = QtGui.QPushButton()




    def connectWindow(self, w):
        self.window = w



    def connectLineEdit(self, le):
        self.lineEdit = le




    def connectListWidget(self, lw):
        self.listWidget = lw





    def connectAddButton(self, ab):
        self.addButton = ab
        QtCore.QObject.connect(self.addButton,  QtCore.SIGNAL("clicked (bool)"),  self.on_addButton_clicked)




    def connectRemoveButton(self, rb):
        self.removeButton = rb
        QtCore.QObject.connect(self.removeButton,  QtCore.SIGNAL("clicked (bool)"),  self.on_removeButton_clicked)








    @QtCore.pyqtSignature("void")
    def on_addButton_clicked(self):
        if self.__behaviorIsLocal:
            dirName = QtGui.QFileDialog.getExistingDirectory(self.window, "", "/", QtGui.QFileDialog.ShowDirsOnly )
            if dirName:
                self.listWidget.addItem(unicode(dirName))
        elif self.lineEdit.text():
            if str(self.lineEdit.text())[:7] in const.REMOTE_PREFIX:
                self.listWidget.addItem(self.lineEdit.text())
                self.lineEdit.setText("")




    @QtCore.pyqtSignature("void")
    def on_removeButton_clicked(self):
        self.listWidget.currentItem()
        self.listWidget.removeItemWidget(self.listWidget.takeItem(self.listWidget.currentRow()))





    def getList(self):
        data = []
        for item in range(self.listWidget.count()):
            data.append(self.listWidget.item(item).text().__str__())
        return(data)




    def setList(self, data):
        self.listWidget.clear()
        for item in data:
            self.listWidget.addItem(item)
        if not len(data):
            self.listWidget.clear()

