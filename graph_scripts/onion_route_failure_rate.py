import numpy as np
import matplotlib.pyplot as plt


malice_vals = [0.005, 0.01, 0.02, 0.04]
ind = np.arange(4)

k2r1 = [1-x for x in [1.0, 1.0, 0.9992, 0.9984000000000001]]
k2r2 = [1-x for x in [1.0, 1.0, 0.9992, 0.9966999999999996]]
k2r3 = [1-x for x in [1.0, 0.9997999999999999, 0.9987999999999998, 0.9950999999999998]]

k3r1 = [1-x for x in [1.0, 1.0, 1.0, 1.0]]
k3r2 = [1-x for x in [1.0, 1.0, 1.0, 0.9999000000000001]]
k3r3 = [1-x for x in [1.0, 1.0, 1.0, 0.9997999999999999]]

k4r1 = [1-x for x in [1.0, 1.0, 1.0, 1.0]]
k4r2 = [1-x for x in [1.0, 1.0, 1.0, 1.0]]
k4r3 = [1-x for x in [1.0, 1.0, 1.0, 0.9999000000000001]]


plt.plot(ind, k2r1, label = "k=2,r=1", marker="X")
plt.plot(ind, k2r2, label = "k=2,r=2", marker="X")
plt.plot(ind, k2r3, label = "k=2,r=3", marker="X")

plt.plot(ind, k3r1, label = "k=3,r=1", marker="X")
plt.plot(ind, k3r2, label = "k=3,r=2", marker="X")
plt.plot(ind, k3r3, label = "k=3,r=3", marker="X")

plt.plot(ind, k4r1, label = "k=4,r=1", marker="X")
plt.plot(ind, k4r2, label = "k=4,r=2", marker="X")
plt.plot(ind, k4r3, label = "k=4,r=3", marker="X")


plt.xticks(ind, ('0.005', '0.01', '0.02', '0.04'))
plt.xlabel('Malice rate', fontsize='large')
plt.ylabel('Probability of being completely identified', fontsize='large')

plt.legend()
plt.savefig('../graphs/users/anonymity_failure_rate.pdf', format='pdf')
