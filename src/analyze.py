#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#Author: Read AUTHORS file.
#License: Read COPYING file.


import lib
from constants import const
from lib import eventHandler
import os







class analyze(object):
    #This class searches the installed packages within resources
    #Resoruces consist of CD repo, pisi cache, paso file and alternative files
    #If found on resources add to __localPackages dict with its path
    #else, add to __remotePackages dict with its repo url
    #Count




    def __init__(self, parentObj):
        self.__clear()
        self.onAddPackage = eventHandler()      #(elementName, totalElements, currentElement)
        self.onError = eventHandler()           #( errorCode, errorData)
        self.parent = parentObj





    def __clear(self):
        self.__remotePackages = {}               #{"packagename":"URL"}
        self.__localPackages = {}                #{"packagename":"Path"}
        self.__totalSize = 0
        self.__downloadSize = 0
        self.__installerSize = 0
        self.__sourceName = ""





    def analyze(self, pasoObject, isoObject, altObject, chcObject):
        #
        self.__clear()
        total = len( pasoObject.getPackageList() )
        for package in pasoObject.getPackageList():
            if self.parent.error:
                self.__clear()
                print "YES"
                self.onError.raiseEvent(const.ERR_03_ID, "")
                return(False)
            self.__totalSize += int(pasoObject.getSize(package))
            if pasoObject.isOn(package):
                self.__localPackages[package] = pasoObject.getPasoFileName()
                self.onAddPackage.raiseEvent(package+" => "+pasoObject.getPasoFileName(), total, len(self.__localPackages) + len(self.__remotePackages))
            elif isoObject.is_on(package):
                self.__localPackages[package] = isoObject.get_path()
                self.onAddPackage.raiseEvent(package+" => "+isoObject.get_path(), total, len(self.__localPackages) + len(self.__remotePackages))
            elif altObject.is_on(package):
                self.__localPackages[package] = altObject.get_path()
                self.onAddPackage.raiseEvent(package+" => "+altObject.get_path(), total, len(self.__localPackages) + len(self.__remotePackages))
            elif chcObject.is_on(package):
                self.__localPackages[package] = chcObject.get_path()
                self.onAddPackage.raiseEvent(package+" => "+chcObject.get_path(), total, len(self.__localPackages) + len(self.__remotePackages))
            elif pasoObject.getPackageUrl(package) == "":
                self.onError.raiseEvent( const.ERR_01_ID, package)
                return(False)
            else:
                self.__downloadSize += int(pasoObject.getSize(package))
                self.__remotePackages[package] = pasoObject.getPackageUrl(package)
                self.onAddPackage.raiseEvent(package+"=>"+pasoObject.getPackageUrl(package), total, len(self.__localPackages) + len(self.__remotePackages))
        installerFiles = []
        isoRoot = lib.stripPath( isoObject.get_path() )
        for f in const.ISOINSTALLER_FILES:
            installerFiles.append(isoRoot+"/"+f)
        self.__installerSize = lib.getSizeOfFiles(installerFiles)
        return(True)





    def getCountOfRemotes(self):
        return(len(self.__remotePackages))




    def getCountOfLocals(self):
        return(len(self.__localPackages))




    def getCountOfPackages(self):
        return( self.getCountOfLocals() + self.getCountOfRemotes() )




    def getSizeOfRemotes(self):
        return(self.__downloadSize)




    def getSizeOfTotal(self):
        return(self.__totalSize)



    def getSizeOfISO(self):
        return( self.getSizeOfTotal() + self.__installerSize)



    def getLocalPackages(self):
        return( self.__localPackages.keys() )




    def getRemotePackages(self):
        return( self.__remotePackages.keys())




    def getLocalPath(self, package):
        return( self.__localPackages[package] )




    def getRemoteURL(self, package):
        return( self.__remotePackages[package] )




