#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#Author: Read AUTHORS file.
#License: Read COPYING file.

import os
import lib
from constants import const
from lib import eventHandler
from pasofile import pasoFile
from packagedir import packageDir
from analyze import analyze
from repobuilder import repoBuilder
from isobuilder import isoBuilder





class bIface():
    #Interface class between build operation modules and GUI

    onAction = eventHandler()    #(totalJobs, currentJob, totalElements, currentElement, jobName, elementName)
    onError = eventHandler()    #(errorCode, errorData)


    def __init__(self):
        #
        self.__pao = pasoFile()
        self.__iso = packageDir()
        self.__alt = packageDir()
        self.__chc = packageDir()
        self.__alz = analyze()
        self.__brp = repoBuilder()
        self.__bis = isoBuilder()
        self.__clear()
        self.__newMission()


        #Events
        self.__pao.onAddPackage.addEventListener(self.__onProgress)
        self.__pao.onError.addEventListener(self.__onError)
        self.__iso.onAddPackage.addEventListener(self.__onProgress)
        self.__iso.onError.addEventListener(self.__onError)
        self.__alt.onAddPackage.addEventListener(self.__onProgress)
        self.__alt.onError.addEventListener(self.__onError)
        self.__chc.onAddPackage.addEventListener(self.__onProgress)
        self.__chc.onError.addEventListener(self.__onError)
        self.__alz.onAddPackage.addEventListener(self.__onProgress)
        self.__alz.onError.addEventListener(self.__onError)
        self.__brp.onAddPackage.addEventListener(self.__onProgress)
        self.__brp.onError.addEventListener(self.__onError)
        self.__bis.onAddPackage.addEventListener(self.__onProgress)
        self.__bis.onError.addEventListener(self.__onError)



    def __clear(self):
        self.__options = {const.OPT_ALTDIRCHECK_ID:False,
                            const.OPT_ISODIR_ID:"",
                            const.OPT_PASOFILE_ID:"",
                            const.OPT_OUTDIR_ID:"",
                            const.OPT_ALTDIR_ID:"",
                            const.OPT_FORCEPASOREAD_ID: False,
                            const.OPT_FORCEALTREAD_ID: False,
                            const.OPT_FORCECDREAD_ID: False}




    def __newMission(self):
        self.__currentJob = const.JOB_NONE_ID
        self.__totalJob = 0
        self.__passedJob = 0
        self.__error = False







    def getcwd(self):           #FIX it with conf file support
        return( os.getcwd() )


    def getroot(self):          #FIX it with conf file support
        return( "/" )









    def setOptions(self, key, value):
        self.__options[key] = value


    def setDir(self, key, value):
        self.__dirs[key] = value








################################################################################
#
#   ANALYZE SECTION
#
################################################################################
    def doAnalyze(self):
        #
        doReadAlt = True
        doReadPaso = True
        doReadIso = True
        self.__newMission()

        #Find job count and update task list
        if self.__options[const.OPT_ALTDIRCHECK_ID] and \
                            (self.__alt.isEmpty() or not self.__options[const.OPT_READALTCHECK_ID] ) \
                            or self.__options[const.OPT_FORCEALTREAD_ID]:
            self.__totalJob += 1
        else:   doReadAlt = False
        if self.__pao.isInfoEmpty() or not self.__options[const.OPT_READPASOCHECK_ID] \
                                     or self.__options[const.OPT_FORCEPASOREAD_ID]:
            self.__totalJob += 1
        else:   doReadPaso = False
        if self.__iso.isEmpty() or self.__options[const.OPT_FORCECDREAD_ID]:
            self.__totalJob += 1
        else: doReadIso = False

        self.__totalJob += 2    # __chc.load(), __alz.analyze()

        self.__chc.clear()

        if doReadPaso and not self.__error:
            self.__passedJob += 1
            self.__currentJob = const.JOB_PAO_ID
            self.__pao.loadInfo(self.__options[const.OPT_PASOFILE_ID])
        if doReadIso and not self.__error:
            self.__passedJob += 1
            self.__currentJob = const.JOB_ISO_ID
            self.__iso.load(self.__options[const.OPT_ISODIR_ID]+const.OPT_CDREPOPATH_VAL)
        if doReadAlt and not self.__error:
            self.__passedJob += 1
            self.__currentJob = const.JOB_ALT_ID
            self.__alt.load(self.__options[const.OPT_ALTDIR_ID])
        if not self.__error:
            self.__passedJob += 1
            self.__currentJob = const.JOB_CHC_ID
            self.__chc.load(const.OPT_CACHEPATH_VAL)
        if not self.__error:
            self.__passedJob += 1
            self.__currentJob = const.JOB_ALZ_ID
            self.__alz.analyze(self.__pao, self.__iso, self.__alt, self.__chc)
















################################################################################
#
#   BUILD SECTION
#
################################################################################
    def build(self):
        #
        self.__newMission()

        self.__totalJob += 2

        #Build iso repo
        if not self.__error:
            self.__passedJob += 1
            self.__currentJob = const.JOB_BRP_ID
            self.__brp.build(self.__alz, self.__options[const.OPT_OUTDIR_ID], self.__options[const.OPT_PASOFILE_ID])
        if not self.__error:
            self.__passedJob += 1
            self.__currentJob = const.JOB_BIS_ID
            self.__bis.build( self.__options[const.OPT_PASOFILE_ID], self.__options[const.OPT_OUTDIR_ID], self.__options[const.OPT_ISODIR_ID])


















    def __onProgress(self, elementName, totalElements, currentElement):
        #
        self.onAction.raiseEvent(self.__totalJob,
                                self.__passedJob,
                                int(totalElements),
                                int(currentElement),
                                self.__currentJob,
                                str(elementName))



    def __onError(self, errorCode, errorData):
        self.__error = True
        self.onError.raiseEvent(self.__currentJob, errorCode, errorData)













    #Prepare lists _________________________________________________
    def __buildResources(self):
        #
        pos = 1
        packages = self.__ins.getPackageList()
        for package in packages:
            packageUri = self.__ins.getPackageUri(package)
            self.__resourceList[packageUri] = ""
            #Search
            repoUri = self.__rep.get_repo_uri(package)
            isoUri = self.__iso.is_on(packageUri)
            altUri = self.__alt.is_on(packageUri)
            #Build Lists
            if repoUri:
                self.__resourceList[packageUri] = repoUri
                self.__onProgress(packageUri+" found on "+self.__rep.get_package_repo(package)+" repo", len(packages), pos)
            if isoUri:
                self.__isoList.append(packageUri)
                self.__onProgress(packageUri+" found on "+self.__iso.get_path(), len(packages), pos)
            if altUri:
                self.__altList.append(packageUri)
                self.__onProgress(packageUri+" found on "+self.__alt.get_path(), len(packages), pos)
            if not repoUri and not isoUri and not altUri:
                self.__onError( const.ERR_04_ID, packageUri)
                break
            pos += 1