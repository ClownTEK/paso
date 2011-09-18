#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Python project dist and i18n utilities
# Ali Erkan İMREK <alierkanimrek at gmail.com>
#

import os
import glob
import sys

from distutils.core import setup
from distutils.cmd import Command
from distutils.command.build import build
from distutils.command.install import install

from src.constants import const




def help():
    print "Python project dist and i18n utilities\n"
    print "Examples:\n"
    print "\tClear project    : python setup.py clear"
    print "\tBuild project    : python setup.py build"
    print "\tInstall project  : python setup.py install"
    print "\tUpdate locales   : python setup.py ts-update"
    print "\tShow help        : python setup.py help"




def makeDirs(dir):
    try:
        os.makedirs(dir)
    except OSError:
        print("%s could not be created." % dir)
        return(False)
    return(True)




def clear():
    os.system("find ./ -iname '*.pyc' |xargs rm -rfv")
    os.system("find ./ -iname '*~' |xargs rm -rfv")
    os.system("find ./src -iname '*.mo' | xargs rm -rfv")
    os.system("find ./src -iname '*.qm' | xargs rm -rfv")
    os.system("find ./src -iname 'ui_*.py' | xargs rm -rfv")
    os.system("find ./ -iname 'MANIFEST' | xargs rm -rfv")
    os.system("find ./ -iname 'lokalize-scripts' | xargs rm -rfv")




def tsUpdate():
    if uiUpdate("src"):
        print("ts Files are updating...")
        for filename in glob.glob1("ts", "*.ts"):
            if os.system("pylupdate4 src/*.py  -ts ts/%s" % filename):
                print("%s could not be updated." % filename)
                return(False)
    return(True)




def uiUpdate(target):
    print("ui Files are building...")
    for filename in glob.glob1("ui", "*.ui"):
        if os.system("/usr/bin/pyuic4 -o %s/ui_%s.py ui/%s" % (target, filename.split(".")[0], filename)):
            print "%s could not be compiled." % filename
            return(False)
    return(True)




def rcUpdate(target):
    print("qrc Files are building...")
    for filename in glob.glob1("rc", "*.qrc"):
        if os.system("/usr/bin/pyrcc4 -o %s/%s_rc.py rc/%s" % (target, filename.split(".")[0], filename)):
            print "%s could not be compiled." % filename
            return(False)
    return(True)




def qmUpdate(target):
    print("qm Files are building...")
    for filename in glob.glob1("ts", "*.ts"):
        if os.system("lrelease ts/%s -qm %s/%s.qm" % (filename, target, filename.split(".")[0])):
            print "%s could not be compiled." % filename
            return(False)
    return(True)





class Build(build):
    def run(self):
        os.system("/bin/rm -rf build")
        clear()
        logo = "rc/"+const.APP_LOGO
        desktop = "addfiles/%s.desktop" %const.APP_NAME
        dirs = ["build/lib/%s" %const.APP_NAME,
                "build/share/%s/translations" %const.APP_NAME,
                "build/bin",
                "build/share/applications",
                "build/share/pixmaps",
                "build/share/doc/%s" %const.APP_NAME]
        for dir in dirs:
            if not makeDirs(dir):   return(False)
        os.system("cp -Rfv src/* %s" % dirs[0])
        if not uiUpdate(dirs[0]):   return(False)
        if not rcUpdate(dirs[0]):   return(False)
        self.copy_file("src/%s.py" %const.APP_NAME, "%s/%s" % (dirs[2], const.APP_NAME) )
        if not qmUpdate(dirs[1]):   return(False)
        try:
            self.copy_file(logo, "%s/%s.png" %(dirs[4],const.APP_NAME))
            self.copy_file(desktop, dirs[3])
        except:
            pass
        self.copy_file("src/%s.py" %const.APP_NAME, "build/lib/" )
        print "Build succesful."





class Install(install):
    def run(self):
        if not os.path.isfile("build/lib/%s/%s_rc.py" %(const.APP_NAME, const.APP_NAME) ):
            print "Build process could not be completed."
            return()
        lib = os.path.join(self.root, self.install_libbase, const.APP_NAME)
        usr = os.path.join(self.root, "/usr")
        exe = os.path.join(usr, "bin", const.APP_NAME)
        makeDirs(usr)
        makeDirs(lib)
        os.system("cp -aRv build/bin %s" %usr)
        os.system("chmod +x %s" %exe )
        os.system("cp -aRv build/share %s" %usr)
        os.system("/bin/rm build/lib/%s.py" %const.APP_NAME)
        os.system("cp -aRv build/lib/%s/* %s" %(const.APP_NAME, lib) )




if "ts-update" in sys.argv:
    tsUpdate()
    sys.exit(0)
if "clear" in sys.argv:
    clear()
    sys.exit(0)
if len(sys.argv) < 2 or "help" in sys.argv:
    help()
    sys.exit(0)




setup(
      name              = const.APP_NAME,
      version           = const.VERSION,
      license           = "GPLv3",
      author            = const.DEVELOPERS,
      url               = const.WEBPAGE,
      packages          = ["src"],
      data_files        = [],
      cmdclass          = {
                            'build': Build,
                            'install': Install
                          }
)
