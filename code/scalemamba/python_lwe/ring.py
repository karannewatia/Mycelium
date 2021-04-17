import random
import numpy as np
from sympy import ntt, intt
# random.seed(100)

class Ring(object):

  # Defines parameters for the ring Z/pZ/<X^n + 1>
  # i.e. A ring of polynomials where coefficients are
  #   in Z/pZ, and where polynomial multiplication is
  #   reduced over X^n+1
  # p is the prime modulus natively used by SCALE-MAMBA
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
    if a >= 0:
        return a % self.p
    else:
        return a % self.p

  # Return a random element in [0, p)
  def randElem(self):
    return random.randint(0, p-1)
    #return sint.get_random_triple()[0]

  # Return a random cint in [0, p)
  def randElemClear(self):
    return self.randElem()

  # Returns 0 or 1 each with chance 0.5
  def randBit(self):
    #b = sint.get_random_int(1)
    b = random.randint(0,1)
    return b

  # Selects r from (X~B(2n, 0.5) - n) mod p
  # i.e. should be centered at 0
  def modBinom(self, n):
    #r = sint(0)
    r = 0
    for i in range(0, 2*n):
      r = self.get_mod(r + self.randBit())
    return self.get_mod(r - n)


  # RING OPERATIONS
  # These operations are performed in a ring Z/pZ/<x^n + 1>
  # Here p is the modulus used by SCALE-MAMBA
  # It is assumed that n = len(a) = len(b).

  # Ring addition (i.e. pointwise vector addition mod p)
  def ringAdd(self, a, b):
    #res = sint.Array(self.n)
    res = [0 for i in range(self.n)]
    #@for_range(self.n)
    #def range_body(i):
    for i in range(self.n):
      res[i] = self.get_mod(a[i] + b[i])
    return res

  # Ring subtraction (i.e. pointwise vector subtraction mod p)
  def ringSub(self, a, b):
    #res = sint.Array(self.n)
    res = [0 for i in range(self.n)]
    #@for_range(self.n)
    #def range_body(i):
    for i in range(self.n):
      res[i] = self.get_mod(a[i] - b[i])
    return res

  def ringMulTest(self, seq1, seq2):
    for i in range (len(seq1)):
        seq1[i] = int(seq1[i])
        seq2[i] = int(seq2[i])

    for i in range (len(seq1)):
        seq1[i] = (seq1[i] * pow(self.w, i, self.p)) % self.p
        seq2[i] = (seq2[i] * pow(self.w, i, self.p)) % self.p

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
        inv_psi_pow = pow(psi_pow, -1) % self.p #pow(psi_pow, -1, self.p)
        seq[i] = (seq[i] * inv_psi_pow) % self.p

    for i in range (len(seq)):
        seq[i] = int(round(seq[i]))
    return seq

  # Ring multiplication (i.e. convolution)
  # Polynomials are represented with lowest powers first
  #   e.g. (1 + 2x + 3x^2) is represented as [1, 2, 3]
  # Reduce polynomial modulo x^(len(a)) + 1
  def ringMul(self, a, b):
    n = self.n
    #conv = sint.Array(2*n)
    conv = [0 for i in range(2*n)]
    #@for_range(2*n)
    #def range_body_zero(i):
    for i in range(2*n):
      #conv[i] = sint(0)
      conv[i] = 0

    #@for_range(n**2)
    #def range_body_mul(i):
    for i in range(n**2):
      j = i % n
      k = i / n
      conv[j+k] = self.get_mod(self.get_mod(conv[j+k]) + self.get_mod(a[j] * b[k]))

    #res = sint.Array(n)
    res = [0 for i in range(n)]
    for i in range(n-1):
      res[i] = self.get_mod(conv[i] - conv[i + n])

    res[n-1] = conv[n-1]
    return res

  def ringMulNumpy(self, a, b):
    mul_res = np.polymul(a[::-1], b[::-1])
    conv_tmp = mul_res[::-1]
    if (len(conv_tmp) < 2*self.n):
        conv_tmp = np.concatenate([conv_tmp, np.zeros(2*self.n - len(conv_tmp))])

    n = self.n
    conv = [0 for i in range(2*n)]
    for i in range(2*n):
        conv[i] = self.get_mod(int(conv_tmp[i]))

    res = [0 for i in range(n)]
    for i in range(n-1):
      res[i] = self.get_mod(self.get_mod(conv[i]) - self.get_mod(conv[i + n]))

    res[n-1] = conv[n-1]
    return res

  def bitRev(self, j, nBits):
    j = self.get_mod(j)
    s = 0
    for i in range(nBits):
      s = s << 1
      s += j%2
      j = self.get_mod(j >> 1)
    return s

  # compute a ** b where a, b are cints
  def cPow(self, a, b, nBitsB):
    #p = cint(1)
    p1 = 1
    bRev = self.bitRev(b, nBitsB)
    for i in range(nBitsB):
      p1 = self.get_mod(p1**2)
      # p = p + (bRev % 2)*(p * a - p)
      p1 = self.get_mod(self.get_mod(p1 + bRev % 2) * self.get_mod(self.get_mod(p1 * a) - p1))
      bRev = bRev >> 1
    return self.get_mod(p1)

  # Find what wExp would be in the recursion
  # wExp is defined as follows
  # wExp(i, nBitsN-1) = n/2
  # To compute at item at depth d < nBitsN-1, look at row d+1 below it.
  #   At the row below there will be a sequence of equal values, of value v.
  #   If i is in the first half of this sequence, wExp(i, d) = v/2
  #   Otherwise wExp(i, d) = v/2 + n/2
  # e.g. the matrix wExp(d, i) when n=8:
  #  1 1 5 5 3 3 7 7
  #  2 2 2 2 6 6 6 6
  #  4 4 4 4 4 4 4 4
  def getWExp(self, d, i):
    n = self.n
    nBits = self.nBitsN
    base = self.get_mod(self.get_mod(self.bitRev(i, nBits)*2) + 1)
    return self.get_mod(base << d) % n

  # Return x_i, where i = 0 (false) or 1 (true)
  def mux(self, i, x0, x1):
    return x0 + i * (x1 - x0)

  # Fast Ring multiplication
  # From Bernstein, Daniel. "Fast multiplication and its applications."
  # See https://cr.yp.to/papers.html#multapps
  # a, b: operands (elements of Z/pZ/<X^n + 1>
  # a must be a cint array, b must me a sint array
  # n : length of polynomials
  # For this to work, need len(a) = len(b) = n = 2^nBitsN
  # Note that this uses operations NATIVELY in the SCALE-MAMBA field.
  # Let p be the modulus used by SCALE-MAMBA
  # We require: p = 1 (mod 2n), w^n = -1 (mod p)
  def ringMulFast(self, a, b):
    n = self.n
    nBitsN = self.nBitsN

    # Rs = sint.Matrix(nBitsN+1, n)
    # As = cint.Matrix(nBitsN+1, n)
    # Bs = sint.Matrix(nBitsN+1, n)
    Rs = [[0 for i in range(n)] for j in range(nBitsN+1)]
    As = [[0 for i in range(n)] for j in range(nBitsN+1)]
    Bs = [[0 for i in range(n)] for j in range(nBitsN+1)]

    #@for_range(n)
    #def topAB(i):
    for i in range(n):
      As[0][i] = a[i]
      Bs[0][i] = b[i]

    #@for_range(1, nBitsN+1)
    #def splitRow(k):
    for k in range(1, nBitsN+1):
      d = nBitsN - k       # Number of recursions left until base layer
      gapSize = 1 << d

      # @for_range(n)
      # def splitCell(i):
      for i in range(n):
        # c = self.cPow(self.w, self.getWExp(cint(d), cint(i)), nBitsN)
        # isRight = cint((i >> d) % 2)
        c = self.cPow(self.w, self.getWExp(d, i), nBitsN)
        isRight = self.get_mod(i >> d) % 2

    AsUp = As[k-1][i]
    if (i-gapSize) >= 0:
        AsUpL = As[k-1][i-gapSize]
    else:
        AsUpL = 0
    if (i+gapSize) < n:
        AsUpR = As[k-1][i+gapSize]
    else:
        AsUpR = 0

        AsIfLeft = self.get_mod(AsUp + self.get_mod(AsUpR * c))
        AsIfRight = self.get_mod(AsUpL - self.get_mod(AsUp*c))

        As[k][i] = self.get_mod(self.mux(isRight, AsIfLeft, AsIfRight))

    # @for_range(1, nBitsN+1)
    # def splitRow(k):
    for k in range(1, nBitsN+1):
      d = nBitsN - k       # Number of recursions left until base layer
      gapSize = 1 << d
      # @for_range(n)
      # def splitCell(i):
      for i in range(n):
        # c = self.cPow(self.w, self.getWExp(cint(d), cint(i)), nBitsN)
        # isRight = cint(((i >> d) % 2))
        c = self.cPow(self.w, self.getWExp(d, i), nBitsN)
        isRight = self.get_mod(i >> d) % 2

    BsUp = Bs[k-1][i]
    if (i-gapSize) >= 0:
        BsUpL = Bs[k-1][i-gapSize]
    else:
        BsUpL = 0
    if (i+gapSize) < n:
        BsUpR = Bs[k-1][i+gapSize]
    else:
        BsUpR = 0

        # BsIfLeft = (((BsUp + BsUpR) % p) * c) % p
        # BsIfRight = (BsUpL - BsUp*c) % p
        BsIfLeft = self.get_mod(BsUp + self.get_mod(BsUpR * c))
        BsIfRight = self.get_mod(BsUpL - self.get_mod(BsUp*c))

        Bs[k][i] = self.get_mod(self.mux(isRight, BsIfLeft, BsIfRight))

    # @for_range(n)
    # def baseRs(i):
    for i in range(n):
      Rs[nBitsN][i] = self.get_mod(As[nBitsN][i] * Bs[nBitsN][i])

    # @for_range(1, nBitsN+1)
    # def combRow(d):
    for d in range(1, nBitsN+1):
      k = nBitsN - d
      gapSize = 1 << (d-1)
      # @for_range(n)
      # def combCell(i):
      for i in range(n):
        # c = self.cPow(self.w, self.getWExp(cint(d-1), cint(i)), nBitsN)
        # isRight = cint((i >> (d-1)) % 2)
        c = self.cPow(self.w, self.getWExp(d-1, i), nBitsN)
        isRight = self.get_mod(i >> (d-1)) % 2
    if (i+gapSize) < n:
        RsLeft = self.get_mod(Rs[k+1][i] + self.get_mod(Rs[k+1][i + gapSize]))
    else:
        RsLeft = 0
        if (i-gapSize) >= 0:
            RsRight = self.get_mod(self.get_mod(Rs[k+1][i - gapSize] - Rs[k+1][i]) / c)
        else:
            RsRight = 0
        Rs[k][i] = self.get_mod(self.mux(isRight, RsLeft, RsRight))

    #res = sint.Array(n)
    res = [0 for i in range(n)]
    # @for_range(n)
    # def setRes(i):
    for i in range(n):
      res[i] = self.get_mod(Rs[0][i] / n)

    return res

  # Returns 0:
  def zero(self):
    n = self.n
    #zero = sint.Array(n)
    zero = [0 for i in range(n)]

    #@for_range(n)
    #def range_body(i):
      #zero[i] = sint(0)

    return zero

  # Random ring element
  # Returns a vector of length n
  # Each item is chosen uniformally at random from [0, p)
  # Assumes n is even
  def ringRand(self):
    n = self.n
    #res = sint.Array(n)
    res = [0 for i in range(n)]

    # @for_range(n/2)
    # def range_body(i):
    # for i in range(n/2):
    #   r = sint.get_random_triple()
    #   res[2*i] = r[0]
    #   res[2*i+1] = r[1]   # r[0] and r[1] are random and independent
    for i in range(n):
        res[i] = random.randint(0, self.p - 1)

    return res

  # Assumes n is even
  def ringRandClear(self):
    rand = self.ringRand()
    res = rand
    return res

  # Returns a vector of length n
  # Each item is chosen independently at random from (B(2N, 0.5) - N) mod p
  def ringBinom(self, N):
    n = self.n
    #res = sint.Array(n)
    res = [0 for i in range(n)]
    #@for_range(n)
    #def range_body(i):
    for i in range(n):
      res[i] = self.modBinom(N)
    return res

  def ringRevealPrettyPrint(self, a):
    print_ln("[ ")
    for i in range(0, len(a)):
      #print_ln("%s ", a[i].reveal())
      print_ln("%s ", a[i])
    print_ln("]")
    return

  # def ringReadFromFile(self, fileName):
  #   f = open(fileName, "r")
  #   a = []
  #   for line in f:
  #     if (line[0] != '[') and (line[0] != ']'):
  #       x = int(line)
  #       #a.append(cint(x))
  #       a.append(x)
  #   return a

  # def readFromPrivateInput(self, partyNum):
  #   res = []
  #   n = self.n
  #   for i in range(0, n):
  #     res.append(sint.get_raw_input_from(partyNum))
  #   return res
