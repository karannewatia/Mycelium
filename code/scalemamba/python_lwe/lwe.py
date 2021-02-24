from ring import Ring
import numpy as np

p=17 #3843321857

class LWE(object):

  # In order for decryption to work,
  #   N and m=2^lgM must be chosen appropriately.
  # Namely, if you wish to do t ciphertext additions
  #   and p is the size of the SCALE-MAMBA field, then need:
  #   t*2*N^2 < p / (2*m)
  def __init__(self, r, N, lgM, l, n, lgP):
    self.r = r  # Ring used
    self.N = N  # Half-width of binomial distributions
    # m = Modulus of ciphertext additions
    # Require p = 1 (mod 2m), and m to be a power of 2
    self.lgM = lgM
    self.m = (2 ** lgM)  # Plaintext modulus (size per element)
    self.l = l           # Plaintext length (number of elements)
    self.n = n
    self.lgP = lgP
    return

  def get_mod(self, a):
    if a >= 0:
        return a % p
    else:
        return a % p

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
    s = r.ringBinom_new(N)
    e = r.ringBinom_new(N)
    a_neg = [self.get_mod(-i) for i in a]
    e = [self.get_mod(2*i) for i in e]
    print("######## e #######")
    print(e)

    b = r.ringAdd(r.ringMul(a_neg, s), e)

    res = [b,a,s]
    return res

  # z is plaintext (array) of l elems each modulo m
  # returns ciphertext [u, v]
  def enc(self, b, a, z):
    r = self.r
    N = self.N
    m = self.m
    e0 = r.ringBinom_new(N)
    e1 = r.ringBinom_new(N)
    e2 = r.ringBinom_new(N)

    # e1 = [self.get_mod(2*i)for i in e1]
    # e2 = [self.get_mod(2*i) for i in e2]
    e1 = [(2*i)for i in e1]
    e2 = [(2*i) for i in e2]

    # u = a*e0 + 2*e1 (mod q)
    u = r.ringMul(a, e0)
    u = r.ringAdd(u, e1)

    print("######## e0 #######")
    print(e0)
    print("######## e1 #######")
    print(e1)
    print("######## e2 #######")
    print(e2)

    # v = b*e0 + 2*e2 + round(p/m)z (mod p)

    #mthP = cint(-1)/cint(m)
    mthP = p/m

    zMthP = r.zero()

    for i in range(0, len(z)):
      zMthP[i] = self.get_mod(z[i]) #self.get_mod(z[i] * mthP)

    v = r.ringMul(b, e0)
    v = r.ringAdd(v, e2)
    v = r.ringAdd(v, zMthP)

    res = [v, u]
    return res


  def dec(self, v, u, s):
    r = self.r
    lgM = self.lgM
    m = 1 << lgM
    clearM = m
    #zNoisy = r.ringSub(v, r.ringMul(u, s))
    zNoisy = r.ringAdd(v, r.ringMul(u, s))

    halfMthP = p/(2*m)

    z = [0 for i in range(self.l)]
    for i in range(self.l):
      # zRangeI = self.get_mod(zNoisy[i] + halfMthP)
      # zNotchesI = self.get_mod(zRangeI * clearM)
      # z[i] = m - 1 - ((zNotchesI - 1) % m)
      z[i] = zNoisy[i] % 2
      # d = p/m
      # z[i] = round(zNoisy[i]/d)

    return [z, zNoisy]

  def dec_mul(self, c0, c1, c2, s):
    r = self.r
    lgM = self.lgM
    m = 1 << lgM
    clearM = m
    #zNoisy = r.ringSub(v, r.ringMul(u, s))
    s1 = r.ringMul(s,s)
    zNoisy = r.ringAdd(r.ringAdd(c0, r.ringMul(c1, s)), r.ringMul(c2, s1))

    halfMthP = p/(2*m)

    z = [0 for i in range(self.l)]
    for i in range(self.l):
      zRangeI = self.get_mod(zNoisy[i] + halfMthP)
      zNotchesI = self.get_mod(zRangeI * clearM)
      z[i] = m - 1 - ((zNotchesI - 1) % m)
      z[i] = self.get_mod(z[i])
      # d = p/m
      # z[i] = round(zNoisy[i]/d)

    return [z, zNoisy]

  def rl_keys(self, s):
      r = self.r
      N = self.N
      tmp_a = r.ringRandClear()
      a = [tmp_a for i in range(self.lgP)]
      # e = r.ringBinom(N)
      # a_neg = [self.get_mod(-i) for i in tmp_a]
      # e = [self.get_mod(2*i) for i in e]
      # tmp_b = r.reveal(r.ringAdd(r.ringMul(a_neg, s), e))
      # b = [tmp_b for i in range(self.lgP)]
      tmp_b = r.ringRandClear()
      b = [tmp_b for i in range(self.lgP)]
      s2 = r.ringMul(s,s)

      for i in range(self.lgP - 1, -1, -1):
          s2_tmp = [self.get_mod((2**i) * j) for j in s2]
          b[i] = r.ringAdd(b[i], s2_tmp)

      return [b, a]

  def relinearization(self, b, a, c0, c1, c2):
      r = self.r
      c2_inverse = [[0 for i in range(self.lgP)] for j in range(self.n)]
      c0_new = [0 for i in range(self.n)]
      c1_new = [0 for i in range(self.n)]

      for i in range(self.n):
        tmp_binary = self.to_binary(c2[i])
        for j in range(self.lgP):
          if (c2[i] < 0):
              tmp_binary[j] = -tmp_binary[j]
          c2_inverse[i][j] = tmp_binary[j]

      for i in range(self.lgP):
        ct = [0 for k in range(self.n)]
        for j in range(self.n):
          ct[j] = c2_inverse[j][i]

        c0_new = r.ringAdd(r.ringMul(ct, b[i]), c0_new)
        c1_new = r.ringAdd(r.ringMul(ct, a[i]), c1_new)

      c0_new = r.ringAdd(c0_new, c0)
      c1_new = r.ringAdd(c1_new, c1)

      return [c0_new, c1_new]

  def add(self, u1, u2):
    r = self.r
    res = r.ringAdd(u1, u2)
    return res

  def mul(self, u1, u2):
      r = self.r
      res = r.ringMul(u1, u2)
      return res

  def switch_key(self, s, s0, v , u):
      g = self.decompose_gadget()
      [s1, v1, u1] = self.key_switching(g, s, s0)
      [v2, u2] = self.new_ciphertext(v, u, v1, u1)
      return [v2, u2, s1]

  def normalize(self, poly):
      while poly and poly[-1] == 0:
          poly.pop()
      if poly == []:
          poly.append(0)

  def poly_divmod_helper(self, num, den):
      #Create normalized copies of the args
      num = num[:]
      self.normalize(num)
      den = den[:]
      self.normalize(den)

      if len(num) >= len(den):
          #Shift den towards right so it's the same degree as num
          shiftlen = len(num) - len(den)
          den = [0] * shiftlen + den
      else:
          return [0], num

      quot = []
      divisor = float(den[-1])
      for i in xrange(shiftlen + 1):
          #Get the next coefficient of the quotient.
          mult = num[-1] / divisor
          quot = [mult] + quot

          #Subtract mult * den from num, but don't bother if mult == 0
          #Note that when i==0, mult!=0; so quot is automatically normalized.
          if mult != 0:
              d = [mult * u for u in den]
              num = [u - v for u, v in zip(num, d)]

          num.pop()
          den.pop(0)

      self.normalize(num)
      return quot, num

  def poly_mod(self, num, den):
      q, r = self.poly_divmod_helper(num, den)
      for i in range(len(r)):
          if (r[i] != 0):
              return int(r[i])
      return 0

  def shift(self, c, k):
      cn = [x for x in c]
      res = [0 for i in range(self.n)]
      res[0] = cn[0]
      xn_1 = [0 for _ in range(self.n + 1)]
      xn_1[0] = 1
      xn_1[-1] = 1
      for i in range(1, self.n):
          pow_0 = i*k
          pow = pow_0 % (self.n)
          num = [0 for _ in range(pow_0 + 1)]
          num[-1] = cn[i]
          ans = self.poly_mod(num, xn_1)
          res[pow] = self.get_mod(res[pow] + self.get_mod(ans))
      return res

  def expand(self, l, s, ciphertexts):
      r = self.r
      for j in range(l):
          for k in range(2**j):
              c0_0, c0_1 = ciphertexts[0][k], ciphertexts[1][k]
              x2j = [0 for _ in range(self.n)]
              x2j[(-2**j) % self.n] = self.get_mod(-1)
              s_new = self.shift(s, 1+(self.n/(2**j)))
              ck_0, ck_1 = self.shift(c0_0, 1+(self.n/(2**j))), self.shift(c0_1, 1+(self.n/(2**j)))
              [ck_1, ck_0, _] = self.switch_key(s_new, s, ck_1, ck_0)
              ck_0, ck_1 = r.ringAdd(c0_0, ck_0), r.ringAdd(c0_1, ck_1)
              c1_0, c1_1 = self.mul(c0_0, x2j), self.mul(c0_1, x2j)
              ck2j_0, ck2j_1 = self.shift(c1_0, 1+(self.n/(2**j))), self.shift(c1_1, 1+(self.n/(2**j)))
              [ck2j_1, ck2j_0, _] = self.switch_key(s_new, s, ck2j_1, ck2j_0)
              ck2j_0, ck2j_1 = r.ringAdd(c1_0, ck2j_0), r.ringAdd(c1_1, ck2j_1)
              ciphertexts[0][k], ciphertexts[1][k] = ck_0, ck_1
              ciphertexts[0][k + 2**j], ciphertexts[1][k + 2**j] = ck2j_0, ck2j_1
      return ciphertexts
