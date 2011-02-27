#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#Author: Read AUTHORS file.
#License: Read COPYING file.



import xml.etree.cElementTree as etree
from os import path
from pkg import pkg
from constants import const
from ..lib import eventHandler, listdir, getfile, ratioCalc





class pkgdir(object):





    def __init__(self, actCode):
        self.__clear()
        self.onError = eventHandler()       #(ActionCode, Error code, data)
        self.onProcessing = eventHandler()   #(ActionCode, ProcessRatio, data)
        self.__actCode = actCode







    def __clear(self):
        self.__path = ""
        self.__packages = {}        #{"pkg name": pkg obj, ...}




    def setTarget(self, p):
        self.__clear()
        self.__path = path.normpath(p)





    def loadList(self):
        pkgdirs = listdir(self.__path)
        if not pkgdirs:
            return False
        return(pkgdirs)




    def loadPackageInfo(self, d):
        xml = getfile( path.join(self.__path, d, const.PACKAGE_INFO_FILE) )
        if xml:
            package = pkg(xml)
            if package.right:
                self.__packages[package.n] = package
                return(True)
        return(False)







    def load(self, p):
        #
        self.__clear()
        self.__path = path.normpath(p)
        pkgdirs = listdir(self.__path)
        if not pkgdirs:
            return False
        totalPackages = len(pkgdirs)
        for d in pkgdirs:
            xml = getfile(
                    path.join(self.__path, d, const.PACKAGE_INFO_FILE)
                )
            if not xml:
                self.__clear()
                return(False)
            package = pkg(xml)
            if package.right:
                self.__packages[package.n] = package
                self.onProcessing.raiseEvent(
                            self.__actCode,
                            ratioCalc(totalPackages, len(self.__packages)),
                            package.n
                        )
            else:
                self.__clear()
                return(False)
        return(True)




    def getPackages(self):
        return(self.__packages)

