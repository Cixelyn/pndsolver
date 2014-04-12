import random
from collections import defaultdict


class Board(object):

  def __init__(self, data=None):
    if data is None:
      self.data = [0] * 30
    else:
      self.data = data

  @classmethod
  def random_board(cls, seed=None):
    if seed is not None:
      random.seed(seed)
    return cls([random.randint(1, 6) for _ in range(30)])

  def get_plus(self, (x,y)):
    """ gets whether a piece at a given position is a plus """
    return bool(self.data[y * 6 + x] >> 4)

  def get(self, (x, y)):
    """ gets piece color at position x. 0 if empty, -1 if out of bounds """
    if 0 <= x < 6 and 0 <= y < 5:
      return self.data[y * 6 + x] & 0x0F
    else:
      return -1

  def set(self, (x, y), value):
    self.data[y * 6 + x] = value

  def copy(self):
    return Board(list(self.data))

  def runpath(self, path):
    """ mutates board based on a given path """
    if len(path) > 1:
      for i in range(len(path) - 1):
        self.swap(path[i], path[i + 1])
    return self

  def swap(self, orb_a, orb_b):
    """ swaps the piece at a coordinate."""
    curpiece = self.get(orb_a)
    newpiece = self.get(orb_b)
    self.set(orb_a, newpiece)
    self.set(orb_b, curpiece)
    return self

  def get_matches(self):
    """ computes matches on the board """
    marked_squares = []
    for x in range(0, 6):
      for y in range(0, 5):
        hlines = ((x-1, y),
                  (x,   y),
                  (x+1, y))
        vlines = ((x, y-1),
                  (x, y  ),
                  (x, y+1))
        for line in (hlines, vlines):
          (v1, v2, v3) = map(self.get, line)
          if v1 > 0 and v1 == v2 and v1 == v3:
            marked_squares.extend(map(tuple, line))
    return frozenset(marked_squares)

  def drop_matches(self, matches):
    """ mutates a board w/ matches removed """
    for m in matches:
      self.set(m, 0)

    for n in range(5):   # the lazy man's way
      for x in range(6):
        for y in range(5 - 1):
          if self.get((x, y + 1)) == 0:
            p = (x, y)
            self.set((x, y + 1), self.get(p))
            self.set(p, 0)

  def get_current_combos(self, matches):
    """ returns a structure containing combo data for a frozen board state """
    combos = []

    # floodfill all match combos
    checked = set()
    def check(x, y, val, matchset, visitcombo):
      p = (x, y,)
      if p in matchset and self.get(p) == val and p not in checked:
        checked.add(p)
        visitcombo.add(p)
        check(x, y - 1, val, matchset, visitcombo)
        check(x, y + 1, val, matchset, visitcombo)
        check(x - 1, y, val, matchset, visitcombo)
        check(x + 1, y, val, matchset, visitcombo)
      return visitcombo

    for m in matches:
      if m not in checked:
        combos.append(check(m[0], m[1], self.get(m), matches, set()))
    return combos

  def get_all_combos(self):
    """ gets the full board combo data including drop matches """
    board = self.copy()
    combos = []
    while True:
      matches = board.get_matches()
      if len(matches):
        combos.extend(board.get_current_combos(matches))
        board.drop_matches(matches)
      else:
        break

    score = defaultdict(list)
    for c in combos:
      score[self.get(c.pop())].append(len(c) + 1)
    return score

  def __str__(self):
    rows = []
    for y in range(5):
      elements = []
      for x in range(6):
        elements.append(self.get((x, y)))
      rows.append(' '.join(map(str, elements)))
    return str('\n'.join(rows))
