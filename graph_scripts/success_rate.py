import random
import datetime
import numpy as np

malicious_fracs = [0.005, 0.01, 0.015, 0.02,]
drops_fracs = [0.01, 0.02, 0.03, 0.04, 0.05] #churn

for malicious_frac in malicious_fracs:
    for drops_frac in drops_fracs:
        success_ratio = 0.0
        for run in range(5): #average over 5 runs
            num_hops = 3
            num_users = 10000
            users = [i for i in range(num_users)]
            num_send_msgs = int(0.02 * len(users)) #send 200 messages
            senders = random.sample(users, num_send_msgs)
            non_senders = [i for i in users if i not in senders]

            num_malicious = int(malicious_frac * (num_users - num_send_msgs))
            num_drops = int(drops_frac * (num_users - num_send_msgs))

            num_copies = 2 #r
            msg = "success"
            random.shuffle(users)
            malicious = random.sample(non_senders, num_malicious)
            good_users = [i for i in non_senders if i not in malicious]
            received = [0 for i in range(num_users)]

            mailboxes = [[] for i in range(num_users)]
            crashed_users = []
            startDate = datetime.datetime(2021, 4, 19, 00, 00)

            noncrashed_users = [u for u in good_users]
            sent_lst = []
            drops = random.sample(noncrashed_users, num_drops)
            drops_dict = {}
            for i in drops:
                drops_dict[i] = random.randint(1, num_hops**2 + 2*num_hops)

            for j in range(num_copies):
                for i in senders:
                    path = random.sample(non_senders, num_hops)
                    tup = (True, msg, [i] + path, [i] + path, 0, 1, 0, 0, startDate)
                    mailboxes[i].append(tup)

            for i in range(0, num_hops**2 + 2*num_hops + 1):
                time_lst = []
                for u in range(num_users):
                    times = []
                    if u in drops and drops_dict[u] <= i:
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
                                    received[full_path[0]] = 1
                    mailboxes[j] = add_list


            num_received = sum(received)
            success_ratio += num_received / (len(senders))

        print("% churn + malice", malicious_frac + drops_frac)
        print("Fraction of messages that make it: ", success_ratio / 5)
