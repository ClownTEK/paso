#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#
#Author: Read AUTHORS file.
#License: Read COPYING file.



import ConfigParser
from constants import const
from lib import eventHandler
import lib
import os







class config(object):




    def __init__(self):
        self.user = {}
        self.dirs = {}
        self.onFirstTime = eventHandler()
        self.onError = eventHandler()
        self.__file = os.path.expanduser("~")+"/"+const.CONFIG_FILE






    def load(self):
        #
        if not os.path.isfile(self.__file):
            self.onFirstTime.raiseEvent()
            return(False)
        config = ConfigParser.SafeConfigParser()
        try:
            config.read([self.__file])
            self.user["name"] = config.get("user","name")
            self.user["email"] = config.get("user", "email")
            self.dirs["cd"] = config.get("dirs", "cd")
            self.dirs["alt"] = config.get("dirs", "alt")
            self.dirs["output"] = config.get("dirs", "output")
            self.dirs["root"] = config.get("dirs", "root")
        except:
            self.onError.raiseEvent()
            return(False)
        return(True)





    def save(self):
        #
        raw = "#This is PASO Configuration File"
        raw += "\n\n[user]"
        raw += "\nname = "+self.user["name"]
        raw += "\nemail = "+self.user["email"]
        raw += "\n\n[dirs]"
        for key in self.dirs.keys():
            raw += "\n"+key+" = "+self.dirs[key]
        return(lib.savefile(self.__file, raw))







