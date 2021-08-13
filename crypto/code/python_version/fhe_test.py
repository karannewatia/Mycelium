from ring import Ring
from lwe import LWE
import random
import sympy

lgP = 100 #ciphertext modulus bitsize
lgM = 10 #plaintext modulus bitsize
lgN = 7
n = 1 << lgN #polynomial degree
N = 1 #used in binomial distribution
l = 5 #plaintext length (number of elements)

p = 1026579212895469736969978638337
w = 667764024479347290416337878961

r = Ring(lgN, w, p)
lwe = LWE(r, N, lgM, l, n, lgP, p)

x = [0 for i in range(l)]
for i in range(l):
  x[i] = random.randrange(0, 100)
print("plaintext: ", x)

[b, a, s] = lwe.key_gen()
[v0, u0] = lwe.enc(b, a, x)
x2 = lwe.dec(v0, u0, s)

print("decrypted text: ", x2[0])
