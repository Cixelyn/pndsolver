""" board solver module
usable as a library but also as a stand-alone process (e.g. pypy integration)
"""

from collections import namedtuple

def in_board(pos):
  x, y = pos
  return (0 <= x < 6) and (0 <= y < 5)


def recurse_paths(cursor, path=tuple(), depth=2):
  newpath = path + (cursor,)

  total_paths = [newpath]
  if len(path) >= depth:
    return total_paths

  x, y = cursor
  dirs = (
    (x - 1, y),
    (x + 1, y),
    (x, y - 1),
    (x, y + 1))

  for d in dirs:
    if in_board(d) and (d != path[-1] if path else True):
      total_paths.extend(recurse_paths(d, newpath, depth))
  return total_paths


def solve_board(board, depth=5):
  max_combos = 0
  solution_board = None
  solution_path = None

  for x in range(6):
    for y in range(5):
      for p in recurse_paths((x,y), depth=depth):
        b = board.copy()
        score = b.runpath(p).score_board()
        if score > max_combos:
          max_combos = score
          solution_board = b
          solution_path = p

  solutions = [
    {
      'score': max_combos,
      'path': solution_path,
    }
  ]

  return solutions


if __name__ == '__main__':

  from models import Board
  board = Board.random_board()

  solve_board(board, 6)