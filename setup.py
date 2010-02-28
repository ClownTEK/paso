#!/usr/bin/python
# -*- coding: utf-8 -*-
#

import os
import glob
import sys

from distutils.core import setup
from distutils.cmd import Command
from distutils.command.build import build
from distutils.command.install import install

from src.constants import const



def clear():
    os.system("find ./ -iname '*.pyc' |xargs rm -rfv")
    os.system("find ./ -iname '*~' |xargs rm -rfv")
    os.system("find ./ -iname '*.mo' | xargs rm -rfv")
    os.system("find ./ -iname 'ui_*.py' | xargs rm -rfv")
    os.system("find ./ -iname 'MANIFEST' | xargs rm -rfv")
    os.system("find ./ -iname 'lokalize-scripts' | xargs rm -rfv")




def msgUpdate():
    # Generate POT file
    os.chdir("po")
    os.system("/usr/bin/intltool-update -p")
    os.system("mv untitled.pot source.pot")
    # Update PO files
    for item in os.listdir("."):
        if item.endswith(".po"):
            os.system("msgmerge -U %s source.pot" % (item) )
    os.chdir("..")
    clear()




def makeDirs(dir):
    try:
        os.makedirs(dir)
    except OSError:
        pass




class Build(build):
    def run(self):
        # Clear source and build data
        clear()
        msgUpdate()
        print os.system("/bin/rm -rf build")
        makeDirs("build/lib")
        makeDirs("build/desktop")
        makeDirs("build/bin")
        makeDirs("build/locales")
        print "Build codes..."
        os.system("cp -Rv src/*.py build/lib")
        # Collect UI files
        print "Build ui..."
        for filename in glob.glob1("qt4", "*.ui"):
            print os.system("/usr/bin/pyuic4 -o build/lib/ui_%s.py qt4/%s" % (filename.split(".")[0], filename))
        for filename in glob.glob1("qt4", "*.qrc"):
            print os.system("/usr/bin/pyrcc4 -o build/lib/%s_rc.py qt4/%s" % (filename.split(".")[0], filename))
        print "Build locales..."
        for filename in glob.glob1("po", "*.po"):
            lang = filename.rsplit(".", 1)[0]
            print os.system("msgfmt po/%s.po -o build/locales/%s.mo" % (lang, lang))
        print "Build .desktop file"
        print os.system("intltool-merge -d po addfiles/%s.desktop.in build/desktop/%s.desktop" %(const.APP_NAME, const.APP_NAME) )
        print "Build bin file"
        self.copy_file("src/%s" %const.APP_NAME, "build/bin/%s" %const.APP_NAME )  #FIX FILE NAME
        print("\n\nYou can run Paso by this command; \n python bulid/lib/paso.py ")






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
        print os.system("cp -v build/lib/* %s" %lib_dir )



if "msgupdate" in sys.argv:
    msgUpdate()
    sys.exit(0)
if "clear" in sys.argv:
    clear()
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
                            'install': Install,
                          }
)
