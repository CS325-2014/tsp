#-----------------------------------------------------------------------------#
# Name: tsp.py
# Desc: Implementation for Traveling Salesman Project for CS 325
# Auth: Cezary Wojcik, Sean McGlothlin, Matthew Eilertson
# Note:
# Opts: -i, --inputfile     : specify input file (defaults to "test.txt")
#       -o, --outputfile    : specify output file for results
#       -s, --speedconstant : specify speed constant
#       -d, --debug         : show debug messages
#-----------------------------------------------------------------------------#

# ---- [ imports ] ------------------------------------------------------------

import getopt, math, random, re, sys

# ---- [ constants ] ----------------------------------------------------------

THRESHOLD = 6
GRID_SIZE = 5

# ---- [ globals ] ------------------------------------------------------------

debug = False
outputfile = "tsp_grp3.txt"
speed_constant = 3

# ---- [ classes ] ------------------------------------------------------------

class City():
  def __init__(self, line):
    arr = re.sub(r"\s+", " ", line).strip().split(' ')
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

  def size(self):
    if len(self.cities) == 0:
      return 0
    if not isinstance(self.cities[0], list):
      return len(self.cities)
    else:
      return len(sum(self.cities, []))

  def finalize(self):
    if len(self.cities) > THRESHOLD:
      self.cities = partition(self.cities)

  def compute_path(self):
    if not isinstance(self.cities[0], list):
      self.path = pathfinder(self.cities)
    else:
      blocks = filter(lambda x: x.size() > 0, sum(self.cities, []))
      for block in blocks:
        block.compute_path()
      self.path = pathfinder(blocks)

# ---- [ tsp utility functions ] ----------------------------------------------

def run(inputfile):
  global outputfile
  with open(inputfile) as f:
    arr = f.readlines()
    block = Block()
    block.cities = [City(x) for x in arr]
    block.finalize()
    block.compute_path()
    path = get_path(block)
    dist = distance(path) + distance([path[0], path[-1]])
    f = open(outputfile, "w+")
    f.write(str(int(dist)) + "\n")
    print str(int(dist))
    for city in path:
      f.write(city.id + "\n")

def get_path(block):
  path = []
  if isinstance(block, City):
    return [block]
  if isinstance(block, list):
    if isinstance(block[0], City):
      return block
    else:
      for el in block:
        path.extend(get_path(el))
      return path
  for el in block.path:
    path.extend(get_path(el))
  return path

def partition(cities):
  min_x = min([city.x for city in cities])
  min_y = min([city.y for city in cities])
  max_x = max([city.x for city in cities])
  max_y = max([city.y for city in cities])

  x_step = int((max_x - min_x) / GRID_SIZE)
  y_step = int((max_y - min_y) / GRID_SIZE)

  blocks = [[Block() for x in range(GRID_SIZE)]
    for x in range(GRID_SIZE)]

  for city in cities:
    x = min(int((city.x - min_x)/x_step), GRID_SIZE - 1)
    y = min(int((city.y - min_y)/y_step), GRID_SIZE - 1)
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
  global speed_constant
  best_path = []
  best_distance = sys.maxint
  for i in range(0, len(cities) ** speed_constant):
    random.shuffle(cities)
    if best_distance > distance(cities):
      best_path = cities[:]
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
  global debug, outputfile, speed_constant

  try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:o:s:d',
      ['inputfile=', 'outputfile=', 'speedconstant=', 'debug'])
  except getopt.GetoptError as err:
    handle_error(str(err))

  inputfile = "test.txt"

  for o, a in opts:
    if o in ['-i', '--inputfile']:
      inputfile = a
    elif o in ['-o', '--outputfile']:
      outputfile = a
    elif o in ['-s', '--speedconstant']:
      speed_constant = int(a)
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
