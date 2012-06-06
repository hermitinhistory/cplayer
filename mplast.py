#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import csv
import shutil
import copy


# confile = os.path.expanduser('~/.mplast.conf')
lastfile = '.mplast.txt'


def mplayer(filename, ss = '0', args = []):
    import subprocess as sp

    if filename[0] != '"':
        filename = '"' + filename + '"'
    cmd2play='mplayer ' + filename + ' -ss ' + ss + ' ' + ' '.join(args)
    # print cmd2play

    tline = sp.check_output(cmd2play, shell=True)[-200:].split('\x1b[J\r')[-2]
    print tline
    t = tline.split(':')[1].split('.')[0].strip()

    # seek backward 10 sec
    t = str(int(t) - 10)
    if int(t) < 0:
        t = '0'

    return t


def read_ss(confile, play):
    r = csv.reader(open(confile, 'rb'))
    for row in r:
        if len(row) < 2: continue  # skip the broken line
        if row[0] == play:
            return row[1]

    return '0'


def write_ss(confile, play, ss):
    tmpfile = '/tmp/lskdfiudvndfklghdiuyfweml'

    rf = open(confile, 'rb')
    wf = open(tmpfile, 'wb')
    r = csv.reader(rf)
    w = csv.writer(wf)


    writed = False
    for row in r:
        if len(row) < 2: continue  # skip the broken line

        # update the play
        if row[0] == play:
            w.writerow([play, ss])
            writed = True
        else:
            w.writerow(row)

    # write the new play
    if writed == False:
        w.writerow([play, ss])

    rf.close()
    wf.close()

    shutil.move(tmpfile, confile)


def play_the_latest_file():
    for line in open(lastfile, 'rb'):
        pass

    play, ss = line.split(',')
    t = mplayer(play, ss)
    write_ss(lastfile, play, t)


def main(file2play, args):
    if len(file2play) == 0:
        play_the_latest_file()
        return

    for play in file2play:
        confile = os.path.join(os.path.dirname(play), lastfile)
        os.system('touch ' + confile)  # create the confile when not exists

        for i in range(len(args)):
            if args[i] == '-ss':
                ss = args[i+1]
                break
        else:
            ss = read_ss(confile, play)

        # remove the '-ss'
        if '-ss' in args:
            index = args.index('-ss')
            args.remove(args[index + 1])
            args.remove('-ss')

        # print args

        t = mplayer(play, ss, args)
        write_ss(confile, play, t)


if __name__ == '__main__':
    file2play = [a for a in sys.argv[1:] if os.path.exists(a)]
    args = [a for a in sys.argv[1:] if a not in file2play]
    file2play = [os.path.abspath(a) for a in file2play]
    main(file2play, args)

