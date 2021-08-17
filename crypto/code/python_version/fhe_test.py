from ring import Ring
from lwe import LWE
import random

lgP = 100 #ciphertext modulus bitsize
lgM = 10 #plaintext modulus bitsize
lgN = 7
n = 1 << lgN #polynomial degree
N = 1 #used in binomial distribution
l = 5 #plaintext length (number of elements)

#ciphertext modulus
p = 1026579212895469736969978638337
#used in polynomial multiplication
w = 667764024479347290416337878961

r = Ring(lgN, w, p)
lwe = LWE(r, N, lgM, l, n, lgP, p)

#create a random plaintext
x = [0 for i in range(l)]
for i in range(l):
  x[i] = random.randrange(0, 100)
print("plaintext: ", x)

#(b,a) is the public key and s is the secret key
[b, a, s] = lwe.key_gen()
#encrypt the plaintext using the public key to create a ciphertext (v0,u0)
[v0, u0] = lwe.enc(b, a, x)
#decrypt the ciphertext using the secret key
x2 = lwe.dec(v0, u0, s)

print("decrypted text: ", x2[0])
