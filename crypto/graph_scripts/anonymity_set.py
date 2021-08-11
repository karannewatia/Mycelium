import numpy as np
import matplotlib.pyplot as plt
import math

k_vals = [2,3,4] #number of hops in the communication path
r = [1,2,3] #number of copies sent
c_vals = [ 0.01, 0.02, 0.04] #fractions of malicious users who collude with the aggregator
f = 0.1 #fraction of forwarders
n = 2**30 #number of users in the system

#equations for calculating the size of the anonymity set
def anon_set(c,r,f,k):
    t = (1-c)*r/f
    result = 0
    if k==2:
        result = ((1-c)**k) * (t**k) + (k*c*(1-c)) * (t**(k-1)) + (c**k) * (t**(k-2))
    if k == 3:
        result = ((1-c)**k) * (t**k) + ((k*c*(1-c))**(k-1)) * (t**(k-1)) + (k*(c**(k-1))*(1-c)) + (c**k)*(t**(k-3))
    if k == 4:
        result = ((1-c)**k) * (t**k) + ((k*c*(1-c))**(k-1)) * (t**(k-1)) + (k**2)*(c**(k-2))*((1-c)**(k-2)) + (k*(c**(k-1))*(1-c)) + (c**k)*(t**(k-4))
    return min(result, n)


font = {'size'   : 15}
plt.rc('font', **font)
plt.gcf().subplots_adjust(bottom=0.15)
plt.gcf().subplots_adjust(left=0.12)


plot_1 = [anon_set(0.01,2,f,k) for k in k_vals]
plot_2 = [anon_set(0.02,2,f,k) for k in k_vals]
plot_3 = [anon_set(0.04,2,f,k) for k in k_vals]

plot_4 = [anon_set(0.01,3,f,k) for k in k_vals]
plot_5 = [anon_set(0.02,3,f,k) for k in k_vals]
plot_6 = [anon_set(0.04,3,f,k) for k in k_vals]

plt.plot(k_vals, plot_1, '--', label = "mal=0.01, r=2",  marker="X", markersize=10, linewidth=5)
plt.plot(k_vals, plot_2, '--', label = "mal=0.02, r=2",  marker="X", markersize=10, linewidth=5)
plt.plot(k_vals, plot_3, '--', label = "mal=0.04, r=2", marker="X", markersize=10, linewidth=5)

plt.plot(k_vals, plot_4, label = "mal=0.01, r=3", marker="D", markersize=10, linewidth=5)
plt.plot(k_vals, plot_5, label = "mal=0.02, r=3", marker="D", markersize=10, linewidth=5)
plt.plot(k_vals, plot_6,  label = "mal=0.04, r=3", marker="D", markersize=10, linewidth=5)


plt.yscale('log')
plt.xticks([2,3,4])
plt.xlabel('Number of hops in the communication path', fontsize='large')
plt.ylabel('Size of the anonymity set', fontsize='large')
plt.legend(loc="best", prop={'size': 12})
plt.savefig('../graphs/users/Anonymity_set.pdf', format='pdf')
