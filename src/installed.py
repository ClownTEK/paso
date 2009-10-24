#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#Author: Read AUTHORS file.
#License: Read COPYING file.


from xml.dom.minidom import parseString
import lib
from constants import const
from lib import eventHandler






class installed(object):
    #Search installed packages on the specify Pardus system and add the package name as key to
    #__packages dict with its pisi filename
    #System may be found other mounted partition




    def __init__(self):
        self.__clear()
        self.onAddPackage = eventHandler()      #(elementName, totalElements, currentElement)
        self.onError = eventHandler()           #(errorCode, errorData)




    def __clear(self):
        self.__path = ""
        self.__uriList = []
        self.__packages = {}
        self.__break = False






    def load(self, path):
        #path is default on Pardus systems
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
            #Open metadata and parse
            xml = lib.getfile(self.__path+uri+"/"+const.PACKAGE_INFO_FILE)
            if xml != False:
                package = self.__parse(xml)
                if not package:
                    self.onError.raiseEvent( const.ERR_02_ID, uri)
                    return False
                self.__packages[package["name"]] = package
                self.onAddPackage.raiseEvent(package["name"], totalPackages, len(self.__packages))
                #if len(self.__packages) > 10: break             #REMOVE!!!
            else:
                self.onError.raiseEvent( const.ERR_01_ID, uri)
                break






    def __parse(self, xml):
        #
        package = {}
        try:
            doc = parseString(xml)
            domPISI = doc.getElementsByTagName("PISI")[0]               #PISI
            domPackage = domPISI.getElementsByTagName("Package")[0]     #PISI/Package
            domName = domPackage.getElementsByTagName("Name")[0]        #PISI/Package/Name
            package["name"] = domName.childNodes[0].nodeValue
            domHistory = domPackage.getElementsByTagName("History")[0]  #PISI/Package/History
            domUpdate = domHistory.getElementsByTagName("Update")[0]    #PISI/Package/History/Update
            package["release"] = domUpdate.attributes["release"].nodeValue
            domVersion = domUpdate.getElementsByTagName("Version")[0]   #PISI/Package/History/Update/Version
            package["version"] = domVersion.childNodes[0].nodeValue
            try:                                                        #
                domBuild = domPackage.getElementsByTagName("Build")[0]      #PISI/Package/Bulid
                package["build"] = domBuild.childNodes[0].nodeValue         #It may be not found
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



    def stop(self):
        self.__break = True



    def isEmpty(self):
        if len(self.__packages) > 0:    return(False)
        else:                           return(True)