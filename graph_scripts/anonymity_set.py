import numpy as np
import matplotlib.pyplot as plt
import math

r = 3 #number of copies sent
n = 1e09 #number of users
k_vals = [2,3,4] #number of hops in the communication path
f_vals = [0.0025, 0.005, 0.01, 0.015, 0.02, 0.025] #fractions of malicious users who collude with the aggregator

#size of the anonymity set = (r/f)**k

plot_1 = [int((r/f_vals[0])**k) for k in k_vals]
plot_2 = [int((r/f_vals[1])**k) for k in k_vals]
plot_3 = [int((r/f_vals[2])**k) for k in k_vals]
plot_4 = [int((r/f_vals[3])**k) for k in k_vals]
plot_5 = [int((r/f_vals[4])**k) for k in k_vals]
plot_6 = [int((r/f_vals[5])**k) for k in k_vals]

plt.plot(k_vals, plot_1, label = "f=0.0025")
plt.plot(k_vals, plot_2, label = "f=0.005")
plt.plot(k_vals, plot_3, label = "f=0.01")
plt.plot(k_vals, plot_4, label = "f=0.015")
plt.plot(k_vals, plot_5, label = "f=0.02")
plt.plot(k_vals, plot_6, label = "f=0.025")

plt.yscale('log')
plt.xticks([2,3,4])

plt.xlabel('Number of hops in the communication path')
plt.ylabel('Size of the anonymity set')
plt.title('Size of the anonymity set (with r=3)')
plt.legend()
plt.savefig('../graphs/users/Anonymity_set.eps', format='eps')
