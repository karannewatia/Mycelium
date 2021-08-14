import matplotlib.pyplot as plt


#malice + churn rate
rho_vals = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09]

#replace these with the data obtained from goodput.py
r1 = [0.975, 0.9349999999999999, 0.916, 0.893, 0.86, 0.8379999999999999, 0.7859999999999999, 0.765, 0.74]
r2 = [1.0, 0.999, 0.9940000000000001, 0.9870000000000001, 0.9770000000000001, 0.966, 0.961, 0.9530000000000001, 0.9399999999999998]
r3 = [1.0, 1.0, 0.999, 1.0, 0.9950000000000001, 0.992, 0.992, 0.986, 0.9850000000000001]

font = {'size'   : 17}
plt.rc('font', **font)
plt.gcf().subplots_adjust(bottom=0.15)
plt.gcf().subplots_adjust(left=0.15)

plt.plot(rho_vals, r1, label = "r=1", marker="X", markersize=15, linewidth=5)
plt.plot(rho_vals, r2, label = "r=2", marker="X", markersize=15, linewidth=5)
plt.plot(rho_vals, r3, label = "r=3", marker="X", markersize=15, linewidth=5)
plt.xlabel('Node failure rate (malice + churn) (%)', fontsize='large')
plt.ylabel('Message success rate', fontsize='large')
plt.xticks(rho_vals, ('1', '2', '3', '4', '5', '6', '7', '8', '9'))
plt.legend()
plt.savefig('../new_graphs/Goodput.pdf', format='pdf')
