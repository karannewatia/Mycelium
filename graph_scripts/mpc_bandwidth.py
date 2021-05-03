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


N = 3

font = {'size'   : 17}
plt.rc('font', **font)
plt.gcf().subplots_adjust(bottom=0.15)

decryption = (bytesto(633026584, 'g'), bytesto(5432784056, 'g'), bytesto(13670440818, 'g'))

# resharing_cost = (32768*550/8) + (6*550/8)
# resharing = (bytesto(resharing_cost*5, 'g'), bytesto(resharing_cost*10, 'g'), bytesto(resharing_cost*15, 'g'), bytesto(resharing_cost*20, 'g'))

ind = np.arange(N)
width = 0.15
p1 = plt.bar(ind, decryption, width, color='tab:blue', edgecolor="black")
# p2 = plt.bar(ind, resharing, width, bottom=decryption, color='tab:orange')

plt.xlabel('Size of the committee', fontsize='large')
plt.ylabel('Traffic (GB)', fontsize='large')
# plt.title('MPC bandwidth')
plt.xticks(ind, ('5', '10', '15'))
plt.yticks(np.arange(0, 16, 2))

# plt.legend((p1[0], p2[0]), ('Decryption', 'Re-sharing'))
plt.savefig('../graphs/committee/mpc_bandwidth.pdf', format='pdf')
