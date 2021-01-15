#execfile('/root/SCALE-MAMBA/Programs/lwe/lwe.mpc')
from ring import Ring
from lwe import LWE

# For use with n=8192, p=300424569129657234489620267994584186881
p=97525013755403038226265609232667509664153716430387711847621888326758687571969
w = 52222849419468845600166076218972653758125222847995807384575638827312162815078

n=8192/8
lgN = 13-3
r = Ring(lgN, w)

N = 1
lgM = 64
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
