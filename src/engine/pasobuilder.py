#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#Author: Read AUTHORS file.
#License: Read COPYING file.

from os import path
from lib import  eventHandler, ratioCalc
from constants import const
from packages.packages import pkgdir
from pisiconf.pisiconf import config
from pasofile.file import pasofile
from pasofile.types import headerFromString, packageList






class buildFromPath():

    def __init__(self):
        self.__totalSubProcess = 0
        self.__currentSubProcess = 0
        self.__errorOccured = False

        self.__ins = pkgdir(const.ACT_LOAD_PACKAGES_FROM_PISI_PATH)
        self.__ins.onProcessing.addEventListener(self.__processing)
        self.__ins.onError.addEventListener(self.__error)

        self.__pisiconf = config(const.ACT_LOAD_PISI_CONF)
        self.__pisiconf.onProcessing.addEventListener(self.__processing)
        self.__pisiconf.onError.addEventListener(self.__error)

        #self.__paso = pasofile(const.ACT_SAVE_PASO_FILE)
        #self.__paso.onProcessing.addEventListener(self.__processing)
        #self.__paso.onError.addEventListener(self.__error)

        self.onError = eventHandler()
        self.onProcessing = eventHandler()





    def __processing(self, act, ratio, pkg):
        self.onProcessing.raiseEvent(act,
                        ratioCalc(100, ratio, self.__totalSubProcess, self.__currentSubProcess),
                        pkg
                        )




    def __error(self, act, code, data):
        self.__errorOccured = True
        self.onError.raiseEvent(act, code)





    def load(self, root):
        self.__errorOccured = False
        self.__totalSubProcess = 1
        self.__currentSubProcess = 1
        pkgs = packageList()
        self.__pisiconf.load(root)
        if self.__errorOccured:     return(False)
        self.__ins.load(self.__pisiconf.packages_dir)
        if self.__errorOccured:     return(False)
        return(True)




    def loadList(self, root):
        if self.__pisiconf.load(root):
            self.__ins.setTarget( path.join(root, self.__pisiconf.packages_dir) )
            dirs = self.__ins.loadList()
            if dirs:    return(dirs)
        return(False)




    def loadPackageInfo(self, pkg):
        return(self.__ins.loadPackageInfo(pkg))




    def getPackages(self):
        return(self.__ins.getPackages())




    def getFiles(self):
        pkgs = packageList()
        for pkg in self.__ins.getPackages().values():
            pkgs.addFile( getPisiFileName(pkg, self.__pisiconf) )
        return(pkgs)




    def getNameList(self):
        pkgs = []
        for pkg in self.__ins.getPackages().keys():
            pkgs.append(pkg)
        return(pkgs)




    def getFileList(self):
        pkgs = []
        for pkg in self.__ins.getPackages().values():
            pkgs.append( getPisiFileName(pkg, self.__pisiconf) )
        return(pkgs)




    def getArch(self):
        return(self.__pisiconf.architecture)




    def getDist(self):
        return(self.__pisiconf.distribution)




def getPisiFileName(pkg, pisiconf):
    name = pkg.n+"-"+pkg.v+"-"+pkg.r
    name += "-"+pisiconf.distribution_id+"-"+pisiconf.architecture+const.PISI_EXT
    return(name)





def createHeader(name, homepage, summary, description, distrubution,
                    release, architecture, date, packager_name, packager_email, packagesizetotal=0):
    return( headerFromString(name, homepage, summary, description, distrubution,
                    release, architecture, date, packager_name, packager_email, packagesizetotal=0) )




def savePaso(info, packages, fn):
    pf = pasofile()
    pf.updateHeader(info)
    pf.updatePackageList(packages)
    return(pf.save(fn))



def loadPaso(fn):
    pf = pasofile()
    if pf.load(fn):
        return(pf.getData())
    return(False)