import numpy as np
import matplotlib.pyplot as plt

def bytesto(bytes, to, bsize=1024):
    """convert bytes to megabytes, etc.
       sample code:
           print('mb= ' + str(bytesto(314575262000000, 'm')))
       sample output:
           mb= 300002347.946
    """

    a = {'k' : 1, 'm': 2, 'g' : 3, 't' : 4, 'p' : 5, 'e' : 6 }
    r = float(bytes)
    for i in range(a[to]):
        r = r / bsize
    return(r)

num_friends = 10 #degree bound
f = 1/0.1 #fraction of forwarders
degree = 32768 #polynomial degree
prime_bitsize = 550
proof_hash_size = 8192 #(in bytes)

#size of the ciphertext
ct_size = bytesto(proof_hash_size + (degree * prime_bitsize * 2 / 8), 'm')

enc_proof_size = 0.00081

final_upload = (prime_bitsize * degree * 12 / 8)
final_upload = bytesto(final_upload , 'm') + 53.347 # 53.347 is for size of aggregation proof

telescoping = [0,0,0]
forwarding = [0,0,0]

telescoping_forwarder = [0,0,0]
forwarding_forwarder = [0,0,0]


#The onion routing bandwidth costs are obtained from running the
#onion routing code on CloudLab machines, and are also in 'onion_routing_costs.xlsx'
#We only consider the write costs for users.

##################### 2 hops ######################
establish_keys_src = 2176
establish_keys_node1 = 5686
establish_keys_node2 = 2834
establish_keys_dst = 304

#each user has to establish a path for each friend,
#and each friend will also be the destination node for each of the friends
telescoping[0] = num_friends*(establish_keys_src + establish_keys_dst)
telescoping[0] = bytesto(telescoping[0], 'm')

#cost of telescoping for a forwarder on expectation
telescoping_forwarder[0] = num_friends*(establish_keys_src + f*((establish_keys_node1 + establish_keys_node2)/2) + establish_keys_dst)
telescoping_forwarder[0] = bytesto(telescoping_forwarder[0], 'm')

encryption_src = 4509109
encryption_node1 = 4509034
encryption_node2 = 4508958

#each user will send an encrypted ciphertext + the corresponding ZKP to each of their friends
forwarding[0] = num_friends*(encryption_src)
forwarding[0] = bytesto(forwarding[0], 'm')
forwarding[0] += enc_proof_size

#cost of forwarding messages on expectation
forwarding_forwarder[0] = num_friends*(encryption_src + f*(encryption_node1 + encryption_node2)/2)
forwarding_forwarder[0] = bytesto(forwarding_forwarder[0], 'm')
forwarding_forwarder[0] += enc_proof_size

#####################  ######################


##################### 3 hops ######################
establish_keys_src = 3195
establish_keys_node1 = 8821
establish_keys_node2 = 5691
establish_keys_node3 = 2837
establish_keys_dst = 304

#each user has to establish a path for each friend,
#and each friend will also be the destination node for each of the friends
telescoping[1] = num_friends*(establish_keys_src)
telescoping[1] = bytesto(telescoping[1], 'm')

#cost of telescoping for a forwarder on expectation
telescoping_forwarder[1] = num_friends*(establish_keys_src + f*((establish_keys_node1 + establish_keys_node2 + establish_keys_node3)/3) + establish_keys_dst)
telescoping_forwarder[1] = bytesto(telescoping_forwarder[1], 'm')

encryption_src = 4509185
encryption_node1 = 4509110
encryption_node2 = 4509034
encryption_node3 = 4508958

#each user will send an encrypted ciphertext + the corresponding ZKP to each of their friends
forwarding[1] = num_friends*(encryption_src)
forwarding[1] = bytesto(forwarding[1], 'm')
forwarding[1] += enc_proof_size

#cost of forwarding messages on expectation
forwarding_forwarder[1] = num_friends*(encryption_src + f*(encryption_node1 + encryption_node2 + encryption_node3)/3)
forwarding_forwarder[1] = bytesto(forwarding_forwarder[1], 'm')
forwarding_forwarder[1] += enc_proof_size
#####################  ######################

##################### 4 hops ######################
establish_keys_src = 4344
establish_keys_node1 = 12244
establish_keys_node2 = 8821
establish_keys_node3 = 5691
establish_keys_node4 = 2837
establish_keys_dst = 304

#each user has to establish a path for each friend,
#and each friend will also be the destination node for each of the friends
telescoping[2] = num_friends*(establish_keys_src)
telescoping[2] = bytesto(telescoping[2], 'm')

#cost of telescoping for a forwarder on expectation
telescoping_forwarder[2] = num_friends*(establish_keys_src + f*((establish_keys_node1 + establish_keys_node2 + establish_keys_node3 + establish_keys_node4)/4) + establish_keys_dst)
telescoping_forwarder[2] = bytesto(telescoping_forwarder[2], 'm')

encryption_src = 4509260
encryption_node1 = 4509185
encryption_node2 = 4509110
encryption_node3 = 4509034
encryption_node4 = 4508958

#each user will send an encrypted ciphertext + the corresponding ZKP to each of their friends
forwarding[2] = num_friends*(encryption_src)
forwarding[2] = bytesto(forwarding[2], 'm')
forwarding[2] += enc_proof_size

#cost of forwarding messages on expectation
forwarding_forwarder[2] = num_friends*(encryption_src + f*(encryption_node1 + encryption_node2 + encryption_node3 + encryption_node4)/4)
forwarding_forwarder[2] = bytesto(forwarding_forwarder[2], 'm')
forwarding_forwarder[2] += enc_proof_size
#####################  ######################

total = [telescoping[0] + forwarding[0], telescoping[1] + forwarding[1], telescoping[2] + forwarding[2]]
p1 = [x + final_upload for x in total]
p2 = [2*x + final_upload for x in total]
p3 = [3*x + final_upload for x in total]

total_forwarder = [telescoping_forwarder[0] + forwarding_forwarder[0], telescoping_forwarder[1] + forwarding_forwarder[1], telescoping_forwarder[2] + forwarding_forwarder[2]]
p4 = [x + final_upload for x in total_forwarder]
p5 = [2*x + final_upload for x in total_forwarder]
p6 = [3*x + final_upload for x in total_forwarder]

result = [p1,p2,p3,p4,p5,p6]
result = [[result[j][i] for j in range(len(result))] for i in range(len(result[0]))]
#row 1 has the costs for 2 hops, row 2 has the costs for 3 hops, row 3 has the costs for 4 hops
#r is the number of copies sent per message
#column 1 has the costs for r=1, column 2 has the costs for r=2, column 3 has the costs for r=3 (all for a non-forwarder)
#column 4 has the costs for r=1, column 5 has the costs for r=2, column 6 has the costs for r=3 (all for a non-forwarder)
print(result)
