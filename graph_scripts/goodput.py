import random
import datetime
import numpy as np

#The data is obtained by simulating a small system where
#senders set up paths for communication and dummy messages are sent along the onion route.
#The data generated will be slightly different each time because of the randomization involved.

num_copies = 3 #r #this can be 1,2, or 3

results = []
num_runs = 10 #average over 10 runs
# % malice + churn
churn_plus_malice = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09]

for rate in churn_plus_malice:
    malicious_frac = rate*0.5
    drops_frac = rate*0.5
    success_ratio = 0.0
    for run in range(num_runs):
        num_hops = 3 #k
        num_users = 10000 #simulate a system with 10000 users
        users = [i for i in range(num_users)]
        num_send_msgs = int(0.01 * len(users)) #number of message senders
        senders = random.sample(users, num_send_msgs)
        non_senders = [i for i in users if i not in senders]
        num_malicious = int(malicious_frac * (num_users - num_send_msgs))
        num_drops = int(drops_frac * (num_users - num_send_msgs)) #sample some users which will crash

        msg = "success" #dummy message
        random.shuffle(users)
        malicious = random.sample(non_senders, num_malicious)
        good_users = [i for i in non_senders if i not in malicious]
        received = [0 for i in range(num_users)]

        mailboxes = [[] for i in range(num_users)]
        crashed_users = []
        startDate = datetime.datetime(2021, 4, 19, 00, 00) #example date and time

        noncrashed_users = [u for u in good_users]
        sent_lst = []
        drops = random.sample(noncrashed_users, num_drops)
        drops_dict = {}
        for i in drops:
            drops_dict[i] = 1

        for j in range(num_copies):
            for i in senders:
                path = random.sample(non_senders, num_hops)
                tup = (True, msg, [i] + path, [i] + path, 0, 1, 0, 0, startDate)
                mailboxes[i].append(tup)

        #set up the times in which messages will be sent/received
        for i in range(0, num_hops**2 + 2*num_hops + 1):
            time_lst = []
            for u in range(num_users):
                times = []
                if u in drops: #crashed users will not be able to send messages
                    continue
                curr = startDate + datetime.timedelta(seconds=random.randrange(180))
                times.append((curr, u))
                for j in range(6):
                    curr += datetime.timedelta(minutes=10)
                    curr += datetime.timedelta(seconds=random.randrange(30))
                    if curr < startDate + datetime.timedelta(hours=1):
                        times.append((curr, u))
                time_lst += times
            time_lst.sort()
            startDate += datetime.timedelta(hours=1)

            #process messages received in the mailbox
            for (t, j) in time_lst:
                add_list = []
                while (len(mailboxes[j]) > 0):
                    (sender_bool, msg, full_path, path, tracker, offset, hop_count, round, timestamp) = mailboxes[j].pop()
                    if round > i or timestamp >= t:
                        add_list.append((sender_bool, msg, full_path, path, tracker, offset, hop_count, round, timestamp))
                    elif round == i:
                        if round != num_hops**2 + 2*num_hops:
                            if sender_bool == True:
                                new_timestamp = timestamp + datetime.timedelta(minutes=random.randrange(2, 5))
                                new_round = round + 1
                                new_hop_count = hop_count + 1
                                hop_idx = hop_count + 2
                                if round !=num_hops**2 + num_hops:
                                    to_send = (False, msg, full_path, full_path[:hop_idx], 1, 1, new_hop_count, new_round, new_timestamp)
                                else:
                                    to_send = (False, msg, full_path, full_path, 1, 1, new_hop_count, new_round, new_timestamp)
                                mailboxes[path[1]].append(to_send)
                                sent_lst.append(path[1])
                            else:
                                new_timestamp = timestamp + datetime.timedelta(minutes=random.randrange(2, 5))

                                #malicious user (which may corrupt/drop a message)
                                if j in malicious:
                                    msg = "failed"

                                new_round = round + 1
                                if len(path) == 2:
                                    to_send = (True, msg, full_path, path, 0, 1, hop_count, new_round, new_timestamp)
                                    mailboxes[path[0]].append(to_send)
                                    sent_lst.append(path[0])
                                else:
                                    if tracker != len(path) - 1:
                                        if tracker == 1 and offset == -1:
                                            to_send = (True, msg, full_path, path, 0, 1, hop_count, new_round, new_timestamp)
                                            mailboxes[path[0]].append(to_send)
                                            sent_lst.append(path[0])

                                        else:
                                            new_idx = tracker+offset
                                            to_send = (False, msg, full_path, path, new_idx, offset, hop_count, new_round, new_timestamp)
                                            mailboxes[path[new_idx]].append(to_send)
                                            sent_lst.append(path[new_idx])
                                    else:
                                        new_idx = tracker - 1
                                        to_send = (False, msg, full_path, path, new_idx, -1, hop_count, new_round, new_timestamp)
                                        mailboxes[path[new_idx]].append(to_send)
                                        sent_lst.append(path[new_idx])
                        else:
                            if msg == "success" and j not in malicious:
                                #message received successfully
                                received[full_path[0]] = 1
                mailboxes[j] = add_list

        num_received = sum(received)
        success_ratio += num_received / (len(senders))

    results.append(success_ratio/num_runs)

print(results)
