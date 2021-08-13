from ring import Ring
from lwe import LWE
import time

lgP = 550 #ciphertext modulus bitsize
lgM = 30 #plaintext modulus bitsize
lgN = 15
n = 1 << lgN #polynomial degree
N = 1 #used in binomial distribution
l = 12 #plaintext length (number of elements)

p = 3608870760655701536654448303084521404059979435669688520664454167677047564331360806878098945169255539464747077653151390316596266506041127794233364507011499768902844417
w = 1032221733394210440441659515349146050267235537140279868931207933950081697226615027346242970871325134062515859878795671410046065213016222308552291565188475284037534470

r = Ring(lgN, w, p)
lwe = LWE(r, N, lgM, l, n, lgP, p)

x = [0 for i in range(l)]
for i in range(l):
  x[i] = 0
x[1] = 1
print("plaintext: ", x)

[b, a, s] = lwe.key_gen()
[v0, u0] = lwe.enc(b, a, x)
s2 = lwe.mul(s,s)
[rlk_b, rlk_a] = lwe.rl_keys(s, s2)

mult_start = time.time()

v1, u1 = v0, u0
v, u = v0, u0

#first multiplication
c0 = lwe.mul(v, v1)
c1 = lwe.add(lwe.mul(u,v1), lwe.mul(v,u1))
c2 = lwe.mul(u, u1)

#remaining 9 multiplications
c = lwe.ciphertext_mult_more([c0,c1,c2], [v, u])
c = lwe.ciphertext_mult_more(c, [v, u])
c = lwe.ciphertext_mult_more(c, [v, u])
c = lwe.ciphertext_mult_more(c, [v, u])
c = lwe.ciphertext_mult_more(c, [v, u])
c = lwe.ciphertext_mult_more(c, [v, u])
c = lwe.ciphertext_mult_more(c, [v, u])
c = lwe.ciphertext_mult_more(c, [v, u])
c = lwe.ciphertext_mult_more(c, [v, u])

print("multiplication time (10 ciphertext-ciphertext multiplications): ", time.time() - mult_start)

x2 = lwe.dec_mul_more(c, s)
print("decrypted text (after 10 ciphertext-ciphertext multiplications): ", x2[0])
