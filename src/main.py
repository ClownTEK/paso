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
from lib import stripFilename, stripPath, getPardusRelease, ratioCalc
from about import aboutDialog
from options import optionsDialog
import datetime



t = gettext.translation(const.APP_NAME, const.APP_I18NDIR, fallback = True)
_ = t.ugettext




class mainDialog(QtGui.QDialog, Ui_Dialog):
    #Controls all GUI operations and manage operation modules via interface clases


    def __init__(self):
        #
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.pIface = pIface()
        self.bIface = bIface()
        self.__jobDesc = {}     #{ID:"text",..}
        self.__errDesc = {}
        self.__error = False
        self.__aboutDialog = aboutDialog()
        self.__optionsDialog = optionsDialog()

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
        self.__infoPName_edit = self.lineEdit
        self.__infoPSumm_edit = self.lineEdit_4
        self.__infoPDesc_edit = self.textBrowser_6
        self.__infoPHome_edit = self.lineEdit_13
        self.__infoBName_label = self.label_33
        self.__infoBSumm_line = self.lineEdit_12
        self.__infoBDesc_text = self.textBrowser_5
        self.__infoBHome_line = self.label_26
        self.__infoBRele_line = self.label_28
        self.__infoBDate_line = self.label_30
        self.__infoBPName_line = self.label_21
        self.__infoBPEmail_line = self.label_23
        self.__reportCount_line = self.label_34
        self.__reportSize_line = self.label_39
        self.__reportDCount_line = self.label_35
        self.__reportDSize_line = self.label_37
        self.__reportISOSize_line = self.label_42
        self.__infoPRepoSize_line = self.label_46
        #self.__stop_button = self.pushButton_xx        #Doesn't work, GUI freezing until python process end over
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
        QtCore.QObject.connect(self.__infoBHome_line, QtCore.SIGNAL("linkActivated(QString)"), self.OpenURL)


        #Register the Progress Bar actions to interface eventHandlers for operation processes
        self.pIface.onCrazy.addEventListener( self.__updateProgress)
        self.pIface.onError.addEventListener( self.__errorHappened)
        self.bIface.onAction.addEventListener( self.__updateProgress)
        self.bIface.onError.addEventListener( self.__errorHappened)
        self.__optionsDialog.onError.addEventListener(self.__errorHappened)

        if self.__optionsDialog.load():
            self.__updateProgress(100, 100, 100, 100, const.JOB_CONF_ID, self.__jobDesc[const.JOB_SUCCES_ID])
        self.pullOptions()

        self.tabWidget.setCurrentIndex(1)







    def pullOptions(self):
        self.__paoDir_edit.setText(self.__optionsDialog.getDir(const.OPT_BPASODIR_KEY))
        self.__bisoDir_edit.setText(self.__optionsDialog.getDir(const.OPT_BCDDIR_KEY))
        self.__baltDir_edit.setText(self.__optionsDialog.getDir(const.OPT_BALTDIR_KEY))
        self.__boutDir_edit.setText(self.__optionsDialog.getDir(const.OPT_BOUTDIR_KEY))
        self.__outFile_edit.setText(self.__optionsDialog.getDir(const.OPT_PPASODIR_KEY))
        self.__rootDir_edit.setText( self.__optionsDialog.getDir(const.OPT_PROOTDIR_KEY))
        self.__isoDir_edit.setText(self.__optionsDialog.getDir(const.OPT_PCDDIR_KEY))
        self.__altDir_edit.setText(self.__optionsDialog.getDir(const.OPT_PALTDIR_KEY))






    def pushOptions(self):
        pao = str(self.__paoDir_edit.text())
        out = str(self.__outFile_edit.text())
        if stripFilename(pao, ".paso") <> stripFilename(pao):
            pao = stripPath(str(self.__paoDir_edit.text()) )
        if stripFilename(out, ".paso") <> stripFilename(out):
            out = stripPath(str(self.__outFile_edit.text()) )
        self.__optionsDialog.setDir(const.OPT_BPASODIR_KEY, pao)
        self.__optionsDialog.setDir(const.OPT_BCDDIR_KEY, str(self.__bisoDir_edit.text()))
        self.__optionsDialog.setDir(const.OPT_BALTDIR_KEY, str(self.__baltDir_edit.text()))
        self.__optionsDialog.setDir(const.OPT_BOUTDIR_KEY, str(self.__boutDir_edit.text()))
        self.__optionsDialog.setDir(const.OPT_PPASODIR_KEY, out)
        self.__optionsDialog.setDir(const.OPT_PROOTDIR_KEY, str(self.__rootDir_edit.text()) )
        self.__optionsDialog.setDir(const.OPT_PCDDIR_KEY, str(self.__isoDir_edit.text()))
        self.__optionsDialog.setDir(const.OPT_PALTDIR_KEY, str(self.__altDir_edit.text()))






    @QtCore.pyqtSignature("void")
    def on_pushButton_3_clicked(self):
        self.pushOptions()
        self.__optionsDialog.save()
        self.close()








