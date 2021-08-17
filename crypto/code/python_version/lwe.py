from ring import Ring
import random
import math

class LWE(object):

  def __init__(self, r, N, lgM, l, n, lgP, p):
    self.r = r  # Ring used
    self.N = N  # Half-width of binomial distributions
    # Require p = 1 (mod 2m), and m to be a power of 2
    self.lgM = lgM #plaintext modulus bitsize
    self.m = (2 ** lgM) #plaintext modulus (size per element)
    self.l = l #plaintext length (number of elements)
    self.n = n #polynomial degree
    self.lgP = lgP #ciphertext modulus bitsize
    self.p = p #ciphertext modulus
    self.lgP_base_m = math.ceil(math.log(self.p, self.m))
    self.mult = self.r.ringMul

  def get_mod(self, a):
       return a % self.p

  # Returns [b, a, s]
  # (b, a) is the public key, s is the secret key
  def key_gen(self):
    r = self.r
    N = self.N
    a = r.ringRand()
    s = [random.randint(-1,1) for _ in range(self.n)] #coeffients of s = -1,0, or 1
    e = r.ringBinom(N)
    a_neg = [self.get_mod(-i) for i in a]
    e = [self.get_mod(self.m*i) for i in e]
    b = r.ringAdd(self.mult(a_neg, s), e)

    res = [b,a,s]
    return res

  #Encryption
  # z is plaintext (array) of l elems each modulo m
  # returns ciphertext [v, u]
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
    mthP = self.p//m
    zMthP = r.zero()

    for i in range(0, len(z)):
      zMthP[i] = self.get_mod(z[i])

    v = self.mult(b, e0)
    v = r.ringAdd(v, e2)
    v = r.ringAdd(v, zMthP)

    res = [v, u]
    return res

  # decrypt the ciphertext [v,u] using the secret key s
  # returns [z,zNoisy] where z is the decrypted ciphertext,
  # and zNoisy is useful for debugging
  def dec(self, v, u, s):
    r = self.r
    lgM = self.lgM
    m = 1 << lgM
    clearM = m
    zNoisy = r.ringAdd(v, self.mult(u, s))
    halfMthP = self.p//(2*m)

    z = [0 for i in range(self.l)]
    for i in range(self.l):
      zNoisy[i] = self.get_mod(zNoisy[i] + halfMthP)
      zNoisy[i] = zNoisy[i] - halfMthP
      if abs(zNoisy[i]) >= halfMthP:
        print(" !!! dec failed !!! ")
        return [False, False]
      z[i] = zNoisy[i] % self.m

    return [z, zNoisy]

  #Same as dec except that the ciphertext is [c0,c1,c2] (obtained after multiplying two size-2 ciphertexts)
  def dec_mul(self, c0, c1, c2, s):
    r = self.r
    lgM = self.lgM
    m = 1 << lgM
    clearM = m
    s1 = self.mult(s,s)
    zNoisy = r.ringAdd(r.ringAdd(c0, self.mult(c1, s)), self.mult(c2, s1))
    halfMthP = self.p//(2*m)

    z = [0 for i in range(self.l)]
    for i in range(self.l):
         zNoisy[i] = self.get_mod(zNoisy[i] + halfMthP)
         zNoisy[i] = zNoisy[i] - halfMthP
         if abs(zNoisy[i]) >= halfMthP:
           print(" !!! dec failed !!! ")
           return [False, False]
         z[i] = zNoisy[i] % self.m

    return [z, zNoisy]

  #Same as dec except that the ciphertext is [c0,...,c11] (obtained after multiplying ten ciphertexts)
  def dec_mul_more(self, c, s):
      r = self.r
      lgM = self.lgM
      m = 1 << lgM
      clearM = m
      s2 = self.mult(s,s)
      s3 = self.mult(s,s2)
      s4 = self.mult(s,s3)
      s5 = self.mult(s,s4)
      s6 = self.mult(s,s5)
      s7 = self.mult(s,s6)
      s8 = self.mult(s,s7)
      s9 = self.mult(s,s8)
      s10 = self.mult(s,s9)
      s11 = self.mult(s,s10)

      zNoisy = r.ringAdd(c[0], self.mult(c[1], s))
      zNoisy = r.ringAdd(zNoisy, self.mult(c[2], s2))
      zNoisy = r.ringAdd(zNoisy, self.mult(c[3], s3))
      zNoisy = r.ringAdd(zNoisy, self.mult(c[4], s4))
      zNoisy = r.ringAdd(zNoisy, self.mult(c[5], s5))
      zNoisy = r.ringAdd(zNoisy, self.mult(c[6], s6))
      zNoisy = r.ringAdd(zNoisy, self.mult(c[7], s7))
      zNoisy = r.ringAdd(zNoisy, self.mult(c[8], s8))
      zNoisy = r.ringAdd(zNoisy, self.mult(c[9], s9))
      zNoisy = r.ringAdd(zNoisy, self.mult(c[10], s10))
      zNoisy = r.ringAdd(zNoisy, self.mult(c[11], s11))

      halfMthP = self.p//(2*m)

      z = [0 for i in range(self.l)]
      for i in range(self.l):
           zNoisy[i] = self.get_mod(zNoisy[i] + halfMthP)
           zNoisy[i] = zNoisy[i] - halfMthP
           if abs(zNoisy[i]) >= halfMthP:
             print(" !!! dec failed !!! ")
             return [False, False]
           z[i] = zNoisy[i] % self.m

      return [z, zNoisy]

  #generate the relinearization key [b,a] using the secret key s
  #si is s multiplied by itself i-1 times
  def rl_keys(self, s, si):
      r = self.r
      N = self.N
      a = []
      b = []

      for _ in range(self.lgP_base_m):
          tmp_a = r.ringRand()
          a.append(tmp_a)
          tmp_a_neg = [self.get_mod(-i) for i in tmp_a]
          tmp_e = r.ringBinom(N)
          tmp_e = [self.get_mod(self.m*i) for i in tmp_e]
          tmp_b = r.ringAdd(self.mult(tmp_a_neg, s), tmp_e)
          b.append(tmp_b)

      for i in range(self.lgP_base_m):
          si_tmp = [self.get_mod((self.m**i) * j) for j in si]
          b[i] = r.ringAdd(b[i], si_tmp)

      return [b, a]

  #helper function used in relinearization
  def number_to_base(self, number):
    if number == 0:
        return [0]
    digits = [0 for _ in range(self.lgP_base_m)]
    count = 0
    while number:
        digits[count] = int(number % self.m)
        count += 1
        number //= self.m
    return digits[::-1]

  # perform relinearization on the ciphertext [c0,c1,...,ck] (reduces the ciphertext size by 1)
  # using the secret key s and the relinearization key [b,a]
  # returns the values in the first two indices of the new ciphertext after relin: [c0_new, c1_new]
  def relinearization(self, b, a, c0, c1, ck, s):
      r = self.r
      ck_inverse = [[0 for i in range(self.lgP_base_m)] for j in range(self.n)]
      c0_new = [0 for i in range(self.n)]
      c1_new = [0 for i in range(self.n)]

      for i in range(self.n):
        tmp_binary = self.number_to_base(ck[i])[::-1]
        for j in range(self.lgP_base_m):
          ck_inverse[i][j] = tmp_binary[j]

      for i in range(self.lgP_base_m):
        ct = [0 for _ in range(self.n)]
        for j in range(self.n):
          ct[j] = ck_inverse[j][i]

        c0_new = r.ringAdd(self.mult(ct, b[i]), c0_new)
        c1_new = r.ringAdd(self.mult(ct, a[i]), c1_new)

      c0_new = r.ringAdd(c0_new, c0)
      c1_new = r.ringAdd(c1_new, c1)

      return [c0_new, c1_new]

  #ring addition on two polynomials
  def add(self, u1, u2):
    r = self.r
    res = r.ringAdd(u1, u2)
    return res

  #ring multiplication on polynomials
  def mul(self, u1, u2):
      r = self.r
      res = self.mult(u1, u2)
      return res

  #multiply two ciphertexts ca and cb such that
  #ca is size-n ciphertext and
  #cb is a size-2 ciphertext
  def ciphertext_mult_more(self, ca, cb):
      result = []
      c0y = self.mul(ca[0], cb[0])
      result.append(c0y)
      for i in range(len(ca) - 1):
          c1y = self.add(self.mul(ca[i], cb[1]), self.mul(ca[i+1], cb[0]))
          result.append(c1y)
      cy = self.mul(ca[len(ca)-1], cb[1])
      result.append(cy)
      return result
