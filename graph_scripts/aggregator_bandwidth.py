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
degree = 32768 #polynomial degree
prime_bitsize = 550 #ciphertext modulus bitsize
enc_proof_size = 810 #in bytes

#size of the ciphertext
ct_size = bytesto(degree * prime_bitsize * 2 / 8, 'm')

telescoping = [0,0,0]
forwarding = [0,0,0]

#The onion routing bandwidth costs are obtained from running the
#onion routing code on CloudLab machines, and are also in 'onion_routing_costs.xlsx'
#We only consider the write costs of the aggregator (which corresponds to the read costs on the spreadsheet)

##################### 2 hops ######################
establish_keys_src = 4386
establish_keys_node1 = 4456
establish_keys_node2 = 1608
establish_keys_dst = 562

#each user will set up a path for all their friends
telescoping[0] = num_friends*(establish_keys_src + establish_keys_node1 + establish_keys_node2 + establish_keys_dst)
telescoping[0] = bytesto(telescoping[0], 'm')

encryption_src = enc_proof_size
encryption_node1 = 4509105
encryption_node2 = 4509030
encryption_dst = 4508954

forwarding[0] = num_friends*(encryption_src + encryption_node1 + encryption_node2)
forwarding[0] = bytesto(forwarding[0], 'm')
#####################  ######################


##################### 3 hops ######################
establish_keys_src = 6641
establish_keys_node1 = 7590
establish_keys_node2 = 4463
establish_keys_node3 = 1608
establish_keys_dst = 562

#each user will set up a path for all their friends
telescoping[1] = num_friends*(establish_keys_src + establish_keys_node1 + establish_keys_node2 + establish_keys_node3 + establish_keys_dst)
telescoping[1] = bytesto(telescoping[1], 'm')

encryption_src = enc_proof_size
encryption_node1 = 4509181
encryption_node2 = 4509106
encryption_node3 = 4509030
encryption_dst = 4508954

forwarding[1] = num_friends*(encryption_src + encryption_node1 + encryption_node2 + encryption_node3 + encryption_dst)
forwarding[1] = bytesto(forwarding[1], 'm')
#####################  ######################

##################### 4 hops ######################
establish_keys_src = 9029
establish_keys_node1 = 10989
establish_keys_node2 = 7590
establish_keys_node3 = 4463
establish_keys_node4 = 1608
establish_keys_dst = 562

#each user will set up a path for all their friends
telescoping[2] = num_friends*(establish_keys_src + establish_keys_node1 + establish_keys_node2 + establish_keys_node3 + establish_keys_node4 + establish_keys_dst)
telescoping[2] = bytesto(telescoping[2], 'm')

encryption_src = enc_proof_size
encryption_node1 = 4509256
encryption_node2 = 4509181
encryption_node3 = 4509106
encryption_node4 = 4509030
encryption_dst = 4508954

forwarding[2] = num_friends*(encryption_src + encryption_node1 + encryption_node2 + encryption_node3 + encryption_node4 + encryption_dst)
forwarding[2] = bytesto(forwarding[2], 'm')
#####################  ######################

font = {'size'   : 17}
plt.rc('font', **font)
plt.gcf().subplots_adjust(bottom=0.25)
plt.gcf().subplots_adjust(left=0.14)

N = 3

total = [telescoping[0] + forwarding[0], telescoping[1] + forwarding[1], telescoping[2] + forwarding[2]]

ind = np.arange(N)
width = 0.15
p1 = plt.bar(ind, total, width, color='tab:cyan', edgecolor="black")
p2 = plt.bar(ind+width, [2*x for x in total], width, color='tab:purple', edgecolor="black")
p3 = plt.bar(ind+2*width, [3*x for x in total], width, color='tab:red', edgecolor="black")

plt.xlabel('Number of hops in the communication path\n(a)', fontsize='large')
plt.ylabel('Traffic (MB sent) per user', fontsize='large')
plt.xticks(ind+width, ('2', '3','4'))
plt.yticks(np.arange(0, 900, 100))
plt.legend((p1[0], p2[0], p3[0]), ('r=1', 'r=2', 'r=3'))
plt.savefig('../new_graphs/Aggregator_bandwidth.pdf', format='pdf')
