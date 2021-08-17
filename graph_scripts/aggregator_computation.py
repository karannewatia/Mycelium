import numpy as np
import matplotlib.pyplot as plt

hours_to_finish_in = 10

#time for adding two size-2 ciphertexts (in seconds) on 4 cores is 0.02592297887802124
#So, to get the time to add two size-12 ciphertexts on 1 core,
#we multiply the time by 4 and then by 6.
#See the Mycelium/crypto/code/python_version folder for instructions on how to obtain crypto costs
addition = 0.02592297887802124 * 4 * 6

#time to verify the enc proof + time to verify the mult proof (in seconds)
#See the Mycelium/zkp folder for instructions on how to obtain ZKP costs
zkp = 0.010 + 4.532

add_frac = addition/(addition + zkp)
zkp_frac = zkp/(addition + zkp)

#the last minute will be used to perform the relinearization
total = (addition + zkp)/((3600*hours_to_finish_in)-60) #convert to hours

#time to perform the relin on 4 cores (in seconds) is 2324.
#So, to get the number of cores needed to finish the relin in one minute,
#we multiply the time by 4 and divide by 60.
relin_cores = 2324 * 4 / 60

font = {'size'   : 17}
plt.rc('font', **font)
plt.gcf().subplots_adjust(bottom=0.25)
plt.gcf().subplots_adjust(left=0.15)

N = 4
width = 0.25
ind = [0,1,2,3]

cores = [total*1e06, total*1e07, total*1e08, total*1e09]
#aggregation involves summing up all the ciphertexts and then performing the relinearization
aggregation_cores = ((cores[0]*add_frac)+relin_cores, (cores[1]*add_frac)+relin_cores, (cores[2]*add_frac)+relin_cores, (cores[3]*add_frac)+relin_cores)
zkp_cores = (cores[0]*zkp_frac, cores[1]*zkp_frac, cores[2]*zkp_frac, cores[3]*zkp_frac)

p1 = plt.bar(ind, zkp_cores, width, color='tab:red')
p2 = plt.bar(ind, aggregation_cores, width, bottom=zkp_cores, color='tab:green')
plt.yscale('log')
plt.xticks(np.arange(4), ["$10^6$", "$10^7$", "$10^8$", "$10^9$"])
plt.yticks([1e2, 1e3, 1e4, 1e5, 1e6])
plt.xlabel('Number of participants\n(b)', fontsize='large')
plt.ylabel('Computation (cores)', fontsize='large')
plt.legend((p1[0], p2[0]), ('ZKP verification', 'Global aggregation'))
plt.savefig('../new_graphs/Aggregator_computation.pdf', format='pdf')
