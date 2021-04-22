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

establish_keys_src = 3123
establish_keys_node1 = 5641
establish_keys_node2 = 3591
establish_keys_node3 = 1799
establish_keys_dst = 304

telescoping = num_friends*(establish_keys_src + establish_keys_node1 + establish_keys_node2 + establish_keys_node3 + establish_keys_dst)
telescoping = bytesto(telescoping, 'm')

encryption_src = 9542312
encryption_node1 = 9542248
encryption_node2 = 9542184
encryption_node3 = 9542120

forwarding = num_friends*(encryption_src + encryption_node1 + encryption_node2 + encryption_node3)

shift_src = 14470616
shift_node1 = 14470552
shift_node2 = 14470488
shift_node3 = 14470424

forwarding += num_friends*(shift_src + shift_node1 + shift_node2 + shift_node3)
forwarding = bytesto(forwarding, 'm')

final_upload = prime_bitsize * degree * 2 / 8 #add size of the multiplication proof here
final_upload  = bytesto(final_upload , 'm')

#total_cost = round(telescoping + forwarding + final_upload)

#print(bytesto(total_cost, 'm'))


N = 3

telescoping_plt = (telescoping, telescoping*2, telescoping*3)
forwarding_plt = (forwarding, forwarding*2, forwarding*3)
final_upload_plt = (final_upload, final_upload, final_upload)
sums = (telescoping+forwarding, 2*(telescoping+forwarding),  3*(telescoping+forwarding))

ind = np.arange(N)
width = 0.25
p1 = plt.bar(ind, telescoping_plt, width, color='tab:blue')
p2 = plt.bar(ind, forwarding_plt, width, bottom=telescoping_plt, color='tab:orange')
p3 = plt.bar(ind, final_upload_plt, width, bottom=sums, color='tab:green')


plt.xlabel('Number of copies sent per message')
plt.ylabel('Traffic (MB sent)')
# plt.title('Total number of bytes sent by a client on average')
plt.xticks(ind, ('1', '2','3'))
plt.yticks(np.arange(0, 3500, 500))

plt.legend((p1[0], p2[0], p3[0]), ('Telescoping', 'Message forwarding', 'Final upload'))
plt.savefig('../graphs/users/user_bandwidth.eps', format='eps')
