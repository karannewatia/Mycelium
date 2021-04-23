import numpy as np
import matplotlib.pyplot as plt

num_friends = 10
hours_to_finish_in = 10

addition = 25.92297887802124*4/1000

zkp = 10 #TODO change this to actual verification time for the final upload zkp

add_frac = addition/(addition + zkp)
zkp_frac = zkp/(addition + zkp)

total = (addition + zkp)/(3600*hours_to_finish_in)


N = 4
width = 0.25

ind = [0,1,2,3]

cores = (total*1e06, total*1e07, total*1e08, total*1e09)

addition_cores = (cores[0]*add_frac, cores[1]*add_frac, cores[2]*add_frac, cores[3]*add_frac)
zkp_cores = (cores[0]*zkp_frac, cores[1]*zkp_frac, cores[2]*zkp_frac, cores[3]*zkp_frac)


p1 = plt.bar(ind, zkp_cores, width, color='tab:red')
p2 = plt.bar(ind, addition_cores, width, bottom=zkp_cores, color='tab:green')


plt.yscale('log')
plt.xticks(np.arange(4), ["$10^6$", "$10^7$", "$10^8$", "$10^9$"])
plt.yticks([1e2, 1e3, 1e4, 1e5, 1e6])
plt.xlabel('Number of participants')
plt.ylabel('Computation (cores)')

plt.legend((p1[0], p2[0]), ('ZKP verification', 'Global aggregation'))

plt.savefig('../graphs/aggregator/aggregator_computation.pdf', format='pdf')
