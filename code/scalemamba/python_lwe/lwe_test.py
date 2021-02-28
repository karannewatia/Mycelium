from ring import Ring
from lwe import LWE
import random

p = 3843321857 #257
w = 9 #385597899

lgN = 4
r = Ring(lgN, w)

N = 1
lgM = 7 #10
l = 16
n = 16
lgP = 32
lwe = LWE(r, N, lgM, l, n, lgP)

x = [0 for i in range(l)]
for i in range(l):
  x[i] = 0 #random.randrange(0, 2)
print("####### plaintext 1 ###########")
x[3] = 1
print(x)

[b, a, s] = lwe.key_gen()

# print("####### public key a ###########")
# print(a)
# print("####### public key b ###########")
# print(b)
# print("####### secret key s ###########")
# print(s)
[v, u] = lwe.enc(b, a, x)
# print("############## original ciphertext u ################")
# print(u)
# print("############## original ciphertext v #################")
# print(v)

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
x[3] = 0
x[5] = 1
print("####### plaintext 2 ###########")
print(x)
[v1, u1] = lwe.enc(b, a, x)
c0 = lwe.mul(v, v1)
c1 = lwe.add(lwe.mul(u,v1), lwe.mul(v,u1))
c2 = lwe.mul(u, u1)
[rlk_b, rlk_a] = lwe.rl_keys(s)
[c0_mul, c1_mul] = lwe.relinearization(rlk_b, rlk_a, c0, c1, c2, s)
x2 = lwe.dec(c0_mul, c1_mul, s)

#x2 = lwe.dec_mul(c0, c1, c2, s)



#x2 = lwe.dec(v, u, s)

print("################# decrypted text ###################")
print(x2)
