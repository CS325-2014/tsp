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

import getopt, sys, random

# ---- [ constants ] ----------------------------------------------------------

THRESHOLD = 7
GRID_SIZE = 10

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
    self.x = -1
    self.y = -1

  def __repr__(self):
    return str(len(self.cities))

  def finalize(self):
    if len(self.cities) > THRESHOLD:
      self.cities = partition(self.cities)

  def compute_path(self):
    # check to make sure we have a list of cities and not a grid
    if len(self.cities.shape) == 1:
      # random function goes here
      best_path = pathfinder(self.cities)
      return best_path

  def pathfinder(self, cities):
    # variable that contains the path and its length
    path_order =() 
    for i in range(0, 42):
      path_order[i][0] = random.shuffle(self.cities)
      path_order[i][1] = distance(path_order[i][0])


# ---- [ tsp utility functions ] ----------------------------------------------

def run(inputfile):
  with open(inputfile) as f:
    arr = f.readlines()
    block = Block()
    block.cities = [City(x) for x in arr]
    block.finalize()

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

  print blocks

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
