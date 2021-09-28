import matplotlib.pyplot as plt
import math

plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

#fg is the malice+churn rate
#C is the size of the committee
def liveness(fg, C):
    p = math.exp(-(fg)*C)
    p *= (5*math.e*(fg))**(C/5)
    return p

font = {'size'   : 17}
plt.rc('font', **font)
plt.gcf().subplots_adjust(bottom=0.25)
plt.gcf().subplots_adjust(left=0.20)

graph_b_1 = []
graph_b_2 = []
graph_b_3 = []
x_vals = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07]
for i in x_vals:
    result = liveness(i, 5)
    graph_b_1.append(1 - result)
    result = liveness(i, 10)
    graph_b_2.append(1 - result)
    result = liveness(i, 15)
    graph_b_3.append(1 - result)

plt.plot(x_vals, graph_b_1, marker="X", markersize=15, linewidth=5)
plt.plot(x_vals, graph_b_2, marker="X", markersize=15, linewidth=5)
plt.plot(x_vals, graph_b_3, marker="X", markersize=15, linewidth=5)
plt.ylabel('Probability of liveness', fontsize='large')
plt.xlabel('% malice + churn\n(b)', fontsize='large')
plt.legend(["C = 5", "C = 10", "C = 15"])
plt.xticks(x_vals, ('1', '2', '3', '4', '5', '6', '7'))
plt.savefig('../new_graphs/MPC_liveness.pdf', format='pdf')
