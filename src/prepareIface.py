#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#Author: Read AUTHORS file.
#License: Read COPYING file.

import os

import lib
from constants import const
from lib import eventHandler
from installed import installed
from repos import repos
from packagedir import packageDir
from pasofile import pasoFile





class pIface():
    #Interface class between prepare operation modules and GUI


    onCrazy = eventHandler()      #(elementName, totalElements, currentElement)
    onError = eventHandler()           #(errorCode, errorData)

    def __init__(self):
        #
        self.__ins = installed()
        self.__rep = repos()
        self.__iso = packageDir()
        self.__alt = packageDir()
        self.__pas = pasoFile()
        self.__clear()
        self.__newMission()

        #Events
        self.__ins.onAddPackage.addEventListener(self.__onProgress)
        self.__ins.onError.addEventListener(self.__onError)
        self.__rep.onAddPackage.addEventListener(self.__onProgress)
        self.__rep.onError.addEventListener(self.__onError)
        self.__iso.onAddPackage.addEventListener(self.__onProgress)
        self.__iso.onError.addEventListener(self.__onError)
        self.__alt.onAddPackage.addEventListener(self.__onProgress)
        self.__alt.onError.addEventListener(self.__onError)
        self.__pas.onAddPackage.addEventListener(self.__onProgress)
        self.__pas.onError.addEventListener(self.__onError)


    def __clear(self):
        self.__options = {const.OPT_ISODIRCHECK_ID:False,
                            const.OPT_ALTDIRCHECK_ID:False,
                            const.OPT_READINSCHECK_ID:False,
                            const.OPT_READREPOCHECK_ID:False,
                            const.OPT_ROOTDIR_ID:"",
                            const.OPT_PASOFILE_ID:"",
                            const.OPT_ISODIR_ID:"",
                            const.OPT_ALTDIR_ID:""}




    def __newMission(self):
        self.__currentJob = const.JOB_NONE_ID
        self.__totalJob = 0
        self.__passedJob = 0
        self.__error = False
        self.__resourceList = {}        #{"packageUri": "httpUrl" or ""} Full list
        self.__isoList = []             #["packageUri",...]
        self.__altList = []             #["packageUri",...]







    def getcwd(self):           #FIX it with conf file support
        return( os.getcwd() )


    def getroot(self):          #FIX it with conf file support
        return( "/" )









    def setOptions(self, key, value):
        self.__options[key] = value


    def setDir(self, key, value):
        self.__dirs[key] = value










    def got_to_crazy(self):
        #
        doReadInstalled = True
        doReadRepos = True
        doReadIso = True
        doReadAlt = True

        self.__newMission()

        #Find job count and update task list
        if not self.__options[const.OPT_READINSCHECK_ID] or self.__ins.isEmpty():   self.__totalJob += 1
        else:   doReadInstalled = False
        if not self.__options[const.OPT_READREPOCHECK_ID] or self.__rep.isEmpty():  self.__totalJob += 1
        else:   doReadRepos = False
        if self.__options[const.OPT_ISODIRCHECK_ID]:   self.__totalJob += 1
        else:   doReadIso = False
        if self.__options[const.OPT_ALTDIRCHECK_ID]:   self.__totalJob += 1
        else: doReadAlt = False
        self.__totalJob += 2    #__buildResources & __pas.create

        #Load installed package job
        if doReadInstalled and not self.__error:
            self.__passedJob += 1
            self.__currentJob = const.JOB_INS_ID
            self.__ins.load(self.__options[const.OPT_ROOTDIR_ID]+const.OPT_PACKPATH_VAL)
        #Load repos
        if doReadRepos and not self.__error:
            self.__passedJob += 1
            self.__currentJob = const.JOB_REP_ID
            self.__rep.load(self.__options[const.OPT_ROOTDIR_ID]+const.OPT_INFOPATH_VAL, self.__options[const.OPT_ROOTDIR_ID]+const.OPT_INDEXPATH_VAL)
        #Load iso packages dir
        if doReadIso and not self.__error:
            self.__passedJob += 1
            self.__currentJob = const.JOB_ISO_ID
            self.__iso.load(self.__options[const.OPT_ISODIR_ID]+const.OPT_CDREPOPATH_VAL)
        #Load alternate packages dir
        if doReadAlt and not self.__error:
            self.__passedJob += 1
            self.__currentJob = const.JOB_ALT_ID
            self.__alt.load(self.__options[const.OPT_ALTDIR_ID])
        #Build resource list
        if not self.__error:
            self.__passedJob += 1
            self.__currentJob = const.JOB_RES_ID
            self.__buildResources()
        #Create .paso file
        if not self.__error:
            self.__passedJob += 1
            self.__currentJob = const.JOB_PAS_ID
            self.__pas.create(self.__options[const.OPT_PASOFILE_ID], self.__resourceList, self.__altList, self.__options[const.OPT_ALTDIR_ID])
        if not self.__error:
            self.__onProgress(self.__pas.getTargetName(), 100, 100)






    def __onProgress(self, elementName, totalElements, currentElement):
        #
        self.onCrazy.raiseEvent(self.__totalJob,
                                self.__passedJob,
                                int(totalElements),
                                int(currentElement),
                                self.__currentJob,
                                str(elementName))



    def __onError(self, errorCode, errorData):
        #
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
            elif isoUri:
                self.__isoList.append(packageUri)
                self.__onProgress(packageUri+" found on "+self.__iso.get_path(), len(packages), pos)
            elif altUri:
                self.__altList.append(packageUri)
                self.__onProgress(packageUri+" found on "+self.__alt.get_path(), len(packages), pos)
            else:
                self.__onError( const.ERR_04_ID, packageUri)
                break
            pos += 1