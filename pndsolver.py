#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Puzzle and Dragons Solver.

Usage:
  pndsolver.py grab
  pndsolver.py load <filename>

Options:
  -h --help     Show this screen.
"""

from subprocess import check_output

from docopt import docopt

import contextlib
import tempfile
import shutil
import os

import cv2

from lib.classifier import classify_orbs
from lib.util import print_board

@contextlib.contextmanager
def temp_dir_ctx(*args, **kwargs):
  temp = tempfile.mkdtemp(*args, **kwargs)
  orig = os.getcwd()
  try:
    os.chdir(temp)
    yield
  finally:
    shutil.rmtree(temp)
    os.chdir(orig)

if __name__ == '__main__':
  args = docopt(__doc__)

  if args['grab']:
    with temp_dir_ctx():
      s = check_output('idevicescreenshot')
      filename = s.strip().split(' ')[-1]
      frame = cv2.imread(filename)

  if args['load']:
    frame = cv2.imread(args['<filename>'])

  board = classify_orbs(frame)
  print_board(board)
