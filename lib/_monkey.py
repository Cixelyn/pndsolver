#!/usr/bin/env monkeyrunner

"""
Low level implementation of android driver
to be run via android jython monkeyrunner via cmdline
"""

import sys
import time

from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
from collections import deque

try:
  arg = sys.argv[1].lower()
except Exception:
  print "android bridge driver"
  print "usage: _monkey.py [capture | run]"
  sys.exit(0)

if arg == "capture":
  device = MonkeyRunner.waitForConnection()
  result = device.takeSnapshot()
  for b in result.convertToBytes('png'):
    sys.stdout.write(chr(b & 0xff))

elif arg == "run":
  device = MonkeyRunner.waitForConnection()

  stream = deque(sys.argv[2].split(':'))


  def pop_coords():
    x, y = map(int, stream.popleft().split(','))
    return x * 100, y * 100

  sx, sy = pop_coords()
  device.touch(sx, sy, MonkeyDevice.DOWN)

  resolution = 20.0
  steptime = 5.0 / (len(stream) * resolution)

  while stream:
    nx, ny = pop_coords()
    for i in range(resolution):
      ix = int(sx + (nx - sx) * i / resolution)
      iy = int(sy + (ny - sy) * i / resolution)
      device.touch(ix, iy, MonkeyDevice.MOVE)
      time.sleep(steptime)
    sx, sy = nx, ny

  device.touch(sx, sy, MonkeyDevice.UP)

