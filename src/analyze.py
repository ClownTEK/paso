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




    def __init__(self):
        self.__clear()
        self.onAddPackage = eventHandler()      #(elementName, totalElements, currentElement)
        self.onError = eventHandler()           #( errorCode, errorData)





    def __clear(self):
        self.__remotePackages = {}               #{"packagename":"URL"}
        self.__localPackages = {}                #{"packagename":"Path"}
        self.__sourceName = ""
        self.__break = False




    def analyze(self, pasoObject, isoObject, altObject, chcObject):
        #
        self.__clear()
        total = len( pasoObject.getFullList() )
        for package in pasoObject.getFullList():
            if pasoObject.isOn(package):
                self.__localPackages[package] = pasoObject.getSourceName()
                self.onAddPackage.raiseEvent(package+" => "+pasoObject.getSourceName(), total, len(self.__localPackages) + len(self.__remotePackages))
            elif isoObject.is_on(package):
                self.__localPackages[package] = isoObject.get_path()
                self.onAddPackage.raiseEvent(package+" => "+isoObject.get_path(), total, len(self.__localPackages) + len(self.__remotePackages))
            elif altObject.is_on(package):
                self.__localPackages[package] = altObject.get_path()
                self.onAddPackage.raiseEvent(package+" => "+altObject.get_path(), total, len(self.__localPackages) + len(self.__remotePackages))
            elif chcObject.is_on(package):
                self.__localPackages[package] = chcObject.get_path()
                self.onAddPackage.raiseEvent(package+" => "+chcObject.get_path(), total, len(self.__localPackages) + len(self.__remotePackages))
            elif pasoObject.getURL(package) == "":
                self.onError.raiseEvent( const.ERR_01_ID, package)
                return(False)
            else:
                self.__remotePackages[package] = pasoObject.getURL(package)
                self.onAddPackage.raiseEvent(package+"=>"+pasoObject.getURL(package), total, len(self.__localPackages) + len(self.__remotePackages))
        return(True)





    def getCountOfRemotes(self):
        return(len(self.__remotePackages))



    def getCountOfLocals(self):
        return(len(self.__localPackages))


    def getLocalPackages(self):
        return( self.__localPackages.keys() )


    def getRemotePackages(self):
        return( self.__remotePackages.keys())

    def getLocalPath(self, package):
        return( self.__localPackages[package] )

    def getRemoteURL(self, package):
        return( self.__remotePackages[package] )




