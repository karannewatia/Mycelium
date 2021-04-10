from ring import Ring
import numpy as np
import math
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
    self.p1 = p ** 3
    return

  def set_p(self, new_p):
      self.p = new_p

  def get_mod(self, a):
      return a % self.p
      # tmp = a % self.p
      # if (tmp >= self.p/2):
      #   tmp = tmp - self.p
      # return tmp

  def get_mod_pq(self, a):
    return a % (self.p * self.p1)

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

      #v = -u*s1 + g*s + e

      s1 = s0 #r.ringBinom(N)

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
        v[i] = r.ringAdd(r.ringAdd(r.ringMul(u_neg[i], s1), gs[i]), e[i])

      #k = (u|v)
      res = [s1, v, u]
      return res

  def new_ciphertext(self, c0, c1, u, v):
      #(c0', c1') = (c0, 0) + g^-1 * K, where K = (u|v)
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

        c0_new = r.ringAdd(r.ringMul(gt, u[i]), c0_new)
        c1_new = r.ringAdd(r.ringMul(gt, v[i]), c1_new)

      c0_new = r.ringAdd(c0_new, c0)

      return [c0_new, c1_new]


  # Returns [a, b, s]
  # (a, b) is the public key, s is the secret key
  def key_gen(self):
    r = self.r
    N = self.N
    a = r.ringRandClear()
    for i in range(self.n):
        if (a[i] > self.p/2):
              a[i] -= self.p
    s = [random.randrange(0,1) for i in range(self.n)]

    e = r.ringBinom(N, take_mod=False)

    b = r.ringAdd(r.ringMul(a, s, take_mod=False), e, take_mod=False)
    b = [self.get_mod(-i) for i in b]
    for i in range(self.n):
        if (b[i] > self.p/2):
              b[i] -= self.p

    res = [b,a,s]
    # print("################# public key b ###################")
    # print(b)
    # print("################# public key a ###################")
    # print(a)
    # print("################# secret key s ###################")
    # print(s)
    # print("################# error e (in key gen) ###################")
    # print(e)
    return res

  # z is plaintext (array) of l elems each modulo m
  # returns ciphertext [u, v]
  def enc(self, b, a, z):
    r = self.r
    N = self.N
    m = self.m

    e1 = r.ringBinom(N, take_mod=False)
    e2 = r.ringBinom(N, take_mod=False)
    u0 = r.ringBinom(N, take_mod=False)

    # print("############ u (as in the paper) #############")
    # print(u0)

    u = r.ringMul(a, u0, take_mod=False)
    u = r.ringAdd(u, e2)

    for i in range(self.n):
        if (u[i] > self.p/2):
              u[i] -= self.p

    mthP = self.p/m

    zMthP = r.zero()

    for i in range(0, len(z)):
      zMthP[i] = z[i] * mthP
    # print("############ delta * m #############")
    # print(zMthP)

    v = r.ringMul(b, u0, take_mod=False)
    # print("############ p0.u #############")
    # print(v)
    v = r.ringAdd(v, e1, take_mod=False)
    v = r.ringAdd(v, zMthP)

    for i in range(self.n):
        if (v[i] > self.p/2):
              v[i] -= self.p

    res = [v, u]
    # print("################# error e1 (in encrypt) ###################")
    # print(e1)
    # print("################# error e2 (in encrypt)###################")
    # print(e2)
    # print("################# ciphertext v ###################")
    # print(v)
    # print("################# ciphertext u ###################")
    # print(u)
    return res


  def dec(self, v, u, s):
    r = self.r
    lgM = self.lgM
    zNoisy = r.ringAdd(v, r.ringMul(u, s, take_mod=False), take_mod=False)
    for i in range(self.n):
        zNoisy[i] = self.get_mod(zNoisy[i])
    # print("################# zNoisy ###################")
    # print(zNoisy)

    z = [0 for i in range(self.l)]
    z_tmp = [0 for i in range(self.l)]
    for i in range(self.l):
         if (zNoisy[i] > self.p/2):
             zNoisy[i] -= self.p
         z_tmp[i] = int(round(zNoisy[i]*self.m / float(self.p)))
         z[i] = z_tmp[i] % self.m

    # print("################# z (before doing mod m) ###################")
    # print(z_tmp)

    return [z, zNoisy]


  def dec_mul(self, c0, c1, c2, s):
      r = self.r
      lgM = self.lgM
      s1 = r.ringMul(s,s)
      zNoisy = r.ringAdd(c0, r.ringMul(c1, s, take_mod=False), take_mod=False)
      zNoisy = r.ringAdd(zNoisy, r.ringMul(c2, s1, take_mod=False), take_mod=False)
      for i in range(self.n):
          zNoisy[i] = self.get_mod(zNoisy[i])
      print("################# zNoisy ###################")
      print(zNoisy)

      z = [0 for i in range(self.l)]
      z_tmp = [0 for i in range(self.l)]
      for i in range(self.l):
           if (zNoisy[i] > self.p/2):
               zNoisy[i] -= self.p
           z_tmp[i] = int(round(zNoisy[i]*self.m / float(self.p)))
           z[i] = z_tmp[i] % self.m

      print("################# z (before doing mod m) ###################")
      print(z_tmp)

      return [z, zNoisy]


  def rl_keys(self, s):
      r = self.r
      N = self.N

      s2 = r.ringMul(s, s)

      tmp_a = r.ringRandClear()
      tmp_e = r.ringBinom(N)
      tmp_b = r.ringAdd(r.ringMul(tmp_a, s), tmp_e)
      tmp_b = [self.get_mod(-i) for i in tmp_b]

      a = [tmp_a for i in range(self.lgP)]
      b = [tmp_b for i in range(self.lgP)]

      for i in range(self.lgP):
          s2_tmp = [self.get_mod((2**i) * j) for j in s2]
          b[i] = r.ringAdd(b[i], s2_tmp)

      return [b, a]

  def rl_keys_alt(self, s):
      r = self.r
      N = self.N

      s2 = r.ringMul(s, s)

      for i in range(self.n):
          s2[i] = self.get_mod_pq(s2[i])
          if (s2[i] >= (self.p*self.p1)/2):
               s2[i] -= self.p*self.p1
      # print(s)
      # print(s2)

      a = r.ringRandClear(pq=True)
      for i in range(self.n):
          if (a[i] > (self.p*self.p1)/2):
                a[i] -= self.p*self.p1
      e = r.ringBinom(N, take_mod=False)
      b = r.ringAdd(r.ringMul(a, s, take_mod=False), e, take_mod=False)
      b = [-i for i in b]

      s2_tmp = [j*self.p1 for j in s2]
      b = r.ringAdd(b, s2_tmp, pq=True)

      for i in range(self.n):
          if (b[i] > (self.p*self.p1)/2):
                b[i] -= self.p*self.p1

      return [b, a]

  def relinearization(self, b, a, c0, c1, c2):
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

        c0_new = r.ringAdd(r.ringMul(ct, b[i]), c0_new)
        c1_new = r.ringAdd(r.ringMul(ct, a[i]), c1_new)

      c0_new = r.ringAdd(c0_new, c0)
      c1_new = r.ringAdd(c1_new, c1)

      return [c0_new, c1_new]

  def relinearization_alt(self, b, a, c0, c1, c2):
      r = self.r
      c0_new = r.ringMul(c2, b, take_mod=False)
      c1_new = r.ringMul(c2, a, take_mod=False)

      for i in range(self.n):
           c0_new[i] = self.get_mod(int(round(float(c0_new[i])/ self.p1)))
           c1_new[i] = self.get_mod(int(round(float(c1_new[i])/ self.p1)))

      for i in range(self.n):
          if (c0_new[i] > self.p/2):
                c0_new[i] -= self.p
          if (c1_new[i] > self.p/2):
                c1_new[i] -= self.p

      c0_new = r.ringAdd(c0_new, c0)
      c1_new = r.ringAdd(c1_new, c1)

      for i in range(self.n):
           if (c0_new[i] > self.p/2):
                 c0_new[i] -= self.p
           if (c1_new[i] > self.p/2):
                 c1_new[i] -= self.p

      return [c0_new, c1_new]


  def add(self, u1, u2, take_mod=True):
    r = self.r
    res = r.ringAdd(u1, u2, take_mod=take_mod)
    return res

  def mul(self, u1, u2, take_mod=True):
      r = self.r
      res = r.ringMul(u1, u2, take_mod=take_mod)
      return res

  def ciphertext_mult(self, v, u, v1, u1):
      c0 = self.mul(v, v1, take_mod=False)
      c1 = self.add(self.mul(u,v1,take_mod=False), self.mul(v,u1,take_mod=False), take_mod=False)
      c2 = self.mul(u, u1, take_mod=False)

      for i in range(self.n):
          c0[i] = int(round(c0[i]*self.m / float(self.p)))
          c1[i] = int(round(c1[i]*self.m / float(self.p)))
          c2[i] = int(round(c2[i]*self.m / float(self.p)))
          c0[i] = self.get_mod(c0[i])
          c1[i] = self.get_mod(c1[i])
          c2[i] = self.get_mod(c2[i])

      for i in range(self.n):
           if (c0[i] > self.p/2):
                c0[i] -= self.p
           if (c1[i] > self.p/2):
               c1[i] -= self.p
           if (c2[i] > self.p/2):
               c2[i] -= self.p

      # print("################# c0 after round ###################")
      # print(c0)
      # print("################# c1 after round  ###################")
      # print(c1)
      # print("################# c2 after round ###################")
      # print(c2)

      return [c0, c1, c2]


  def custom_round(self, x, base):
      return int(base * round(x/base))

  def modulus_switching(self, q0, q1, c0, c1):
      q1q0 = q1/float(q0)
      c0_new = [self.get_mod(self.custom_round(i, q1q0)) for i in c0]
      c1_new = [self.get_mod(self.custom_round(i, q1q0)) for i in c1]
      # c0_new = [self.get_mod(int(round(i*q1q0))) for i in c0]
      # c1_new = [self.get_mod(int(round(i*q1q0))) for i in c1]
      return [c0_new, c1_new]


  # def shift(self, c, k):
  #     cn = [x for x in c]
  #     res = [0 for i in range(self.n)]
  #     res[0] = cn[0]
  #     xn_1 = [0 for _ in range(self.n + 1)]
  #     xn_1[0] = 1
  #     xn_1[-1] = 1
  #     for i in range(1, self.n):
  #         pow_0 = i*k
  #         pow = pow_0 % (self.n)
  #         num = [0 for _ in range(pow_0 + 1)]
  #         num[-1] = cn[i]
  #         ans = self.poly_mod(num, xn_1)
  #         res[pow] = self.get_mod(res[pow] + self.get_mod(ans))
  #     return res


  # def switch_key(self, s, s0, v , u):
  #     g = self.decompose_gadget()
  #     [s1, v1, u1] = self.key_switching(g, s, s0)
  #     [v2, u2] = self.new_ciphertext(v, u, v1, u1)
  #     return [v2, u2, s1]

  # def normalize(self, poly):
  #     while poly and poly[-1] == 0:
  #         poly.pop()
  #     if poly == []:
  #         poly.append(0)

  # def poly_divmod_helper(self, num, den):
  #     #Create normalized copies of the args
  #     num = num[:]
  #     self.normalize(num)
  #     den = den[:]
  #     self.normalize(den)
  #
  #     if len(num) >= len(den):
  #         #Shift den towards right so it's the same degree as num
  #         shiftlen = len(num) - len(den)
  #         den = [0] * shiftlen + den
  #     else:
  #         return [0], num
  #
  #     quot = []
  #     divisor = float(den[-1])
  #     for i in xrange(shiftlen + 1):
  #         #Get the next coefficient of the quotient.
  #         mult = num[-1] / divisor
  #         quot = [mult] + quot
  #
  #         #Subtract mult * den from num, but don't bother if mult == 0
  #         #Note that when i==0, mult!=0; so quot is automatically normalized.
  #         if mult != 0:
  #             d = [mult * u for u in den]
  #             num = [u - v for u, v in zip(num, d)]
  #
  #         num.pop()
  #         den.pop(0)
  #
  #     self.normalize(num)
  #     return quot, num
  #
  # def poly_mod(self, num, den):
  #     q, r = self.poly_divmod_helper(num, den)
  #     for i in range(len(r)):
  #         if (r[i] != 0):
  #             return int(r[i])
  #     return 0

  # def expand(self, l, s, ciphertexts):
  #     r = self.r
  #     for j in range(l):
  #         for k in range(2**j):
  #             c0_0, c0_1 = ciphertexts[0][k], ciphertexts[1][k]
  #             x2j = [0 for _ in range(self.n)]
  #             x2j[(-2**j) % self.n] = self.get_mod(-1)
  #             s_new = self.shift(s, 1+(self.n/(2**j)))
  #             ck_0, ck_1 = self.shift(c0_0, 1+(self.n/(2**j))), self.shift(c0_1, 1+(self.n/(2**j)))
  #             [ck_1, ck_0, _] = self.switch_key(s_new, s, ck_1, ck_0)
  #             ck_0, ck_1 = r.ringAdd(c0_0, ck_0), r.ringAdd(c0_1, ck_1)
  #             c1_0, c1_1 = self.mul(c0_0, x2j), self.mul(c0_1, x2j)
  #             ck2j_0, ck2j_1 = self.shift(c1_0, 1+(self.n/(2**j))), self.shift(c1_1, 1+(self.n/(2**j)))
  #             [ck2j_1, ck2j_0, _] = self.switch_key(s_new, s, ck2j_1, ck2j_0)
  #             ck2j_0, ck2j_1 = r.ringAdd(c1_0, ck2j_0), r.ringAdd(c1_1, ck2j_1)
  #             ciphertexts[0][k], ciphertexts[1][k] = ck_0, ck_1
  #             ciphertexts[0][k + 2**j], ciphertexts[1][k + 2**j] = ck2j_0, ck2j_1
  #     return ciphertexts
