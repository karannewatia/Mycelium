import random
import datetime
import numpy as np

results = []
num_runs = 100
malice = [0.005, 0.01, 0.02, 0.04]

for malicious_frac in malice:
    success_ratio = 0.0
    for run in range(num_runs): #average over 5 runs
        num_hops = 2
        num_users = 10000
        users = [i for i in range(num_users)]
        num_send_msgs = int(0.01 * len(users))
        senders = random.sample(users, num_send_msgs)
        non_senders = [i for i in users if i not in senders]

        num_malicious = int(malicious_frac * (num_users - num_send_msgs))

        num_copies = 3 #r
        random.shuffle(users)
        malicious = random.sample(non_senders, num_malicious)
        good_users = [i for i in non_senders if i not in malicious]
        received = [0 for i in range(num_users)]
        mailboxes = [[] for i in range(num_users)]
        sent_lst = []
        num_success = {}

        for sender in senders:
            for j in range(num_copies):
                path = random.sample(non_senders, num_hops)
                malicious_count = 0
                for node in path:
                    if node in malicious:
                        malicious_count+=1
                if malicious_count == num_hops:
                    num_success[sender] = 0
                    break
                else:
                    num_success[sender] = 1

        success_ratio +=sum(num_success.values()) / (len(senders))

    print("%malice", malicious_frac)
    print("Success rate: ", success_ratio/num_runs)
    results.append(success_ratio/num_runs)

print("k= ", num_hops, " r= ", num_copies)
print(malice)
print(results)
