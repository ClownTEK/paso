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
from pasodata import pasoMetadata






class pIface(object):
    #Interface class between prepare operation modules and GUI




    def __init__(self):
        #
        self.error = False
        self.__ins = installed(self)
        self.__rep = repos(self)
        self.__iso = packageDir(self)
        self.__alt = packageDir(self)
        self.__pas = pasoFile(self)
        self.__clear()
        self.__newMission()

        #Events
        self.onCrazy = eventHandler()      #(elementName, totalElements, currentElement)
        self.onError = eventHandler()           #(errorCode, errorData)

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
        self.pasoMetadata = pasoMetadata()
        self.isoDirCheck = False
        self.altDirCheck = False
        self.readInsCheck = False
        self.readRepoCheck = False
        self.rootDir = ""
        self.pasoFile = ""
        self.isoDir = ""
        self.altDir = ""





    def __newMission(self):
        self.__currentJob = const.JOB_NONE_ID
        self.__totalJob = 0
        self.__passedJob = 0
        self.error = False
        self.__resourceList = {}        #{"packageUri": "repoName" or "" } Full list
        self.__isoList = []             #["packageUri",...]
        self.__altList = []             #["packageUri",...]
        self.__repoList = {}            #{"repoName": "httpUrl", }




    def stopProgress(self):
        self.error = True





    def getcwd(self):           #FIX it with conf file support
        return( os.getcwd() )


    def getroot(self):          #FIX it with conf file support
        return( "/" )









    def setOptions(self, key, value):
        self.__options[key] = value


    def setDir(self, key, value):
        self.__dirs[key] = value





    def getInfo(self, filename):
        #
        self.__currentJob = const.JOB_PAO_ID
        self.__totalJob = 1
        self.__passedJob = 1
        if self.__pas.open(filename):
            return( self.__pas.getInfo() )
        return(False)




    def getPrepareInfo(self):
        return(self.__pas.getInfo())




    def go_to_crazy(self):
        #
        doReadInstalled = True
        doReadRepos = True
        doReadIso = True
        doReadAlt = True
        self.__newMission()

        #Find job count and update task list
        if not self.readInsCheck or self.__ins.isEmpty():   self.__totalJob += 1
        else:   doReadInstalled = False
        if not self.readRepoCheck or self.__rep.isEmpty():  self.__totalJob += 1
        else:   doReadRepos = False
        if self.isoDirCheck:   self.__totalJob += 1
        else:   doReadIso = False
        if self.altDirCheck:   self.__totalJob += 1
        else: doReadAlt = False
        self.__totalJob += 2    #__buildResources & __pas.create

        #Load installed package job
        if doReadInstalled and not self.error:
            self.__passedJob += 1
            self.__currentJob = const.JOB_INS_ID
            self.__ins.load(self.rootDir+const.OPT_PACKPATH_VAL)
        #Load repos
        if doReadRepos and not self.error:
            self.__passedJob += 1
            self.__currentJob = const.JOB_REP_ID
            self.__rep.load(self.rootDir+const.OPT_INFOPATH_VAL, self.rootDir+const.OPT_INDEXPATH_VAL)
        #Load iso packages dir
        if doReadIso and not self.error:
            self.__passedJob += 1
            self.__currentJob = const.JOB_ISO_ID
            self.__iso.load(self.isoFile+const.OPT_CDREPOPATH_VAL)
        #Load alternate packages dir
        if doReadAlt and not self.error:
            self.__passedJob += 1
            self.__currentJob = const.JOB_ALT_ID
            self.__alt.load(self.altDir)
        #Build resource list
        if not self.error:
            self.__passedJob += 1
            self.__currentJob = const.JOB_RES_ID
            self.__buildResources()
        #Create .paso file
        if not self.error:
            self.__passedJob += 1
            self.__currentJob = const.JOB_PAS_ID
            self.__pas.create(self.pasoFile, \
                                self.__resourceList, \
                                self.__alt, self.__altList, self.altDir, \
                                self.__iso, self.__isoList, self.isoDir, \
                                self.__repoList, self.pasoMetadata, \
                                self.__rep)

        if not self.error:
            self.__onProgress(self.__pas.getFileName(), 100, 100)





    def updateInfo(self):
        self.__pas.updateInfo(self.pasoFile, self.pasoMetadata)




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
        self.error = True
        self.onError.raiseEvent(self.__currentJob, errorCode, errorData)













    #Prepare lists _________________________________________________
    def __buildResources(self):
        #
        pos = 1
        packages = self.__ins.getPackageList()
        self.__repoList = self.__rep.get_repos()
        for package in packages:
            if self.error:
                self.__onError(const.ERR_03_ID, "")
                break
            packageUri = self.__ins.getPackageUri(package)
            self.__resourceList[packageUri] = ""
            #Search
            repo = self.__rep.get_package_repo(package)
            isoUri = self.__iso.is_on(packageUri)
            altUri = self.__alt.is_on(packageUri)
            #Build Lists
            if repo:
                self.__resourceList[packageUri] = repo
                self.__onProgress(packageUri+" found on "+repo+" repo", len(packages), pos)
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







