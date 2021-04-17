from ring import Ring
from lwe import LWE
import random
import numpy as np
import time
import sympy

lgP = 109
lgM = 30
lgN = 2
n = 1 << lgN

########### generate p ###############
p = 4
while (not sympy.isprime(p)):
  p = random.randrange(2**(lgP-lgM-2), 2**(lgP-lgM-1)-1) * 2**(lgM+1) +1

########### generate w ###############
y = (p-1)/(2*n)
z = 1
w = p-1
while z!= (p-1):
  a = random.randrange(0, p)
  w = pow(a, y, p)
  z = pow(w, n, p)
#######################

print("############ q ###############")
print(p)
print("############ w ###############")
print(w)

start = time.time()

r = Ring(lgN, w, p)
N = 1
l = 4
lwe = LWE(r, N, lgM, l, n, lgP, p)

x = [0 for i in range(l)]
for i in range(l):
  x[i] = 0 # random.randrange(0, 100)
x[1] = 1
print("################# plaintext ###################")
print(x)

[b, a, s] = lwe.key_gen()
[v0, u0] = lwe.enc(b, a, x)

x2 = lwe.dec(v0, u0, s)

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
# x2 = lwe.dec_mul(c0, c1, c2, s)

############## check mult with relin ###############
# s2 = lwe.mul(s,s)
# [rlk_b, rlk_a] = lwe.rl_keys(s, s2)
# [c0_mul, c1_mul] = lwe.relinearization(rlk_b, rlk_a, c0, c1, c2, s)
# mult_count = 0
# for k in range(1):
#     tmp = lwe.dec(c0_mul, c1_mul, s)
#     if (tmp[0] == False):
#         break
#     else:
#         x2 = tmp
#     v,u = c0_mul, c1_mul
#     c0 = lwe.mul(v, v1)
#     c1 = lwe.add(lwe.mul(u,v1), lwe.mul(v,u1))
#     c2 = lwe.mul(u, u1)
#     [c0_mul, c1_mul] = lwe.relinearization(rlk_b, rlk_a, c0, c1, c2, s)
#     mult_count += 1
#
# print(mult_count)

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
print("time taken", end-start)
