import numpy as np
import matplotlib.pyplot as plt

num_copies = 3
num_friends = 10

establish_keys = 0.100233

telescoping = num_copies * num_friends * establish_keys

send_encrypt = 1.39565

forwarding = num_copies * num_friends * send_encrypt

send_shift = 1.69511

forwarding += num_copies * num_friends * send_encrypt

encryption_zkp = 15.146

shift_zkp = 4.460

zkp = encryption_zkp + (shift_zkp * num_friends)

fhe = 0 #this should be cost of encrypting a ciphertext +  num_friends*cost of shifting + cost of multiplying 10 ciphertexts (with relin)

print(telescoping + forwarding + zkp + fhe)
