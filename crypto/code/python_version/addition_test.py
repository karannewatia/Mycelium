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
[v, u] = lwe.enc(b, a, x)
[v1, u1] = lwe.enc(b, a, x)

add_start = time.time()
v2, u2 = v1, u1
for _ in range(100): #take the average over 100 additions
    v2 = lwe.add(v, v2)
    u2 = lwe.add(u, u2)
add_end = time.time()
print("ciphertext addition time (averaged over 100 additions) : ", (add_end - add_start)/100)

x2 = lwe.dec(v2, u2, s)
print("decrypted text (after 100 additions): ", x2[0])
