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


#Include const and use global values below

const.NAME = "Paso"
const.VERSION = "0.2"
const.WEBPAGE = "http://github.com/alierkanimrek/paso"
const.DEVELOPERS = "Ali Erkan İMREK  alierkanimrek[at]gmail.com <br> \
                    "
const.TRANSLATORS = ""

const.APP_NAME = "paso"
const.APP_I18NDIR = "/usr/share/locale/"


const.JOB_NONE_ID = 0
const.JOB_INS_ID = 1
const.JOB_REP_ID = 2
const.JOB_ISO_ID = 3
const.JOB_ALT_ID = 4
const.JOB_RES_ID = 5
const.JOB_PAS_ID = 6
const.JOB_PAO_ID = 7
const.JOB_ALZ_ID = 8
const.JOB_CHC_ID = 9
const.JOB_BRP_ID = 10
const.JOB_BIS_ID = 11
const.JOB_SUCCES_ID = 12
const.JOB_CONF_ID = 13
const.JOB_CONFS_ID = 14


const.OPT_CACHEPATH_VAL = "/var/cache/pisi/packages"
const.OPT_PACKPATH_VAL = "/var/lib/pisi/package"
const.OPT_INFOPATH_VAL = "/var/lib/pisi/info"
const.OPT_INDEXPATH_VAL = "/var/lib/pisi/index"
const.OPT_CDREPOPATH_VAL = "/repo"

const.PASO_METAFILE_VAL = "metadata.xml"
const.PASO_DATAFILE_VAL = "files.xml"
const.PACKAGE_INFO_FILE = "metadata.xml"
const.CONFIG_FILE = ".paso.conf"
const.PASO_EXT = ".paso"
const.ISO_EXT = ".iso"
const.PISI_EXT = ".pisi"
const.ISOINSTALLER_FILES = ["boot", "pardus.img"]


const.ERR_01_ID = 1
const.ERR_02_ID = 2
const.ERR_03_ID = 3
const.ERR_04_ID = 4
const.ERR_05_ID = 5
const.ERR_06_ID = 6
const.ERR_07_ID = 7
const.ERR_08_ID = 8
const.ERR_09_ID = 9
const.ERR_10_ID = 10
const.ERR_11_ID = 11
const.ERR_12_ID = 12

const.OPT_USER_KEY = "user"
const.OPT_DIRS_KEY = "dirs"
const.OPT_USERNAME_KEY = "name"
const.OPT_USEREMAIL_KEY = "email"
const.OPT_BPASODIR_KEY = "build_paso"
const.OPT_BCDDIR_KEY = "build_cd"
const.OPT_BALTDIR_KEY = "build_alt"
const.OPT_BOUTDIR_KEY = "build_out"
const.OPT_PPASODIR_KEY = "prepare_paso"
const.OPT_PROOTDIR_KEY = "prepare_root"
const.OPT_PCDDIR_KEY = "prepare_cd"
const.OPT_PALTDIR_KEY = "prepare_alt"