from ring import Ring
import numpy as np
import random

class LWE(object):

  # In order for decryption to work,
  #   N and m=2^lgM must be chosen appropriately.
  # Namely, if you wish to do t ciphertext additions
  #   and p is the size of the SCALE-MAMBA field, then need:
  #   t*2*N^2 < p / (2*m)
  def __init__(self, r, N, lgM, l, n, lgP, p):
    self.r = r  # Ring used
    self.N = N  # Half-width of binomial distributions
    # m = Modulus of ciphertext additions
    # Require p = 1 (mod 2m), and m to be a power of 2
    self.lgM = lgM
    self.m = (2 ** lgM)  # Plaintext modulus (size per element)
    self.l = l           # Plaintext length (number of elements)
    self.n = n
    self.lgP = lgP
    self.p = p
    self.mult = self.r.ringMul

  def set_p(self, new_p):
      self.p = new_p

  def get_mod(self, a):
       return a % self.p


  def decompose_gadget(self):
    g = [0 for i in range(self.lgP)]
    for i in range(self.lgP-1, -1, -1):
        g[(self.lgP-1) - i] = 2**i
    return g

  def to_binary(self, number):
      res = [0 for i in range(self.lgP)]
      if (number < 0):
          number = -number

      for i in range(self.lgP-1, -1, -1):
        if (number > 1):
            res[i] = number % 2
            number = number >> 1
        else:
            res[i] = number % 2
            number = 0

      return res

  def key_switching(self, g, s, s0):
      r = self.r
      N = self.N

      s1 = s0

      u = [r.ringRandClear() for i in range(self.lgP)]
      u_neg = [[0 for i in range(self.n)] for j in range(self.lgP)]
      for i in range(self.lgP):
          for j in range(self.n):
              u_neg[i][j] = self.get_mod(-u[i][j])

      e = [r.ringBinom(N) for i in range(self.lgP)]

      gs = [[0 for i in range(self.n)] for j in range(self.lgP)]
      for i in range(self.lgP):
        for j in range(self.n):
            gs[i][j] = self.get_mod(g[i] * s[j])

      v = [[0 for i in range(self.n)] for j in range(self.lgP)]
      for i in range(self.lgP):
        v[i] = r.ringAdd(r.ringAdd(self.mult(u_neg[i], s1), gs[i]), e[i])

      res = [s1, v, u]
      return res

  def new_ciphertext(self, c0, c1, u, v):
      r = self.r

      g_inverse = [[0 for i in range(self.lgP)] for j in range(self.n)]
      c0_new = [0 for i in range(self.n)]
      c1_new = [0 for i in range(self.n)]

      for i in range(self.n):
        tmp_binary = self.to_binary(c1[i])
        for j in range(self.lgP):
          if (c1[i] < 0):
              tmp_binary[j] = -tmp_binary[j]
          g_inverse[i][j] = tmp_binary[j]

      for i in range(self.lgP):
        gt = [0 for k in range(self.n)]
        for j in range(self.n):
          gt[j] = g_inverse[j][i]

        c0_new = r.ringAdd(self.mult(gt, u[i]), c0_new)
        c1_new = r.ringAdd(self.mult(gt, v[i]), c1_new)

      c0_new = r.ringAdd(c0_new, c0)

      return [c0_new, c1_new]


  # Returns [a, b, s]
  # (a, b) is the public key, s is the secret key
  def key_gen(self):
    r = self.r
    N = self.N
    a = r.ringRandClear()
    s = [random.randint(-1,1) for _ in range(self.n)] #coeffients of s = -1,0, or 1
    e = r.ringBinom(N)
    a_neg = [self.get_mod(-i) for i in a]
    e = [self.get_mod(self.m*i) for i in e]

    b = r.ringAdd(self.mult(a_neg, s), e)

    res = [b,a,s]
    return res

  # z is plaintext (array) of l elems each modulo m
  # returns ciphertext [u, v]
  def enc(self, b, a, z):
    r = self.r
    N = self.N
    m = self.m
    e0 = r.ringBinom(N)
    e1 = r.ringBinom(N)
    e2 = r.ringBinom(N)

    e1 = [self.get_mod(self.m*i) for i in e1]
    e2 = [self.get_mod(self.m*i) for i in e2]

    u = self.mult(a, e0)
    u = r.ringAdd(u, e1)

    mthP = self.p/m

    zMthP = r.zero()

    for i in range(0, len(z)):
      zMthP[i] = self.get_mod(z[i]) #self.get_mod(z[i] * mthP)

    v = self.mult(b, e0)
    v = r.ringAdd(v, e2)
    v = r.ringAdd(v, zMthP)

    res = [v, u]
    return res


  def dec(self, v, u, s):
    r = self.r
    lgM = self.lgM
    m = 1 << lgM
    clearM = m
    zNoisy = r.ringAdd(v, self.mult(u, s))

    halfMthP = self.p/(2*m)

    z = [0 for i in range(self.l)]
    for i in range(self.l):
      zNoisy[i] = self.get_mod(zNoisy[i] + halfMthP)
      zNoisy[i] = zNoisy[i] - halfMthP
      if abs(zNoisy[i]) >= halfMthP:
        print(" !!! dec fails !!! ")
        return [False, False]

      z[i] = zNoisy[i] % self.m

    return [z, zNoisy]

  def dec_mul(self, c0, c1, c2, s):
    r = self.r
    lgM = self.lgM
    m = 1 << lgM
    clearM = m
    s1 = self.mult(s,s)
    zNoisy = r.ringAdd(r.ringAdd(c0, self.mult(c1, s)), self.mult(c2, s1))

    halfMthP = self.p/(2*m)

    z = [0 for i in range(self.l)]
    for i in range(self.l):
         zNoisy[i] = self.get_mod(zNoisy[i] + halfMthP)
         zNoisy[i] = zNoisy[i] - halfMthP
         if abs(zNoisy[i]) >= halfMthP:
           print(" !!! dec fails !!! ")
           return [False, False]

         z[i] = zNoisy[i] % self.m

    return [z, zNoisy]

  def rl_keys(self, s, s2):
      r = self.r
      N = self.N

      tmp_a = r.ringRandClear()
      tmp_a_neg = [self.get_mod(-i) for i in tmp_a]
      tmp_e = r.ringBinom(N)
      tmp_e = [self.get_mod(self.m*i) for i in tmp_e]
      tmp_b = r.ringAdd(self.mult(tmp_a_neg, s), tmp_e)

      a = [tmp_a for i in range(self.lgP)]
      b = [tmp_b for i in range(self.lgP)]

      for i in range(self.lgP):
          s2_tmp = [self.get_mod((2**i) * j) for j in s2]
          b[i] = r.ringAdd(b[i], s2_tmp)

      return [b, a]

  def relinearization(self, b, a, c0, c1, c2, s):
      r = self.r
      c2_inverse = [[0 for i in range(self.lgP)] for j in range(self.n)]
      c0_new = [0 for i in range(self.n)]
      c1_new = [0 for i in range(self.n)]

      for i in range(self.n):
        tmp_binary = self.to_binary(c2[i])[::-1]
        for j in range(self.lgP):
          if (c2[i] < 0):
              tmp_binary[j] = -tmp_binary[j]
          c2_inverse[i][j] = tmp_binary[j]

      for i in range(self.lgP):
        ct = [0 for _ in range(self.n)]
        for j in range(self.n):
          ct[j] = c2_inverse[j][i]

        c0_new = r.ringAdd(self.mult(ct, b[i]), c0_new)
        c1_new = r.ringAdd(self.mult(ct, a[i]), c1_new)

      c0_new = r.ringAdd(c0_new, c0)
      c1_new = r.ringAdd(c1_new, c1)

      return [c0_new, c1_new]

  def add(self, u1, u2):
    r = self.r
    res = r.ringAdd(u1, u2)
    return res

  def mul(self, u1, u2):
      r = self.r
      res = self.mult(u1, u2)
      return res

  def slow_mul(self, u1, u2):
      r = self.r
      res = r.ringMul(u1, u2)
      return res



  def custom_round(self, x, base):
      return int(base * round(x/base))

  def modulus_switching(self, q0, q1, c0, c1):
      q1q0 = q1/float(q0)
      c0_new = [self.get_mod(self.custom_round(i, q1q0)) for i in c0]
      c1_new = [self.get_mod(self.custom_round(i, q1q0)) for i in c1]
      # c0_new = [self.get_mod(int(round(i*q1q0))) for i in c0]
      # c1_new = [self.get_mod(int(round(i*q1q0))) for i in c1]
      return [c0_new, c1_new]
