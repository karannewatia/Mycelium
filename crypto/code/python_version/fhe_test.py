from ring import Ring
from lwe import LWE
import random

lgP = 550 #ciphertext modulus bitsize
lgM = 30 #plaintext modulus bitsize
lgN = 15
n = 1 << lgN #polynomial degree
N = 1 #used in binomial distribution
l = 12 #plaintext length (number of elements)

p = 3608870760655701536654448303084521404059979435669688520664454167677047564331360806878098945169255539464747077653151390316596266506041127794233364507011499768902844417
# ########### generate p ###############
# p = 4
# while (not sympy.isprime(p)):
#   p = random.randrange(2**(lgP-lgM-2), 2**(lgP-lgM-1)-1) * 2**(lgM+1) +1
#
# print("############ p ###############")
# print(p)

w = 1032221733394210440441659515349146050267235537140279868931207933950081697226615027346242970871325134062515859878795671410046065213016222308552291565188475284037534470
########### generate w ###############
# y = (p-1)/(2*n)
# z = 1
# w = p-1
# while z!= (p-1):
#   a = random.randrange(0, p)
#   w = pow(a, y, p)
#   z = pow(w, n, p)

# print("############ w ###############")
# print(w)


r = Ring(lgN, w, p)
lwe = LWE(r, N, lgM, l, n, lgP, p)

x = [0 for i in range(l)]
for i in range(l):
  x[i] = random.randrange(0, 100)
print("################# plaintext ###################")
print(x)

[b, a, s] = lwe.key_gen()
[v0, u0] = lwe.enc(b, a, x)
x2 = lwe.dec(v0, u0, s)

print("################# decrypted text ###################")
print(x2[0])
