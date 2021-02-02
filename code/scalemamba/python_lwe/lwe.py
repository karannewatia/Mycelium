#execfile('/root/SCALE-MAMBA/Programs/ring/ring.mpc')
from ring import Ring
p=3843321857

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
    self.m = (2 ** lgM)   # Plaintext modulus (size per element)
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

  def key_switching(self, g, s):
      r = self.r
      N = self.N

      #v = -u*s1 + g*s + e

      s1 = r.ringBinom(N)

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

      uvs = [[0 for i in range(self.n)] for j in range(self.lgP)]
      for i in range(self.lgP):
        uvs[i] = r.ringAdd(r.ringMul(u[i], s1), v[i])

      # #k = (u|v)
      res = [s1, v, u, e, uvs, gs]
      return res

  def new_ciphertext(self, c0, c1, u, v, g, e, uvs, gs, s1, s):
      #(c0', c1') = (c0, 0) + g^-1 * K, where K = (u|v)
      r = self.r

      g_inverse = [[0 for i in range(self.lgP)] for j in range(self.n)]
      c0_new = [0 for i in range(self.n)]
      c1_new = [0 for i in range(self.n)]
      g_inv_g_tmp = [[0 for i in range(self.lgP)] for j in range(self.n)]
      g_inv_g = [0 for i in range(self.n)]
      g_inv_e = [0 for i in range(self.n)]
      g_inv_uvs = [0 for i in range(self.n)]
      g_inv_uvs_c0 = [0 for i in range(self.n)]
      g_inv_gs = [0 for i in range(self.n)]

      for i in range(self.n):
        tmp_binary = self.to_binary(c1[i])
        for j in range(self.lgP):
          if (c1[i] < 0):
              tmp_binary[j] = -tmp_binary[j]
          g_inverse[i][j] = tmp_binary[j]
          g_inv_g_tmp[i][j] = self.get_mod(g_inverse[i][j] * g[j])
        g_inv_g[i] = self.get_mod(sum(g_inv_g_tmp[i]))

      for i in range(self.lgP):
        gt = [0 for i in range(self.n)]
        for j in range(self.n):
          gt[j] = g_inverse[j][i]

        c0_new = r.ringAdd(r.ringMul(gt, u[i]), c0_new)
        c1_new = r.ringAdd(r.ringMul(gt, v[i]), c1_new)
        g_inv_e = r.ringAdd(r.ringMul(gt, e[i]), g_inv_e)
        g_inv_uvs = r.ringAdd(r.ringMul(gt, uvs[i]), g_inv_uvs)
        g_inv_gs = r.ringAdd(r.ringMul(gt, gs[i]), g_inv_gs)

      c0_tmpa_tmpb_s1 = [0 for i in range(self.n)]
      c0_tmpa_tmpb_s1 = r.ringAdd(r.ringAdd(r.ringMul(c1_new, s1), c0_new), c0)

      c0_new = r.ringAdd(c0_new, c0)
      g_inv_uvs_c0 = r.ringAdd(g_inv_uvs, c0)
      g_inv_gs_e = r.ringAdd(g_inv_gs, g_inv_e)
      g_inv_gs_e_c0 = r.ringAdd(g_inv_gs_e, c0)
      zNoisy = r.ringAdd(r.ringAdd(c0, r.ringMul(c1, s)), g_inv_e)
      c1s = r.ringMul(c1, s)
      g_inv_g_s = r.ringMul(g_inv_g, s)

      return [c0_new, c1_new, g_inverse, g_inv_g, g_inv_e, g_inv_uvs, g_inv_uvs_c0, gs, g_inv_gs, g_inv_gs_e, c0_tmpa_tmpb_s1, zNoisy, g_inv_gs_e_c0, c1s, g_inv_g_s]


  # Returns [a, b, s]
  # (a, b) is the public key, s is the secret key
  def key_gen(self):
    r = self.r
    N = self.N
    a = r.ringRandClear()
    s = r.ringBinom(N)
    e = r.ringBinom(N)
    a_neg = [self.get_mod(-i) for i in a]
    e = [self.get_mod(2*i) for i in e]
    b = r.reveal(r.ringAdd(r.ringMul(a_neg, s), e)) #2*e

    res = [b,a,s] #[a, b, s]
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

    e1 = [self.get_mod(2*i)for i in e1]
    e2 = [self.get_mod(2*i) for i in e2]


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

    res = [r.reveal(v), r.reveal(u)]
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
      zRangeI = self.get_mod(zNoisy[i] + halfMthP)
      zNotchesI = self.get_mod(zRangeI * clearM)
      z[i] = m - 1 - ((zNotchesI - 1) % m)
      z[i] = self.get_mod(z[i])
      # d = p/m
      # z[i] = round(zNoisy[i]/d)

    return [z, zNoisy]

  def dec_new(self, c0, c1, c2, s):
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

  def add(self, u1, u2):
    r = self.r
    res = r.ringAdd(u1, u2)
    return res

  def mul(self, u1, u2):
      r = self.r
      res = r.ringMul(u1, u2)
      return res
