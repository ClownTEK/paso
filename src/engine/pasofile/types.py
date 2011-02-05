#!/usr/bin/python
# -*- coding: utf-8 -*-


import xml.etree.cElementTree as etree
from ..lib import createXmlNode



class header(object):




    def __init__(self):
        self.__clear()




    def __clear(self):
        self.n = ""
        self.hp = ""
        self.s = ""
        self.dc = ""
        self.ds = ""
        self.r = ""
        self.d = ""
        self.a = ""
        self.pn = ""
        self.pm = ""
        self.st = 0
        self.right = True




    def fromXml(self, xml):
        try:
            element = etree.fromstring(xml)
            self.n = element.find("Name").text
            self.hp = element.find("Homepage").text
            self.s = element.find("Summary").text
            self.dc = element.find("Description").text
            self.ds = element.find("Distrubution").text
            self.r = element.find("Release").text
            self.a = element.find("Architecture").text
            self.d = element.find("Date").text
            self.pn = element.find("Packager").find("Name").text
            self.pm = element.find("Packager").find("Email").text
            try:
                self.st = int( element.find("PackageSizeTotal").text )
            except:
                self.st = 0
            self.right = True
            return(True)
        except:
            self.right = False
            return(False)




    def toXml(self):
        xml = createXmlNode("Name", self.n, indents=1)
        xml += createXmlNode("Homepage", self.hp, indents=1)
        xml += createXmlNode("Packager", indents=1)
        xml += createXmlNode("Name", self.pn, indents=2)
        xml += createXmlNode("Email", self.pm, indents=2)
        xml += createXmlNode("Packager", indents=1, close=True)
        xml += createXmlNode("Summary", self.s, indents=1)
        xml += createXmlNode("Description", self.dc, indents=1)
        xml += createXmlNode("Distrubution", self.ds, indents=1)
        xml += createXmlNode("Architecture", self.a, indents=1)
        xml += createXmlNode("Release", self.r, indents=1)
        xml += createXmlNode("Date", self.d, indents=1)
        xml += createXmlNode("PackageSizeTotal", str(self.st), indents=1)
        return(xml)







def headerFromString(name, homepage, summary, description, distrubution,
                    release, architecture, date, packager_name, packager_email, packagesizetotal=0):
    aHeader = header()
    aHeader.n = name
    aHeader.hp = homepage
    aHeader.s = summary
    aHeader.dc = description
    aHeader.ds = distrubution
    aHeader.r = release
    aHeader.a = architecture
    aHeader.d = date
    aHeader.pn = packager_name
    aHeader.pm = packager_email
    aHeader.st = packagesizetotal
    return(aHeader)









class packageList():



    def __init__(self):
        self.__clear()



    def __clear(self):
        self.files = {}     #{'filename': { 'size':'123'}, }
        self.right = True



    def fromXml(self, xml):
        try:
            element = etree.fromstring(xml)
            for package in element.find("Packages").getchildren():
                self.files[package.text] = { "size":package.attrib["size"] }
            self.right = True
            return(True)
        except:
            self.right = False
            return(False)



    def toXml(self):
        xml = createXmlNode("Packages", indents=1)
        for package in self.files.keys():
            packageData = self.files[package]
            xml += createXmlNode("Package",
                                    package,
                                    {"size":packageData["size"]},
                                    indents=2
                                )
        xml += createXmlNode("Packages", indents=1, close=True)
        return(xml)




    def addFile(self, package, size=0):
        self.files[package] = { 'size':str(size)}









class paso():



    def __init__(self):
        self.__clear()




    def __clear(self):
        self.header = header()
        self.packages = packageList()
        self.right = True




    def toXml(self):
        xml = "<?xml version='1.0' ?>\n"
        xml += createXmlNode("PASO")
        xml += self.header.toXml()
        xml += self.packages.toXml()
        xml += createXmlNode("PASO", close=True)
        return(xml)




    def fromXml(self, xml):
        self.header.fromXml(xml)
        self.packages.fromXml(xml)
        if self.header.right and self.packages.right:
            return(True)
        else:
            self.right = False
            return(False)




    def setHeader(self, newHeader):
        self.header = newHeader




