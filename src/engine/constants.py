#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#Author: Read AUTHORS file.
#License: Read COPYING file.


class _const:
    class ConstError(TypeError): pass
    def __setattr__(self,name,value):
        if self.__dict__.has_key(name):
            raise self.ConstError, "Can't rebind const(%s)"%name
        self.__dict__[name]=value


const = _const()


const.PISI_EXT = ".pisi"
const.REPO_PATH = "repo"
const.SYS_ROOT = "/"

#ACTION CODES
const.ACT_LOAD_PACKAGES_FROM_PISI_PATH = "01"
const.ACT_LOAD_PISI_CONF = "02"
const.ACT_SAVE_PASO_FILE = "03"