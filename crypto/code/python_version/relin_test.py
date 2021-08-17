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
for i in range(l):
  x[i] = 0
x[1] = 1
print("plaintext: ", x)

#(b,a) is the public key and s is the secret key
[b, a, s] = lwe.key_gen()
#encrypt the plaintext using the public key to create a ciphertext (v0,u0)
[v0, u0] = lwe.enc(b, a, x)

print("encryption done")

#generate the set of relin keys needed to perform 10 relins
s2 = lwe.mul(s,s)
[rlk_b1, rlk_a1] = lwe.rl_keys(s, s2)
s3 = lwe.mul(s2,s)
[rlk_b2, rlk_a2] = lwe.rl_keys(s, s3)
s4 = lwe.mul(s3,s)
[rlk_b3, rlk_a3] = lwe.rl_keys(s, s4)
s5 = lwe.mul(s4,s)
[rlk_b4, rlk_a4] = lwe.rl_keys(s, s5)
s6 = lwe.mul(s5,s)
[rlk_b5, rlk_a5] = lwe.rl_keys(s, s6)
s7 = lwe.mul(s6,s)
[rlk_b6, rlk_a6] = lwe.rl_keys(s, s7)
s8 = lwe.mul(s7,s)
[rlk_b7, rlk_a7] = lwe.rl_keys(s, s8)
s9 = lwe.mul(s8,s)
[rlk_b8, rlk_a8] = lwe.rl_keys(s, s9)
s10 = lwe.mul(s9,s)
[rlk_b9, rlk_a9] = lwe.rl_keys(s, s10)
s11 = lwe.mul(s10,s)
[rlk_b10, rlk_a10] = lwe.rl_keys(s, s11)

print("generated all relin keys")

#multiply the ciphertext with itself 10 times

#first multiplication
v1, u1 = v0, u0
v, u = v0, u0
c0 = lwe.mul(v, v1)
c1 = lwe.add(lwe.mul(u,v1), lwe.mul(v,u1))
c2 = lwe.mul(u, u1)

#the remaining 9 multiplications
c = lwe.ciphertext_mult_more([c0,c1,c2], [v, u])
c = lwe.ciphertext_mult_more(c, [v, u])
c = lwe.ciphertext_mult_more(c, [v, u])
c = lwe.ciphertext_mult_more(c, [v, u])
c = lwe.ciphertext_mult_more(c, [v, u])
c = lwe.ciphertext_mult_more(c, [v, u])
c = lwe.ciphertext_mult_more(c, [v, u])
c = lwe.ciphertext_mult_more(c, [v, u])
c = lwe.ciphertext_mult_more(c, [v, u])

print("all 10 multiplications done")

relin_start = time.time()
#perform 10 relins, each time reducing the size of the ciphertext by 1
[c0, c1] = lwe.relinearization(rlk_b10, rlk_a10, c[0], c[1], c[-1], s)
c = c[:-1]
c[0] = c0
c[1] = c1
[c0, c1] = lwe.relinearization(rlk_b9, rlk_a9, c[0], c[1], c[-1], s)
c = c[:-1]
c[0] = c0
c[1] = c1
[c0, c1] = lwe.relinearization(rlk_b8, rlk_a8, c[0], c[1], c[-1], s)
c = c[:-1]
c[0] = c0
c[1] = c1
[c0, c1] = lwe.relinearization(rlk_b7, rlk_a7, c[0], c[1], c[-1], s)
c = c[:-1]
c[0] = c0
c[1] = c1
[c0, c1] = lwe.relinearization(rlk_b6, rlk_a6, c[0], c[1], c[-1], s)
c = c[:-1]
c[0] = c0
c[1] = c1
[c0, c1] = lwe.relinearization(rlk_b5, rlk_a5, c[0], c[1], c[-1], s)
c = c[:-1]
c[0] = c0
c[1] = c1
[c0, c1] = lwe.relinearization(rlk_b4, rlk_a4, c[0], c[1], c[-1], s)
c = c[:-1]
c[0] = c0
c[1] = c1
[c0, c1] = lwe.relinearization(rlk_b3, rlk_a3, c[0], c[1], c[-1], s)
c = c[:-1]
c[0] = c0
c[1] = c1
[c0, c1] = lwe.relinearization(rlk_b2, rlk_a2, c[0], c[1], c[-1], s)
c = c[:-1]
c[0] = c0
c[1] = c1
[c0_mul, c1_mul] = lwe.relinearization(rlk_b1, rlk_a1, c[0], c[1], c[-1], s)

print("time taken for 10 relinearization operations (to convert a size-12 ciphertext to a size-2 ciphertext): ", time.time() - relin_start)

x2 = lwe.dec(c0_mul, c1_mul, s) #decrypt the ciphertext using the secret key

print("decrypted text: ", x2[0])
