#!/usr/bin/python
# -*- coding: utf-8 -*-


import xml.etree.cElementTree as etree



class pkg(object):




    def __init__(self, xml):
        #
        try:
            element = etree.fromstring(xml)
            self.n = element.find("Package").find("Name").text
            self.r = element.find("Package").find("History").find("Update").attrib["release"]
            self.v = element.find("Package").find("History").find("Update").find("Version").text
            self.right = True
        except:
            self.right = False