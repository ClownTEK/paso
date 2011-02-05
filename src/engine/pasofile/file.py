#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#Author: Read AUTHORS file.
#License: Read COPYING file.



from os import path
from constants import const
from ..lib import eventHandler, savefile, getfile, ratioCalc
from types import paso, header, packageList
import zlib



class pasofile(object):





    def __init__(self, ):
        self.__clear()
        self.onError = eventHandler()       #(ActionCode, Error code, data)
        self.onProcessing = eventHandler()   #(ActionCode, ProcessRatio, data)
        self.__actCode = "actCode"

        self.__data = paso()




    def __clear(self):
        self.__file = ""




    def load(self, location):
        self.__file = path.normpath(location)
        xml = zlib.decompress(getfile(self.__file))
        if not xml:
            self.onError.raiseEvent(self.__actCode, "01", self.__file)
            return(False)
        self.__data.fromXml(xml)
        if not self.__data.right:
            self.onError.raiseEvent(self.__actCode, "02", self.__file)
            return(False)
        return(True)






    def updateHeader(self, header=header()):
        self.__data.header = header





    def updatePackageList(self, plist=packageList()):
        self.__data.packages = plist




    def addPackage(self, name, size=0):
        self.__data.packages.addFile(name, size)




    def save(self, location):
        self.__file = path.normpath(location)
        if not savefile(self.__file, zlib.compress(self.__data.toXml())):
            self.onError.raiseEvent(self.__actCode, "03", self.__file)
            print "err"
            return(False)
        return(True)




    def getData(self):
        return(self.__data)



    def getList(self):
        return(self.__data.packages.files.keys())



