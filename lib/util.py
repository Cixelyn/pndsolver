import contextlib
import tempfile
import shutil
import os

from cStringIO import StringIO
from pprint import pprint
import numpy as np

from xtermcolor import colorize

from .data import ORB_DATA


def board_to_coloredstring(board):
  sb = StringIO()
  for y in range(5):
    for x in range(6):
      od = ORB_DATA[board.get((x, y))]
      plus = board.get_plus(((x, y)))
      sb.write(colorize(od.termchar,
                        ansi=od.termcolor,
                        ansi_bg=21 if plus else None,
                        ))
    sb.write('\n')
  return sb.getvalue()


def board_to_pndopt(board):
  sb = StringIO()
  for d in board.data:
    sb.write(ORB_DATA[d & 0x0F].abbr)
  return sb.getvalue()


def debug_hue_ranges():
  data = [(od.name, od.huerange) for od in ORB_DATA.values() if od.huerange]
  pprint(sorted(data, key=lambda (k, v): v[0]))


def bgr_to_rgb(img):
  return np.fliplr(img.reshape(-1,3)).reshape(img.shape)

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
