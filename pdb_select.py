#!/usr/bin/env python
# -*- coding: UTF8 -*-

# Author: Guillaume Bouvier -- guillaume.bouvier@pasteur.fr
# https://research.pasteur.fr/en/member/guillaume-bouvier/
# 2018-11-19 16:26:10 (UTC+0100)

import __main__
__main__.pymol_argv = [ 'pymol', '-cqi' ]
import pymol
import pymol.cmd as cmd
pymol.finish_launching()
import sys

try:
    PDBFILENAME = sys.argv[1]
    SELECTION = sys.argv[2]
    OUTFILE = sys.argv[3]
except IndexError:
    print("Help:")
    print("    pdbselect input.pdb 'selection string' output.pdb")
    sys.exit()

cmd.load(PDBFILENAME)
cmd.save(OUTFILE, selection=SELECTION, state=1)
cmd.quit()
