#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#Author: Read AUTHORS file.
#License: Read COPYING file.

#from xml.dom.minidom import parseString
import lib
from constants import const
from lib import eventHandler
import os
import tarfile
import urllib2




class repoBuilder(object):
    #Build CD repo, collect the packages from Pardus repositories,
    #local directories and source paso file




    def __init__(self):
        self.clear()
        self.onAddPackage = eventHandler()      #(elementName, totalElements, currentElement)
        self.onError = eventHandler()           #( errorCode, errorData)




    def clear(self):
        self.__target = ""
        self.__break = False







    def build(self, alz, out, source):
        #
        self.clear()
        currentPackage = 0
        totalPackage = alz.getCountOfLocals() + alz.getCountOfRemotes() + 1
        sourceName = lib.stripFilename(source, const.PASO_EXT)
        self.__target = self.__openDirs( out, sourceName)
        if not self.__target:  return(False)
        #Copy local packages to repo
        for package in alz.getLocalPackages():
            currentPackage += 1
            packageUri = alz.getLocalPath(package)+"/"+package
            if alz.getLocalPath(package) == source:     #In paso file
                self.onAddPackage.raiseEvent(package+" in "+lib.stripFilename(source), totalPackage, currentPackage)
                if not self.__extractPaso(source, package):
                    return(False)
            elif os.path.isfile(packageUri):
                self.onAddPackage.raiseEvent(packageUri, totalPackage, currentPackage)
                if not self.__cpFile(packageUri):
                    return(False)
            else:
                self.onError.raiseEvent( const.ERR_01_ID, alz.getLocalPath(package))
                return(False)
        #Download remote packages
        for package in alz.getRemotePackages():
            currentPackage += 1
            packageUrl = alz.getRemoteURL(package)+package
            self.onAddPackage.raiseEvent(packageUrl, totalPackage, currentPackage)
            if not self.__download(packageUrl):
                return(False)
        #Build repo index
        self.onAddPackage.raiseEvent("pisi-index.xml", totalPackage, totalPackage)
        self.__buildIndex()





    def __openDirs(self, out, path):
        #
        repoPath = out+"/"+path+const.OPT_CDREPOPATH_VAL
        if not os.path.isdir(out+"/"+path):
            self.onAddPackage.raiseEvent(out+"/"+path, 100, 1)
            try:
                if not os.path.isdir(out+"/"+path):
                    os.mkdir(out+"/"+path)
                if not os.path.isdir(repoPath):
                    try:
                        os.mkdir(repoPath)
                    except:
                        self.onError.raiseEvent( const.ERR_05_ID, repoPath)
                        return(False)
            except:
                self.onError.raiseEvent( const.ERR_05_ID, out+"/"+path)
                return(False)
        return( repoPath )








    def __cpFile(self, source):
        #
        if not os.path.isfile(self.__target+"/"+lib.stripFilename(source)):
            cmd = "/bin/cp "+source+" "+self.__target
            if os.system(cmd) > 0:
                self.onError.raiseEvent( const.ERR_05_ID, cmd)
                return(False)
        return(True)







    def __extractPaso(self, sourceFile, package):
        #
        if not os.path.isfile(self.__target+"/"+package):
            try:
                source = tarfile.open(sourceFile)
            except:
                self.onError.raiseEvent( const.ERR_01_ID, sourceFile)
                return(False)
            try:
                source.extract(package, self.__target)
            except:
                self.onError.raiseEvent( const.ERR_01_ID, sourceFile+":"+package)
                return(False)
            if not os.path.isfile(self.__target+"/"+package):
                self.onError.raiseEvent( const.ERR_01_ID, self.__target+"/"+package)
                return(False)
        return(True)






    def __download(self, url):
        #
        targetFile = self.__target+"/"+lib.stripFilename(url)
        if not os.path.isfile(self.__target+"/"+lib.stripFilename(url) ):
            try:
                remote = urllib2.urlopen(url)
            except:
                self.onError.raiseEvent( const.ERR_08_ID, url)
                return(False)
            try:
                if lib.savefile(targetFile+".part", remote.read()) == False:
                    self.onError.raiseEvent( const.ERR_05_ID, targetFile)
                    return(False)
            except:
                self.onError.raiseEvent( const.ERR_08_ID, url)
                return(False)
            cmd = "mv "+targetFile+".part "+targetFile
            if os.system(cmd) > 0:
                self.onError.raiseEvent( const.ERR_05_ID, targetFile)
                return(False)
        return(True)






    def __buildIndex(self):
        #
        os.chdir(self.__target)
        cmd = "pisi ix --skip-signing"
        if os.system(cmd) > 0:
                self.onError.raiseEvent( const.ERR_05_ID, self.__target+"/pisi-index.xml.bz2")
                return(False)
        os.system("/bin/rm pisi-index.xml")
        os.system("/bin/rm pisi-index.xml.sha1sum")
        return(True)





    def getTarget(self):
        return( self.__target )


