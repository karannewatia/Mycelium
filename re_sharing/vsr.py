import random

n = 10
m = 6
p = 97 #TODO change this to a 550 bit prime
degree = 32768 #TODO do everthing 32768 times

#TODO verification steps at both levels

k = random.randint(0, p-1)
#print(k)
a = [random.randint(0, p-1) for _ in range(m-1)]

s_shares = []

for i in range(1, n+1):
    s_i = k
    for j in range(1, m):
        s_i = (s_i + ((((a[j-1]*i) % p)**j) % p)) % p
    #print(s_i)
    s_shares.append(s_i)

generator = random.randint(0, p-1)
generator_lst = [0 for _ in range(m)]
generator_lst[0] = (generator ** k) % p
for i in range(1, m):
    generator_lst[i] = (generator ** a[i-1]) % p
#print(generator_lst)

# print((generator ** s_shares[0]) % p)
# prod = generator_lst[0]
# for j in range(1, m):
#     prod = (prod * (generator_lst[j] ** 1)) % p
# print(prod)


sub_shares = [[0 for _ in range(n)] for _ in range(n)]
for member in range(n): #TODO change the range to be the authorized subset
    a_prime = [random.randint(0, p-1) for _ in range(m-1)]

    for i in range(1, n+1):
        s_i = s_shares[member]
        for j in range(1, m):
            s_i = (s_i + ((((a_prime[j-1]*i) % p)**j) % p)) % p
        #print(s_i)
        sub_shares[i-1][member] = s_i

    generator_lst_new = [0 for _ in range(m)]
    generator_lst_new[0] = (generator ** s_shares[member]) % p
    for i in range(1, m):
        generator_lst_new[i] = (generator ** a_prime[i-1]) % p

# for i in range(n):
#     print(sub_shares[i])

new_shares = [0 for _ in range(n)]
for j in range(n):
    new_share = 0
    for i in range(n): #TODO change the range to be the admissible subset
        b = 1
        for l in range(n): #TODO change the range to be the admissible subset
            if l != i:
                b *= l/(l-i)
        new_share = (new_share + ((b * sub_shares[j][i]) % p)) % p
    new_share = int(new_share)
    new_shares[j] = new_share
    #print(new_share)
