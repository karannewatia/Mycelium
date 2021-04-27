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

num_friends = 10
degree = 32768
prime_bitsize = 550

ct_size = bytesto(degree * prime_bitsize * 2 / 8, 'm')
enc_proof_size = 4.6
shift_proof_size = 12

telescoping = [0,0,0]
forwarding = [0,0,0]

final_upload = (prime_bitsize * degree * 2 / 8) #TODO add size of the actual multiplication proof here
final_upload = bytesto(final_upload , 'm') + 51

##################### 2 hops ######################
establish_keys_src = 2001
establish_keys_node1 = 3441
establish_keys_node2 = 1757
establish_keys_dst = 298

telescoping[0] = num_friends*(establish_keys_src + establish_keys_node1 + establish_keys_node2 + establish_keys_dst)
telescoping[0] = bytesto(telescoping[0], 'm')


encryption_src = (1048774*(ct_size+enc_proof_size)) + 8192
encryption_node1 = (1048710*ct_size) + 8192
encryption_node2 = (1048646*ct_size) + 8192

forwarding[0] = num_friends*(encryption_src + encryption_node1 + encryption_node2)

shift_src = (1048774*(ct_size+shift_proof_size)) + 8192
shift_node1 = (1048710*ct_size) + 8192
shift_node2 = (1048646*ct_size) + 8192

forwarding[0] += num_friends*(shift_src + shift_node1 + shift_node2)
forwarding[0] = bytesto(forwarding[0], 'm')
#####################  ######################


##################### 3 hops ######################
establish_keys_src = 3123
establish_keys_node1 = 5641
establish_keys_node2 = 3591
establish_keys_node3 = 1799
establish_keys_dst = 304

telescoping[1] = num_friends*(establish_keys_src + establish_keys_node1 + establish_keys_node2 + establish_keys_node3 + establish_keys_dst)
telescoping[1] = bytesto(telescoping[1], 'm')


encryption_src = (1048838*(ct_size+enc_proof_size)) + 8192
encryption_node1 = (1048774*ct_size) + 8192
encryption_node2 = (1048710*ct_size) + 8192
encryption_node3 = (1048646*ct_size) + 8192

forwarding[1] = num_friends*(encryption_src + encryption_node1 + encryption_node2 + encryption_node3)

shift_src = (1048838*(ct_size+shift_proof_size)) + 8192
shift_node1 = (1048774*ct_size) + 8192
shift_node2 = (1048710*ct_size) + 8192
shift_node3 = (1048646*ct_size) + 8192

forwarding[1] += num_friends*(shift_src + shift_node1 + shift_node2 + shift_node3)
forwarding[1] = bytesto(forwarding[1], 'm')
#####################  ######################

##################### 4 hops ######################
establish_keys_src = 4235
establish_keys_node1 = 7947
establish_keys_node2 = 5641
establish_keys_node3 = 3591
establish_keys_node4 = 1799
establish_keys_dst = 304

telescoping[2] = num_friends*(establish_keys_src + establish_keys_node1 + establish_keys_node2 + establish_keys_node3 + establish_keys_node4 + establish_keys_dst)
telescoping[2] = bytesto(telescoping[2], 'm')


encryption_src = (1048902*(ct_size+enc_proof_size)) + 8192
encryption_node1 = (1048838*ct_size) + 8192
encryption_node2 = (1048774*ct_size) + 8192
encryption_node3 = (1048710*ct_size) + 8192
encryption_node4 = (1048646*ct_size) + 8192

forwarding[2] = num_friends*(encryption_src + encryption_node1 + encryption_node2 + encryption_node3 + encryption_node4)

shift_src = (1048902*(ct_size+shift_proof_size)) + 8192
shift_node1 = (1048838*ct_size) + 8192
shift_node2 = (1048774*ct_size) + 8192
shift_node3 = (1048710*ct_size) + 8192
shift_node4 = (1048646*ct_size) + 8192

forwarding[2] += num_friends*(shift_src + shift_node1 + shift_node2 + shift_node3 + shift_node4)
forwarding[2] = bytesto(forwarding[2], 'm')
#####################  ######################



N = 3

total = [telescoping[0] + forwarding[0], telescoping[1] + forwarding[1], telescoping[2] + forwarding[2]]

ind = np.arange(N)
width = 0.15
p1 = plt.bar(ind, [x + final_upload for x in total], width, color='tab:blue', edgecolor="black")
p2 = plt.bar(ind+width, [2*x + final_upload for x in total], width, color='tab:orange', edgecolor="black")
p3 = plt.bar(ind+2*width, [3*x + final_upload for x in total], width, color='tab:green', edgecolor="black")


plt.xlabel('Number of hops in the communication path', fontsize='large')
plt.ylabel('Traffic (MB sent)', fontsize='large')
# plt.title('Total number of bytes sent by a client on average')
plt.xticks(ind+width, ('2', '3','4'))
plt.yticks(np.arange(0, 2200, 200))

plt.legend((p1[0], p2[0], p3[0]), ('r=1', 'r=2', 'r=3'))
plt.savefig('../graphs/users/user_bandwidth.pdf', format='pdf')
