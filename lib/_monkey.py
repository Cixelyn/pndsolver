#!/usr/bin/env monkeyrunner

"""
Low level implementation of android driver
to be run via android jython monkeyrunner via cmdline
"""

import sys
import time

from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
from collections import deque

arg = sys.argv[-1].lower()

if arg == "capture":
  device = MonkeyRunner.waitForConnection()
  result = device.takeSnapshot()
  sys.stdout.write(result.convertToBytes('png'))

elif arg == "run":
  device = MonkeyRunner.waitForConnection()
  stream = deque(sys.stdin.read().split(';'))

  sx, sy = stream.popleft()
  device.touch(sx, sy, MonkeyDevice.DOWN)

  resolution = 10
  steptime = 3 / (len(stream) * resolution)

  while stream:
    nx, ny = stream.popleft()

    for i in range(resolution):
      device.touch(
        sx + (sx - nx) * i / resolution,
        sy + (sy - ny) * i / resolution,
        MonkeyDevice.MOVE
      )
      time.sleep(steptime)

    sx, sy = nx, ny

  device.touch(sx, sy, MonkeyDevice.UP)

else:
  print "android bridge driver"
  print "usage: _monkey.py [capture | run]"

