import os
import fnmatch
import re
import argparse
# -*- coding: utf-8 -*-
__author__ = 'marcelomartins'

# Marcelo Martins, linkedin.com/in/marcelomartins
# Version 1.0
# Written on Python 2.7.10
# This script converts VTT subtitles into SRT format. Why? Coursera.

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--source", action='store', help="converts subtitles in the specified location",
                    default=".")

args = parser.parse_args()


def convert(vttformat):
    if vttformat != "0/0":
        srtformat = re.sub(r'([\d]+)\.([\d]+)', r'\1,\2', vttformat)
        srtformat = re.sub(r'WEBVTT\n\n', '', srtformat)
        srtformat = re.sub(r'^\d+\n', '', srtformat)
        srtformat = re.sub(r'\n\d+\n', '\n', srtformat)
    else:
        srtformat = vttformat
    return srtformat


def readvtt(filename):
    if os.path.exists(filename):
        f = open(filename, "r")
        content = f.read().decode("windows-1252").encode('ascii', 'ignore')
        f.close()
        return content
    else:
        print "[ERROR] Read error while reading " + filename
        return "0/0"


def writesrt(content, filename):
    if content != "0/0":
        if not os.path.exists(filename):
            try:
                f = open(filename, "w")
                f.writelines(str(content))
                f.close()
            except IOError:
                print "[ERROR] Write error while writing " + filename
            else:
                print "[DONE] " + filename
        else:
            print "[ERROR] File already exists: " + filename


def walker(source):
    matches = []
    for root, dirnames, filenames in os.walk(source):
        for filename in fnmatch.filter(filenames, '*.vtt'):
            matches.append(os.path.join(root, filename))

    for f in matches:
        writesrt(convert(readvtt(f)), os.path.splitext(f)[0] + ".srt")


if os.path.exists(args.source):
    walker(args.source)
