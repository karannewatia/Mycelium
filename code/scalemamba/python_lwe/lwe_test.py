#execfile('/root/SCALE-MAMBA/Programs/lwe/lwe.mpc')
from ring import Ring
from lwe import LWE
import random

#p = 3843321857
w = 3457723958

lgN = 4
r = Ring(lgN, w)

N = 1
lgM = 10
l = 4
lwe = LWE(r, N, lgM, l)

x = [0 for i in range(l)]
for i in range(l):
  x[i] = i
  print(x[i])

[a, b, s] = lwe.key_gen()
[u, v] = lwe.enc(a, b, x)
#x2 = lwe.dec(u, v, s)

###### key switching #######
g = lwe.decompose_gadget()
[s1, u1, v1] = lwe.key_switching(g,s)
[v2, u2] = lwe.new_ciphertext(v, u, v1, u1)
x2 = lwe.dec(u2, v2, s1)

###### check addition on ciphertext #######
# [u1, v1] = lwe.enc(a, b, x)
# u2 = lwe.add(u, u1)
# v2 = lwe.add(v, v1)
# x2 = lwe.dec(u2, v2, s)

for i in range(l):
  print(x2[i])
