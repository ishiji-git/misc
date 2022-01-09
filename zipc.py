#!/usr/bin/env python
# -*- coding: sjis -*-

import zipfile
import glob
import os
import sys

class zipc():
    def __init__(self):
        """
            set default
                compression = ZIP_DEFLATED
                allowZip64 = True
                complessionlevel = None (auto)
        """
        self.compression = zipfile.ZIP_DEFLATED
        self.allowZip64 = True
        self.compresslevel = None
        pass

    def create(self, archive, args, mode="w"):
        """
            create(archive, args)
                  archive: zip file path
                  args:    list of files
                  return:  -
        """
        def makelist(path):
            """
              glob.glob("**",recursive=True) が .(dot)で始まるファイル/ディレクトリを
              globしてくれないので、os.listdir() でやる。
            """
            r = []
            fl = os.listdir(path)
            for x in fl:
                x = os.path.join(path, x)
                try:
                    if os.path.isdir(x):
                        r.append(x)
                        r += makelist(x)
                    else:
                        r.append(x)
                except:
                    r.append(x)
            return sorted(list(set(r)))

        tmplist = []
        with zipfile.ZipFile(archive, mode=mode, compression=self.compression,
                allowZip64=self.allowZip64, compresslevel=self.compresslevel) as z:
            for arg in args:
                print("arg:" + arg)
                tmplist += makelist(arg)
            filelist = sorted(tmplist)
            for f in filelist:
                try:
                    os.stat(f)
                    print(f)
                    z.write(f)
                except:
                    print("Error: "+f)
                    z.write(".", f) # empty directory
        z.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: {} archive file [file ...]".format(sys.argv[0]))
        sys.exit(2)

    arc = sys.argv[1]
    fls = sys.argv[2:]

    try:
        z = zipc()
        z.create(arc, fls)
    except Exception as err:
        print(err)
        sys.exit(1)