################################################################################
#
#   PREPARE SECTION ACTIONS
#
################################################################################

    #ISO Directory Browse button
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




    #Alternative Package Directory Browse button
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
        else:
            self.__altDir_edit.setEnabled(False)
            self.__altDir_check.setCheckState(0)



    #ROOT Directory Browse button
    @QtCore.pyqtSignature("void")
    def on_pushButton_10_clicked(self):
        #
        dirName = QtGui.QFileDialog.getExistingDirectory(self, self.__dialog1, self.__rootDir_edit.text(), QtGui.QFileDialog.ShowDirsOnly )
        if dirName:
            self.__rootDir_edit.setText(dirName)




    #OUTPUT File Browse button
    @QtCore.pyqtSignature("void")
    def on_pushButton_9_clicked(self):
        #
        fileName = QtGui.QFileDialog.getSaveFileName(self, self.__dialog2, self.__outFile_edit.text(), "Paso (*.paso)")
        if fileName:
            if stripFilename(str(fileName), ".paso") == stripFilename(str(fileName)):
                fileName += ".paso"
            self.__outFile_edit.setText(fileName)
            self.__updatePrepareInfo(self.pIface.getInfo( str(fileName)))





    #Directory inputs control
    def check_edit(self, txt):
        rootDir = str(self.__rootDir_edit.text())
        outFile = str(self.__outFile_edit.text())
        isoDir = str(self.__isoDir_edit.text())
        altDir = str(self.__altDir_edit.text())
        if  rootDir.strip() == "" :    self.__go_button.setEnabled(False)
        elif stripFilename(outFile.strip()) == "":   self.__go_button.setEnabled(False)
        elif stripFilename(outFile.strip(), ".paso") == stripFilename(outFile.strip()):  self.__go_button.setEnabled(False)
        elif self.__isoDir_check.checkState() and isoDir.strip() == "":  self.__go_button.setEnabled(False)
        elif self.__altDir_check.checkState() and altDir.strip() == "":  self.__go_button.setEnabled(False)
        else:   self.__go_button.setEnabled(True)






    def __updatePrepareInfo(self, info):
        #info is type of pasoMetadata
        if info:
            self.__infoPName_edit.setText(info.name)
            self.__infoPSumm_edit.setText(info.summary)
            self.__infoPDesc_edit.setText(info.description)
            self.__infoPHome_edit.setText(info.homepage)
            try:
                self.__infoPRepoSize_line.setText(str((info.repoSize/1024)/1024))
            except:
                pass




    #PREPARE button
    @QtCore.pyqtSignature("void")
    def on_pushButton_2_clicked(self):
        #
        self.__error = False
        self.__go_button.setEnabled(False)

        #pass values to pIface
        self.pIface.pasoMetadata.packagerName = self.__optionsDialog.getUser(const.OPT_USERNAME_KEY)
        self.pIface.pasoMetadata.packagerEmail = self.__optionsDialog.getUser(const.OPT_USEREMAIL_KEY)
        self.pIface.pasoMetadata.name = self.__infoPName_edit.text()
        self.pIface.pasoMetadata.summary = self.__infoPSumm_edit.text()
        self.pIface.pasoMetadata.description = self.__infoPDesc_edit.toPlainText()
        self.pIface.pasoMetadata.homepage = self.__infoPHome_edit.text()
        self.pIface.pasoMetadata.date = datetime.datetime.now().strftime("%d/%m/%Y")
        self.pIface.pasoMetadata.release = getPardusRelease(self.__rootDir_edit.text())
        self.pIface.isoDirCheck = bool(self.__isoDir_check.checkState())
        self.pIface.altDirCheck = bool(self.__altDir_check.checkState())
        self.pIface.readInsCheck = bool(self.__readIns_check.checkState())
        self.pIface.readRepoCheck = bool(self.__readRepo_check.checkState())
        self.pIface.rootDir = str(self.__rootDir_edit.text())
        self.pIface.pasoFile = str(self.__outFile_edit.text())
        self.pIface.isoDir = str(self.__isoDir_edit.text())
        self.pIface.altDir = str(self.__altDir_edit.text())

        self.pIface.go_to_crazy()
        if not self.__error:
            self.__updateProgress(100, 100, 100, 100, const.JOB_PAS_ID, \
                                    self.__jobDesc[const.JOB_SUCCES_ID]+" "+self.__outFile_edit.text() )
            try:
                self.__infoPRepoSize_line.setText(str((self.pIface.getPrepareInfo().repoSize/1024)/1024))
            except:
                pass
        self.__go_button.setEnabled(True)











