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



const.ISO_FILES = ["boot", "pardus.img"]
const.ISO_EXT = ".iso"
const.MKISO_CMD = 'mkisofs -f -J -joliet-long -R -l -V "PardusLiveImage" -o "%s" -b boot/isolinux/isolinux.bin -c boot/isolinux/boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table "%s"'
const.MKHYBRID_CMD = 'isohybrid -partok -offset 1 "%s"'