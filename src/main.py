#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#Author: Read AUTHORS file.
#License: Read COPYING file.


import gettext
from PyQt4 import *

from constants import const
from ui_main import Ui_Dialog
from prepareIface import pIface
from buildIface import bIface
from lib import ratioCalc
from lib import stripFilename



t = gettext.translation(const.APP_NAME, const.APP_I18NDIR, fallback = True)
_ = t.ugettext




class mainDialog(QtGui.QDialog, Ui_Dialog, pIface, bIface):
    #Controls all GUI operations and manage operation modules via interface clases


    def __init__(self):
        #
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.__jobDesc = {}     #{ID:"text",..}
        self.__errDesc = {}
        self.__error = False

        #Init interfaces
        pIface.__init__(self)
        bIface.__init__(self)

        #Aliases for GUI objects
        self.__isoDir_check = self.checkBox_5
        self.__isoDir_edit = self.lineEdit_3
        self.__isoDir_browse = self.pushButton_4
        self.__altDir_check = self.checkBox_4
        self.__altDir_edit = self.lineEdit_5
        self.__altDir_browse = self.pushButton
        self.__outFile_edit = self.lineEdit_6
        self.__outFile_browse = self.pushButton_9
        self.__rootDir_edit = self.lineEdit_7
        self.__rootDir_browse = self.pushButton_10
        self.__readIns_check = self.checkBox_2
        self.__readRepo_check = self.checkBox
        self.__prgBar = self.progressBar
        self.__prgText = self.label_7
        self.__go_button = self.pushButton_2
        self.__paoDir_edit = self.lineEdit_11
        self.__readPao_check = self.checkBox_3
        self.__readAlt_check = self.checkBox_6
        self.__build_button = self.pushButton_17
        self.__analyze_button = self.pushButton_18
        self.__boutDir_edit = self.lineEdit_8
        self.__bisoDir_edit = self.lineEdit_10
        self.__baltDir_edit = self.lineEdit_9
        self.__baltDir_check = self.checkBox_7
        #self.__stop_button = self.pushButton_xx        #Doesn't work, GUI is freeze until python process end over
                                                        #Maybe we use python threading etc.

        #Get user dialogs and decriptions
        self.i18n()

        #GUI Events
        QtCore.QObject.connect(self.__isoDir_check,  QtCore.SIGNAL("stateChanged (int)"),  self.set_isoEdit)
        QtCore.QObject.connect(self.__altDir_check,  QtCore.SIGNAL("stateChanged (int)"),  self.set_altEdit)
        QtCore.QObject.connect(self.__isoDir_check,  QtCore.SIGNAL("stateChanged (int)"),  self.check_edit)
        QtCore.QObject.connect(self.__altDir_check,  QtCore.SIGNAL("stateChanged (int)"),  self.check_edit)
        QtCore.QObject.connect(self.__rootDir_edit,  QtCore.SIGNAL("textChanged (const QString&)"),  self.check_edit)
        QtCore.QObject.connect(self.__outFile_edit,  QtCore.SIGNAL("textChanged (const QString&)"),  self.check_edit)
        QtCore.QObject.connect(self.__altDir_edit,  QtCore.SIGNAL("textChanged (const QString&)"),  self.check_edit)
        QtCore.QObject.connect(self.__isoDir_edit,  QtCore.SIGNAL("textChanged (const QString&)"),  self.check_edit)
        QtCore.QObject.connect(self.__paoDir_edit,  QtCore.SIGNAL("textChanged (const QString&)"),  self.check_b_edit)
        QtCore.QObject.connect(self.__bisoDir_edit,  QtCore.SIGNAL("textChanged (const QString&)"),  self.check_b_edit)
        QtCore.QObject.connect(self.__baltDir_edit,  QtCore.SIGNAL("textChanged (const QString&)"),  self.check_b_edit)
        QtCore.QObject.connect(self.__baltDir_check,  QtCore.SIGNAL("stateChanged (int)"),  self.set_baltEdit)
        QtCore.QObject.connect(self.__baltDir_check,  QtCore.SIGNAL("stateChanged (int)"),  self.check_b_edit)

        #Register the Progress Bar actions to interface eventHandlers for operation processes
        pIface.onCrazy.addEventListener( self.__updateProgress)
        pIface.onError.addEventListener( self.__errorHappened)
        bIface.onAction.addEventListener( self.__updateProgress)
        bIface.onError.addEventListener( self.__errorHappened)


        #Default variables                                      #It should be takes from config file, but config file not supported yet
        self.__rootDir_edit.setText(pIface.getroot(self))
        self.__boutDir_edit.setText(bIface.getcwd(self))



    @QtCore.pyqtSignature("void")
    def on_pushButton_3_clicked(self):
        self.close()








