#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#Author: Read AUTHORS file.
#License: Read COPYING file.



from PyQt4 import *
from ui_aboutdialog import Ui_aboutDialog
from constants import const





class about(QtGui.QDialog, Ui_aboutDialog):


    def __init__(self):
        #
        QtGui.QDialog.__init__(self)
        self.setupUi(self)

        pic = QtGui.QPixmap(":/Paso_logo128.png")
        scene = QtGui.QGraphicsScene()
        scene.setSceneRect(0, 0, 128, 128)
        scene.addItem(QtGui.QGraphicsPixmapItem(pic))
        self.graphicsView.setScene(scene)
        self.graphicsView.setRenderHint(QtGui.QPainter.Antialiasing)
        self.label.setText(const.NAME)
        version = QtGui.QApplication.translate("aboutDialog", "Version :", None, QtGui.QApplication.UnicodeUTF8)
        version.append(const.VERSION+"<p>")
        desc = QtGui.QApplication.translate("aboutDialog", "Paso is an installation builder for Pardus Linux. For moore information and new versions visit to ", None, QtGui.QApplication.UnicodeUTF8)
        desc.append(const.WEBPAGE+"<p>")
        dev = QtGui.QApplication.translate("aboutDialog", "Developers :", None, QtGui.QApplication.UnicodeUTF8)
        dev.append("<br>")
        trans = QtGui.QApplication.translate("aboutDialog", "Translators :", None, QtGui.QApplication.UnicodeUTF8)
        trans.append("<br>")
        media = QtGui.QApplication.translate("aboutDialog", "Media designers :", None, QtGui.QApplication.UnicodeUTF8)
        media.append("<br>")
        license = QtGui.QApplication.translate("aboutDialog", "License :", None, QtGui.QApplication.UnicodeUTF8)
        license.append("GNU GPL<p>")

        html = version.append(desc)
        html = html.append(license)
        html = html.append(dev)
        html = html.append(const.DEVELOPERS)
        html = html.append(trans)
        html = html.append(const.TRANSLATORS)
        html = html.append(media)
        html = html.append(const.DESIGNERS)

        self.label_2.setText(html)
