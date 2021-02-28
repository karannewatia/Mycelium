from ring import Ring
from lwe import LWE
import random

p = 17 #3843321857
w = 9 #385597899

lgN = 2#4
r = Ring(lgN, w)

N = 1
lgM = 1 #10
l = 4#16
n = 4#16
lgP = 4#32
lwe = LWE(r, N, lgM, l, n, lgP)

x = [0 for i in range(l)]
for i in range(l):
  x[i] = 1 #random.randrange(0, 9)
print("####### plaintext ###########")
x[1] = 0
x[3] = 1

print(x)

[b, a, s] = lwe.key_gen()

print("####### public key a ###########")
print(a)
print("####### public key b ###########")
print(b)
print("####### secret key s ###########")
print(s)
[u, v] = lwe.enc(b, a, s, x)
print("############## original ciphertext u ################")
print(u)
print("############## original ciphertext v #################")
print(v)

# u = lwe.shift(u, 7)
# v = lwe.shift(v, 7)
# s_new = lwe.shift(s, 7)
# x2 = lwe.dec(v, u, s_new)


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
# [v1, u1] = lwe.enc(b, a, x)
# c0 = lwe.mul(v, v1)
# c1 = lwe.add(lwe.mul(u,v1), lwe.mul(v,u1))
# c2 = lwe.mul(u, u1)
# print("################# c2 ###################")
# print(c2)
# [rlk_b, rlk_a] = lwe.rl_keys(s)
# # print("################# rlk a ###################")
# # for i in range(lgP):
# #     print(rlk_a[i])
# # print("################# rlk b ###################")
# # for i in range(lgP):
# #     print(rlk_b[i])
# [c0_mul, c1_mul] = lwe.relinearization(rlk_b, rlk_a, c0, c1, c2)
# print("################# c0 relin ###################")
# print(c0_mul)
# print("################# c1 relin ###################")
# print(c1_mul)
# x2 = lwe.dec(c0_mul, c1_mul, s)
# #x2 = lwe.dec_mul(c0, c1, c2, s)


x2 = lwe.dec(u, v, s)

print("################# decrypted text ###################")
print(x2)