################################################################################
#
#   BUILD SECTION ACTIONS
#
################################################################################


    #Paso file browse button
    @QtCore.pyqtSignature("void")
    def on_pushButton_15_clicked(self):
        #
        old = self.__paoDir_edit.text()
        fileName = QtGui.QFileDialog.getOpenFileName(self, self.__dialog2, self.__paoDir_edit.text(), "Paso (*.paso)")
        if fileName:
            self.__paoDir_edit.setText(fileName)
        if fileName <> old:
            self.__build_button.setEnabled(False)
            self.bIface.forcePasoRead =  True
            self.__updateBuildInfo(self.bIface.getInfo( str(fileName)))





    #Output directory browse button
    @QtCore.pyqtSignature("void")
    def on_pushButton_11_clicked(self):
        #
        dirName = QtGui.QFileDialog.getExistingDirectory(self, self.__dialog1, self.__boutDir_edit.text(), QtGui.QFileDialog.ShowDirsOnly )
        if dirName:
            self.__boutDir_edit.setText(dirName)




    #ISO directory browse button
    @QtCore.pyqtSignature("void")
    def on_pushButton_13_clicked(self):
        #
        old = self.__bisoDir_edit.text()
        dirName = QtGui.QFileDialog.getExistingDirectory(self, self.__dialog1, self.__bisoDir_edit.text(), QtGui.QFileDialog.ShowDirsOnly )
        if dirName:
            self.__bisoDir_edit.setText(dirName)
        if dirName <> old:
            self.__build_button.setEnabled(False)
            self.bIface.forceCdRead =  True




    #Alternative directory browse button
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
            self.bIface.forceAltRead = True




    def set_baltEdit(self, state):
        #
        if state == 2 and str(self.__baltDir_edit.text()):
            self.__baltDir_edit.setEnabled(True)
        else:
            self.__baltDir_edit.setEnabled(False)
            self.__baltDir_check.setCheckState(0)




    #Directory inputs control
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



    def __updateBuildInfo(self, info):
        #info is type of pasoMetadata
        if info:
            self.__infoBName_label.setText(info.name)
            self.__infoBSumm_line.setText(info.summary)
            self.__infoBDesc_text.setText(info.description)
            self.__infoBHome_line.setText("<qt><a href='"+info.homepage+ \
                                            "'>"+info.homepage+"</a></qt>")
            self.__infoBRele_line.setText(info.release)
            self.__infoBDate_line.setText(info.date)
            self.__infoBPName_line.setText(info.packagerName)
            self.__infoBPEmail_line.setText(info.packagerEmail)




    def OpenURL(self, URL):
        QtGui.QDesktopServices().openUrl(QtCore.QUrl(URL))





    #Analyze button
    @QtCore.pyqtSignature("void")
    def on_pushButton_18_clicked(self):
        #
        self.__error = False

        self.bIface.pasoFile = str(self.__paoDir_edit.text())
        self.bIface.isoDir = str(self.__bisoDir_edit.text())
        self.bIface.altDir = str(self.__baltDir_edit.text())
        self.bIface.readPasoCheck = bool(self.__readPao_check.checkState())
        self.bIface.readAltCheck = bool(self.__readAlt_check.checkState())
        self.bIface.altDirCheck = bool(self.__baltDir_check.checkState())
        self.bIface.doAnalyze()
        self.bIface.forcePasoRead = False
        self.bIface.forceCdRead = False
        self.bIface.forceAltRead = False
        self.check_b_edit("")
        if not self.__error:
            self.__build_button.setEnabled(True)
            self.__updateProgress(100, 100, 100, 100, const.JOB_ALZ_ID,self.__jobDesc[const.JOB_SUCCES_ID])
            report = self.bIface.getReport()
            self.__reportCount_line.setText( str(report[0]) )
            self.__reportSize_line.setText( str(report[1] / 1024) )
            self.__reportDCount_line.setText( str(report[2]) )
            self.__reportDSize_line.setText( str(report[3] / 1024) )
            self.__reportISOSize_line.setText( str(report[4] / 1024) )





    #Build button
    @QtCore.pyqtSignature("void")
    def on_pushButton_17_clicked(self):
        #
        self.__error = False
        self.bIface.outDir =  str(self.__boutDir_edit.text())
        self.bIface.build()
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
#   OTHER ACTIONS
#
################################################################################


    #About button
    @QtCore.pyqtSignature("void")
    def on_pushButton_7_clicked(self):
        #
        self.__aboutDialog.exec_()






    #Options button
    @QtCore.pyqtSignature("void")
    def on_pushButton_8_clicked(self):
        #
        self.__optionsDialog.action()





    def setOptions(self):
        self.__optionsDialog.setDir(const.OPT_ROOTDIR_KEY, self.__rootDir_edit.text())
        self.__optionsDialog.setDir(const.OPT_OUTDIR_KEY, self.__boutDir_edit.text())
        self.__optionsDialog.setDir(const.OPT_CDDIR_KEY, self.__bisoDir_edit.text())




