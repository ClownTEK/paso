#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#Author: Read AUTHORS file.
#License: Read COPYING file.
#


from xml.dom.minidom import parseString
import lib
from constants import const
from lib import eventHandler






class repos(object):





    def __init__(self):
        self.__clear()
        self.onAddPackage = eventHandler()      #(elementName, totalElements, currentElement)
        self.onError = eventHandler()           #(errorCode, errorData)



    def __clear(self):
        self.__repoPath = ""
        self.__repoIndexPath = ""
        self.__packages = {}
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
                repo = {}
                doc = parseString(xml)
                if not doc:
                    self.onError.raiseEvent( const.ERR_02_ID, self.__repoPath+"/repos")
                    return( False)
                domREPOS = doc.getElementsByTagName("REPOS")[0]              #REPOS
                repos = domREPOS.getElementsByTagName("Repo")
                for domRepo in repos:
                    domName = domRepo.getElementsByTagName("Name")[0]
                    repo["name"] = domName.childNodes[0].nodeValue
                    domUrl = domRepo.getElementsByTagName("Url")[0]
                    repo["url"] = domUrl.childNodes[0].nodeValue[0:-18]
                    self.__repos[repo["name"]] = repo["url"]
                    self.onAddPackage.raiseEvent("Found "+repo["name"], 100, 1)
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
        try:
            self.onAddPackage.raiseEvent(repo+" parsing...", len(self.__repos), self.__currentRepo-1)
            doc = parseString(xml)
            if not doc:
                self.onError.raiseEvent( const.ERR_02_ID, repo)
                return( False)
            domPISI = doc.getElementsByTagName("PISI")[0]
            packages = domPISI.getElementsByTagName("Package")
            for domPackage in packages:
                if len(domPackage.childNodes) > 1:
                    domName = domPackage.getElementsByTagName("Name")[0]
                    self.__packages[domName.childNodes[0].nodeValue] = repo
                    currentElement = lib.ratioCalc(len(packages), currentPos, len(self.__repos), self.__currentRepo)
                    self.onAddPackage.raiseEvent(repo+":"+domName.childNodes[0].nodeValue, 100, currentElement)
                    #if len(self.__packages) > 10: break             #REMOVE!!!
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



    def isEmpty(self):
        if len(self.__packages) > 0:    return(False)
        else:                           return(True)