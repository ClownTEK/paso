#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#Author: Read AUTHORS file.
#License: Read COPYING file.


from lib import  eventHandler, ratioCalc
from os import path, makedirs
from constants import const
from isorepo.builder import isorepo
from iso.builder import iso
from pisiconf.pisiconf import config
from repos.pisirepo import repos






class builder():



    def __init__(self):
        self.__repo = isorepo("")
        self.__iso = iso("")
        self.__path = ""
        self.__pName = ""
        self.__pim =""

        self.__localSources = []
        self.__remoteSources = []

        self.pisiconfLoaded = False
        self.repoUrlsLoaded = False




    def setTarget(self, pth, prjName):
        self.__path = path.normpath(pth)
        self.__pName = prjName
        self.__repo.setTarget(path.join(self.__path, self.__pName, const.REPO_PATH))
        self.__iso.setTarget( path.join(self.__path, self.__pName) )




    def setSources(self, local, remote):
        self.__localSources = local
        self.__remoteSources = remote
        self.__repo.setLocalURLs(self.__localSources)
        self.__repo.setRemoteURLs(self.__remoteSources)




    def getLocalSources(self):
        return(self.__localSources)




    def getRemoteSources(self):
        return(self.__remoteSources)




    def setPIMPath(self, pim):
        self.__pim = pim




    def makeDirs(self):
        d = path.join(self.__path, self.__pName, const.REPO_PATH)
        if path.isdir(d):
            return(True)
        try:
            makedirs(d)
        except:
            return(False)
        return(True)




    def loadSources(self):
        cfg = config("")
        rp = repos("")
        if cfg.load(const.SYS_ROOT):
            self.__localSources.append(cfg.cached_packages_dir)
            self.pisiconfLoaded = True
            if rp.load(path.join(const.SYS_ROOT,cfg.info_dir)):
                self.__localSources += rp.getLocalURLs()
                self.__remoteSources += rp.getRemoteURLs()
                self.repoUrlsLoaded = True
            else: self.repoUrlsLoaded = False
        else: self.pisiconfLoaded = False




    def searchPackage(self, package):
        return(self.__repo.search(package))




    def bringPackage(self, pkgInfo):
        return(self.__repo.cpPackage(pkgInfo))




    def buildIndex(self):
        return(self.__repo.buildRepoIndex())




    def transferInstallationSystem(self):
        return(self.__iso.buildContents(self.__pim))



    def createISO(self):
        return(self.__iso.buildImage(self.__path, self.__pName))



    def getTargetName(self):
        return(self.__iso.iso)



    def calcSUM(self):          #FIX IT
        return(True)