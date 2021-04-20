import random
from lagrange import lagrange

n = 10
m = 6
p = 11 #TODO change this to a 550 bit prime
r = 23
degree = 32768 #TODO do everthing 32768 times

#TODO verification steps at both levels

def modInverse(a, b):
    for x in range(1, p):
        if (((a%p) * (x%p)) % p == b):
            return x
    return -1

k = random.randint(0, p-1)
print("original secret: ", k)
a = [random.randint(0, p-1) for _ in range(m-1)]

s_shares = []

for i in range(1, n+1):
    s_i = k
    for j in range(1, m):
        s_i = (s_i + ((((a[j-1]*i) % p)**j) % p)) % p
    #print(s_i)
    s_shares.append(s_i)
print("shares: ", s_shares)

print("original secret reconstructed: ", lagrange(s_shares, p))

generator = 9 #random.randint(0, p-1)
generator_lst = [0 for _ in range(m)]
generator_lst[0] = (generator ** k) % r
for i in range(1, m):
    generator_lst[i] = (generator ** a[i-1]) % r
print("a vals: ", a)
print("generator: ", generator)
print("generator list: ", generator_lst)
print(" ")
for player in range(n):
    print((generator ** s_shares[player]) % r)
    prod = generator_lst[0]
    for l in range(1, m):
        #prod = (prod * (generator_lst[l] ** ((player+1)**l)) % p) % p
        prod = (prod * (generator_lst[l] ** ((player+1)**l)) % r) % r
    print(prod)
    print(" ")


# sub_shares = [[0 for _ in range(n)] for _ in range(n)]
# for member in range(n): #TODO change the range to be the authorized subset
#     a_prime = [random.randint(0, p-1) for _ in range(m-1)]
#
#     for i in range(1, n+1):
#         s_i = s_shares[member]
#         for j in range(1, m):
#             s_i = (s_i + ((((a_prime[j-1]*i) % p)**j) % p)) % p
#         #print(s_i)
#         sub_shares[i-1][member] = s_i
#
#     generator_lst_new = [0 for _ in range(m)]
#     generator_lst_new[0] = (generator ** s_shares[member]) % p
#     for i in range(1, m):
#         generator_lst_new[i] = (generator ** a_prime[i-1]) % p
#
# new_shares = [lagrange(sub_shares[i], p) for i in range(n)]
# print("new shares: ", new_shares)
# print("secret reconstructed by new committee: ", lagrange(new_shares, p))
