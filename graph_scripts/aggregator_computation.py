import numpy as np
import matplotlib.pyplot as plt

num_friends = 10
hours_to_finish_in = 10

addition = 25.92297887802124*4/1000

zkp = 0.643 + (num_friends*1.081)

total = (addition + zkp)/(3600*hours_to_finish_in)


N = 4

ind = [1e6, 1e7, 1e8, 1e9]

costs = (total*1e06, total*1e07, total*1e08, total*1e09)

p1 = plt.plot(ind, costs, marker="X")
plt.yscale('log')
plt.xscale('log')

plt.xlabel('Number of participants')
plt.ylabel('Computation (cores)')
# plt.title('Total number of bytes sent by a client on average')
plt.yticks([1e2, 1e3, 1e4, 1e5, 1e6, 1e7])

#plt.legend(['1-hop query', '2-hop query'])

plt.savefig('../graphs/aggregator/aggregator_computation.eps', format='eps')
