from cStringIO import StringIO
from pprint import pprint

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
  pprint(sorted(data, key=lambda (k,v): v[0]))