#!/usr/bin/env python

import os, sys
import shutil


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'which dir to process?'
        sys.exit(1)

    dirname = sys.argv[1]
    # print dirname
    os.chdir(dirname)
    allfile = os.listdir('./')
    allfile.sort()

    mp4file = filter(lambda x: x[-4:] == '.mp4', allfile)
    mp4list = map(lambda x: x.split(' - ', 2), mp4file)
    srtfile = filter(lambda x: x[-4:] == '.srt', allfile)
    srtlist = map(lambda x: x.split(' - ', 2), srtfile)

    i, j = 0, 0
    while i < len(mp4file) and j < len(srtfile):
        if mp4list[i][0] == srtlist[j][0] and mp4list[i][1] == srtlist[j][1]:
            if srtfile[j][:-4] != mp4file[i][:-4]:
                print 'mv %s %s' % (srtfile[j], mp4file[i][:-4] + '.srt')
                shutil.move(srtfile[j], mp4file[i][:-4] + '.srt')
            i += 1; j += 1
        elif mp4list[i][0] < srtlist[j][0] or mp4list[i][1] < srtlist[j][1]:
            i += 1
        else:
            j += 1
