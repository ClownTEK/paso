#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#Author: Read AUTHORS file.
#License: Read COPYING file.


import lib
from constants import const
from lib import eventHandler
import os
import time





class packageDir(object):
    #Load .pisi filenames to __uriList from specify folder




    def __init__(self):
        self.clear()
        self.onAddPackage = eventHandler()      #(elementName, totalElements, currentElement)
        self.onError = eventHandler()           #(errorCode, errorData)



    def clear(self):
        self.__path = ""
        self.__uriList = []
        self.__sizes = {}   # {"name":size, }
        self.__break = False




    def __load_dir(self):
        #
        pos = 1
        self.onAddPackage.raiseEvent(self.__path, 100, 1)
        self.__uriList = lib.listdir(self.__path, [const.PISI_EXT])
        if self.__uriList:
            self.__uriList.sort()
        for package in self.__uriList:
            self.__sizes[package] = os.stat(self.__path+"/"+package).st_size
            self.onAddPackage.raiseEvent(self.__path+"/"+package, len(self.__uriList), pos)
            pos += 1
        return( True )






    def load(self, path):
        #
        self.__path = path
        if os.path.isdir(self.__path):
            if self.__load_dir():
                return( True)
        else:
            self.onError.raiseEvent( const.ERR_01_ID, path)
            return( False)





    def is_on(self, uri):
        #
        if uri in self.__uriList:   return( True)
        else:   return( False)




    def get_path(self):
        return(self.__path)




    def getSize(self, name):
        try:
            result = self.__sizes[name]
        except:
            result = False
        return(result)



    def isEmpty(self):
        if len(self.__uriList) > 0:     return(False)
        else:                           return(True)



