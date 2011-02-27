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

const.NAME = "Paso"
const.VERSION = "2.0_Alpha"
const.WEBPAGE = "http://github.com/alierkanimrek/paso"
const.DEVELOPERS = unicode("Ali Erkan İMREK   &lt;alierkanimrek@gmail.com&gt; <p> ")
const.TRANSLATORS = "<p>"
const.DESIGNERS = unicode("Abdülkerim AYDIN   &lt;a.kerim.aydin@gmail.com&gt; <p> ")

const.APP_NAME = "paso"
const.APP_LOGO = "Paso_logo32.png"
const.APP_I18NDIR = "/usr/share/locale/"



const.PASO_EXT = ".paso"

const.CONF_PATH = ".config/paso"
const.CONF_FILE = "paso.conf"
const.CONF_FILE_TITLE = "#PASO Configuration file\n\n"
const.CONF_FILE_LOCALDIRS = "LocalDirs"
const.CONF_FILE_REMOTEURLS = "RemoteUrls"
const.CONF_FILE_USER = "User"
const.CONF_FILE_USER_NAME = "name"
const.CONF_FILE_USER_EMAIL = "email"
const.CONF_FILE_WORKSPACE = "Workspace"
const.CONF_FILE_WORKSPACE_PATH = "path"
const.CONF_FILE_GENERAL = "General"
const.CONF_FILE_GENERAL_PIM_PATH = "pimpath"


const.DEFAULT_WORKSPACE = const.APP_NAME
const.PIM_REPO = "repo"
const.REMOTE_PREFIX = ["http://", "HTTP://"]

const.INSTALLER_NAME = "yali"