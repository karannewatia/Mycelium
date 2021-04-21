import numpy as np
import matplotlib.pyplot as plt


#malice + churn
rho_vals = [0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05, 0.055, 0.06, 0.065, 0.07]

# from success_rate.py and success_data.txt
r1 = [0.9524999999999999, 0.9460000000000001, 0.9305, 0.9165000000000001, 0.899, 0.8960000000000001, 0.8725000000000002, 0.85, 0.8480000000000001, 0.8494999999999999, 0.8225, 0.805]
r2 = [0.9975000000000002, 0.9984999999999999, 0.9955, 0.9904999999999999, 0.9924999999999999, 0.9854999999999998, 0.9869999999999999, 0.9789999999999999, 0.9795000000000001, 0.9724999999999999, 0.9735000000000001, 0.962]
r3 = [1.0, 0.999, 0.9995, 1.0, 1.0, 0.9984999999999999, 0.9974999999999999, 0.9984999999999999, 0.9964999999999999, 0.9945, 0.9929999999999998, 0.9935]

plt.plot(rho_vals, r1, label = "r=1")
plt.plot(rho_vals, r2, label = "r=2")
plt.plot(rho_vals, r3, label = "r=3")

plt.xlabel('Node failure rate (malice + churn)')
plt.ylabel('Success rate')
# plt.title('Probability of success for 200 messages')
plt.legend()
plt.savefig('../graphs/users/Success_rate.eps', format='eps')