################################################################################
#
#   i18n
#
################################################################################

    def i18n(self):
        #
        self.setWindowTitle(const.NAME+" "+const.VERSION)
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
        self.__jobDesc[const.JOB_CONF_ID] = _("Configuration loading")
        self.__jobDesc[const.JOB_CONFS_ID] = _("Configuration saving")

        self.label_8.setText(  _("Special installation builder for Pardus Linux") )
        self.pushButton_8.setText(  _("Options") )
        self.pushButton_7.setText(  _("About") )
        self.tabWidget.setTabText(0,  _("Build") )
        self.tabWidget.setTabText(1,  _("Prepare") )
        self.label_11.setText(  _(".paso File") )
        self.label_19.setText(  _("Mounted Pardus CD directory") )
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
        self.__readPao_check.setText(  _("Don't read paso packages again") )
        self.__readAlt_check.setText(  _("Don't read alternative packages again") )
        self.groupBox_3.setTitle( _("Info") )
        self.groupBox_5.setTitle( self.groupBox_3.title() )
        self.groupBox_2.setTitle( _("Analyze report") )
        self.label_2.setText( _("Name") )
        self.label_4.setText( _("Summary") )
        self.label_22.setText( _("Description"))
        self.label_12.setText( _("Homepage"))
        self.label_25.setText( self.label_12.text()+":" )
        self.label_27.setText( _("Release")+":" )
        self.label_29.setText( _("Date")+":" )
        self.label_20.setText( _("Prepared by")+":" )
        self.label_32.setText( _("Total")+":" )
        self.label_36.setText( _("Download")+":" )
        self.label_41.setText( _("Estimated ISO size")+":" )
        self.label_45.setText( _("Repo size")+":" )

        #About Dialog
        description = _("<p>Paso is an installation builder for Pardus Linux.\
                        For moore information and new versions visit to;<br>")
        developers = _("<p>Developers;<br>")
        translators = _("<p>Translated by;<br>")
        copying =  _("<p>This program released under  \
                    the terms of the GNU General Public \
                    License. Please read COPYING file</p>")
        abouttext = description+"<a href="+const.WEBPAGE+">"+const.WEBPAGE+"</a></p>"
        abouttext += copying
        abouttext += developers + const.DEVELOPERS + "</p>"
        abouttext += translators + const.TRANSLATORS + "</p>"
        self.__aboutDialog.textBrowser.setText(abouttext)
        self.__aboutDialog.label.setText( const.NAME )
        self.__aboutDialog.label_2.setText( const.VERSION )

        #Options Dialog
        self.__optionsDialog.setWindowTitle( self.pushButton_8.text())
        self.__optionsDialog.groupBox.setTitle( _("User"))
        self.__optionsDialog.label.setText( _("Full name") )
        self.__optionsDialog.label_2.setText( _("E-mail") )
        self.__optionsDialog.pushButton_2.setText( _("Save") )
        self.__optionsDialog.pushButton.setText( _("Cancel") )

        #Error messages
        self.__errDesc[const.ERR_01_ID] = _("Directory or file not found")
        self.__errDesc[const.ERR_02_ID] = _("Bad xml structure")
        self.__errDesc[const.ERR_03_ID] = _("User break")
        self.__errDesc[const.ERR_04_ID] = _("Package not found")
        self.__errDesc[const.ERR_05_ID] = _("File not created")
        self.__errDesc[const.ERR_06_ID] = _("Bad paso info")
        self.__errDesc[const.ERR_07_ID] = _("Paso file corrupted")
        self.__errDesc[const.ERR_08_ID] = _("HTTP Error")
        self.__errDesc[const.ERR_09_ID] = _("ISO image not craeted")
        self.__errDesc[const.ERR_10_ID] = _("Configuration not loaded")
        self.__errDesc[const.ERR_11_ID] = _("running for the first time")
        self.__errDesc[const.ERR_12_ID] = _("Configuration not saved")
        self.__errDesc[const.ERR_13_ID] = _("ISO image not converted to hybrid")

