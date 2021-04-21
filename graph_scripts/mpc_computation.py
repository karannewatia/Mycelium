import numpy as np
import matplotlib.pyplot as plt

N = 4

decryption = (369/60, 788/60, 1450/60, 2304/60)

# resharing = (1/60, 1/60, 1/60, /60)

ind = np.arange(N)
width = 0.25
p1 = plt.bar(ind, decryption, width, color='tab:blue')
# p2 = plt.bar(ind, resharing, width, bottom=decryption, color='tab:orange')

plt.xlabel('Size of the committee')
plt.ylabel('Computation time (min)')
# plt.title('MPC computation')
plt.xticks(ind, ('5', '10', '15', '20'))

# plt.legend((p1[0], p2[0]), ('Decryption', 'Re-sharing'))
plt.savefig('../graphs/committee/mpc_computation.eps', format='eps')