################################################################################
#
#   PREPARE SECTION ACTIONS
#
################################################################################

    #ISO Directory Browse button _______________________________________________
    @QtCore.pyqtSignature("void")
    def on_pushButton_4_clicked(self):
        #
        dirName = QtGui.QFileDialog.getExistingDirectory(self, self.__dialog1, self.__isoDir_edit.text(), QtGui.QFileDialog.ShowDirsOnly )
        if dirName:
            self.__isoDir_edit.setText(dirName)
            self.__isoDir_edit.setEnabled(True)
            self.__isoDir_check.setCheckState(2)




    def set_isoEdit(self, state):
        #
        if state == 2 and str(self.__isoDir_edit.text()):
            self.__isoDir_edit.setEnabled(True)
        else:
            self.__isoDir_edit.setEnabled(False)
            self.__isoDir_check.setCheckState(0)




    #Alternative Package Directory Browse button _______________________________________________
    @QtCore.pyqtSignature("void")
    def on_pushButton_clicked(self):
        #
        dirName = QtGui.QFileDialog.getExistingDirectory(self, self.__dialog1, self.__altDir_edit.text(), QtGui.QFileDialog.ShowDirsOnly )
        if dirName:
            self.__altDir_edit.setText(dirName)
            self.__altDir_edit.setEnabled(True)
            self.__altDir_check.setCheckState(2)




    def set_altEdit(self, state):
        #
        if state == 2 and str(self.__altDir_edit.text()):
            self.__altDir_edit.setEnabled(True)




    #ROOT Directory Browse button _______________________________________________
    @QtCore.pyqtSignature("void")
    def on_pushButton_10_clicked(self):
        #
        dirName = QtGui.QFileDialog.getExistingDirectory(self, self.__dialog1, self.__rootDir_edit.text(), QtGui.QFileDialog.ShowDirsOnly )
        if dirName:
            self.__rootDir_edit.setText(dirName)




    #OUTPUT File Browse button _______________________________________________
    @QtCore.pyqtSignature("void")
    def on_pushButton_9_clicked(self):
        #
        fileName = QtGui.QFileDialog.getSaveFileName(self, self.__dialog2, self.__outFile_edit.text(), "Paso (*.paso)")
        if fileName:
            if stripFilename(str(fileName), ".paso") == stripFilename(str(fileName)):
                fileName += ".paso"
            self.__outFile_edit.setText(fileName)





    #Directory inputs control _______________________________________________
    def check_edit(self, txt):
        rootDir = str(self.__rootDir_edit.text())
        outFile = str(self.__outFile_edit.text())
        isoDir = str(self.__isoDir_edit.text())
        altDir = str(self.__altDir_edit.text())
        if  rootDir.strip() == "" :    self.__go_button.setEnabled(False)
        elif stripFilename(outFile.strip()) == "":   self.__go_button.setEnabled(False)
        elif self.__isoDir_check.checkState() and isoDir.strip() == "":  self.__go_button.setEnabled(False)
        elif self.__altDir_check.checkState() and altDir.strip() == "":  self.__go_button.setEnabled(False)
        else:   self.__go_button.setEnabled(True)




    #GO TO CRAZY button _______________________________________________
    @QtCore.pyqtSignature("void")
    def on_pushButton_2_clicked(self):
        #
        self.__error = False
        self.__go_button.setEnabled(False)

        #pass values to pIface
        pIface.setOptions(self, const.OPT_ISODIRCHECK_ID, bool(self.__isoDir_check.checkState()) )
        pIface.setOptions(self, const.OPT_ALTDIRCHECK_ID, bool(self.__altDir_check.checkState()) )
        pIface.setOptions(self, const.OPT_READINSCHECK_ID, bool(self.__readIns_check.checkState()) )
        pIface.setOptions(self, const.OPT_READREPOCHECK_ID, bool(self.__readRepo_check.checkState()) )
        pIface.setOptions(self, const.OPT_ROOTDIR_ID, str(self.__rootDir_edit.text()) )
        pIface.setOptions(self, const.OPT_PASOFILE_ID, str(self.__outFile_edit.text()) )
        pIface.setOptions(self, const.OPT_ISODIR_ID, str(self.__isoDir_edit.text()) )
        pIface.setOptions(self, const.OPT_ALTDIR_ID, str(self.__altDir_edit.text()) )
        pIface.got_to_crazy(self)
        if not self.__error:
            self.__updateProgress(100, 100, 100, 100, const.JOB_PAS_ID, \
                                    self.__jobDesc[const.JOB_SUCCES_ID]+" "+self.__outFile_edit.text() )
            self.__go_button.setEnabled(True)











