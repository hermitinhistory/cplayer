#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import csv
import shutil


def mplayer(filename, ss='0', args=[]):
    import subprocess as sp

    if filename[0] != '"':
        filename = '"' + filename + '"'
    cmd2play = 'mplayer ' + filename + ' -ss ' + ss + ' ' + ' '.join(args)
    print cmd2play
    cmd2play += ' 2>/dev/null'

    player_out_txt = sp.check_output(cmd2play, shell=True)
    try:
        tline = player_out_txt[-200:].split('\r')[-2]
        t = int(tline.split(':')[1].split('.')[0].strip())
    except:
        return None

    # seek backward 10 sec
    t = t - 10
    if t < 0:
        t = 0

    return str(t)


def read_ss(confile, play):
    r = csv.reader(open(confile, 'rb'))
    for row in r:
        if len(row) != 2:
            continue  # skip the broken line
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
        if len(row) != 2:
            continue  # skip the broken line

        # update the play
        if row[0] == play:
            w.writerow([play, ss])
            writed = True
        else:
            w.writerow(row)

    # write the new play
    if not writed:
        w.writerow([play, ss])

    rf.close()
    wf.close()

    shutil.move(tmpfile, confile)


def get_the_latest_avfile_list(configfile):
    def sort_cmp(x, y):
        import re
        digit_in_x = map(int, re.findall(r'\d+', x))
        digit_in_y = map(int, re.findall(r'\d+', y))
        return 1 if digit_in_x > digit_in_y else -1

    avsuffix = ['mp4', 'f4v', 'flv']
    avfiles = filter(lambda x: os.path.isfile(x) and x.split('.')[-1] in avsuffix, os.listdir('./'))
    avfiles.sort(cmp=sort_cmp)
    avfiles = map(os.path.abspath, avfiles)

    try:
        play, ss = open(configfile, 'rb').readlines()[-1].strip().split(',')
        i = avfiles.index(play)
    except:
        i = 0
    return avfiles[i:]


def play_the_given_file(file2play, configfile, args=''):
    firstflay = True
    for play in file2play:
        if not firstflay:
            prompt = play + ', continue(y/n):[y] '
            c = raw_input(prompt)
            if c != '' and c != 'y':
                break

        firstflay = False

        confile = os.path.join(os.path.dirname(play), configfile)
        os.system('touch ' + confile)  # create the confile when not exists

        for i in range(len(args)):
            if args[i] == '-ss':
                ss = args[i + 1]
                break
        else:
            ss = read_ss(confile, play)

        # remove the '-ss'
        if '-ss' in args:
            index = args.index('-ss')
            args.remove(args[index + 1])
            args.remove('-ss')

        t = mplayer(play, ss, args)
        if t is not None:
            write_ss(confile, play, t)


def main(file2play, configfile, args):
    if len(file2play) == 0:
        file2play = get_the_latest_avfile_list(configfile)

    play_the_given_file(file2play, configfile, args)


if __name__ == '__main__':
    configfile = '.cplayer.txt'

    file2play = [a for a in sys.argv[1:] if os.path.exists(a)]
    args = [a for a in sys.argv[1:] if a not in file2play]
    file2play = [os.path.abspath(a) for a in file2play]
    main(file2play, configfile, args)
