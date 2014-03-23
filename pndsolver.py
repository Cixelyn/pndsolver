#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Puzzle and Dragons Solver.

Usage:
  pndsolver.py grab [-o] [--dump=<outfile>]
  pndsolver.py load <filename>
  pndsolver.py gui [--port=<port>]
  pndsolver.py debug
  pndsolver.py --help

Arguments:
  grab                    Grabs an image from an active device
  load                    Loads an image from a given file
  gui                     Opens the pndsolver gui
  debug                   Print a bunch of debug information

Options:
  -h --help               Show this screen.
  -d --dump=<outfile>     Dump captured frame to file.
  -p --port=<port>        Sets server port number [default: 9999]
  -o --pndopt             Write pndopt file to stdout
"""

from docopt import docopt

from lib.classifier import classify_orbs
from lib.util import board_to_coloredstring, board_to_pndopt, debug_hue_ranges
from lib.grabber import grab_ios

import sys

import cv2

if __name__ == '__main__':
  args = docopt(__doc__)

  if args['grab'] or args['load']:
    if args['grab']:
      frame = grab_ios()
    elif args['load']:
      frame = cv2.imread(args['<filename>'])

    board = classify_orbs(frame)
    if args['--pndopt']:
      sys.stdout.write(board_to_pndopt(board))
    else:
      sys.stdout.write(board_to_coloredstring(board))

    if args['--dump']:
      cv2.imwrite(args['--dump'], frame)

  elif args['gui']:
    from lib.server import app
    app.listen(args['--port'])

  elif args['debug']:
    debug_hue_ranges()



