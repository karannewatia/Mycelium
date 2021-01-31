#execfile('/root/SCALE-MAMBA/Programs/lwe/lwe.mpc')
from ring import Ring
from lwe import LWE
import random

#p = 3843321857
w = 2791827151 #3457723958

lgN = 2 #4
r = Ring(lgN, w)

N = 1
lgM = 10
l = 4
lwe = LWE(r, N, lgM, l)

x = [0 for i in range(l)]
for i in range(l):
  x[i] = i
  #print(x[i])

print("####### plaintext ###########")
print(x)

[a, b, s] = lwe.key_gen()
print("####### public key a ###########")
print(a)
print("####### public key b ###########")
print(b)
print("####### secret key s ###########")
print(s)
[u, v] = lwe.enc(a, b, x)
print("############## original ciphertext u ################")
print(u)
print("############## original ciphertext v #################")
print(v)
#x2 = lwe.dec(u, v, s)

###### key switching #######
g = lwe.decompose_gadget()
print("############## decompose gadget g ###################")
print(g)
[s1, u1, v1, e] = lwe.key_switching(g,s)
print("############## new secret key s' ##################")
print(s1)
print("############# key switching key u ##################")
for i in range(32):
    print(u1[i])
print("############# key switching key v ####################")
for i in range(32):
    print(v1[i])
[v2, u2, g_inverse, g_inv_g, g_inv_e] = lwe.new_ciphertext(v, u, v1, u1, g, e)
print("################# g inverse ##################")
for i in range(4):
    print(g_inverse[i])
print("################# <g inverse, g> ##################")
print(g_inv_g)
print("################# <g inverse, e> ##################")
print(g_inv_e)
print("################# new ciphertext u2 ##################")
print(u2)
print("#################### new ciphertext v2 #####################")
print(v2)
x2 = lwe.dec(u2, v2, s1)

###### check addition on ciphertext #######
# [u1, v1] = lwe.enc(a, b, x)
# u2 = lwe.add(u, u1)
# v2 = lwe.add(v, v1)
# x2 = lwe.dec(u2, v2, s)

print("################# decrypted text ###################")
print(x2)
