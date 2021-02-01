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
  x[i] = i

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

###### key switching #######
g = lwe.decompose_gadget()
print("############## decompose gadget g ###################")
print(g)
[s1, v1, u1, e, uvs, gs] = lwe.key_switching(g,s)
print("############## new secret key s' ##################")
print(s1)
print("############# key switching key u ##################")
for i in range(32):
    print(u1[i])
print("############# key switching key v ####################")
for i in range(32):
    print(v1[i])
print("############# k0 + k1s' ####################")
for i in range(32):
    print(uvs[i])
[v2, u2, g_inverse, g_inv_g, g_inv_e, g_inv_uvs, g_inv_uvs_c0, gs, g_inv_gs, g_inv_gs_e, c0_tmpa_tmpb_s1] = lwe.new_ciphertext(v, u, v1, u1, g, e, uvs, gs, s1)
print("################# g inverse ##################")
for i in range(4):
    print(g_inverse[i])
print("################# <g inverse, g> ##################")
print(g_inv_g)
print("################# <g inverse, e> ##################")
print(g_inv_e)
print("################# <g inverse, k0 + k1s'> ##################")
print(g_inv_uvs)
print("################# new ciphertext u2 ##################")
print(u2)
print("#################### new ciphertext v2 #####################")
print(v2)

[x2, c0c1s] = lwe.dec(v2, u2, s1)
print("#################### gs #####################")
for i in range(32):
    print(gs[i])
print("#################### <g inverse, gs> #####################")
print(g_inv_gs)
print("#################### <g inverse, gs> + <g inverse, e> #####################")
print(g_inv_gs_e)
print("#################### <g inverse, k0 + k1s'> + c0 #####################")
print(g_inv_uvs_c0)
print("#################### c0 + tmp_a + tmp_b s' #####################")
print(c0_tmpa_tmpb_s1)
print("#################### c0' + c1's' (zNoisy) #####################")
print(c0c1s)

###### check addition on ciphertext #######
# [u1, v1] = lwe.enc(a, b, x)
# u2 = lwe.add(u, u1)
# v2 = lwe.add(v, v1)
# x2 = lwe.dec(u2, v2, s)

#x2 = lwe.dec(v, u, s)
print("################# decrypted text ###################")
print(x2)
