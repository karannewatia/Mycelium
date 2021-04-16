# A simple python script to generate a 2*nth root of unity mod p
# Requires that p = 1 (mod 2n)

from random import *

p = 2661133959799589672036590708237675984973638057068497021452622131886244052869803741648438540534925799893994831564937294541065181388700035350795108331241972926532026369
n = 32768

y = (p-1)/(2*n)

z = 1
w = p-1
while z!= (p-1):
  a = randrange(0, p)
  w = pow(a, y, p)
  z = pow(w, n, p)

print w
