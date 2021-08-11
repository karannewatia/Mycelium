import random
import numpy as np
from sympy import ntt, intt

class Ring(object):

  # Defines parameters for the ring Z/pZ/<X^n + 1>
  # i.e. A ring of polynomials where coefficients are
  #   in Z/pZ, and where polynomial multiplication is
  #   reduced over X^n+1
  # p is the prime modulus
  # Require also that p = 1 (mod 2n)
  # n = 2^nBitsN
  # w is a 2nth primitive root of unity
  # All are public (non-secret) values
  def __init__(self, nBitsN, w, p):
    self.n = 1 << nBitsN
    self.nBitsN = nBitsN
    self.w = w
    self.p = p
    return

  def get_mod(self, a):
    return a % self.p

  # Returns 0 or 1 each with chance 0.5
  def randBit(self):
    b = random.randint(0,1)
    return b

  # Selects r from (X~B(2n, 0.5) - n) mod p
  # i.e. should be centered at 0
  def modBinom(self, n):
    r = 0
    for i in range(0, 2*n):
      r = self.get_mod(r + self.randBit())
    return self.get_mod(r - n)

  # Ring addition (i.e. pointwise vector addition mod p)
  def ringAdd(self, a, b):
    res = [0 for i in range(self.n)]
    for i in range(self.n):
      res[i] = self.get_mod(a[i] + b[i])
    return res

  def ringMul(self, a, b):
    seq1 = [0 for i in range(self.n)]
    seq2 = [0 for i in range(self.n)]

    for i in range (len(seq1)):
        seq1[i] = (a[i] * pow(self.w, i, self.p)) % self.p
        seq2[i] = (b[i] * pow(self.w, i, self.p)) % self.p

    # compute NTT
    transform1 = ntt(seq1, self.p)
    transform2 = ntt(seq2, self.p)
    transform = [0]*len(seq1)

    # compute vector component-wise multiplication
    for i in range (len(seq1)):
        transform[i] = (transform1[i] * transform2[i]) % self.p

    # compute iNTT
    seq = intt(transform, self.p)

    # compute inv nega-cyclic vector
    for i in range (len(seq)):
        psi_pow = pow(self.w, i, self.p)
        inv_psi_pow = pow(psi_pow, -1, self.p)
        seq[i] = (seq[i] * inv_psi_pow) % self.p

    return seq

  # Returns 0:
  def zero(self):
    n = self.n
    zero = [0 for i in range(n)]
    return zero

  # Random ring element
  # Returns a vector of length n
  # Each item is chosen uniformally at random from [0, p)
  def ringRand(self):
    n = self.n
    res = [0 for i in range(n)]
    for i in range(n):
        res[i] = random.randint(0, self.p - 1)
    return res

  # Returns a vector of length n
  # Each item is chosen independently at random from (B(2N, 0.5) - N) mod p
  def ringBinom(self, N):
    n = self.n
    res = [0 for i in range(n)]
    for i in range(n):
      res[i] = self.modBinom(N)
    return res
