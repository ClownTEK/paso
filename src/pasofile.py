#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#Author: Read AUTHORS file.
#License: Read COPYING file.


import lib
from constants import const
from lib import eventHandler
import os
import tarfile
import time





class pasoFile(object):
    #.paso file operatinos, bulid, extract, get info etc.
    #.paso file is actually tar.gz file
    #It contains a package.txt file and some pisi packages if necessary for bulid
    #Unfotunately package.txt does not have full information yet, just package names and urls      #NEEDS DEVELOPING
    #I imagine that will be an xml file
    #Current file format like this: "package filename = package url" :)




    def __init__(self):
        self.__clear()
        self.onAddPackage = eventHandler()      #(elementName, totalElements, currentElement)
        self.onError = eventHandler()           #( errorCode, errorData)




    def __clear(self):
        self.__path = ""
        self.__targetName = ""
        self.__sourceName = ""
        self.__listRawData = ""
        self.__listFull = {}
        self.__pasoRepo = []
        self.__break = False







    def create(self, outFile, listFull, altList, altDir):
        #
        self.__clear()
        jobList = {}    #{"packageName": "Full Uri"}
        if outFile:
            self.__path = outFile.strip(lib.stripFilename(outFile))
            self.__targetName = outFile
        else:
            return()
        print self.__path, self.__targetName
        listFile = self.__path+const.PASO_DATAFILE_VAL
        #Convert dict to paso format
        self.__listRawData = self.__buildData(listFull)
        self.onAddPackage.raiseEvent(listFile, 1, 0)
        #Save
        if lib.savefile(listFile, self.__listRawData) > 0:
            self.onError.raiseEvent( const.ERR_05_ID, listFile)
            return(False)
        self.onAddPackage.raiseEvent(self.__targetName, 1, 0)
        #Create paso file (tar.gz file)
        try:
            target = tarfile.open(self.__targetName, 'w:gz')
        except:
            self.onError.raiseEvent( const.ERR_05_ID, self.__targetName)
            return(False)
        #Add packages.txt to list
        jobList[const.PASO_DATAFILE_VAL] = listFile
        #Add pisi files to list
        for package in altList:
            jobList[package] = altDir+"/"+package
        #Add files to paso file
        if not self.__addPackages(target, jobList):
            return(False)






    def __addPackages(self, target, packageList):
        #
        totalJob = len(packageList)
        jobPos = 1
        for package in packageList.keys():
            self.onAddPackage.raiseEvent(packageList[package], totalJob, jobPos)
            try:
                target.add(packageList[package], package, False)
            except:
                self.onError.raiseEvent( const.ERR_05_ID, packageList[package])
                return(False)
            jobPos += 1
        target.close()
        os.unlink(packageList[const.PASO_DATAFILE_VAL])






    def __buildData(self, listFull):
        #
        result = ""
        for package in listFull.keys():
            result += package+"="+listFull[package]+"\n"
        return(result)


    def getTargetName(self):
        return( self.__targetName)



    def getSourceName(self):
        return( self.__sourceName)




    def loadInfo(self, source):
        #source=paso file (tar.gz)
        self.__clear()
        self.__sourceName = source
        self.onAddPackage.raiseEvent(self.__targetName, 100, 1)
        #Open and load file list
        try:
            source = tarfile.open(self.__sourceName)
            self.__getRepoList(source)
        except:
            self.onError.raiseEvent( const.ERR_01_ID, self.__sourceName)
            return(False)
        self.onAddPackage.raiseEvent("paso info", 100, 1)
        #Extract packages.txt
        try:
            packagesTar = source.extractfile(const.PASO_DATAFILE_VAL)
        except:
            self.onError.raiseEvent(const.ERR_05_ID, const.PASO_DATAFILE_VAL)
            return(False)
        #Parse txt to __listFull dict
        if not self.__parseInfo(packagesTar):
            return(False)
        try:    tarfile.close()
        except: pass
        return(True)




    def __getRepoList(self, source):
        #
        for tarinfo in source:
            if tarinfo.name != const.PASO_DATAFILE_VAL:
                self.onAddPackage.raiseEvent(tarinfo.name, 100, 1)
                self.__pasoRepo.append(tarinfo.name)




    def __parseInfo(self, packagesTar):
        #
        pos = 1
        try:
            lines = packagesTar.readlines()
        except:
            self.onError.raiseEvent( const.ERR_06_ID, const.PASO_DATAFILE_VAL)
            return(False)
        for line in lines:
            p = line.split("=")
            self.__listFull[ p[0] ] = p[1].strip()
            self.onAddPackage.raiseEvent(p[0], len(lines), pos)
            pos += 1
        return(True)




    def getFullList(self):
        return(self.__listFull.keys())




    def getURL(self, key):
        return(self.__listFull[key])



    def isOn(self, package):
        if package in self.__pasoRepo:   return( True)
        else:   return( False)


    def isInfoEmpty(self):
        if len(self.__listFull) > 0:    return(False)
        else:                           return(True)


