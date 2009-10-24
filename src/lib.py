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
		print "Open Error :"+name
		return (False)
    return( f.read() )





def savefile(name, data):
    #
    try:
    	f = open(name, "w")
    except:
		print "Open Error :"+name
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





