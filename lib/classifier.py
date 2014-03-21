import cv2
import numpy as np

from .models import Board
from .data import ORB_DATA

sift = cv2.SIFT()
matcher = cv2.BFMatcher(cv2.NORM_L2)


def count_matches(matches, ratio=0.75):
    count = 0
    for m in matches:
      if len(m) == 2 and m[0].distance < m[1].distance * ratio:
        count += 1
    return count


def fix_colors(img):
  """ convert bgr to rgb """
  return np.fliplr(img.reshape(-1, 3)).reshape(img.shape)


def crop_center_square(arr, s):
  h, w, _ = arr.shape
  return arr[
      (h - s) / 2:(h + s) / 2,
      (w - s) / 2:(w + s) / 2,
      :]


def classify_orbs(frame):
  """ classifies the orbs in a given BGR frame and returns a board object """

  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV_FULL)
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

  plus = cv2.imread('resources/plus.png', 0)
  kpp, desp = sift.detectAndCompute(plus, None)

  height, width, _ = hsv.shape
  size = width / 6

  # compute true baseline from the bottom (necessary for some form-factors)
  yend = height
  while True:
    yend -= 1
    if max(hsv[yend, width / 2]) > 0:
      break

  ystart = yend - size * 5

  data = []
  for y in range(5):
    for x in range(6):
      coords = (slice(y * size + ystart, (y + 1) * size + ystart),
                slice(x * size, (x + 1) * size),
                slice(None))

      cellhsv = hsv[coords]
      cellgray = gray[coords[:2]]

      # assign cell base value
      cut = crop_center_square(cellhsv, size / 3)
      avg = np.mean(cut[:, :, 0])
      for k, v in ORB_DATA.items():
        if v.huerange:
          lower, upper = v.huerange
          if lower < avg < upper:
            cellvalue = k
            break
      else:
        raise Exception("Unidentifiable Cell (%s, %s). Hue: %s" % (x, y, avg))

      # determine cell + status
      kp2, des2 = sift.detectAndCompute(cellgray, None)
      matches = matcher.knnMatch(desp, trainDescriptors=des2, k=2)
      if count_matches(matches) > 10:
        cellvalue |= 0x10

      data.append(cellvalue)

  assert len(data) == 30
  return Board(data)


