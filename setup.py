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
    print "My Python project dist and i18n utilities\n"
    print "Examples:\n"
    print "\tClean project    : python setup.py clear"
    print "\tBuild project    : python setup.py build"
    print "\tInstall project  : python setup.py install"
    print "\tUpdate locales   : python setup.py msg-update"
    print "\tBuild .po file   : python setup.py build-po tr"
    print "\tShow help        : python setup.py help"



def clear():
    os.system("find ./ -iname '*.pyc' |xargs rm -rfv")
    os.system("find ./ -iname '*~' |xargs rm -rfv")
    os.system("find ./ -iname '*.mo' | xargs rm -rfv")
    os.system("find ./ -iname 'ui_*.py' | xargs rm -rfv")
    os.system("find ./ -iname 'MANIFEST' | xargs rm -rfv")
    os.system("find ./ -iname 'lokalize-scripts' | xargs rm -rfv")




def msgUpdate():
    clear()
    # Generate POT file
    os.chdir("po")
    os.system("/usr/bin/intltool-update -p")
    os.system("mv untitled.pot source.pot")
    # Update PO files
    for item in os.listdir("."):
        if item.endswith(".po"):
            print "Updating %s" %item
            os.system("msgmerge -U %s source.pot" % (item) )
    os.chdir("..")





def buildpo():
    clear()
    # Generate PO file
    os.chdir("po")
    try:
        os.system("/usr/bin/msginit -l %s" %sys.argv[2])
    except:
        print "Example: python setup.py build-po en"
        pass
    os.chdir("..")







def makeDirs(dir):
    try:
        os.makedirs(dir)
    except OSError:
        pass




class Build(build):
    def run(self):
        # Clear source and build data
        libdir = "build/lib/%s" %const.APP_NAME
        clear()
        print os.system("/bin/rm -rf build")
        makeDirs(libdir)
        makeDirs("build/desktop")
        makeDirs("build/bin")
        makeDirs("build/locales")
        print "Build codes..."
        os.system("cp -Rv src/*.py %s" %libdir)
        # Collect UI files
        print "Build ui..."
        for filename in glob.glob1("qt4", "*.ui"):
            print os.system("/usr/bin/pyuic4 -o %s/ui_%s.py qt4/%s" % (libdir, filename.split(".")[0], filename))
        for filename in glob.glob1("qt4", "*.qrc"):
            print os.system("/usr/bin/pyrcc4 -o %s/%s_rc.py qt4/%s" % (libdir, filename.split(".")[0], filename))
        print "Build locales..."
        for filename in glob.glob1("po", "*.po"):
            lang = filename.rsplit(".", 1)[0]
            print os.system("msgfmt po/%s.po -o build/locales/%s.mo" % (lang, lang))
        print "Build .desktop file"
        print os.system("intltool-merge -d po addfiles/%s.desktop.in build/desktop/%s.desktop" %(const.APP_NAME, const.APP_NAME) )
        print "Build bin file"
        self.copy_file("src/%s.py" %const.APP_NAME, "build/bin/%s" %const.APP_NAME )
        self.copy_file("src/%s.py" %const.APP_NAME, "build/lib/" )
        print("\n\nYou can run %s by this command; \n python build/lib/%s.py" %(const.APP_NAME, const.APP_NAME))






class Install(install):
    def run(self):
        print os.system("/bin/rm -rf install")
        bin_dir = os.path.join(self.root, "usr/bin")
        lib_dir = os.path.join(self.root, self.install_libbase, const.APP_NAME)
        locale_dir = os.path.join(self.root, "usr/share/locale")
        doc_dir = os.path.join(self.root, "usr/share/doc/%s" %const.APP_NAME)
        icon_dir = os.path.join(self.root, "usr/share/pixmaps")
        apps_dir = os.path.join(self.root, "usr/share/applications")
        # Make directories
        print "Making directories..."
        makeDirs(bin_dir)
        makeDirs(lib_dir)
        makeDirs(locale_dir)
        makeDirs(doc_dir)
        makeDirs(icon_dir)
        makeDirs(apps_dir)
        # Install desktop files
        print "Installing desktop and icon files..."
        try:
            self.copy_file("build/desktop/%s.desktop" %const.APP_NAME,  "%s" %apps_dir)
            self.copy_file("qt4/%s.png" %const.APP_NAME,  "%s" %icon_dir)
        except:
            pass
        # Install locales
        print "Installing locales..."
        for filename in glob.glob1("build/locales", "*.mo"):
            lang = filename.rsplit(".", 1)[0]
            try:
                os.makedirs(os.path.join(locale_dir, "%s/LC_MESSAGES" %lang))
            except OSError:
                pass
            self.copy_file("build/locales/%s.mo" % lang, os.path.join(locale_dir, "%s/LC_MESSAGES" %lang, "%s.mo" %const.APP_NAME))
        # Install Docs
        for filename in ["README", "COPYING", "AUTHORS", "ChangeLog"]:
            self.copy_file(filename, os.path.join(doc_dir) )
        print "Installing bin file"
        self.copy_file("build/bin/%s" %const.APP_NAME, "%s/%s" %(bin_dir,const.APP_NAME)  )
        os.chmod("%s/%s" %(bin_dir,const.APP_NAME), 0755)
        # Install Libraries
        print "Installing libraries... "
        print os.system("cp -v build/lib/%s/* %s" %(const.APP_NAME, lib_dir) )




if "msg-update" in sys.argv:
    msgUpdate()
    sys.exit(0)
if "build-po" in sys.argv:
    buildpo()
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
