""" utilities for grabbing data directly from the phone
"""

from subprocess import check_output
import contextlib
import tempfile
import shutil
import os

import cv2


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


def grab_ios():
  with temp_dir_ctx():
    s = check_output('idevicescreenshot')
    filename = s.strip().split(' ')[-1]
    frame = cv2.imread(filename)
    return frame


def grab_android():
  pass