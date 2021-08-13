import random
from lagrange import lagrange

n = 10 #size of the committee
m = 6 #threshold size of the committee needed to reconstruct the secret

#some hard-coded values used to check the correctness of the protocol
p = 11 #prime modulus
generator = 9
r = 23 #size of the finite field of the generator

k = random.randint(0, p-1) #secret
print("original secret: ", k)

a = [random.randint(0, p-1) for _ in range(m-1)]
s_shares = []
for i in range(1, n+1):
    s_i = k
    for j in range(1, m):
        s_i = (s_i + ((((a[j-1]*i) % p)**j) % p)) % p
    s_shares.append(s_i)
print("shares: ", s_shares)

print("secret reconstructed: ", lagrange(s_shares, p))

generator_lst = [0 for _ in range(m)]
generator_lst[0] = (generator ** k) % r
for i in range(1, m):
    generator_lst[i] = (generator ** a[i-1]) % r
for player in range(n):
    prod = generator_lst[0]
    for l in range(1, m):
        prod = (prod * (generator_lst[l] ** ((player+1)**l)) % r) % r

sub_shares = [[0 for _ in range(n)] for _ in range(n)]
for member in range(n):
    a_prime = [random.randint(0, p-1) for _ in range(m-1)]
    for i in range(1, n+1):
        s_i = s_shares[member]
        for j in range(1, m):
            s_i = (s_i + ((((a_prime[j-1]*i) % p)**j) % p)) % p
        sub_shares[i-1][member] = s_i
    generator_lst_new = [0 for _ in range(m)]
    generator_lst_new[0] = (generator ** s_shares[member]) % p
    for i in range(1, m):
        generator_lst_new[i] = (generator ** a_prime[i-1]) % p
new_shares = [lagrange(sub_shares[i], p) for i in range(n)]
print("new shares (after redistribution): ", new_shares)

print("secret reconstructed by the new committee: ", lagrange(new_shares, p))
print("secret can also be reconstructed if there's at least m members in the new committee: ", lagrange(new_shares[:m], p))
