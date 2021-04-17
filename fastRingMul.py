from sympy import ntt, intt

prime_no = 17 # 97
n = 4
seq1 = [1, 0, 3, 1]  #[15, 21, 13, 44]
seq2 = [0, 16, 0, 0] #[2, 90, 35, 16]

psi = 9 #33 # 2n-primitive root of unity in Z_prime_no 

# compute nega-cyclic vector
for i in range (len(seq1)):
    seq1[i] = (seq1[i] * pow(psi, i, prime_no)) % prime_no
    seq2[i] = (seq2[i] * pow(psi, i, prime_no)) % prime_no

# compute NTT
transform1 = ntt(seq1, prime_no)
transform2 = ntt(seq2, prime_no)
transform = [0]*len(seq1)

# compute vector component-wise multiplication
for i in range (len(seq1)):
    transform[i] = (transform1[i] * transform2[i])%prime_no

# compute iNTT
seq = intt(transform, prime_no)

# compute inv nega-cyclic vector
for i in range (len(seq)):
    psi_pow = pow(psi, i, prime_no)
    inv_psi_pow = pow(psi_pow, -1, prime_no)
    seq[i] = (seq[i] * inv_psi_pow) % prime_no

# print result
print(seq)
