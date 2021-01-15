#execfile('/root/SCALE-MAMBA/Programs/lwe/lwe.mpc')
from ring import Ring
from lwe import LWE

# For use with n=8192, p=300424569129657234489620267994584186881
#default p =340282366920938463463374607431768211507

p = 91373611627975532689656720489413429524532579978358356112637016726871503536129
w = 11200535685289185561926270644739074305482390736187634305477126859353441374665

n=8192/8
lgN = 13-3
r = Ring(lgN, w)

N = 1
lgM = 50
l = 4
lwe = LWE(r, N, lgM, l)

#x = sint.Array(l)
x = [0 for i in range(l)]
for i in range(l):
  #x[i] = sint(i)
  x[i] = i
  print(x[i])

[a, b, s] = lwe.key_gen()

[u, v] = lwe.enc(a, b, x)

x2 = lwe.dec(u, v, s)

for i in range(l):
  #x2[i].reveal_to(0)
  print(x2[i])
