#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#Author: Read AUTHORS file.
#License: Read COPYING file.



import xml.etree.cElementTree as etree
from os import path
from constants import const
from ..lib import eventHandler,  getfile





class repos(object):





    def __init__(self, actCode):
        self.__clear()
        self.onError = eventHandler()       #(ActionCode, Error code, data)
        self.onProcessing = eventHandler()   #(ActionCode, ProcessRatio, data)
        self.__actCode = actCode





    def __clear(self):
        self.__file = ""
        self.right = True
        self.__remoteURL = []        #["repo url", ...]
        self.__localURL = []        #["repo url", ...]





    def load(self, p):
        self.__clear()
        self.__file = path.join(path.normpath(p), const.PISI_REPO_LIST_FILE )
        xml = getfile(self.__file)
        if xml:
            try:
                for repo in etree.fromstring(xml).getchildren():
                    if repo.find("Url").text[:4] == const.HTTP_REPO_PREFIX:
                        self.__remoteURL.append( path.dirname( repo.find("Url").text ) )
                    else:
                        self.__localURL.append( path.dirname( repo.find("Url").text ) )
                    self.onProcessing.raiseEvent(self.__actCode, 0, repo.find("Url").text )
            except:
                self.right = False
                self.onError.raiseEvent( self.__actCode, "01", self.__file )
                return(False)
        else:
            self.right = False
            self.onError.raiseEvent( self.__actCode, "02", self.__file )
            return (False)
        return(True)




    def getRemoteURLs(self):
        return(self.__remoteURL)



    def getLocalURLs(self):
        return(self.__localURL)
