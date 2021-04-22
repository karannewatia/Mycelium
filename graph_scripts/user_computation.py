import numpy as np
import matplotlib.pyplot as plt

num_friends = 10


establish_keys = 0.098852 + 0.01961584 + 0.02060137 + 0.020653698 + 0.0169654
telescoping = num_friends * establish_keys
telescoping /= 60

send_encrypt = 0.314325 + 0.0967714 + 0.0915351 + 0.092841 + 0.0472378
forwarding = num_friends * send_encrypt

send_shift = 0.370311 + 0.179348 + 0.162397 + 0.137747 + 0.133751
forwarding += num_friends * send_shift
forwarding /= 60

encryption_zkp = 15.146
shift_zkp = 4.460 #change this
zkp = encryption_zkp + (shift_zkp * num_friends)
zkp /= 60

fhe = 14.493421077728271 + (20.33608603477478*num_friends) #encryption + shift
fhe += 275.0299119949341*num_friends #ciphertext mult
fhe /= 60

# print(telescoping + forwarding + zkp + fhe)


N = 3

telescoping_plt = (telescoping, telescoping*2, telescoping*3)
forwarding_plt = (forwarding, forwarding*2, forwarding*3)
zkp_plt = (zkp, zkp, zkp)
sums = (telescoping+forwarding, 2*(telescoping+forwarding),  3*(telescoping+forwarding))
fhe_plt = (fhe, fhe, fhe)
new_sums = (zkp+telescoping+forwarding, zkp+(2*(telescoping+forwarding)), zkp+(3*(telescoping+forwarding)))

ind = np.arange(N)
width = 0.15
p1 = plt.bar(ind, telescoping_plt, width, color='tab:blue')
p2 = plt.bar(ind, forwarding_plt, width, bottom=telescoping_plt, color='tab:orange')
p3 = plt.bar(ind, zkp_plt, width, bottom=sums, color='tab:green')
p4 = plt.bar(ind, fhe_plt, width, bottom=new_sums, color='tab:red')


plt.xlabel('Number of copies sent per message')
plt.ylabel('Computation time (min)')
# plt.title('Total number of bytes sent by a client on average')
plt.xticks(ind, ('1', '2','3'))
plt.yticks(np.arange(0, 70, 10))

plt.legend((p1[0], p2[0], p3[0], p4[0]), ('Telescoping', 'Message forwarding', 'ZKP', 'Crypto'))
plt.savefig('../graphs/users/user_computation.pdf', format='pdf')
