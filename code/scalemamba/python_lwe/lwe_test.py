#execfile('/root/SCALE-MAMBA/Programs/lwe/lwe.mpc')
from ring import Ring
from lwe import LWE
import random

#p = 3843321857
w = 2791827151

lgN = 2
r = Ring(lgN, w)

N = 1
lgM = 10
l = 4
n = 4
lgP = 32
lwe = LWE(r, N, lgM, l, n, lgP)

x = [0 for i in range(l)]
for i in range(l):
  x[i] = i #random.randrange(0, 500)


print("####### plaintext ###########")
print(x)

[b, a, s] = lwe.key_gen()
print("####### public key a ###########")
print(a)
print("####### public key b ###########")
print(b)
print("####### secret key s ###########")
print(s)
[v, u] = lwe.enc(b, a, x)
print("############## original ciphertext u ################")
print(u)
print("############## original ciphertext v #################")
print(v)
#
# ###### key switching #######
# g = lwe.decompose_gadget()
# [s1, v1, u1] = lwe.key_switching(g,s)
# [v2, u2] = lwe.new_ciphertext(v, u, v1, u1)
# x2 = lwe.dec(v2, u2, s1)

###### check addition on ciphertext #######
# [v1, u1] = lwe.enc(b, a, x)
# u2 = lwe.add(u, u1)
# v2 = lwe.add(v, v1)
# x2 = lwe.dec(v2, u2, s)
#

###### check multiplication on ciphertext #######
[v1, u1] = lwe.enc(b, a, x)
c0 = lwe.mul(v, v1)
c1 = lwe.add(lwe.mul(u,v1), lwe.mul(v,u1))
c2 = lwe.mul(u, u1)
print("################# c2 ###################")
print(c2)
[rlk_b, rlk_a] = lwe.rl_keys(s)
# print("################# rlk a ###################")
# for i in range(lgP):
#     print(rlk_a[i])
# print("################# rlk b ###################")
# for i in range(lgP):
#     print(rlk_b[i])
[c0_mul, c1_mul] = lwe.relinearization(rlk_b, rlk_a, c0, c1, c2)
print("################# c0 relin ###################")
print(c0_mul)
print("################# c1 relin ###################")
print(c1_mul)
x2 = lwe.dec(c0_mul, c1_mul, s)
#x2 = lwe.dec_mul(c0, c1, c2, s)

#x2 = lwe.dec(v, u, s)

print("################# decrypted text ###################")
print(x2)
