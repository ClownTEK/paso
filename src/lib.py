#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#Author: Read AUTHORS file.
#License: Read COPYING file.

import os




def getfile(name):
    #
    try:
    	f = open(name, "r")
    except:
		#print "Open Error :"+name
		return (False)
    return( f.read() )





def savefile(name, data):
    #
    try:
    	f = open(name, "w")
    except:
		#print "Open Error :"+name
		return (False)
    return( f.write(data)  )





def listdir(path, filters=[]):
    #filters = ["pisi", "tar.gz"...etc]
    result = []
    try:
        files = os.listdir(path)
        if len(filters) == 0:
            result = files
        else:
            for file in files:
                for filter in filters:
                    if filter in file:  result.append(file)
        return(result)
    except:
        return(False)





def stripFilename(uri, ext=""):
    #("/home/ali/test.tar.gz", ".gz") Return(test.tar)
    if ext == "" or uri.find(ext) == -1:
        return (uri[ (uri.rfind("/") + 1 ) : len(uri)] )         #test.tar.gz
    else:
        return (uri[ (uri.rfind("/") + 1 ) : uri.find(ext) ])   #"test.tar"






def ratioCalc(totalElements, currentElement, totalParts=1, currentPart=1, size=100):
    #
    ratioOfOne = size  / totalParts
    ratioOfElements = (ratioOfOne * currentElement) / totalElements
    currentPos = (ratioOfOne * (currentPart -1) ) + ratioOfElements
    return(currentPos)





class eventHandler():
    #

    def __init__(self):
        self.__actions = []


    def addEventListener(self, func):   self.__actions.append( func )


    def removeEventListener(self, func):    self.__actions.remove( func )


    def raiseEvent(self, *args):
        for e in self.__actions: e(*args)






def createXmlNode(name, value={}, attributes={}, close=False, indents=0, linefeed=True, empty=False):
    #("Name", "text", {'attrName':'attrVal',})
    space = " "
    less = "<"
    greater = ">"
    dvide = "/"
    apos = "\""
    equal = "=\""
    linefeed = "\n"
    xml = ("    "*indents)
    if type(value) != type(dict()):
        value = str(value)
        if value.strip() == "":     value = " "
        xml += less+name+space
        for attribute in attributes.keys():
            xml += attribute+equal+attributes[attribute]+apos+space
        xml += greater+value+less+dvide+name+greater
    elif close:
        xml += less+dvide+name+greater
    elif close and empty:
        xml += less+name+dvide+greater
    else:
        xml += less+name+greater
    if linefeed:
        xml += linefeed
    return(xml)




def getPardusRelease(root):
    return( getfile(root+"etc/pardus-release").strip() )



