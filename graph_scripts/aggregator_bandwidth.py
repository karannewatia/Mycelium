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


num_copies = 2
num_friends = 10
degree = 32768
prime_bitsize = 550

ct_size = bytesto(degree * prime_bitsize * 2 / 8, 'm')


establish_keys_src = 2214
establish_keys_node1 = 2660
establish_keys_node2 = 1525
establish_keys_dst = 549


telescoping = num_friends*(establish_keys_src + establish_keys_node1 + establish_keys_node2 + establish_keys_dst)


encryption_src = 8192
encryption_node1 = (1048774*ct_size) + 8192
encryption_node2 = (1048710*ct_size) + 8192
encryption_dst = (1048646*ct_size) + 8192
forwarding = num_friends*(encryption_src + encryption_node1 + encryption_node2 + encryption_dst)

shift_src = 8192
shift_node1 = (1048774*ct_size) + 8192
shift_node2 = (1048710*ct_size) + 8192
shift_dst = (1048646*ct_size) + 8192
forwarding += num_friends*(shift_src + shift_node1 + shift_node2 + shift_dst)


total_cost = round((num_copies*telescoping) + (num_copies*forwarding))
total_cost = bytesto(total_cost, 't')
# print(total_cost)


N = 4

ind = [1e6, 1e7, 1e8, 1e9]

bandwidth = (total_cost*1e06, total_cost*1e07, total_cost*1e08, total_cost*1e09)


p1 = plt.plot(ind, bandwidth, marker="X")

plt.yscale('log')
plt.xscale('log')

plt.xlabel('Number of participants')
plt.ylabel('Traffic (TB sent)')
# plt.title('Total number of bytes sent by a client on average')
#plt.xticks(ind, ('1e6', '1e7','1e8', '1e9'))
plt.yticks([1e3, 1e4, 1e5, 1e6])

plt.savefig('../graphs/aggregator/aggregator_bandwidth.pdf', format='pdf')
