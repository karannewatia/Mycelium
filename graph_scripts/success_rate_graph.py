import numpy as np
import matplotlib.pyplot as plt


#malice + churn
rho_vals = [0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05, 0.055, 0.06, 0.065, 0.07]

# from success_rate.py and success_data.txt
r1 = [0.9490000000000001, 0.9390000000000001, 0.93, 0.905, 0.8969999999999999, 0.893, 0.866, 0.8550000000000001, 0.843, 0.8459999999999999, 0.836, 0.804]
r2 = [0.998, 0.994, 0.994, 0.992, 0.986, 0.992, 0.985, 0.976, 0.9710000000000001, 0.9709999999999999, 0.97, 0.9559999999999998]
r3 = [1.0, 1.0, 1.0, 1.0, 0.999, 0.998, 0.998, 0.998, 0.998, 0.9940000000000001, 0.9940000000000001, 0.994]

plt.plot(rho_vals, r1, label = "r=1")
plt.plot(rho_vals, r2, label = "r=2")
plt.plot(rho_vals, r3, label = "r=3")

plt.xlabel('Node failure rate (malice + churn) (%)')
plt.ylabel('Success rate (%)')
plt.title('Probability of success for 200 messages')
plt.legend()
plt.savefig('../graphs/users/Success_rate.eps', format='eps')
