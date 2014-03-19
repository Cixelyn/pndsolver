import random

class Board(object):

  def __init__(self, data=None):
    if data is None:
      self.data = [0] * 30
    else:
      self.data = data

  @classmethod
  def random_board(cls):
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
    marked_squares = set()
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
            marked_squares.update(map(tuple, line))
    return marked_squares

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

  def get_combos(self, matches):
    """ returns a structure containing combo data on the board """
    combos = []

    # floodfill all match combos
    for m in matches:
      def check(x, y, val, visited):
        p = (x,y)
        if p in matches and self.get(p) == val and p not in visited:
          visited.add(p)
          check(x  , y-1, val, visited)
          check(x  , y+1, val, visited)
          check(x-1, y  , val, visited)
          check(x+1, y  , val, visited)
        return visited
      combos.append(check(m[0], m[1], self.get(m), set()))

    # remove the duplicate ones
    combos = [sorted(c) for c in combos]
    return {c[0]: c for c in combos}.values()

  def score_board(self):
    """ scores the current configuration of the board """
    board = self.copy()
    combos = []
    while True:
      matches = board.get_matches()
      if len(matches):
        combos.extend(board.get_combos(matches))
        board.drop_matches(matches)
      else:
        break
    return len(combos)

  def __str__(self):
    rows = []
    for y in range(5):
      elements = []
      for x in range(6):
        elements.append(self.get((x, y)))
      rows.append(' '.join(map(str, elements)))
    return str('\n'.join(rows))
