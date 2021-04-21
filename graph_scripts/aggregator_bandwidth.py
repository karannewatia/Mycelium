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

establish_keys_src = 3123
establish_keys_node1 = 5641
establish_keys_node2 = 3591
establish_keys_node3 = 1799
establish_keys_dst = 304

telescoping = num_copies*num_friends*(establish_keys_src + establish_keys_node1 + establish_keys_node2 + establish_keys_node3 + establish_keys_dst)

encryption_src = 8388872
encryption_node1 = 16777681/2
encryption_node2 = 16777553/2
encryption_node3 = 16777425/2
encryption_dst = 0

forwarding = num_copies*num_friends*(encryption_src + encryption_node1 + encryption_node2 + encryption_node3 + encryption_dst)

shift_src = 13317176
shift_node1 = 26634289/2
shift_node2 = 26634161/2
shift_node3 = 26634033/2
shift_dst = 0

forwarding += num_copies*num_friends*(shift_src + shift_node1 + shift_node2 + shift_node3 + shift_dst)

final_upload = prime_bitsize * degree * 2 / 8 #add size of the multiplication proof here


total_cost = round(telescoping + forwarding + final_upload)
total_cost = bytesto(total_cost, 't')

total_cost2 = round(telescoping + 2*forwarding + final_upload)
total_cost2 = bytesto(total_cost2, 't')
# print(total_cost)


N = 4


ind = np.arange(N)
width = 0.25

bandwidth = (total_cost*1e06, total_cost*1e07, total_cost*1e08, total_cost*1e09)
bandwidth2 = (total_cost2*1e06, total_cost2*1e07, total_cost2*1e08, total_cost2*1e09)

p1 = plt.plot(ind, bandwidth, marker="X")
p2 = plt.plot(ind, bandwidth2, marker="X")
plt.yscale('log')

plt.xlabel('Number of participants')
plt.ylabel('Traffic (TB sent)')
# plt.title('Total number of bytes sent by a client on average')
plt.xticks(ind, ('1e6', '1e7','1e8', '1e9'))
plt.yticks([1e3, 1e4, 1e5, 1e6, 1e7])

plt.legend(['1-hop query', '2-hop query'])

plt.savefig('../graphs/aggregator/aggregator_bandwidth.eps', format='eps')
