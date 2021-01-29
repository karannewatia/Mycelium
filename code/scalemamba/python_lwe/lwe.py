#execfile('/root/SCALE-MAMBA/Programs/ring/ring.mpc')
from ring import Ring
p=3843321857

class LWE(object):

  # In order for decryption to work,
  #   N and m=2^lgM must be chosen appropriately.
  # Namely, if you wish to do t ciphertext additions
  #   and p is the size of the SCALE-MAMBA field, then need:
  #   t*2*N^2 < p / (2*m)
  def __init__(self, r, N, lgM, l):
    self.r = r  # Ring used
    self.N = N  # Half-width of binomial distributions
    # m = Modulus of ciphertext additions
    # Require p = 1 (mod 2m), and m to be a power of 2
    self.lgM = lgM
    self.m = (2 ** lgM)   # Plaintext modulus (size per element)
    self.l = l           # Plaintext length (number of elements)
    return

  def get_mod(self, a):
    if a >= 0:
        return a % p
    else:
        return a % p

  # Returns [a, b, s]
  # (a, b) is the public key, s is the secret key
  def key_gen(self):
    r = self.r
    N = self.N
    a = r.ringRandClear()
    s = r.ringBinom(N)
    e = r.ringBinom(N)
    a_neg = [-i for i in a]
    b = r.reveal(r.ringAdd(r.ringMul(a, s), e)) #2*e

    res = [a,b,s] #[a, b, s]
    return res

  # z is plaintext (array) of l elems each modulo m
  # returns ciphertext [u, v]
  def enc(self, a, b, z):
    r = self.r
    N = self.N
    m = self.m
    e0 = r.ringBinom(N)
    e1 = r.ringBinom(N)
    e2 = r.ringBinom(N)

    # u = a*e0 + 2*e1 (mod q)
    u = r.ringMul(a, e0)
    u = r.ringAdd(u, e1)

    # v = b*e0 + 2*e2 + round(p/m)z (mod p)
    #mthP = cint(-1)/cint(m)
    mthP = p/m

    zMthP = r.zero()

    for i in range(0, len(z)):
      zMthP[i] = self.get_mod(z[i] * mthP)

    v = r.ringMul(b, e0)
    v = r.ringAdd(v, e2)
    v = r.ringAdd(v, zMthP)

    res = [r.reveal(u), r.reveal(v)]
    return res


  def dec(self, u, v, s):
    r = self.r
    lgM = self.lgM
    m = 1 << lgM
    clearM = m
    zNoisy = r.ringSub(v, r.ringMul(u, s))

    halfMthP = p/(2*m)

    z = [0 for i in range(self.l)]
    for i in range(self.l):
      zRangeI = self.get_mod(zNoisy[i] + halfMthP)
      zNotchesI = self.get_mod(zRangeI * clearM)
      z[i] = m - 1 - ((zNotchesI - 1) % m)
      z[i] = self.get_mod(z[i])

    return z
