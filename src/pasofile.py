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
from pasodata import pasoMetadata
from pasodata import pasoFiles





class pasoFile(object):
    #.paso file operatinos, bulid, extract, get info etc.
    #.paso file is actually tar.gz file
    #It contains a package.txt file and some pisi packages if necessary for bulid
    #Unfotunately package.txt does not have full information yet, just package names and urls      #NEEDS DEVELOPING
    #I imagine that will be an xml file
    #Current file format like this: "package filename = package url" :)




    def __init__(self, parentObj):
        #
        self.__metadata = pasoMetadata()
        self.__files = pasoFiles()
        self.__clear()
        self.onAddPackage = eventHandler()      #(elementName, totalElements, currentElement)
        self.onError = eventHandler()           #( errorCode, errorData)
        self.__files.onAdd.addEventListener(self.__onPasoFilesRead)
        self.parent = parentObj




    def __clear(self):
        self.__file = ""
        self.__path = ""
        self.__targetName = ""
        self.__sourceName = ""
        self.__listRawData = ""
        self.__listFull = {}
        self.__pasoRepo = []






    def open(self, filename):
        #source=paso file (tar.gz)
        if os.path.isfile(filename):
            try:
                self.onAddPackage.raiseEvent( filename, 4, 1)
                handle = tarfile.open(filename)
            except:
                self.onError.raiseEvent( const.ERR_07_ID, filename)
                return( False )
            try:
                self.onAddPackage.raiseEvent( filename, 4, 2)
                metadata = handle.extractfile(const.PASO_METAFILE_VAL)
                self.onAddPackage.raiseEvent( filename, 4, 3)
                xml = metadata.read()
            except:
                self.onError.raiseEvent( const.ERR_06_ID, filename)
                return( False )
            if not self.__metadata.parse(xml):
                self.onError.raiseEvent( const.ERR_02_ID, filename+":"+const.PASO_METAFILE_VAL)
                return( False )
            self.onAddPackage.raiseEvent( filename, 4, 4)
            self.__file = filename
            handle.close()
            return(True)
        else:
            self.onError.raiseEvent( const.ERR_01_ID, filename)
            return(False)






    def create(self, outFile, listFull, \
                alt, altList, altDir, \
                iso, isoList, isoDir, \
                repoList, metadata, repo):
        #
        self.__file = outFile
        self.__metadata = metadata
        pasoFileList = {}       #{"filename": uri}
        path = outFile.strip(lib.stripFilename(self.__file))
        metadataFile = path+const.PASO_METAFILE_VAL
        filesdataFile = path+const.PASO_DATAFILE_VAL
        #Build files.xml
        self.__files.clear()
        self.__files.repos = repoList
        for package in listFull.keys():
            if self.parent.error:
                self.__clear()
                self.onError.raiseEvent(const.ERR_03_ID, "")
                return(False)
            size = repo.get_package_size(lib.stripFilename(package))
            if not size and alt.is_on(package):
                size = alt.getSize(package)
            elif not size and iso.is_on(package):
                size = iso.getSize(package)
            elif not size:
                size = 0
            self.__files.addPackage( package, listFull[package], size )
        for file in altList:
            if self.parent.error:
                self.__clear()
                self.onError.raiseEvent(const.ERR_03_ID, "")
                return(False)
            self.__files.addFile(file)
        #Save temp files
        self.__metadata.repoSize = self.__files.sizeCount
        if not lib.savefile(metadataFile, self.__metadata.toXml()):
            self.onError.raiseEvent( const.ERR_05_ID, metadataFile)
            return(False)
        if not lib.savefile(filesdataFile, self.__files.toXml()):
            self.onError.raiseEvent( const.ERR_05_ID, filesdataFile)
            return(False)
        #Create file list for paso archive
        pasoFileList[const.PASO_METAFILE_VAL] = metadataFile
        pasoFileList[const.PASO_DATAFILE_VAL] = filesdataFile
        for aFile in altList:
            if self.parent.error:
                self.__clear()
                self.onError.raiseEvent(const.ERR_03_ID, "")
                return(False)
            pasoFileList[aFile] = altDir+"/"+aFile
        #Create paso file
        if not self.__createPaso(pasoFileList):
            return(False)
        return(True)






    def __createPaso(self, fileList):
        #
        try:
            target = tarfile.open(self.__file, 'w:gz')
        except:
            self.onError.raiseEvent( const.ERR_05_ID, self.__file)
            return(False)
        totalJob = len(fileList)
        jobPos = 1
        for aFile in fileList.keys():
            if self.parent.error:
                self.__clear()
                self.onError.raiseEvent(const.ERR_03_ID, "")
                return(False)
            self.onAddPackage.raiseEvent(fileList[aFile], totalJob, jobPos)
            try:
                target.add(fileList[aFile], aFile, False)
            except:
                target.close()
                os.unlink(fileList[const.PASO_METAFILE_VAL])
                os.unlink(fileList[const.PASO_DATAFILE_VAL])
                self.onError.raiseEvent( const.ERR_01_ID, fileList[aFile])
                return(False)
            jobPos += 1
        target.close()
        os.unlink(fileList[const.PASO_METAFILE_VAL])
        os.unlink(fileList[const.PASO_DATAFILE_VAL])
        return(True)




    def load(self):
        if os.path.isfile(self.__file):
            try:
                handle = tarfile.open(self.__file)
            except:
                self.onError.raiseEvent( const.ERR_07_ID, self.__file)
                return( False )
            try:
                files = handle.extractfile(const.PASO_DATAFILE_VAL)
                xml = files.read()
            except:
                self.onError.raiseEvent( const.ERR_06_ID, self.__file)
                return( False )
            if not self.__files.parse(xml):
                self.onError.raiseEvent( const.ERR_02_ID, self.__file+":"+const.PASO_DATAFILE_VAL)
                return( False )
            handle.close()
            if self.parent.error:
                self.__clear()
                self.onError.raiseEvent(const.ERR_03_ID, "")
                return(False)
            return(True)
        else:
            self.onError.raiseEvent( const.ERR_01_ID, filename)
            return(False)




    def __onPasoFilesRead(self, name, total, current):
        self.onAddPackage.raiseEvent(name, total, current)



    def getFileName(self):
        return(self.__file)



    def getInfo(self):
        return(self.__metadata)



    def isPackagesEmpty(self):
        if len(self.__files.packages) > 0:      return(False)
        else:                                   return(True)


    def getPackageList(self):
        return(self.__files.packages.keys())



    def isOn(self, package):
        if package in self.__files.additionals:   return( True)
        else:   return( False)


    def getPasoFileName(self):
        return(self.__file)


    def getPackageUrl(self, package):
        return( self.__files.repos[ self.__files.packages[package]["repo"] ] )



    def getSize(self, package):
        return( self.__files.packages[package]["size"] )

