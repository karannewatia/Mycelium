import matplotlib.pyplot as plt
import numpy as np
import math

def graph_a(f, C, m):
    p = math.exp(-f*C)
    p *= (5*math.e*f/2)**(2*C/5)
    return min(2*p*m, 1)

def graph_b(fg, C):
    p = math.exp(-(fg)*C)
    p *= (5*math.e*(fg))**(C/5)
    return p


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
    result = graph_a(i/100, 5, 1)
    graph_a_1.append(result)
    result = graph_a(i/100, 10, 1)
    graph_a_2.append(result)
    result = graph_a(i/100, 15, 1)
    graph_a_3.append(result)

plt.plot(byzantine_rates, graph_a_1, marker="X", markersize=15, linewidth=5)
plt.plot(byzantine_rates, graph_a_2, marker="X", markersize=15, linewidth=5)
plt.plot(byzantine_rates, graph_a_3, marker="X", markersize=15, linewidth=5)
plt.ylabel('Probability of privacy failure', fontsize='large')
plt.xlabel('% of malicious users\n(a)', fontsize='large')
plt.yscale('log')

# plt.title('Probability of the MPC failing (committee size 10)')
plt.legend(["C = 5", "C = 10", "C = 15"])
plt.xticks(byzantine_rates, ('0.5', '1', '2', '4'))
plt.savefig('../graphs/committee/mpc_failure_rate.pdf', format='pdf')



graph_b_1 = []
graph_b_2 = []
graph_b_3 = []
x_vals = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07]
for i in x_vals:
    result = graph_b(i, 5)
    graph_b_1.append(1 - result)
    result = graph_b(i, 10)
    graph_b_2.append(1 - result)
    result = graph_b(i, 15)
    graph_b_3.append(1 - result)


plt.plot(x_vals, graph_b_1, marker="X", markersize=15, linewidth=5)
plt.plot(x_vals, graph_b_2, marker="X", markersize=15, linewidth=5)
plt.plot(x_vals, graph_b_3, marker="X", markersize=15, linewidth=5)
#
plt.ylabel('Probability of liveness', fontsize='large')
plt.xlabel('% malice + churn\n(b)', fontsize='large')
plt.title('Query succes rate with malice + churn (committee size 10)')
plt.legend(["C = 5", "C = 10", "C = 15"])
plt.xticks(x_vals, ('1', '2', '3', '4', '5', '6', '7'))
#
plt.savefig('../graphs/committee/mpc_success_rate.pdf', format='pdf')
