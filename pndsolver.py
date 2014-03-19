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

from PIL import Image
import cv2
from matplotlib import pyplot as plt
import numpy as np

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


def count_matches(matches, ratio = 0.75):
    count = 0
    for m in matches:
        if len(m) == 2 and m[0].distance < m[1].distance * ratio:
          count+=1
    return count

def fix_colors(img):
  ''' convert bgr to rgb '''
  return np.fliplr(img.reshape(-1,3)).reshape(img.shape)

if __name__ == '__main__':
  args = docopt(__doc__)

  if args['grab']:
    with temp_dir_ctx():
      s = check_output('idevicescreenshot')
      fname = s.strip().split(' ')[-1]
      frame = cv2.imread(fname)

  if args['load']:
    frame = cv2.imread(args['<filename>'])

  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV_FULL)
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

  sift = cv2.SIFT()

  plus = cv2.imread('resources/plus.png', 0)
  kpp, desp = sift.detectAndCompute(plus, None)

  matcher = cv2.BFMatcher(cv2.NORM_L2)

  height, width, _ =  hsv.shape
  size = width / 6

  def crop_center_square(arr, s):
    h, w, _ = arr.shape
    return arr[
      (h-s)/2:(h+s)/2,
      (w-s)/2:(w+s)/2,
      :]

  testdata = {
              'Fire':  (18, 32),
              'Light': (33, 47),
              'Wood':  (93, 107),
              'Water': (138, 152),
              'Dark':  (200, 214),
              'Heal':  (223, 237),
          }

  ystart = height - size * 5
  for y in range(5):
    for x in range(6):

      coords = (slice(y*size+ystart, (y+1)*size+ystart),
                slice(x*size,(x+1)*size),
                slice(None))

      cellhsv = hsv[coords]
      cellgray = gray[coords[:2]]

      kp2, des2 = sift.detectAndCompute(cellgray, None)
      matches = matcher.knnMatch(desp, trainDescriptors = des2, k=2)
      if count_matches(matches) > 10:
        print '+'

      cut = crop_center_square(cellhsv, size/3)
      avg = np.mean(cut[:, :, 0])
      for k, v in testdata.items():
        if v[0] < avg < v[1]:
          print k