################################################################################
#
#   BUILD SECTION ACTIONS
#
################################################################################


    #Paso file browse button _______________________________________________
    @QtCore.pyqtSignature("void")
    def on_pushButton_15_clicked(self):
        #
        old = self.__paoDir_edit.text()
        fileName = QtGui.QFileDialog.getOpenFileName(self, self.__dialog2, self.__paoDir_edit.text(), "Paso (*.paso)")
        if fileName:
            self.__paoDir_edit.setText(fileName)
        if fileName <> old:
            self.__build_button.setEnabled(False)
            bIface.setOptions(self, const.OPT_FORCEPASOREAD_ID, True )





    #Output directory browse button _______________________________________________
    @QtCore.pyqtSignature("void")
    def on_pushButton_11_clicked(self):
        #
        dirName = QtGui.QFileDialog.getExistingDirectory(self, self.__dialog1, self.__boutDir_edit.text(), QtGui.QFileDialog.ShowDirsOnly )
        if dirName:
            self.__boutDir_edit.setText(dirName)




    #ISO directory browse button _______________________________________________
    @QtCore.pyqtSignature("void")
    def on_pushButton_13_clicked(self):
        #
        old = self.__bisoDir_edit.text()
        dirName = QtGui.QFileDialog.getExistingDirectory(self, self.__dialog1, self.__bisoDir_edit.text(), QtGui.QFileDialog.ShowDirsOnly )
        if dirName:
            self.__bisoDir_edit.setText(dirName)
        if dirName <> old:
            self.__build_button.setEnabled(False)
            bIface.setOptions(self, const.OPT_FORCECDREAD_ID, True )




    #Alternative directory browse button _______________________________________________
    @QtCore.pyqtSignature("void")
    def on_pushButton_12_clicked(self):
        #
        old = self.__baltDir_edit.text()
        dirName = QtGui.QFileDialog.getExistingDirectory(self, self.__dialog1, self.__baltDir_edit.text(), QtGui.QFileDialog.ShowDirsOnly )
        if dirName:
            self.__baltDir_edit.setText(dirName)
            self.__baltDir_edit.setEnabled(True)
            self.__baltDir_check.setCheckState(2)
        if dirName <> old:
            self.__build_button.setEnabled(False)
            bIface.setOptions(self, const.OPT_FORCEALTREAD_ID, True )




    def set_baltEdit(self, state):
        #
        if state == 2 and str(self.__baltDir_edit.text()):
            self.__baltDir_edit.setEnabled(True)
        else:
            self.__baltDir_edit.setEnabled(False)
            self.__baltDir_check.setCheckState(0)




    #Directory inputs control _______________________________________________
    def check_b_edit(self, txt):
        #
        paoFile = str( self.__paoDir_edit.text()).strip()
        isoDir = str( self.__bisoDir_edit.text()).strip()
        altDir = str( self.__baltDir_edit.text()).strip()
        outDir = str( self.__boutDir_edit.text()).strip()
        if paoFile and outDir and isoDir:
            self.__analyze_button.setEnabled(True)
        else:
            self.__analyze_button.setEnabled(False)
            self.__build_button.setEnabled(False)





    #Analyze button _______________________________________________
    @QtCore.pyqtSignature("void")
    def on_pushButton_18_clicked(self):
        #
        self.__error = False

        bIface.setOptions(self, const.OPT_PASOFILE_ID, str(self.__paoDir_edit.text()) )
        bIface.setOptions(self, const.OPT_ISODIR_ID, str(self.__bisoDir_edit.text()) )
        bIface.setOptions(self, const.OPT_ALTDIR_ID, str(self.__baltDir_edit.text()) )
        bIface.setOptions(self, const.OPT_READPASOCHECK_ID, bool(self.__readPao_check.checkState()) )
        bIface.setOptions(self, const.OPT_READALTCHECK_ID, bool(self.__readAlt_check.checkState()) )
        bIface.setOptions(self, const.OPT_ALTDIRCHECK_ID, bool(self.__baltDir_check.checkState()))
        bIface.doAnalyze(self)
        bIface.setOptions(self, const.OPT_FORCEPASOREAD_ID, False )
        bIface.setOptions(self, const.OPT_FORCECDREAD_ID, False )
        bIface.setOptions(self, const.OPT_FORCEALTREAD_ID, False )
        self.check_b_edit("")
        if not self.__error:
            self.__build_button.setEnabled(True)
            self.__updateProgress(100, 100, 100, 100, const.JOB_ALZ_ID,self.__jobDesc[const.JOB_SUCCES_ID])





    #Build button _______________________________________________
    @QtCore.pyqtSignature("void")
    def on_pushButton_17_clicked(self):
        #
        self.__error = False
        bIface.setOptions(self, const.OPT_OUTDIR_ID, str(self.__boutDir_edit.text()) )
        bIface.build(self)
        if not self.__error:
            self.__updateProgress(100, 100, 100, 100, const.JOB_BIS_ID, \
                                    self.__jobDesc[const.JOB_SUCCES_ID]+" "+ \
                                    self.__boutDir_edit.text()+"/"+stripFilename(str(self.__paoDir_edit.text()), const.PASO_EXT)+const.ISO_EXT )








