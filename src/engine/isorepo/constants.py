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


const.REMOTE_HTTP = "http://"

const.DOWNLOADING_EXT = ".part"
const.PISI_BUILD_INDEX_CMD = "pisi ix --skip-signing --compression-types bz2"
const.PISI_INDEX_XML_FILE = "pisi-index.xml"
const.PISI_INDEX_SHA1SUM_FILE = "pisi-index.xml.sha1sum"

