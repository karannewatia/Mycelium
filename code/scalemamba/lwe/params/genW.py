# A simple python script to generate a 2*nth root of unity mod p
# Requires that p = 1 (mod 2n)

from random import *

p = 97
n = 4

y = (p-1)/(2*n)

z = 1
w = p-1
while z!= (p-1):
  a = randrange(0, p)
  w = pow(a, y, p)
  z = pow(w, n, p)

print w
