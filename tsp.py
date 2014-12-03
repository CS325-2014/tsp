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

import getopt, sys, re

# ---- [ globals ] ------------------------------------------------------------

debug = False
outputfile = "tsp_grp3.txt"

# ---- [ classes ] ------------------------------------------------------------

class City():
  def __init__(self):
    print "TODO"

# ---- [ utility functions ] --------------------------------------------------

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
      .format(benchmarkfile))

  # TODO - parse input file

if __name__ == "__main__":
    main(sys.argv[1:])
