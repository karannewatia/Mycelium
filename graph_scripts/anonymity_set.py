import numpy as np
import matplotlib.pyplot as plt
import math

r = [2,3] #number of copies sent
n = 1e09 #number of users
k_vals = [2,3,4] #number of hops in the communication path
f_vals = [0.005, 0.01, 0.02, 0.04] #fractions of malicious users who collude with the aggregator

#size of the anonymity set = (r/f)**k

plot_1 = [int((r[0]/f_vals[0])**k) for k in k_vals]
plot_2 = [int((r[0]/f_vals[1])**k) for k in k_vals]
plot_3 = [int((r[0]/f_vals[2])**k) for k in k_vals]
plot_4 = [int((r[0]/f_vals[3])**k) for k in k_vals]

plot_5 = [int((r[1]/f_vals[0])**k) for k in k_vals]
plot_6 = [int((r[1]/f_vals[1])**k) for k in k_vals]
plot_7 = [int((r[1]/f_vals[2])**k) for k in k_vals]
plot_8 = [int((r[1]/f_vals[3])**k) for k in k_vals]


plt.plot(k_vals, plot_1, '--', label = "f=0.005, r=2", color='tab:blue', marker="X")
plt.plot(k_vals, plot_2, '--', label = "f=0.01, r=2", color='tab:orange', marker="X")
plt.plot(k_vals, plot_3, '--', label = "f=0.02, r=2", color='tab:green', marker="X")
plt.plot(k_vals, plot_4, '--', label = "f=0.04, r=2", color='tab:red', marker="X")

plt.plot(k_vals, plot_5, label = "f=0.005, r=3", color='tab:blue', marker="X")
plt.plot(k_vals, plot_6, label = "f=0.01, r=3", color='tab:orange', marker="X")
plt.plot(k_vals, plot_7, label = "f=0.02, r=3", color='tab:green', marker="X")
plt.plot(k_vals, plot_8, label = "f=0.04, r=3", color='tab:red', marker="X")

plt.yscale('log')
plt.xticks([2,3,4])

plt.xlabel('Number of hops in the communication path')
plt.ylabel('Size of the anonymity set')
#plt.title('Size of the anonymity set')
plt.legend()

plt.savefig('../graphs/users/Anonymity_set.pdf', format='pdf')
