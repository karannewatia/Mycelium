from fastecdsa.curve import secp256k1
from fastecdsa.point import Point

from math import sqrt
from math import ceil
from math import log

# Limit dictionary to 5 million elements.
# Otherwise may use up all the RAM of the VM, and then bad things happen
MAX_DICTIONARY_SIZE=5000000

# Needs to be consistent with .mpc file
def discrete_log_id():
  return 19


def discrete_log_kangaroo(g, a_min, a_max, b):

  sqrtDiff = int(sqrt(a_max - a_min))
  print("sqrtDiff:" + str(sqrtDiff))

  jumpRange = int(round(log(sqrtDiff, 2)))

  print("jumprange= " + str(jumpRange))

  t = (a_max + a_min)/2
  tame = g*t

  tDict = {}

  w = 0
  wild = b

  wDict = {}

  # Assume 0 <= a_min <= a <= a_max <= ord(G)/2. 
  for i in range(a_max - a_min):
    if (wild.x % sqrtDiff) < 2:
      if tDict.get(wild.x) != None:
        print(sorted(tDict.items(), key=lambda item: item[1]))
        print(sorted(wDict.items(), key=lambda item: item[1]))
        print("i=" + str(i))
        return tDict.get(wild.x) - w
      else:
        wDict[wild.x] = w
    if (tame.x % sqrtDiff) < 2:
      if wDict.get(tame.x) != None:
        print(sorted(tDict.items(), key=lambda item: item[1]))
        print(sorted(wDict.items(), key=lambda item: item[1]))
        print("i=" + str(i))
        return t - wDict.get(tame.x)
      else:
        tDict[tame.x] = t

    tStep = 2**(tame.x % jumpRange)
    t += tStep
    tame = tame + g*tStep

    wStep = 2**(wild.x % jumpRange)
    w += wStep
    wild = wild + g*wStep

  print("Something, somewhere, went horribly wrong...")
  print(tDict)
  print(wDict)


# Solve for g^a = b, where g is a secp256k1 point
# and 0 <= a < a_max
def discrete_log(g, a_min, a_max, b):
  a_diff = a_max - a_min
  h = min(int(ceil(sqrt(a_diff))), MAX_DICTIONARY_SIZE)
  w = int(ceil(a_diff/h))

  giantSteps = {}

  # Just hashing x co-ordinate.
  # Negation of point has the same x-coordinate
  #   so this is safe provided a_max < 2^255... which it better be.
  giantStep = g*a_min
  giantStepSize = g*w
  for i in range(h):
    giantSteps[giantStep.x] = (i*w + a_min)
    giantStep = giantStep + giantStepSize

  babyStep = b
  for j in range(w):
    inv = giantSteps.get(babyStep.x)
    if inv != None:
      return inv + j
    babyStep = babyStep - g

  return -1     # Didn't find it


def discrete_log_io(fin, fout, playerId, nPlayers):

  a_max = int(fin.readline())
  gx = int(fin.readline())
  gy = int(fin.readline())
  g = Point(gx, gy, secp256k1)

  bx = int(fin.readline())
  by = int(fin.readline())
  b = Point(bx, by, secp256k1)

  my_a_min = int( (playerId * a_max) / nPlayers)
  my_a_max = int( ( (playerId + 1) * a_max) / nPlayers)

  a = discrete_log(g, my_a_min, my_a_max, b)

  # To make it easy to find valid value, MPC-end just sums
  #   the inputs provided, hence outputting 0 if not found.
  if(a == -1):
    fout.write(str(0) + "\n")
  else:
    fout.write(str(a) + "\n")
  fout.flush()

  
