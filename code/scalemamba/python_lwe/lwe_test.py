from ring import Ring
from lwe import LWE
import random
import numpy as np

p = 285896339783634948757783167889218300929
w = 1

lgN = 1
r = Ring(lgN, w, p)

N = 1
lgM = 7
l = 2
n = 2
lgP = 128
lwe = LWE(r, N, lgM, l, n, lgP, p)

x = [0 for i in range(l)]
# for i in range(l):
#   x[i] = random.randrange(0, 100)
x[1] = 1
print(x)

[b, a, s] = lwe.key_gen()
[v0, u0] = lwe.enc(b, a, x)

new_p = 14543227543197505793
lwe.set_p(new_p)
[v0, u0] = lwe.modulus_switching(p, new_p, v0, u0)

#s2 = lwe.mul(s,s)


####### expand #######
# zeros = [0 for i in range(n)]
# expand_outer_loop_count = 4
# c0 = [zeros for i in range(2**expand_outer_loop_count)]
# c1 = [zeros for i in range(2**expand_outer_loop_count)]
# c0[0] = u
# c1[0] = v
# ciphertexts = lwe.expand(expand_outer_loop_count, s, (c0, c1))
# for i in range(len(ciphertexts[0])):
#     [x2, zNoisy] = lwe.dec(ciphertexts[1][i], ciphertexts[0][i], s)
#     print("################# decrypted text ###################")
#     print(x2)

####### key switching #######
# g = lwe.decompose_gadget()
# [s1, v1, u1] = lwe.key_switching(g, s, s)
# [v2, u2] = lwe.new_ciphertext(v, u, v1, u1)
# x2 = lwe.dec(v2, u2, s1)

###### check addition on ciphertext #######
# [v1, u1] = lwe.enc(b, a, x)
# u2 = lwe.add(u, u1)
# v2 = lwe.add(v, v1)
# x2 = lwe.dec(v2, u2, s)

###### check multiplication on ciphertext #######
# [rlk_b, rlk_a] = lwe.rl_keys(s, s2)
#
# [v1, u1] = [v0, u0]
# v, u = v0, u0
# c0 = lwe.mul(v, v1)
# c1 = lwe.add(lwe.mul(u,v1), lwe.mul(v,u1))
# c2 = lwe.mul(u, u1)
# [c0_mul, c1_mul] = lwe.relinearization(rlk_b, rlk_a, c0, c1, c2, s)
#
# mult_count = 0
#
# for k in range(10):
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
# print(x2[0])

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

x2 = lwe.dec(v0, u0, s)

print("################# decrypted text ###################")
print(x2[0])
