from ring import Ring
from lwe import LWE
import random
import sympy

#change these as needed
lgP = 100 #ciphertext modulus bitsize
lgM = 10 #plaintext modulus bitsize
lgN = 7
l = 5 #plaintext length (number of elements)

#don't change these
n = 1 << lgN #polynomial degree
N = 1 #used in binomial distribution

# ########### generate p (ciphertext modulus) ###############
p = 4
while (not sympy.isprime(p)):
  p = random.randrange(2**(lgP-lgM-2), 2**(lgP-lgM-1)-1) * 2**(lgM+1) +1

print("############ p ###############")
print(p)

########### generate w (used for polynomial multiplication) ###############
y = (p-1)/(2*n)
z = 1
w = p-1
while z!= (p-1):
  a = random.randrange(0, p)
  w = pow(a, y, p)
  z = pow(w, n, p)

print("############ w ###############")
print(w)
