import numpy as np
import matplotlib.pyplot as plt

def bytesto(bytes, to, bsize=1024):
    """convert bytes to megabytes, etc.
       sample code:
           print('mb= ' + str(bytesto(314575262000000, 'm')))
       sample output:
           mb= 300002347.946
    """

    a = {'k' : 1, 'm': 2, 'g' : 3, 't' : 4, 'p' : 5, 'e' : 6 }
    r = float(bytes)
    for i in range(a[to]):
        r = r / bsize
    return(r)

num_friends = 10
degree = 32768
prime_bitsize = 550

ct_size = bytesto(degree * prime_bitsize * 2 / 8, 'm')
enc_proof_size = 4.6
shift_proof_size = 12


telescoping_lst = [0,0,0]
forwarding_lst = [0,0,0]

################ 2 hops #####################
establish_keys = 0.076233 + 0.019769073 + 0.020225769 + 0.0201244
telescoping = num_friends * establish_keys
telescoping /= 60
telescoping_lst[0] = telescoping

send_encrypt = 0.034193 + 0.01483 + 0.0157621 + 0.00722612
forwarding = num_friends * send_encrypt * ct_size

send_shift = 0.034193 + 0.01483 + 0.0157621 + 0.00722612
forwarding += num_friends * send_shift * ct_size
forwarding /= 60
forwarding_lst[0] = forwarding
##########################################

############### 3 hops #######################
establish_keys = 0.098852 + 0.01961584 + 0.02060137 + 0.020653698 + 0.0169654
telescoping = num_friends * establish_keys
telescoping /= 60
telescoping_lst[1] = telescoping

send_encrypt = 0.042593 + 0.0147645 + 0.0150112 + 0.0159831 + 0.00906639
forwarding = num_friends * send_encrypt * ct_size

send_shift = 0.042593 + 0.0147645 + 0.0150112 + 0.0159831 + 0.00906639
forwarding += num_friends * send_shift * ct_size
forwarding /= 60
forwarding_lst[1] = forwarding
############################################

################### 4 hops ######################
establish_keys = 0.127917 + 0.019280258 + 0.020574946 + 0.020783 + 0.019399376 + 0.017891
telescoping = num_friends * establish_keys
telescoping /= 60
telescoping_lst[2] = telescoping

send_encrypt = 0.047799 + 0.0155274 + 0.0157811 + 0.0157041 + 0.0147972 + 0.00981608
forwarding = num_friends * send_encrypt * ct_size

send_shift = 0.047799 + 0.0155274 + 0.0157811 + 0.0157041 + 0.0147972 + 0.00981608
forwarding += num_friends * send_shift * ct_size
forwarding /= 60
forwarding_lst[2] = forwarding
##################################################

encryption_zkp = 15.146
shift_zkp = 4.460 #TODO change shift proof generation time and add time for final upload proof
final_upload_zkp = 72
zkp = encryption_zkp + (shift_zkp * num_friends) + final_upload_zkp
zkp /= 60

fhe = 14.493421077728271 + (20.33608603477478*num_friends) #encryption + shift
fhe += 275.0299119949341*num_friends #ciphertext mult
fhe /= 60

# print(telescoping + forwarding + zkp + fhe)


N = 3

telescoping_plt = [telescoping_lst[0], telescoping_lst[1], telescoping_lst[2]]
forwarding_plt = [forwarding_lst[0], forwarding_lst[1], forwarding_lst[2]]
zkp_plt = [zkp, zkp, zkp]
sums = [telescoping_lst[0]+forwarding_lst[0], telescoping_lst[1]+forwarding_lst[1],  telescoping_lst[2]+forwarding_lst[2]]
fhe_plt = [fhe, fhe, fhe]
new_sums = [zkp+telescoping_lst[0]+forwarding_lst[0], zkp+telescoping_lst[1]+forwarding_lst[1], zkp+telescoping_lst[2]+forwarding_lst[2]]
new_sums2 = [zkp+2*(telescoping_lst[0]+forwarding_lst[0]), zkp+2*(telescoping_lst[1]+forwarding_lst[1]), zkp+2*(telescoping_lst[2]+forwarding_lst[2])]
new_sums3 = [zkp+3*(telescoping_lst[0]+forwarding_lst[0]), zkp+3*(telescoping_lst[1]+forwarding_lst[1]), zkp+3*(telescoping_lst[2]+forwarding_lst[2])]

ind = np.arange(N)
width = 0.2

p1 = plt.bar(ind+width, [2*x for x in telescoping_plt], width, color='tab:brown', edgecolor="black")
p2 = plt.bar(ind+width, [2*x for x in forwarding_plt], width, bottom=[2*x for x in telescoping_plt], color='tab:blue', edgecolor="black")
p3 = plt.bar(ind+width, zkp_plt, width, bottom=[2*x for x in sums], color='tab:red', edgecolor="black")
p4 = plt.bar(ind+width, fhe_plt, width, bottom=new_sums2, color='tab:green', edgecolor="black")

# p1 = plt.bar(ind, telescoping_plt, width, color='tab:brown', edgecolor="black")
# p2 = plt.bar(ind, forwarding_plt, width, bottom=telescoping_plt, color='tab:blue', edgecolor="black")
# p3 = plt.bar(ind, zkp_plt, width, bottom=sums, color='tab:red', edgecolor="black")
# p4 = plt.bar(ind, fhe_plt, width, bottom=new_sums, color='tab:green', edgecolor="black")

# p5 = plt.bar(ind+width, [2*x for x in telescoping_plt], width, color='tab:brown', edgecolor="black")
# p6 = plt.bar(ind+width, [2*x for x in forwarding_plt], width, bottom=[2*x for x in telescoping_plt], color='tab:blue', edgecolor="black")
# p7 = plt.bar(ind+width, zkp_plt, width, bottom=[2*x for x in sums], color='tab:red', edgecolor="black")
# p8 = plt.bar(ind+width, fhe_plt, width, bottom=new_sums2, color='tab:green', edgecolor="black")

# p9 = plt.bar(ind+2*width, [3*x for x in telescoping_plt], width, color='tab:brown', edgecolor="black")
# p10 = plt.bar(ind+2*width, [3*x for x in forwarding_plt], width, bottom=[3*x for x in telescoping_plt], color='tab:blue', edgecolor="black")
# p11 = plt.bar(ind+2*width, zkp_plt, width, bottom=[3*x for x in sums], color='tab:red', edgecolor="black")
# p12 = plt.bar(ind+2*width, fhe_plt, width, bottom=new_sums3, color='tab:green', edgecolor="black")

plt.xlabel('Number of hops in the communication path')
plt.ylabel('Computation time (min)')
# plt.title('Total number of bytes sent by a client on average')
plt.xticks(ind+width, ('2', '3','4'))
plt.yticks(np.arange(0, 90, 10))

# for rect in p4:
#     height = rect.get_height()
#     plt.text(rect.get_x() + rect.get_width()/2., 1.05*height, "r=2", ha='center', va='bottom')

# for rect in p8:
#     height = rect.get_height()
#     plt.text(rect.get_x() + rect.get_width()/2., 1.05*height, "r=2", ha='center', va='bottom')
#
# for rect in p12:
#     height = rect.get_height()
#     plt.text(rect.get_x() + rect.get_width()/2., 1.05*height, "r=3", ha='center', va='bottom')


plt.legend((p4[0], p2[0], p1[0], p3[0]), ('Ciphertext operations', 'Message forwarding', 'Telescoping', 'ZKP')) #, loc='center right')
plt.savefig('../graphs/users/user_computation.pdf', format='pdf')
