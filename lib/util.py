from cStringIO import StringIO
from xtermcolor import colorize

from .data import ORB_DATA


def print_board(board):
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
  print sb.getvalue()
