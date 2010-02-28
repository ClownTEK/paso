#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#Author: Read AUTHORS file.
#License: Read COPYING file.


import xml.etree.cElementTree as etree
from lib import eventHandler
from lib import createXmlNode






class pasoMetadata(object):
    #



    def __init__(self):
        #
        self.name = ""
        self.homepage = ""
        self.packagerName = ""
        self.packagerEmail = ""
        self.summary = ""
        self.description = ""
        self.release = ""
        self.date = ""
        self.repoSize = 0







    def parse(self, xml):
        #
        try:
            doc = etree.fromstring(xml)
            self.name = doc.find("Name").text
            self.homepage = doc.find("Homepage").text
            self.summary = doc.find("Summary").text
            self.description = doc.find("Description").text
            self.release = doc.find("Release").text
            self.date = doc.find("Date").text
            try:
                self.repoSize = int(doc.find("RepoSize").text)
            except:
                pass
            self.packagerName = doc.find("Packager").find("Name").text
            self.packagerEmail = doc.find("Packager").find("Email").text
        except:
            return( False )
        return( True )




    def toXml(self):
        #
        xml = "<?xml version='1.0' ?>\n"
        xml += createXmlNode("PASO")
        xml += createXmlNode("Name", self.name, indents=1)
        xml += createXmlNode("Homepage", self.homepage, indents=1)
        xml += createXmlNode("Packager", indents=1)
        xml += createXmlNode("Name", self.packagerName, indents=2)
        xml += createXmlNode("Email", self.packagerEmail, indents=2)
        xml += createXmlNode("Packager", indents=1, close=True)
        xml += createXmlNode("Summary", self.summary, indents=1)
        xml += createXmlNode("Description", self.description, indents=1)
        xml += createXmlNode("Release", self.release, indents=1)
        xml += createXmlNode("Date", self.date, indents=1)
        xml += createXmlNode("RepoSize", str(self.repoSize), indents=1)
        xml += createXmlNode("PASO", close=True)
        return(xml)














class pasoFiles(object):



    def __init__(self):
        #
        self.clear()
        self.onAdd = eventHandler() #( packageName, totalPackages, currentValue)



    def clear(self):
        self.repos = {}             #{'repo name': 'url', }
        self.packages = {}          #{'package name': {'repo':'name', 'size':'123'}, }
        self.additionals = []       #['package file name', ]
        self.sizeCount = 0



    def parse(self, xml):
        #
        try:
            doc = etree.fromstring(xml)
            totalPackages = len(doc.find("Repos").getchildren()) \
                            + len( doc.find("Packages").getchildren()) \
                            + len(doc.find("AdditionalFiles").getchildren())
            for repo in doc.find("Repos").getchildren():
                self.repos[ repo.attrib["name"] ] = repo.text
                self.onAdd.raiseEvent(repo.attrib["name"], totalPackages, len(self.repos))
            for package in doc.find("Packages").getchildren():
                self.packages[ package.text ] = { "repo":package.attrib["repo"], \
                                                    "size":package.attrib["size"] }
                self.onAdd.raiseEvent(package.text, totalPackages, \
                                                    len(self.packages)+len(self.repos))
            for file in doc.find("AdditionalFiles").getchildren():
                self.additionals.append(file.text)
                self.onAdd.raiseEvent(file.text, totalPackages, \
                                    len(self.packages)+len(self.repos)+len(self.additionals))
        except:
            return( False )
        return( True )





    def toXml(self):
        #
        xml = "<?xml version='1.0' ?>\n"
        xml += createXmlNode("PASO")
        xml += createXmlNode("Repos",indents=1)
        for repo in self.repos.keys():
            xml += createXmlNode("Repo", self.repos[repo], {"name":repo}, indents=2)
        xml += createXmlNode("Repos",indents=1, close=True)
        xml += createXmlNode("Packages", indents=1)
        for package in self.packages.keys():
            packageData = self.packages[package]
            xml += createXmlNode("Package", package, {"repo":packageData["repo"], \
                                        "size":packageData["size"]}, indents=2)
        xml += createXmlNode("Packages", indents=1, close=True)
        xml += createXmlNode("AdditionalFiles",indents=1)
        for aFile in self.additionals:
            xml += createXmlNode("File", aFile, indents=2)
        xml += createXmlNode("AdditionalFiles",indents=1, close=True)
        xml += createXmlNode("PASO", close=True)
        return(xml)


    def addPackage(self, package, repo, size):
        self.packages[package] = {'repo':repo, 'size':str(size)}
        self.sizeCount += int(size)



    def addFile(self, file):
        self.additionals.append(file)


    def addRepo(self, name, url):
        self.repos[name] = url


