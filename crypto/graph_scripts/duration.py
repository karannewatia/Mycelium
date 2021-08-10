import numpy as np
import matplotlib.pyplot as plt

N = 3
hops = [2,3,4]

# if number of hops = k, telescoping takes k^2+k C-rounds,
# and message forwarding takes 2k C-rounds (for 1-hop queries)
telescoping = (2**2 + 2, 3**2 + 3, 4**2 + 4)
message_forwarding_1hop = (2*2, 2*3, 2*4)

font = {'size'   : 17}
plt.rc('font', **font)
plt.gcf().subplots_adjust(bottom=0.15)

ind = np.arange(N)
width = 0.2
p1 = plt.bar(ind, telescoping, width, color='tab:orange', edgecolor="black")
p2 = plt.bar(ind, message_forwarding_1hop, width, bottom=telescoping, color='tab:purple', edgecolor="black")
plt.xlabel('Number of hops in the communication path', fontsize='large')
plt.ylabel('Number of C-rounds', fontsize='large')
plt.xticks(ind, ('2', '3', '4'))
plt.yticks(np.arange(0, 35, 5))
plt.legend((p1[0], p2[0]), ('Telescoping', 'Message forwarding'))
plt.savefig('../graphs/users/Duration.pdf', format='pdf')
