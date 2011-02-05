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

const.FILE = "etc/pisi/pisi.conf"

#Conf tags
const.DIRECTORIES = "directories"
const.GENERAL = "general"
const.PACKAGES = "packages_dir"
const.CACHE = "cached_packages_dir"
const.INFO = "info_dir"
const.ARCH = "architecture"
const.DIST = "distribution"
const.RELEASE = "distribution_release"
const.DIST_ID = "distribution_id"

