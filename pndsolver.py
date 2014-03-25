#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Puzzle and Dragons Solver.

Usage:
  pndsolver.py grab (-a | -i | -m) [-o] [--dump=<outfile>]
  pndsolver.py gui (-a | -i | -m) [--port=<port>]
  pndsolver.py load <filename>
  pndsolver.py debug
  pndsolver.py --help

Arguments:
  grab                    Grabs an image from an active device
  load                    Loads an existing image from a given file
  gui                     Opens the pndsolver gui and launches the server
  debug                   Print a bunch of debug information

Options:
  -a --android            Uses the android driver
  -i --ios                Uses the ios driver
  -m --mock               Uses the mock debug driver
  -h --help               Show this screen.
  -d --dump=<outfile>     Dump captured frame to file.
  -p --port=<port>        Sets server port number [default: 9999]
  -o --pndopt             Write pndopt file to stdout
"""

from docopt import docopt

from lib.classifier import classify_orbs
from lib.util import board_to_coloredstring, board_to_pndopt, debug_hue_ranges
import lib.driver as libdriver

from subprocess import check_call
import sys
import cv2

import logging

if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO)

  args = docopt(__doc__)

  driver = None
  if args['--android']:
    driver = libdriver.AndroidDriver()
  elif args['--ios']:
    driver = libdriver.IosDriver()
  elif args['--mock']:
    driver = libdriver.MockDriver()
  if driver:
    driver.check_dependencies()

  if args['grab'] or args['load']:
    if args['grab']:
      frame = driver.capture()
    else:
      frame = cv2.imread(args['<filename>'])

    board = classify_orbs(frame)
    if args['--pndopt']:
      sys.stdout.write(board_to_pndopt(board))
    else:
      sys.stdout.write(board_to_coloredstring(board))

    if args['--dump']:
      cv2.imwrite(args['--dump'], frame)

  elif args['gui']:
    from lib.server import create_app, run_app
    p = args['--port']
    check_call(['open', 'http://localhost:%s/index.html' % p])
    app = create_app(driver)
    run_app(app, args['--port'])

  elif args['debug']:
    debug_hue_ranges()