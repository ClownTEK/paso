#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#
#Author: Read AUTHORS file.
#License: Read COPYING file.



import ConfigParser
from constants import const
import lib
import os







class config(object):




    def __init__(self):
        self.data = {}  #{"user": {"name":"", "email":""}, "dirs": {}}
        self.onFirstTime = False
        self.__file = os.path.expanduser("~")+"/"+const.CONFIG_FILE
        self.initDefaults()






    def load(self):
        #
        if not os.path.isfile(self.__file):
            self.onFirstTime = True
            return(False)
        config = ConfigParser.SafeConfigParser()
        try:
            config.read([self.__file])
            self.data[const.OPT_USER_KEY][const.OPT_USERNAME_KEY] = unicode(config.get(const.OPT_USER_KEY,const.OPT_USERNAME_KEY), "utf-8")
            self.data[const.OPT_USER_KEY][const.OPT_USEREMAIL_KEY] = unicode(config.get(const.OPT_USER_KEY, const.OPT_USEREMAIL_KEY), "utf-8")
            self.data[const.OPT_DIRS_KEY][const.OPT_BPASODIR_KEY] = unicode(config.get(const.OPT_DIRS_KEY, const.OPT_BPASODIR_KEY), "utf-8")
            self.data[const.OPT_DIRS_KEY][const.OPT_BALTDIR_KEY] = unicode(config.get(const.OPT_DIRS_KEY, const.OPT_BALTDIR_KEY), "utf-8")
            self.data[const.OPT_DIRS_KEY][const.OPT_BCDDIR_KEY] = unicode(config.get(const.OPT_DIRS_KEY, const.OPT_BCDDIR_KEY), "utf-8")
            self.data[const.OPT_DIRS_KEY][const.OPT_BOUTDIR_KEY] = unicode(config.get(const.OPT_DIRS_KEY, const.OPT_BOUTDIR_KEY), "utf-8")
            self.data[const.OPT_DIRS_KEY][const.OPT_PPASODIR_KEY] = unicode(config.get(const.OPT_DIRS_KEY, const.OPT_PPASODIR_KEY), "utf-8")
            self.data[const.OPT_DIRS_KEY][const.OPT_PALTDIR_KEY] = unicode(config.get(const.OPT_DIRS_KEY, const.OPT_PALTDIR_KEY), "utf-8")
            self.data[const.OPT_DIRS_KEY][const.OPT_PCDDIR_KEY] = unicode(config.get(const.OPT_DIRS_KEY, const.OPT_PCDDIR_KEY), "utf-8")
            self.data[const.OPT_DIRS_KEY][const.OPT_PROOTDIR_KEY] = unicode(config.get(const.OPT_DIRS_KEY, const.OPT_PROOTDIR_KEY), "utf-8")
        except:
            return(False)
        return(True)





    def initDefaults(self):
        self.data[const.OPT_USER_KEY] = {}
        self.data[const.OPT_DIRS_KEY] = {}
        self.data[const.OPT_USER_KEY][const.OPT_USERNAME_KEY] = os.getenv("LOGNAME")
        self.data[const.OPT_USER_KEY][const.OPT_USEREMAIL_KEY] = ""
        self.data[const.OPT_DIRS_KEY][const.OPT_BPASODIR_KEY] = os.path.expanduser("~")
        self.data[const.OPT_DIRS_KEY][const.OPT_BALTDIR_KEY] = ""
        self.data[const.OPT_DIRS_KEY][const.OPT_BCDDIR_KEY] = "/media"
        self.data[const.OPT_DIRS_KEY][const.OPT_BOUTDIR_KEY] = os.path.expanduser("~")
        self.data[const.OPT_DIRS_KEY][const.OPT_PPASODIR_KEY] = os.path.expanduser("~")
        self.data[const.OPT_DIRS_KEY][const.OPT_PALTDIR_KEY] = ""
        self.data[const.OPT_DIRS_KEY][const.OPT_PCDDIR_KEY] = "/media"
        self.data[const.OPT_DIRS_KEY][const.OPT_PROOTDIR_KEY] = "/"




    def save(self):
        #
        raw = "#This is PASO Configuration File"
        raw += "\n\n[user]"
        raw += "\nname = "+self.data[const.OPT_USER_KEY][const.OPT_USERNAME_KEY]
        raw += "\nemail = "+self.data[const.OPT_USER_KEY][const.OPT_USEREMAIL_KEY]
        raw += "\n\n[dirs]"
        for key in self.data[const.OPT_DIRS_KEY].keys():
            raw += "\n"+key+" = "+self.data[const.OPT_DIRS_KEY][key]
        if not lib.savefile(self.__file, raw):
            return(False)
        return(True)










