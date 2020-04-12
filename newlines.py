#! /usr/bin/env python

""" Go thorough all *.md files and fix indentations before chapters """ 

import re
from glob import glob
from typing import Iterable

N_NEWLINES = 21


def main(filenames: Iterable):
    for filename in filenames:
        contents = readfile(filename)
        contents = fix_newlines(contents)
        writefile(filename, contents)


def fix_newlines(text: str):
    return re.sub(newlines_rex, newlines_replace, text)


def readfile(filename: str):
    with open(filename, 'rt') as f:
        return f.read()


def writefile(filename: str, contents: str):
    with open(filename, 'wt') as f:
        f.write(contents)


# Regexps: find chapters (#...) and add N_NEWLINES before them
newlines_rex = re.compile(r'\n+^##', re.M)
newlines_replace = '\n'*N_NEWLINES + '##'

main(
    filenames=glob('*.md')
)
