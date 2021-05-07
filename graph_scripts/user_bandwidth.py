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
f = 1/0.1
degree = 32768
prime_bitsize = 550

ct_size = bytesto(degree * prime_bitsize * 2 / 8, 'm')
enc_proof_size = 4.6

telescoping = [0,0,0]
forwarding = [0,0,0]

telescoping_forwarder = [0,0,0]
forwarding_forwarder = [0,0,0]

final_upload = (prime_bitsize * degree * 12 / 8)
final_upload = bytesto(final_upload , 'm') + 51 # 51 is for size of aggregation proof

##################### 2 hops ######################
establish_keys_src = 2167
establish_keys_node1 = 5688
establish_keys_node2 = 2836
establish_keys_dst = 304

telescoping[0] = num_friends*(establish_keys_src + establish_keys_dst)
telescoping[0] = bytesto(telescoping[0], 'm')

telescoping_forwarder[0] = num_friends*(establish_keys_src + f*((establish_keys_node1 + establish_keys_node2)/2) + establish_keys_dst)
telescoping_forwarder[0] = bytesto(telescoping_forwarder[0], 'm')


encryption_src = (9332557*ct_size/8.9) + 8192
encryption_node1 = (9332482*ct_size/8.9) + 8192
encryption_node2 = (9332407*ct_size/8.9) + 8192

forwarding[0] = num_friends*(encryption_src)
forwarding[0] = bytesto(forwarding[0], 'm')
forwarding[0] += enc_proof_size

forwarding_forwarder[0] = num_friends*(encryption_src + f*(encryption_node1 + encryption_node2)/2)
forwarding_forwarder[0] = bytesto(forwarding_forwarder[0], 'm')
forwarding_forwarder[0] += enc_proof_size

#####################  ######################


##################### 3 hops ######################
establish_keys_src = 3178
establish_keys_node1 = 8816
establish_keys_node2 = 5688
establish_keys_node3 = 2836
establish_keys_dst = 304

telescoping[1] = num_friends*(establish_keys_src)
telescoping[1] = bytesto(telescoping[1], 'm')

telescoping_forwarder[1] = num_friends*(establish_keys_src + f*((establish_keys_node1 + establish_keys_node2 + establish_keys_node3)/3) + establish_keys_dst)
telescoping_forwarder[1] = bytesto(telescoping_forwarder[1], 'm')


encryption_src = (9332632*ct_size/8.9) + 8192
encryption_node1 = (9332557*ct_size/8.9) + 8192
encryption_node2 = (9332482*ct_size/8.9) + 8192
encryption_node3 = (9332407*ct_size/8.9) + 8192

forwarding[1] = num_friends*(encryption_src)
forwarding[1] = bytesto(forwarding[1], 'm')
forwarding[1] += enc_proof_size

forwarding_forwarder[1] = num_friends*(encryption_src + f*(encryption_node1 + encryption_node2 + encryption_node3)/3)
forwarding_forwarder[1] = bytesto(forwarding_forwarder[1], 'm')
forwarding_forwarder[1] += enc_proof_size
#####################  ######################

##################### 4 hops ######################
establish_keys_src = 4327
establish_keys_node1 = 12222
establish_keys_node2 = 8816
establish_keys_node3 = 5688
establish_keys_node4 = 2836
establish_keys_dst = 304

telescoping[2] = num_friends*(establish_keys_src)
telescoping[2] = bytesto(telescoping[2], 'm')

telescoping_forwarder[2] = num_friends*(establish_keys_src + f*((establish_keys_node1 + establish_keys_node2 + establish_keys_node3 + establish_keys_node4)/4) + establish_keys_dst)
telescoping_forwarder[2] = bytesto(telescoping_forwarder[2], 'm')


encryption_src = (9332707*ct_size/8.9) + 8192
encryption_node1 = (9332632*ct_size/8.9) + 8192
encryption_node2 = (9332557*ct_size/8.9) + 8192
encryption_node3 = (9332482*ct_size/8.9) + 8192
encryption_node4 = (9332407*ct_size/8.9) + 8192

forwarding[2] = num_friends*(encryption_src)
forwarding[2] = bytesto(forwarding[2], 'm')
forwarding[2] += enc_proof_size

forwarding_forwarder[2] = num_friends*(encryption_src + f*(encryption_node1 + encryption_node2 + encryption_node3 + encryption_node4)/4)
forwarding_forwarder[2] = bytesto(forwarding_forwarder[2], 'm')
forwarding_forwarder[2] += enc_proof_size
#####################  ######################

font = {'size'   : 14}
plt.rc('font', **font)
plt.gcf().subplots_adjust(bottom=0.15)

N = 6
ind = np.arange(N)
width = 0.15

total = [telescoping[0] + forwarding[0], telescoping[1] + forwarding[1], telescoping[2] + forwarding[2]]
p1 = plt.bar(ind[:3], [x + final_upload for x in total], width, color='tab:blue', edgecolor="black")
p2 = plt.bar(ind[:3]+width, [2*x + final_upload for x in total], width, color='tab:orange', edgecolor="black")
p3 = plt.bar(ind[:3]+2*width, [3*x + final_upload for x in total], width, color='tab:green', edgecolor="black")


total_forwarder = [telescoping_forwarder[0] + forwarding_forwarder[0], telescoping_forwarder[1] + forwarding_forwarder[1], telescoping_forwarder[2] + forwarding_forwarder[2]]
p4 = plt.bar(ind[3:], [x + final_upload for x in total_forwarder], width, color='tab:brown', edgecolor="black")
p5 = plt.bar(ind[3:]+width, [2*x + final_upload for x in total_forwarder], width, color='tab:pink', edgecolor="black")
p6 = plt.bar(ind[3:]+2*width, [3*x + final_upload for x in total_forwarder], width, color='tab:olive', edgecolor="black")

print([2*x + final_upload for x in total])
print([2*x + final_upload for x in total_forwarder])


plt.xlabel('Number of hops in the communication path', fontsize='large')
plt.ylabel('Traffic (MB sent)', fontsize='large')
plt.yscale('log')
plt.yticks([1e1, 1e2, 1e3, 1e4])
plt.xticks(ind+width, ('2', '3','4', '2', '3','4'))

plt.legend((p1[0], p2[0], p3[0], p4[0], p5[0], p6[0]), ('r=1, non-forwarder', 'r=2, non-forwarder', 'r=3, non-forwarder', 'r=1, forwarder', 'r=2, forwarder', 'r=3, forwarder'))
plt.savefig('../graphs/users/user_bandwidth.pdf', format='pdf')
