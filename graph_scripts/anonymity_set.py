import numpy as np
import matplotlib.pyplot as plt
import math

k_vals = [2,3,4] #number of hops in the communication path
r = [1,2,3] #number of copies sent
c_vals = [0.005, 0.01, 0.02, 0.04] #fractions of malicious users who collude with the aggregator
f = 0.1

n = 2**30

def intersect(set_size, num_mal, r):
    return 1
    #q = 1-1/(r*n) #prob of any one message being selected
    #if num_mal == 2:
    #    res = (r*n)*(1-2*q**set_size+2**(2*set_size))
    #else:
    #    res = 1 #TODO: CHANGE!
    #
    #print('Intersect is %d' % res)
    #return res

    
def anon_set(c,r,f,k):
    t = (1-c)*r/f
    print('t is %d' % t)
    result = 0
    if k==2:
        result = ((1-c)**k) * (t**k) + (k*c*(1-c)) * (t**(k-1)) + (c**k) * (t**(k-2))
    if k == 3:
        result = ((1-c)**k) * (t**k) + ((k*c*(1-c))**(k-1)) * (t**(k-1)) + (k*(c**(k-1))*(1-c)*(intersect(t**2, 2,  r))) + (c**k)*(t**(k-3))
    if k == 4:
        result = ((1-c)**k) * (t**k) + ((k*c*(1-c))**(k-1)) * (t**(k-1)) + (k**2)*(c**(k-2))*((1-c)**(k-2))*(intersect(t**3, 2, r)) + (k*(c**(k-1))*(1-c)*(intersect(t**3,3, r))) + (c**k)*(t**(k-4))

    return min(result, 1e9)



# print(anon_set(0.01,2,0.01,4))

plot_1 = [anon_set(0.005,2,f,k) for k in k_vals]
plot_2 = [anon_set(0.01,2,f,k) for k in k_vals]
plot_3 = [anon_set(0.02,2,f,k) for k in k_vals]
plot_4 = [anon_set(0.04,2,f,k) for k in k_vals]

plot_5 = [anon_set(0.005,3,f,k) for k in k_vals]
plot_6 = [anon_set(0.01,3,f,k) for k in k_vals]
plot_7 = [anon_set(0.02,3,f,k) for k in k_vals]
plot_8 = [anon_set(0.04,3,f,k) for k in k_vals]


plt.plot(k_vals, plot_1, '--', label = "malicious=0.005, r=2", color='tab:blue', marker="X")
plt.plot(k_vals, plot_2, '--', label = "malicious=0.01, r=2", color='tab:orange', marker="X")
plt.plot(k_vals, plot_3, '--', label = "malicious=0.02, r=2", color='tab:green', marker="X")
plt.plot(k_vals, plot_4, '--', label = "malicious=0.04, r=2", color='tab:red', marker="X")

plt.plot(k_vals, plot_5, label = "malicious=0.005, r=3", color='tab:blue', marker="D")
plt.plot(k_vals, plot_6, label = "malicious=0.01, r=3", color='tab:orange', marker="D")
plt.plot(k_vals, plot_7, label = "malicious=0.02, r=3", color='tab:green', marker="D")
plt.plot(k_vals, plot_8,  label = "malicious=0.04, r=3", color='tab:red', marker="D")


plt.yscale('log')
plt.xticks([2,3,4])

plt.xlabel('Number of hops in the communication path', fontsize='large')
plt.ylabel('Size of the anonymity set', fontsize='large')
#plt.title('Size of the anonymity set')
plt.legend()

plt.savefig('../graphs/users/Anonymity_set.pdf', format='pdf')
