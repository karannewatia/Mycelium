import random
import numpy as np

#The data is obtained by simulating a small system where senders set up paths for communication.
#The data generated will be slightly different each time because of the randomization involved.

num_runs = 100 #average over 100 runs
malice = [0.005, 0.01, 0.02, 0.04] #malice rates
print("% malice: ", malice)

hops = [2,3] #k
copies = [1,2,3] #r

for num_hops in hops:
    for num_copies in copies:
        results = []
        for malicious_frac in malice:
            success_ratio = 0.0
            for run in range(num_runs):
                num_users = 10000 #simulate a system with 10000 users
                users = [i for i in range(num_users)]
                num_send_msgs = int(0.01 * len(users)) #number of message senders
                senders = random.sample(users, num_send_msgs)
                non_senders = [i for i in users if i not in senders]
                num_malicious = int(malicious_frac * (num_users - num_send_msgs))
                random.shuffle(users)
                malicious = random.sample(non_senders, num_malicious)
                good_users = [i for i in non_senders if i not in malicious]
                received = [0 for i in range(num_users)]
                mailboxes = [[] for i in range(num_users)]
                sent_lst = []
                num_success = {}
                for sender in senders:
                    for j in range(num_copies):
                        #set up the message forwarding path
                        path = random.sample(non_senders, num_hops)
                        malicious_count = 0
                        for node in path:
                            if node in malicious:
                                malicious_count+=1
                        if malicious_count == num_hops:
                            num_success[sender] = 0
                            #the user is identified if any of the paths is fully malicious
                            break
                        else:
                            num_success[sender] = 1
                success_ratio += sum(num_success.values()) / (len(senders))
            results.append(1-(success_ratio/num_runs))
        print("k = ", num_hops, " r = ", num_copies)
        print(results)
