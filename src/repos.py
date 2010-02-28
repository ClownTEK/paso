#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#Author: Read AUTHORS file.
#License: Read COPYING file.
#


import xml.etree.cElementTree as etree
import lib
from constants import const
from lib import eventHandler






class repos(object):





    def __init__(self, parentObj):
        self.__clear()
        self.onAddPackage = eventHandler()      #(elementName, totalElements, currentElement)
        self.onError = eventHandler()           #(errorCode, errorData)
        self.parent = parentObj



    def __clear(self):
        self.__repoPath = ""
        self.__repoIndexPath = ""
        self.__packages = {}    #{"name":repo, }
        self.__packageSizes = {}
        self.__packageNames = {}
        self.__repos = {}
        self.__currentRepo = 1
        #self.__break = False







    def load(self, repoPath, repoIndexPath):
        #
        self.__clear()
        self.__repoPath = repoPath
        self.__repoIndexPath = repoIndexPath
        if self.__load_repos():
            if self.__load_packages():
                return(True)
        return(False)





    def __load_repos(self):
        #
        xml = lib.getfile(self.__repoPath+"/repos")
        if xml != False:
            try:
                for reposTree in etree.fromstring(xml).getchildren():
                    self.__repos[ reposTree.find("Name").text ] = reposTree.find("Url").text[0:-18]
                    self.onAddPackage.raiseEvent("Found "+reposTree.find("Name").text, 100, 1)
            except:
                self.onError.raiseEvent( const.ERR_02_ID, self.__repoPath+"/repos")
                return(False)
        else:
            self.onError.raiseEvent( const.ERR_01_ID, self.__repoPath+"repos")
            return (False)
        return( True)




    def __load_packages(self):
        #
        for repo in self.__repos:
            xml = lib.getfile(self.__repoIndexPath+"/"+repo+"/pisi-index.xml")
            if xml != False:
                if not self.__parse_index(xml, repo):
                    return(False)
            else:
                self.onError.raiseEvent( const.ERR_01_ID, self.__repoIndexPath+repo+"/"+"/pisi-index.xml")
                return(False)
            self.__currentRepo += 1
        return(True)





    def __parse_index(self, xml, repo):
        #
        currentPos = 1
        currentElement = 0
        repoCount = len(self.__repos)
        try:
            doc = etree.fromstring(xml)
            packageCount = len(doc.findall("Package") )
            for package in doc.getchildren():
                if self.parent.error:
                    self.__clear()
                    self.onError.raiseEvent(const.ERR_03_ID, "")
                    return(False)
                if package.tag == "Package":
                    name = package.find("Name").text
                    size = package.find("PackageSize").text
                    uri = package.find("PackageURI").text
                    self.__packages[name] = repo
                    self.__packageSizes[name] = size
                    self.__packageNames[uri] = name
                    currentElement = lib.ratioCalc(packageCount, currentPos, repoCount, self.__currentRepo)
                    self.onAddPackage.raiseEvent(repo+":"+name, 100, currentElement)
                    currentPos += 1
        except:
            self.onError.raiseEvent( const.ERR_02_ID, repo)
            return( False)
        return(True)






    def get_repo_uri(self,name):
        try:
            result = self.__repos[self.get_package_repo(name)]
        except:
            result = False
        return(result)





    def get_package_repo(self,name):
        try:
            result = self.__packages[name]
        except:
            result = False
        return(result)



    def get_package_size(self, name):
        if name.rfind(const.PISI_EXT) <> -1:
            name = self.get_package_name(name)
        try:
            result = self.__packageSizes[name]
        except:
            result = False
        return(result)



    def get_package_name(self, uri):
        try:
            result = self.__packageNames[uri]
        except:
            result = False
        return(result)



    def get_repos(self):
        return(self.__repos)



    def isEmpty(self):
        if len(self.__packages) > 0:    return(False)
        else:                           return(True)