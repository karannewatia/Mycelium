from ring import Ring
from lwe import LWE
import time

lgP = 550 #ciphertext modulus bitsize
lgM = 30 #plaintext modulus bitsize
lgN = 15
n = 1 << lgN #polynomial degree
N = 1 #used in binomial distribution
l = 12 #plaintext length (number of elements)

#ciphertext modulus
p = 3608870760655701536654448303084521404059979435669688520664454167677047564331360806878098945169255539464747077653151390316596266506041127794233364507011499768902844417
#used in polynomial multiplication
w = 1032221733394210440441659515349146050267235537140279868931207933950081697226615027346242970871325134062515859878795671410046065213016222308552291565188475284037534470

r = Ring(lgN, w, p)
lwe = LWE(r, N, lgM, l, n, lgP, p)

#create a plaintext x
x = [0 for i in range(l)]
x[1] = 1
print("plaintext: ", x)

#(b,a) is the public key and s is the secret key
[b, a, s] = lwe.key_gen()
enc_start = time.time()
#encrypt the plaintext using the public key to create a ciphertext (v0,u0)
[v0, u0] = lwe.enc(b, a, x)
enc_end = time.time()
print("encryption time: ", enc_end - enc_start)

x2 = lwe.dec(v0, u0, s) #decrypt the ciphertext using the secret key
print("decrypted text: ", x2[0])
