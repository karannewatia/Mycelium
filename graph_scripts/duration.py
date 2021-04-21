import numpy as np
import matplotlib.pyplot as plt

N = 3
hops = [2,3,4]
# if number of hops = k, telescoping takes k^2 + k C-rounds,
# and message forwarding takes 2k C-rounds (for 1-hop queries)
telescoping = (2**2 + 2, 3**2 + 3, 4**2 + 4)
message_forwarding_1hop = (2*2, 2*3, 2*4)
message_forwarding_2hops = (4*2, 4*3, 4*4)
ind = np.arange(N)
width = 0.35
p1 = plt.bar(ind, telescoping, width, color='tab:blue')
p2 = plt.bar(ind, message_forwarding_1hop, width, bottom=telescoping, color='tab:orange')
p3 = plt.bar(ind + width, telescoping, width, color='tab:blue')
p4 = plt.bar(ind + width, message_forwarding_2hops, width, bottom=telescoping, color='tab:green')
plt.xlabel('Number of hops in the communication path')
plt.ylabel('Duration of the query (in hours)')
# plt.title('Duration of queries if C-rounds are 1 hour long')
plt.xticks(ind+width/2, ('2', '3', '4'))
axes = plt.gca()
axes.set_ylim([0,40])
plt.legend((p1[0], p2[0], p4[0]), ('Telescoping (same for 1-hop and 2-hop queries)', 'Message forwarding (1-hop query)', 'Message forwarding (2-hop query)'))
plt.savefig('../graphs/users/Duration.eps', format='eps')
