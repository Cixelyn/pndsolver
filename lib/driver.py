""" utilities for grabbing data directly from the phone
"""

from subprocess import check_output
import cStringIO
import numpy


import cv2

from .util import temp_dir_ctx

import setuptools


class Driver(object):
  dependencies = []

  def check_dependencies(self):
    for d in self.dependencies:
      if not setuptools.distutils.spawn.find_executable(d):
        raise Exception("Missing driver dependency: %s" % d)

  def capture(self):
    raise NotImplementedError('driver capture method unimplemented')

  def run_path(self):
    raise NotImplementedError('driver path runner not implemented')


class MockDriver(Driver):
  def capture(self):
    return cv2.imread('./examples/test.png')

  def run_path(self):
    pass


class IosDriver(Driver):
  dependencies = ['idevicescreenshot']

  def capture(self):
    with temp_dir_ctx():
      s = check_output('idevicescreenshot')
      filename = s.strip().split(' ')[-1]
      frame = cv2.imread(filename)
      return frame


class AndroidDriver(Driver):
  dependencies = ['monkeyrunner', 'adb']
