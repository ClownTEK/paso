#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#Author: Read AUTHORS file.
#License: Read COPYING file.


import gettext
from PyQt4 import *

from constants import const
from ui_about import Ui_Dialog




t = gettext.translation(const.APP_NAME, const.APP_I18NDIR, fallback = True)
_ = t.ugettext




class aboutDialog(QtGui.QDialog, Ui_Dialog):



    def __init__(self):
        #
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.i18n()




    #Build button _______________________________________________
    @QtCore.pyqtSignature("void")
    def on_pushButton_clicked(self):
        #
        self.close()


################################################################################
#
#   i18n
#
################################################################################

    def i18n(self):
        #
        description = _("<p>Paso is an installation builder for Pardus Linux.\
                        For moore information and new versions visit to;<br>")
        developers = _("<p>Current developers;<br>")
        translators = _("<p>Thanks to translators;<br>")
        copying =  _("<p>This program is free software; \
                    you can redistribute it and/or modify it \
                    under the terms of the GNU General Public \
                    License as published by the Free Software Foundation.\
                    Please read COPYING file</p>")
        abouttext = description+"<a href="+const.WEBPAGE+">"+const.WEBPAGE+"</a></p>"
        abouttext += copying
        abouttext += developers + const.DEVELOPERS + "</p>"
        abouttext += translators + const.TRANSLATORS + "</p>"
        self.textBrowser.setText(abouttext)
        self.label.setText( const.NAME )
        self.label_2.setText( const.VERSION )




