import numpy as np
import matplotlib.pyplot as plt


#malice + churn
rho_vals = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09]

# from success_rate.py and success_data.txt
r1 = [0.975, 0.9349999999999999, 0.916, 0.893, 0.86, 0.8379999999999999, 0.7859999999999999, 0.765, 0.74]
r2 = [1.0, 0.999, 0.9940000000000001, 0.9870000000000001, 0.9770000000000001, 0.966, 0.961, 0.9530000000000001, 0.9399999999999998]
r3 = [1.0, 1.0, 0.999, 1.0, 0.9950000000000001, 0.992, 0.992, 0.986, 0.9850000000000001]

plt.plot(rho_vals, r1, label = "r=1")
plt.plot(rho_vals, r2, label = "r=2")
plt.plot(rho_vals, r3, label = "r=3")

plt.xlabel('Node failure rate (malice + churn)')
plt.ylabel('Message success rate')
# plt.title('Probability of success for 200 messages')
plt.legend()
plt.savefig('../graphs/users/Success_rate.pdf', format='pdf')
