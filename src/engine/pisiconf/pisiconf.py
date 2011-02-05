#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#
#Author: Read AUTHORS file.
#License: Read COPYING file.



import ConfigParser
from constants import const
from os import path
from ..lib import eventHandler






class config(object):





    def __init__(self, actCode):
        self.__clear()
        self.onError = eventHandler()       #(ActionCode, Error code, data)
        self.onProcessing = eventHandler()   #(ActionCode, ProcessRatio, data)
        self.__actCode = actCode




    def __clear(self):
        self.packages_dir = ""
        self.cached_packages_dir = ""
        self.info_dir = ""
        self.architecture = ""
        self.distribution = ""
        self.distribution_release = ""
        self.distribution_id = ""




    def load(self, root):
        #
        self.__file = path.join( path.normpath(root), const.FILE )
        config = ConfigParser.SafeConfigParser()
        try:
            config.read([self.__file])
            self.packages_dir = path.join( root, config.get(const.DIRECTORIES,const.PACKAGES)[1:] )
            self.cached_packages_dir = path.join( root, config.get(const.DIRECTORIES,const.CACHE)[1:] )
            self.info_dir = path.join( root, config.get(const.DIRECTORIES,const.INFO)[1:] )
            self.distribution = config.get(const.GENERAL,const.DIST)
            self.architecture = config.get(const.GENERAL,const.ARCH)
            self.distribution_release = config.get(const.GENERAL,const.RELEASE)
            self.distribution_id = config.get(const.GENERAL,const.DIST_ID)
        except:
            #self.onError.raiseEvent(self.__actCode, "01")
            return(False)
        return(True)













