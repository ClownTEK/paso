#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#Author: Read AUTHORS file.
#License: Read COPYING file.


#from xml.dom.minidom import parseString
import lib
from constants import const
from lib import eventHandler
import os





class isoBuilder(object):
    #Builds .iso file




    def __init__(self):
        self.clear()
        self.onAddPackage = eventHandler()      #(elementName, totalElements, currentElement)
        self.onError = eventHandler()           #(errorCode, errorData)
        self.__totalJob = 3




    def clear(self):
        self.__isoSource = ""
        self.__isoName = ""
        self.__break = False







    def build(self, source, outDir, isoDir):
        #("paso file", "where will be create .iso file", "mounted Pardus CD directory")
        self.clear()
        self.__isoSource = outDir+"/"+lib.stripFilename(source, const.PASO_EXT)
        self.__isoName = self.__isoSource+const.ISO_EXT
        #copy files from CD and build iso
        if self.__cpFiles(isoDir):
            if self.__buildIso():
                self.onAddPackage.raiseEvent("", self.__totalJob, 3)




    def __cpFiles(self, isoDir):
        #
        uriList = lib.listdir(isoDir)
        if uriList:
            uriList.sort()
        for uri in uriList:
            if uri <> "repo":
                self.onAddPackage.raiseEvent(uri+"...", self.__totalJob, 1)
                cmd = "cp -rf "+isoDir+"/"+uri+" "+self.__isoSource
                if os.system(cmd) <> 0:
                    self.onError.raiseEvent(const.ERR_05_ID, uri)
                    return(False)
        return( True )






    def __buildIso(self):
        #
        self.onAddPackage.raiseEvent(self.__isoName+"...", self.__totalJob, 2)
        #I copied the cmd from pardusman :)
        cmd = 'mkisofs -f -J -joliet-long -R -l -V Pardus -o '+self.__isoName+' -b boot/isolinux/isolinux.bin -c boot/isolinux/boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table '+self.__isoSource
        if os.system(cmd) <> 0:
            self.onError.raiseEvent( const.ERR_09_ID, self.__isoName)
            return(False)
        return( True )




'''
run('mkisofs -f -J -joliet-long -R -l -V "Pardus" -o "%s" -b boot/isolinux/isolinux.bin -c boot/isolinux/boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table "%s"' % (
            iso_file,
            iso_dir,
        ))

mkisofs -o $ISONAME.iso -b isolinux/isolinux.bin -c isolinux/boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table -l -allow-leading-dots -relaxed-filenames -joliet-long -max-iso9660-filenames -D -R -J -T -V $VOLID -v /path/to/directory/full/of/files

'''
