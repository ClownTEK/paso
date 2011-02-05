#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#Author: Read AUTHORS file.
#License: Read COPYING file.



import os
from os import path, makedirs
from constants import const
from ..lib import eventHandler,  savefile, getfile, ratioCalc
















class iso(object):





    def __init__(self, actCode):
        self.__clear()
        self.onError = eventHandler()       #(ActionCode, Error code, data)
        self.onProcessing = eventHandler()   #(ActionCode, ProcessRatio, data)
        self.__actCode = actCode





    def __clear(self):
        self.right = True
        self.__path = ""
        self.iso = ""







    def setTarget(self, target):
        self.__path = path.normpath(target)






    def buildContents(self, source):
        for f in const.ISO_FILES:
            src = path.join(source, f)
            cmd = "cp -rfv '%s' '%s'" %(src, self.__path)
            print cmd
            try:
                if os.system(cmd) <> 0: return(False)
            except:
                return(False)
        return( True )





    def buildImage(self, pth, pName):
        pName += const.ISO_EXT
        cmd = const.MKISO_CMD %( path.join(pth, pName), self.__path)
        try:
            if os.system(cmd) <> 0: return(False)
        except:
            return(False)
        cmd = const.MKHYBRID_CMD %( path.join(pth, pName))
        try:
            if os.system(cmd) <> 0: return(False)
        except:
            return(False)
        self.iso = path.join(pth, pName)
        return(True)


