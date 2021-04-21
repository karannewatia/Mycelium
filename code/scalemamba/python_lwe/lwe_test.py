from ring import Ring
from lwe import LWE
import random
import numpy as np
import time
import sympy
import gmpy2
from gmpy2 import mpz

lgP = 550
lgM = 30
lgN = 12
n = 1 << lgN

p = 3608870760655701536654448303084521404059979435669688520664454167677047564331360806878098945169255539464747077653151390316596266506041127794233364507011499768902844417

# ########### generate p ###############
# p = 4
# while (not sympy.isprime(p)):
#   p = random.randrange(2**(lgP-lgM-2), 2**(lgP-lgM-1)-1) * 2**(lgM+1) +1
#
########### generate w ###############
# y = (p-1)/(2*n)
# z = 1
# w = p-1
# while z!= (p-1):
#   a = random.randrange(0, p)
#   w = pow(a, y, p)
#   z = pow(w, n, p)
# ######################
# print(w)

w = 2358725313548793953437394003655954801060216040272190506880021058157597902378675657944961344275684323693688877632238499135305262010092352809615726751416655380200150292
#w = 1032221733394210440441659515349146050267235537140279868931207933950081697226615027346242970871325134062515859878795671410046065213016222308552291565188475284037534470

# print("############ q ###############")
# print(p)
# print("############ w ###############")
# print(w)

start = time.time()

r = Ring(lgN, w, p)
N = 1 #used in binomial distribution
l = 15
lwe = LWE(r, N, lgM, l, n, lgP, p)

x = [0 for i in range(l)]
for i in range(l):
  x[i] = 0 # random.randrange(0, 100)
x[1] = 1
print("################# plaintext ###################")
print(x)

# y = lwe.mul(x,x)
# print(y)

[b, a, s] = lwe.key_gen()
[v0, u0] = lwe.enc(b, a, x)

# x2 = lwe.dec(v0, u0, s)

###### check addition on ciphertext #######
# [v, u] = lwe.enc(b, a, x)
# [v1, u1] = lwe.enc(b, a, x)
# u2 = lwe.add(u, u1)
# v2 = lwe.add(v, v1)
# x2 = lwe.dec(v2, u2, s)

###### check multiplication on ciphertext #######
v1, u1 = v0, u0
v, u = v0, u0
c0 = lwe.mul(v, v1)
c1 = lwe.add(lwe.mul(u,v1), lwe.mul(v,u1))
c2 = lwe.mul(u, u1)

########### check mult without relin #############
#x2 = lwe.dec_mul(c0, c1, c2, s)
# c = lwe.ciphertext_mult_more([c0,c1,c2], [v, u])
# c = lwe.ciphertext_mult_more(c, [v, u])
# c = lwe.ciphertext_mult_more(c, [v, u])
# c = lwe.ciphertext_mult_more(c, [v, u])
# c = lwe.ciphertext_mult_more(c, [v, u])
# c = lwe.ciphertext_mult_more(c, [v, u])
# c = lwe.ciphertext_mult_more(c, [v, u])
# c = lwe.ciphertext_mult_more(c, [v, u])
# c = lwe.ciphertext_mult_more(c, [v, u])
# x2 = lwe.dec_mul_more(c, s)

# ############## check mult with relin ###############
s2 = lwe.mul(s,s)
[rlk_b, rlk_a] = lwe.rl_keys(s, s2)

# relin_start = time.time()
[c0_mul, c1_mul] = lwe.relinearization(rlk_b, rlk_a, c0, c1, c2, s)
# relin_end = time.time()
#
# x2 = lwe.dec(c0_mul, c1_mul, s)

mult_count = 0
for k in range(12):
    tmp = lwe.dec(c0_mul, c1_mul, s)
    if (tmp[0] == False):
        break
    else:
        x2 = tmp
        print(x2[0])
    v,u = c0_mul, c1_mul
    c0 = lwe.mul(v, v1)
    c1 = lwe.add(lwe.mul(u,v1), lwe.mul(v,u1))
    c2 = lwe.mul(u, u1)
    [c0_mul, c1_mul] = lwe.relinearization(rlk_b, rlk_a, c0, c1, c2, s)
    mult_count += 1
    print(mult_count)

print(mult_count)

##################  check multiplicative depth ##############
# plaintexts = []
# for i in range(32):
#     x = [0 for _ in range(l)]
#     x[1] = 1
#     plaintexts.append(x)

# mult_lvl_1 = []
# for i in range(0, 16, 2):
#     [v, u] = [v0, u0] #lwe.enc(b, a, plaintexts[i])
#     [v1, u1] = [v0, u0] #lwe.enc(b, a, plaintexts[i+1])
#     c0 = lwe.mul(v, v1)
#     c1 = lwe.add(lwe.mul(u,v1), lwe.mul(v,u1))
#     c2 = lwe.mul(u, u1)
#     [c0_mul, c1_mul] = lwe.relinearization(rlk_b, rlk_a, c0, c1, c2, s)
#     mult_lvl_1.append([c0_mul, c1_mul])
#
# mult_lvl_2 = []
# for i in range(0, 8, 2):
#     [v, u] = mult_lvl_1[i]
#     [v1, u1] = mult_lvl_1[i+1]
#     c0 = lwe.mul(v, v1)
#     c1 = lwe.add(lwe.mul(u,v1), lwe.mul(v,u1))
#     c2 = lwe.mul(u, u1)
#     [c0_mul, c1_mul] = lwe.relinearization(rlk_b, rlk_a, c0, c1, c2, s)
#     mult_lvl_2.append([c0_mul, c1_mul])
#
# mult_lvl_3 = []
# for i in range(0, 4, 2):
#     [v, u] = mult_lvl_2[i]
#     [v1, u1] = mult_lvl_2[i+1]
#     c0 = lwe.mul(v, v1)
#     c1 = lwe.add(lwe.mul(u,v1), lwe.mul(v,u1))
#     c2 = lwe.mul(u, u1)
#     [c0_mul, c1_mul] = lwe.relinearization(rlk_b, rlk_a, c0, c1, c2, s)
#     mult_lvl_3.append([c0_mul, c1_mul])
#
# [v, u] = mult_lvl_3[0]
# [v1, u1] = mult_lvl_3[1]
# c0 = lwe.mul(v, v1)
# c1 = lwe.add(lwe.mul(u,v1), lwe.mul(v,u1))
# c2 = lwe.mul(u, u1)
# [c0_mul, c1_mul] = lwe.relinearization(rlk_b, rlk_a, c0, c1, c2, s)
#
# x2 = lwe.dec(c0_mul, c1_mul, s)
# print(x2[0])

######################################

print("################# decrypted text ###################")
print(x2[0])

end = time.time()
# print(relin_end - relin_start)
print("total time taken", end-start)
