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
telescoping = bytesto(telescoping, 'm')

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
forwarding = bytesto(forwarding, 'm')

final_upload = prime_bitsize * degree * 2 / 8 #add size of the multiplication proof here
final_upload  = bytesto(final_upload , 'm')

#total_cost = round(telescoping + forwarding + final_upload)

#print(bytesto(total_cost, 'm'))

N = 2

telescoping_plt = (telescoping, telescoping)
forwarding_plt = (forwarding, 2*forwarding)
final_upload_plt = (final_upload, final_upload)
sums = (telescoping+forwarding, telescoping+2*forwarding)

ind = np.arange(N)
width = 0.25
p1 = plt.bar(ind, telescoping_plt, width, color='tab:blue')
p2 = plt.bar(ind, forwarding_plt, width, bottom=telescoping_plt, color='tab:orange')
p3 = plt.bar(ind, final_upload_plt, width, bottom=sums, color='tab:green')


plt.xlabel('Number of hops in the query')
plt.ylabel('Traffic (MB sent)')
# plt.title('Total number of bytes sent by a client on average')
plt.xticks(ind, ('1', '2'))

plt.legend((p1[0], p2[0], p3[0]), ('Telescoping', 'Message forwarding', 'Final upload'))
plt.savefig('../graphs/users/User_bandwidth.eps', format='eps')
