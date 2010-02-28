#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#Author: Read AUTHORS file.
#License: Read COPYING file.



import xml.etree.cElementTree as etree
import lib
from constants import const
from lib import eventHandler






class installed(object):
    #Search installed packages on the specify Pardus system and
    # add the package name as key to
    #__packages dict with its pisi filename
    #System may be found other mounted partition




    def __init__(self, parentObj):
        self.__clear()
        self.onAddPackage = eventHandler()      #(elementName, totalElements, currentElement)
        self.onError = eventHandler()           #(errorCode, errorData)
        self.parent = parentObj




    def __clear(self):
        self.__path = ""
        self.__uriList = []
        self.__packages = {}







    def load(self, path):
        #
        self.__clear()
        self.__path = path+"/"
        #Get list of packages, they're found as a directory each one
        self.__uriList = lib.listdir(self.__path, [])
        if not self.__uriList:
            self.onError.raiseEvent( const.ERR_01_ID, path)
            return False
        self.__uriList.sort()
        totalPackages = len(self.__uriList)
        #Walk
        for uri in self.__uriList:
            if self.parent.error:
                self.__clear()
                self.onError.raiseEvent(const.ERR_03_ID, "")
                return(False)
            #Open metadata and parse
            xml = lib.getfile(self.__path+uri+"/"+const.PACKAGE_INFO_FILE)
            if xml != False:
                package = self.__parse(xml)
                if not package:
                    self.onError.raiseEvent( const.ERR_02_ID, uri)
                    self.__clear()
                    return(False)
                self.__packages[package["name"]] = package
                self.onAddPackage.raiseEvent(package["name"], totalPackages, len(self.__packages))
            else:
                self.onError.raiseEvent( const.ERR_01_ID, uri)
                self.__clear()
                return(False)





    def __parse(self, xml):
        #
        package = {}
        try:
            packageTree = etree.fromstring(xml).getchildren()[1]
            package["name"] = packageTree.find("Name").text
            package["release"] = packageTree.find("History").find("Update").attrib["release"]
            package["version"] = packageTree.find("History").find("Update").find("Version").text
            try:
                package["build"] = packageTree.find("Build").text
            except:
                package["build"] = False
        except:
            return False
        return( package )





    def getPackage(self, name):
        #
        return( self.__packages[name] )




    def getPackageUri(self, name):
        #
        p = self.__packages[name]
        uri = p["name"]+"-"+p["version"]+"-"+p["release"]
        if p["build"]:  uri += "-"+p["build"]
        return(  uri+const.PISI_EXT )




    def getPackageList(self):
        #
        return( self.__packages.keys() )




    def isEmpty(self):
        if len(self.__packages) > 0:    return(False)
        else:                           return(True)