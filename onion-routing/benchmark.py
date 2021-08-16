import sys

if sys.argv[1] == "src":
    sender = True
else:
    sender = False

file = open('out.txt', 'r')
lines = file.readlines()
file.close()

write_telescoping_total = 0
write_send_total = 0
read_telescoping_total = 0
read_send_total = 0
telescoping_time = 0
send_msg_time = 0

if sender:
    telescoping = True
    for line in lines:
        if "please input an id of established ips" in line:
            telescoping = False
        if "write" in line:
            idx = line.find("write: ")
            if telescoping:
                write_telescoping_total += int(line[idx+7:])
            else:
                write_send_total += int(line[idx+7:])
        if "read" in line:
            idx = line.find("read: ")
            if telescoping:
                read_telescoping_total += int(line[idx+6:])
            else:
                read_send_total += int(line[idx+6:])
        if "TIME: handshake:" in line:
            idx = line.find("TIME: handshake: ")
            telescoping_time = float(line[idx+17:])
        if "TIME: send msg:" in line:
            idx = line.find("TIME: send msg: ")
            send_msg_time = float(line[idx+16:])
else:
    last_write = 0
    last_read = 0
    last_req_time = 0
    for line in lines:
        if "write" in line:
            idx = line.find("write: ")
            write_telescoping_total += int(line[idx+7:])
            last_write = int(line[idx+7:])
        if "read" in line:
            idx = line.find("read: ")
            read_telescoping_total += int(line[idx+6:])
            last_read = int(line[idx+6:])
        if "time" in line:
            idx = line.find("time: ")
            telescoping_time += float(line[idx+6:])
            last_req_time = float(line[idx+6:])
    if sys.argv[1] != "dst":
        write_telescoping_total -= last_write
    read_telescoping_total -= last_read
    if sys.argv[1] == "dst":
        write_send_total = 0
    else:
        write_send_total = last_write
    read_send_total = last_read
    telescoping_time -= last_req_time
    send_msg_time = last_req_time

print("total bytes written for telescoping: ", write_telescoping_total)
print("total bytes written for sending the message: ", write_send_total)

print("total bytes read for telescoping: ", read_telescoping_total)
print("total bytes read for sending the message: ", read_send_total)

print("time taken for telescoping: ", telescoping_time)
print("time taken for sending the message: ", send_msg_time)
