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

telescoping = [0,0,0]
forwarding = [0,0,0]

##################### 2 hops ######################
establish_keys_src = 4394
establish_keys_node1 = 4446
establish_keys_node2 = 1598
establish_keys_dst = 557

telescoping[0] = num_friends*(establish_keys_src + establish_keys_node1 + establish_keys_node2 + establish_keys_dst)
telescoping[0] = bytesto(telescoping[0], 'm')


encryption_src = 8192
encryption_node1 = (9332557*ct_size/8.9) + 8192
encryption_node2 = (9332482*ct_size/8.9) + 8192
encryption_dst = (9332407*ct_size/8.9) + 8192

forwarding[0] = num_friends*(encryption_src + encryption_node1 + encryption_node2)


forwarding[0] = bytesto(forwarding[0], 'm')
#####################  ######################


##################### 3 hops ######################
establish_keys_src = 6649
establish_keys_node1 = 6817
establish_keys_node2 = 4446
establish_keys_node3 = 1598
establish_keys_dst = 557

telescoping[1] = num_friends*(establish_keys_src + establish_keys_node1 + establish_keys_node2 + establish_keys_node3 + establish_keys_dst)
telescoping[1] = bytesto(telescoping[1], 'm')


encryption_src = 8192
encryption_node1 = (9332632*ct_size/8.9) + 8192
encryption_node2 = (9332557*ct_size/8.9) + 8192
encryption_node3 = (9332482*ct_size/8.9) + 8192
encryption_dst = (9332407*ct_size/8.9) + 8192

forwarding[1] = num_friends*(encryption_src + encryption_node1 + encryption_node2 + encryption_node3 + encryption_dst)

# shift_src = 8192
# shift_node1 = (1048838*ct_size) + 8192
# shift_node2 = (1048774*ct_size) + 8192
# shift_node3 = (1048710*ct_size) + 8192
# shift_dst = (1048646*ct_size) + 8192
#
# forwarding[1] += num_friends*(shift_src + shift_node1 + shift_node2 + shift_node3 + shift_dst)

forwarding[1] = bytesto(forwarding[1], 'm')
#####################  ######################

##################### 4 hops ######################
establish_keys_src = 9044
establish_keys_node1 = 10976
establish_keys_node2 = 7572
establish_keys_node3 = 4446
establish_keys_node4 = 1598
establish_keys_dst = 557

telescoping[2] = num_friends*(establish_keys_src + establish_keys_node1 + establish_keys_node2 + establish_keys_node3 + establish_keys_node4 + establish_keys_dst)
telescoping[2] = bytesto(telescoping[2], 'm')


encryption_src = 8192
encryption_node1 = (9332707*ct_size/8.9) + 8192
encryption_node2 = (9332632*ct_size/8.9) + 8192
encryption_node3 = (9332557*ct_size/8.9) + 8192
encryption_node4 = (9332482*ct_size/8.9) + 8192
encryption_dst = (9332407*ct_size/8.9) + 8192

forwarding[2] = num_friends*(encryption_src + encryption_node1 + encryption_node2 + encryption_node3 + encryption_node4 + encryption_dst)

# shift_src = 8192
# shift_node1 = (1048902*ct_size) + 8192
# shift_node2 = (1048838*ct_size) + 8192
# shift_node3 = (1048774*ct_size) + 8192
# shift_node4 = (1048710*ct_size) + 8192
# shift_dst = (1048646*ct_size) + 8192
#
# forwarding[2] += num_friends*(shift_src + shift_node1 + shift_node2 + shift_node3 + shift_node4 + shift_dst)

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
# plt.title('Total number of bytes sent by a client on average')
plt.xticks(ind+width, ('2', '3','4'))
plt.yticks(np.arange(0, 900, 100))

plt.legend((p1[0], p2[0], p3[0]), ('r=1', 'r=2', 'r=3'))


plt.savefig('../original_graphs/Aggregator_bandwidth.pdf', format='pdf')
