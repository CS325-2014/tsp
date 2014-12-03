#-----------------------------------------------------------------------------#
# Name: tsp.py
# Desc: Implementation for Traveling Salesman Project for CS 325
# Auth: Cezary Wojcik, Sean McGlothlin, Matthew Eilertson
# Note:
# Opts: -i, --inputfile     : specify input file (defaults to "test.txt")
#       -o, --outputfile    : specify output file for results
#       -d, --debug           : show debug messages
#-----------------------------------------------------------------------------#

# ---- [ imports ] ------------------------------------------------------------

import getopt, sys, math, random

# ---- [ constants ] ----------------------------------------------------------

THRESHOLD = 6
GRID_SIZE = 5

# ---- [ globals ] ------------------------------------------------------------

debug = False
outputfile = "tsp_grp3.txt"

# ---- [ classes ] ------------------------------------------------------------

class City():
  def __init__(self, line):
    arr = line.split(' ')
    self.id = str(arr[0])
    self.x = int(arr[1])
    self.y = int(arr[2])

  def __repr__(self):
    return "(" + str(self.x) + ", " + str(self.y) + ") - " + self.id

class Block():
  def __init__(self):
    self.cities = []

  def __repr__(self):
    if len(self.cities) == 0:
      return "0"
    if not isinstance(self.cities[0], list):
      return str(len(self.cities))
    return str(self.cities)

  def finalize(self):
    if len(self.cities) > THRESHOLD:
      self.cities = partition(self.cities)

  def compute_path(self):
    if not isinstance(self.cities[0], list):
      self.path = pathfinder(self.cities)

# ---- [ tsp utility functions ] ----------------------------------------------

def run(inputfile):
  with open(inputfile) as f:
    arr = f.readlines()
    block = Block()
    block.cities = [City(x) for x in arr]
    block.finalize()
    print block

def partition(cities):
  max_x = max([city.x for city in cities])
  max_y = max([city.y for city in cities])

  x_step = int(max_x / GRID_SIZE)
  y_step = int(max_y / GRID_SIZE)

  blocks = [[Block() for x in range(GRID_SIZE)]
    for x in range(GRID_SIZE)]

  for city in cities:
    x = min(int(city.x/x_step), GRID_SIZE - 1)
    y = min(int(city.y/y_step), GRID_SIZE - 1)
    blocks[x][y].cities.append(city)
    blocks[x][y].x = x
    blocks[x][y].y = y

  for block_row in blocks:
    for block in block_row:
      block.finalize()

  return blocks

def distance(cities):
  if len(cities) == 2:
    return math.sqrt(math.pow((cities[0].y - cities[1].y), 2)
     + math.pow((cities[0].x - cities[1].x), 2))
  total = 0
  for i in range(0, len(cities) - 1):
    total += distance([cities[i], cities[i + 1]])
  return total

def pathfinder(cities):
  best_path = []
  best_distance = sys.maxint
  for i in range(0, len(cities) * len(cities)):
    random.shuffle(cities)
    if best_distance > distance(cities):
      best_path = cities.copy()
      best_distance = distance(best_path)
  return best_path

# ---- [ general utility functions ] ------------------------------------------

def handle_error(message):
  print "Error: {0}".format(message)
  sys.exit(2)

def debug_message(message):
  global debug
  if debug:
    print message

# ---- [ main ] ---------------------------------------------------------------

def main(argv):
  global debug, outputfile

  try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:o:d',
      ['inputfile=', 'outputfile=', 'debug'])
  except getopt.GetoptError as err:
    handle_error(str(err))

  inputfile = "test.txt"

  for o, a in opts:
    if o in ['-i', '--inputfile']:
      inputfile = a
    elif o in ['-o', '--outputfile']:
      outputfile = a
    elif o in ['-d', '--debug']:
      debug = True
    else:
      handle_error("unhandled option '{0}' detected".format(o))

  # create results output file
  try:
    f = open(outputfile, "w+")
    f.close()
  except IOError:
    handle_error("failed to write to file, '{0}'."
      .format(outputfile))

  run(inputfile)

if __name__ == "__main__":
    main(sys.argv[1:])
