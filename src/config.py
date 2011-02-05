#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#
#Author: Read AUTHORS file.
#License: Read COPYING file.



import ConfigParser
from constants import const
from os import path, makedirs
from engine.lib import savefile







class config(object):





    def __init__(self):
        self.__file = path.join( path.expanduser("~"), const.CONF_PATH, const.CONF_FILE )
        self.localDirs = []
        self.remoteUrls = []
        self.name = ""
        self.email = ""
        self.workspace = ""
        self.pim = ""

        self.__initDefaults()



    def isExist(self):
        if path.isfile(self.__file):    return(True)
        return(False)





    def load(self):
        if not self.isExist():
            return(False)
        config = ConfigParser.SafeConfigParser()
        try:
            config.read([self.__file])
            a = dict(config.items(const.CONF_FILE_LOCALDIRS)).values()
            a = map(lambda x: unicode(x), a)
            a.reverse()
            self.localDirs = a
            a = dict(config.items(const.CONF_FILE_REMOTEURLS)).values()
            a = map(lambda x: unicode(x), a)
            a.reverse()
            self.remoteUrls = a
            self.name = unicode(config.get(const.CONF_FILE_USER, const.CONF_FILE_USER_NAME))
            self.email = config.get(const.CONF_FILE_USER, const.CONF_FILE_USER_EMAIL)
            self.workspace = unicode(config.get(const.CONF_FILE_WORKSPACE, const.CONF_FILE_WORKSPACE_PATH))
            self.pim = unicode(config.get(const.CONF_FILE_GENERAL, const.CONF_FILE_GENERAL_PIM_PATH))
        except:
            return(False)
        return(True)





    def save(self):
        raw = const.CONF_FILE_TITLE
        raw += "\n[%s]\n" %const.CONF_FILE_LOCALDIRS
        for d in self.localDirs:  raw += "dir%s=%s\n" %(self.localDirs.index(d), d)
        raw += "\n[%s]\n" %const.CONF_FILE_REMOTEURLS
        for d in self.remoteUrls:  raw += "url%s=%s\n" %(self.remoteUrls.index(d), d)
        raw += "\n[%s]\n" %const.CONF_FILE_USER
        raw += "%s=%s\n" %(const.CONF_FILE_USER_NAME, self.name)
        raw += "%s=%s\n" %(const.CONF_FILE_USER_EMAIL, self.email)
        raw += "\n[%s]\n" %const.CONF_FILE_WORKSPACE
        raw += "%s=%s\n" %(const.CONF_FILE_WORKSPACE_PATH, self.workspace)
        raw += "\n[%s]\n" %const.CONF_FILE_GENERAL
        raw += "%s=%s\n" %(const.CONF_FILE_GENERAL_PIM_PATH, self.pim)
        if savefile(self.__file, raw):  return(True)
        return(False)





    def create(self):
        self.__initDefaults()
        if self.__makeDirs():
            if self.save():     return(True)
        return(False)




    def __initDefaults(self):
        self.workspace = path.join(path.expanduser("~"), const.DEFAULT_WORKSPACE)





    def __makeDirs(self):
        try:
            makedirs(path.join(path.expanduser("~"), const.CONF_PATH))
        except:
            return(False)
        return(True)













