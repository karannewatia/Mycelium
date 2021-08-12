#include "io.cpp"

int id = 0;

int main(int argc, char *argv[]) {
    if (argc != 2) {
        cout << "Usage: ./router IP:PORT\n";
        return 0;
    }
    Router router = Router(string(argv[1]));
    struct timeval starttime, endtime;
    vector<vector<string>> stored_ip;

    while(1) {
        char cmd[100];
        cout << "Please choose cmd to run: 0 for handshake, 1 for sending msg: ";
        memset(cmd, 0, sizeof(cmd));
        cin.getline(cmd, sizeof(cmd));
        string cmd_str = string(cmd, 1);
        // only accept 0 for handshake, 1 for send message
        if (cmd_str != "0" && cmd_str != "1") {
            cout << "invalid command, should be either 0 or 1\n";
            continue;
        }
        vector<string> ips;
        if (cmd_str == "0") {
            cout << "input number of rounters: ";
            memset(cmd, 0, sizeof(cmd));
            cin.getline(cmd, sizeof(cmd));
            stringstream ss;
            ss << cmd;
            int num;
            ss >> num;
            cout << "You input " << num << endl;
            for (int i = 0; i < num; i++) {
                cout << "Please input " << i << " ip: ";
                memset(cmd, 0, sizeof(cmd));
                cin.getline(cmd, sizeof(cmd));
                string ip = string(cmd);
                cout << "You input " << ip << endl;
                ips.push_back(ip);
            }
            assert(ips.size() == num);
            stored_ip.push_back(ips);
            cout << "Your id for these ips is: " << id << endl;
            id++;
        }
        else {
            cout << "please input an id of established ips: ";
            memset(cmd, 0, sizeof(cmd));
            cin.getline(cmd, sizeof(cmd));
            stringstream ss;
            ss << cmd;
            int input_id;
            ss >> input_id;
            if (input_id >= stored_ip.size()) {
                cout << "invalid id\n";
                continue;
            }
            ips = stored_ip[input_id];
        }
        uint64_t msgSize;
        if (cmd_str == "1") {
            cout << "input size of msg you want to send (MB): ";
            memset(cmd, 0, sizeof(cmd));
            cin.getline(cmd, sizeof(cmd));
            stringstream ss;
            ss << cmd;
            double size_mb;
            ss >> size_mb;
            msgSize = size_mb * 1024 * 1024;
            cout << "You want to send " << size_mb << " MB, " << msgSize << " bytes" << endl;
        }
        if (cmd_str == "0") {
            gettimeofday(&starttime, 0);
            router.estabilsh_key_exchange(ips);
            gettimeofday(&endtime, 0);
            cout << "TIME: handshake: " << ((double)(endtime.tv_sec - starttime.tv_sec) + (double) (endtime.tv_usec - starttime.tv_usec) / 1000000) << endl;
        }
        else if (cmd_str == "1") {
            string msg = string(msgSize, 0);
            assert(msg.size() == msgSize);
            gettimeofday(&starttime, 0);
            router.sendMsg(msg, ips);
            gettimeofday(&endtime, 0);
            cout << "TIME: send msg: " << ((double)(endtime.tv_sec - starttime.tv_sec) + (double) (endtime.tv_usec - starttime.tv_usec) / 1000000) << endl;
        }
        else {
            assert(0);
        }
    }

    return 0;
}
