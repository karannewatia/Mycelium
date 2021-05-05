import numpy as np
import matplotlib.pyplot as plt

N = 3

decryption = (84/60, 180/60, 382/60)

# resharing = (1/60, 1/60, 1/60, /60)
font = {'size'   : 17}
plt.rc('font', **font)
plt.gcf().subplots_adjust(bottom=0.25)

ind = np.arange(N)
width = 0.15
p1 = plt.bar(ind, decryption, width, color='tab:blue', edgecolor="black")
# p2 = plt.bar(ind, resharing, width, bottom=decryption, color='tab:orange')

plt.xlabel('Size of the committee\n(b)', fontsize='large')
plt.ylabel('Computation time (min)', fontsize='large')
# plt.title('MPC computation')
plt.xticks(ind, ('5', '10', '15'))

# plt.legend((p1[0], p2[0]), ('Decryption', 'Re-sharing'))
plt.savefig('../graphs/committee/mpc_computation.pdf', format='pdf')
