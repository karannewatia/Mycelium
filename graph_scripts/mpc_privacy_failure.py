import matplotlib.pyplot as plt
import math

plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

#f is the malice rate
#C is the size of the Committee
def privacy_failure(f, C):
    p = math.exp(-f*C)
    p *= (5*math.e*f/2)**(2*C/5)
    return min(2*p, 1)

font = {'size'   : 17}
plt.rc('font', **font)
plt.gcf().subplots_adjust(bottom=0.25)
plt.gcf().subplots_adjust(left=0.20)

graph_a_1 = []
graph_a_2 = []
graph_a_3 = []

byzantine_rates = []
for i in [0.5,1,2,4]:
   byzantine_rates.append(i)
   result = privacy_failure(i/100, 5)
   graph_a_1.append(result)
   result = privacy_failure(i/100, 10)
   graph_a_2.append(result)
   result = privacy_failure(i/100, 15)
   graph_a_3.append(result)

plt.plot(byzantine_rates, graph_a_1, marker="X", markersize=15, linewidth=5)
plt.plot(byzantine_rates, graph_a_2, marker="X", markersize=15, linewidth=5)
plt.plot(byzantine_rates, graph_a_3, marker="X", markersize=15, linewidth=5)
plt.ylabel('Probability of privacy failure', fontsize='large')
plt.xlabel('% of malicious users\n(a)', fontsize='large')
plt.yscale('log')
plt.legend(["C = 5", "C = 10", "C = 15"])
plt.xticks(byzantine_rates, ('0.5', '1', '2', '4'))
plt.savefig('../new_graphs/MPC_privacy_failure.pdf', format='pdf')
