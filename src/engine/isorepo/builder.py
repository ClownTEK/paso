#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#Author: Read AUTHORS file.
#License: Read COPYING file.



import xml.etree.cElementTree as etree
import os
from os import path, makedirs
from constants import const
from ..lib import eventHandler,  savefile, getfile, ratioCalc
from urllib2 import urlopen
from shutil import copy, move








class pkgInfo(object):


    def __init__(self):
        self.package = ""
        self.__path = ""
        self.__http = False
        self.local = False




    def setpath(self, p):
        self.__path = p
        if p[:len(const.REMOTE_HTTP)] == const.REMOTE_HTTP:
            self.__http = True
            self.local = False
        else:
            self.__http = False
            self.local = True



    def getpath(self):
        return(self.__path)



    path = property(getpath, setpath)








class isorepo(object):





    def __init__(self, actCode):
        self.__clear()
        self.onError = eventHandler()       #(ActionCode, Error code, data)
        self.onProcessing = eventHandler()   #(ActionCode, ProcessRatio, data)
        self.__actCode = actCode





    def __clear(self):
        self.right = True
        self.__path = ""
        self.__localURLs = []
        self.__remoteURLs = []




    def __clearReport(self):
        self.__reportLocalPackage = 0
        self.__reportRemotePackage = 0
        self.__reportRemoteSize = 0
        self.__reportLocalSize = 0
        self.__reportReadyPackage = 0
        self.__reportNotFoundPackage = 0
        self.__reportNotFoundPackages = []





    def setLocalURLs(self, urls):
        self.__localURLs = urls




    def setRemoteURLs(self, urls):
        self.__remoteURLs = urls





    def getRemoteURLs(self):
        return(self.__remoteURLs)




    def getLocalURLs(self):
        return(self.__localURLs)




    def setTarget(self, pth):
        self.__path = path.normpath(pth)





    '''def build(self, allPackages, mode=ACTIVE_MODE):
        self.__clearReport()
        self.__mode = mode
        if not self.__makeDirs():
            self.onError.raiseEvent( self.__actCode, "01", "" )
            return(False)
        remotePackages = []
        packageCount = len(allPackages)
        currentPackage = 0
        for package in allPackages:
            self.onProcessing.raiseEvent(self.__actCode, ratioCalc(packageCount, currentPackage), package)
            if not self.__isOnRepo(package):
                packagePath = self.__isLocalPackage(package)
                if packagePath:
                    self.__reportLocalPackage += 1
                    if not self.__cpLocalPackage(packagePath, package):
                        self.onError.raiseEvent( self.__actCode, "02",  path.join(packagePath, package) )
                else:
                    packagePath = self.__isRemotePackage(package)
                    if packagePath:
                        self.__reportRemotePackage += 1
                        if not self.__cpRemotePackage(packagePath, package):
                            self.onError.raiseEvent( self.__actCode, "03",  path.join(packagePath, package) )
                    else:
                        self.__reportNotFoundPackage += 1
                        self.__reportNotFoundPackages.append(package)
            else:
                self.__reportReadyPackage += 1
            currentPackage += 1
        return(True)'''





    def search(self, package):
        pkg = pkgInfo()
        pkg.package = package
        if not self.__isOnRepo(package):
            packagePath = self.__isLocalPackage(package)
            if packagePath:
                pkg.path = packagePath
            else:
                packagePath = self.__isRemotePackage(package)
                if packagePath:
                    pkg.path = packagePath
                else:
                    return(False)
        return(pkg)








    def __isOnRepo(self, package):
        if path.isfile( path.join(self.__path, package) ):
            return(True)
        else:
            return(False)





    def __isLocalPackage(self, package):
        for p in self.__localURLs:
            if path.isfile( path.join(p, package) ):
                return(p)
        return(False)






    def __isRemotePackage(self, package):
        for p in self.__remoteURLs:
            try:
                urlopen( path.join(p,package))
                return(p)
            except:
                pass
        return(False)





    def __cpLocalPackage(self, packagePath, package):
        try:
            copy( path.join(packagePath, package), self.__path )
        except:
            return(False)
        return(True)




    def __cpRemotePackage(self, packagePath, package):
        f = path.join(self.__path, package)
        try:
            h = urlopen( path.join(packagePath, package) )
            if not savefile( f+const.DOWNLOADING_EXT, h.read()):
                return(False)
            move( f+const.DOWNLOADING_EXT, f )
        except:
            return(False)
        return(True)




    def cpPackage(self, pkg=pkgInfo() ):
        if pkg.local:
            return(self.__cpLocalPackage(pkg.path, pkg.package))
        else:
            return(self.__cpRemotePackage(pkg.path, pkg.package))





    def buildRepoIndex(self):
        os.chdir(self.__path)
        if os.system(const.PISI_BUILD_INDEX_CMD) > 0:
            return(False)
        os.unlink(const.PISI_INDEX_XML_FILE)
        os.unlink(const.PISI_INDEX_SHA1SUM_FILE)
        return(True)