################################################################################
#
#   PROGRESS SECTION ACTIONS
#
################################################################################

    def __updateProgress(self, totalJobs, currentJob, totalElements, currentElement, jobId, elementName):
        #
        currentPos = ratioCalc(totalElements, currentElement, totalJobs, currentJob)
        self.__prgText.setText(self.__jobDesc[jobId]+"... "+elementName)
        self.__prgBar.setValue(currentPos)
        self.__prgText.repaint()
        self.__prgBar.repaint()
        print (self.__prgText.text())





    def __errorHappened(self, jobId, errorCode, errorData):
        #
        self.__error = True
        errText = self.__jobDesc[jobId]+". "+self.__errDesc[errorCode]+":"+errorData
        self.__prgText.setText(errText)
        print( errText)









################################################################################
#
#   i18n
#
################################################################################

    def i18n(self):
        #
        self.__dialog1 =  _("Select directory")
        self.__dialog2 =  _("Select file")
        self.__jobDesc[const.JOB_INS_ID] =  _("Reading installed packages")
        self.__jobDesc[const.JOB_REP_ID] =  _("Reading repos")
        self.__jobDesc[const.JOB_ISO_ID] =  _("Reading Pardus CD repo")
        self.__jobDesc[const.JOB_ALT_ID] =  _("Reading alternative packages")
        self.__jobDesc[const.JOB_RES_ID] =  _("Building resource list")
        self.__jobDesc[const.JOB_PAS_ID] =  _("Creating paso file")
        self.__jobDesc[const.JOB_PAO_ID] =  _("Reading paso file")
        self.__jobDesc[const.JOB_ALZ_ID] =  _("Analyzing packages")
        self.__jobDesc[const.JOB_CHC_ID] =  _("Reading pisi cache")
        self.__jobDesc[const.JOB_BRP_ID] =  _("Building repo")
        self.__jobDesc[const.JOB_BIS_ID] =  _("Building iso")
        self.__jobDesc[const.JOB_SUCCES_ID] = _("Succesfully")

        self.label_8.setText(  _("Special installation builder for Pardus Linux") )
        self.pushButton_8.setText(  _("Options") )
        self.pushButton_7.setText(  _("About") )
        self.tabWidget.setTabText(0,  _("Build") )
        self.tabWidget.setTabText(1,  _("Prepare") )
        self.label_11.setText(  _(".paso File") )
        self.label_19.setText(  _("Pardus CD mount directory") )
        self.label_18.setText(  _("Alternative packages directory") )
        self.label_10.setText(  _("Output directory") )
        self.groupBox_4.setTitle(  _("Progress") )
        self.pushButton_3.setText(  _("Close") )
        self.pushButton_18.setText(  _("Analyze") )
        self.pushButton_17.setText(  _("Build") )
        self.label_9.setText(  _("Pardus Root directory") )
        self.label_6.setText( self.label_11.text() )
        self.label_3.setText( self.label_19.text() )
        self.label_5.setText( self.label_18.text() )
        self.checkBox_2.setText(  _("Don't read installed packages again") )
        self.checkBox.setText(  _("Don't read repo index again") )
        self.pushButton_2.setText(  _("Prepare") )
        self.__readPao_check.setText(  _("Don't read paso info again") )
        self.__readAlt_check.setText(  _("Don't read alternative packages again") )

        self.__errDesc[const.ERR_01_ID] = _("Directory or file not found")
        self.__errDesc[const.ERR_02_ID] = _("Bad xml structure")
        self.__errDesc[const.ERR_03_ID] = _("User break")
        self.__errDesc[const.ERR_04_ID] = _("Package not found")
        self.__errDesc[const.ERR_05_ID] = _("File not created")
        self.__errDesc[const.ERR_06_ID] = _("Bad paso info")
        self.__errDesc[const.ERR_07_ID] = _("")
        self.__errDesc[const.ERR_08_ID] = _("HTTP Error")
        self.__errDesc[const.ERR_09_ID] = _("ISO image not craeted")

