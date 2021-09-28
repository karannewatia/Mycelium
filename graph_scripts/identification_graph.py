import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42


malice_vals = [0.005, 0.01, 0.02, 0.04]
ind = np.arange(4)


#replace these with the data obtained from identification.py
k2r1 = [0.0, 0.0, 0.0008000000000000229, 0.0015999999999999348]
k2r2 = [0.0, 0.0, 0.0008000000000000229, 0.0033000000000004137]
k2r3 = [0.0, 0.000200000000000089, 0.001200000000000201, 0.0049000000000002375]
k3r1 = [0.0, 0.0, 0.0, 0.0]
k3r2 = [0.0, 0.0, 0.0, 9.999999999987796e-05]
k3r3 = [0.0, 0.0, 0.0, 0.000200000000000089]

font = {'size'   : 17}
plt.rc('font', **font)
plt.gcf().subplots_adjust(bottom=0.15)
plt.gcf().subplots_adjust(left=0.20)

plt.plot(ind, k2r1, label = "k=2,r=1", marker="X", markersize=10, linewidth=5)
plt.plot(ind, k2r2, label = "k=2,r=2", marker="X", markersize=10, linewidth=5)
plt.plot(ind, k2r3, label = "k=2,r=3", marker="X", markersize=10, linewidth=5)

plt.plot(ind, k3r1, label = "k=3,r=1", marker="X", markersize=10, linewidth=5)
plt.plot(ind, k3r2, label = "k=3,r=2", marker="X", markersize=10, linewidth=5)
plt.plot(ind, k3r3, label = "k=3,r=3", marker="X", markersize=10, linewidth=5)

plt.xticks(ind, ('0.5', '1', '2', '4'))
plt.xlabel('Malice rate (%)', fontsize='large')
plt.ylabel('Probability of identification', fontsize='large')
plt.legend()
plt.savefig('../new_graphs/Identification.pdf', format='pdf')
