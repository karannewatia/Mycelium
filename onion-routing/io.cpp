#include <arpa/inet.h>
#include <openssl/bio.h>
#include <openssl/bn.h>
#include <openssl/dh.h>
#include <openssl/ec.h>
#include <openssl/err.h>
#include <openssl/evp.h>
#include <openssl/pem.h>
#include <openssl/rand.h>
#include <stdio.h>
#include <sys/socket.h>
#include <openssl/rsa.h>

#include "assert.h"
#include "iostream"
#include "proto/interface.pb.h"
#include "random"
#include "string"
#include "string.h"
#include "sys/time.h"
#include "vector"
#include "stdlib.h"
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include "thread"
#include "map"
#include "sstream"
#include <openssl/sha.h>
#include <openssl/evp.h>
#include <chrono>

using namespace std;
using namespace chrono;

#define ROUTER_OUTPUT cout << "[" << getip() << "] "

class Router {
private:
    enum reqType {
        HANDSHAKE,
        FORWARD,
        ENCMSG,
        QUIT,
        HANDSHAKE_REPLY,
        FORWARD_BACK,
        FORWARD_HANDSHAKE,
        QUERY_PK,
        QUERY_RESPONSE,
        ACK,
    };

    void handleErrors() {
        ERR_print_errors_fp(stderr);
        abort();
    }

    int AESencrypt(unsigned char *plaintext, int plaintext_len,
                   unsigned char *key, unsigned char *iv,
                   unsigned char *ciphertext, unsigned char* tag) {
        EVP_CIPHER_CTX *ctx;

        int len;

        int ciphertext_len;

        /* Create and initialise the context */
        if (!(ctx = EVP_CIPHER_CTX_new())) handleErrors();

        /*
         * Initialise the encryption operation. IMPORTANT - ensure you use a key
         * and IV size appropriate for your cipher
         * In this example we are using 256 bit AES (i.e. a 256 bit key). The
         * IV size for *most* modes is the same as the block size. For AES this
         * is 128 bits
         */
        if(1 != EVP_EncryptInit_ex(ctx, EVP_aes_256_gcm(), NULL, NULL, NULL))
            handleErrors();

        /*
        * Set IV length if default 12 bytes (96 bits) is not appropriate
        */
        if(1 != EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_SET_IVLEN, 16, NULL))
            handleErrors();

        /* Initialise key and IV */
        if(1 != EVP_EncryptInit_ex(ctx, NULL, NULL, key, iv))
            handleErrors();

        /*
         * Provide the message to be encrypted, and obtain the encrypted output.
         * EVP_EncryptUpdate can be called multiple times if necessary
         */
        if (1 !=
            EVP_EncryptUpdate(ctx, ciphertext, &len, plaintext, plaintext_len))
            handleErrors();
        ciphertext_len = len;

        /*
         * Finalise the encryption. Further ciphertext bytes may be written at
         * this stage.
         */
        if (1 != EVP_EncryptFinal_ex(ctx, ciphertext + len, &len))
            handleErrors();
        ciphertext_len += len;

        /* Get the tag */
        if(1 != EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_GET_TAG, 16, tag))
            handleErrors();

        /* Clean up */
        EVP_CIPHER_CTX_free(ctx);

        return ciphertext_len;
    }

    int AESdecrypt(unsigned char *ciphertext, int ciphertext_len,
                   unsigned char *key, unsigned char *iv,
                   unsigned char *plaintext, unsigned char* tag) {
        EVP_CIPHER_CTX *ctx;

        int len;

        int plaintext_len;

        /* Create and initialise the context */
        if (!(ctx = EVP_CIPHER_CTX_new())) handleErrors();

        /* Initialise the decryption operation. */
        if(!EVP_DecryptInit_ex(ctx, EVP_aes_256_gcm(), NULL, NULL, NULL))
            handleErrors();

        /* Set IV length. Not necessary if this is 12 bytes (96 bits) */
        if(!EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_SET_IVLEN, 16, NULL))
            handleErrors();

        /* Initialise key and IV */
        if(!EVP_DecryptInit_ex(ctx, NULL, NULL, key, iv))
            handleErrors();

        /*
         * Provide the message to be decrypted, and obtain the plaintext output.
         * EVP_DecryptUpdate can be called multiple times if necessary.
         */
        if (1 !=
            EVP_DecryptUpdate(ctx, plaintext, &len, ciphertext, ciphertext_len))
            handleErrors();
        plaintext_len = len;

        /* Set expected tag value. Works in OpenSSL 1.0.1d and later */
        if(!EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_SET_TAG, 16, tag))
            handleErrors();

        /*
         * Finalise the decryption. Further plaintext bytes may be written at
         * this stage.
         */
        if (1 != EVP_DecryptFinal_ex(ctx, plaintext + len, &len))
            handleErrors();
        plaintext_len += len;

        /* Clean up */
        EVP_CIPHER_CTX_free(ctx);

        return plaintext_len;
    }

    vector<string> split(string &s, const string &delim) {
        vector<string> results;
        if (s == "") {
            return results;
        }
        size_t prev = 0, cur = 0;
        do {
            cur = s.find(delim, prev);
            if (cur == string::npos) {
                cur = s.length();
            }
            string part = s.substr(prev, cur - prev);
            if (!part.empty()) {
                results.emplace_back(part);
            }
            prev = cur + delim.length();
        } while (cur < s.length() && prev < s.length());
        return results;
    }

    bool do_write(int fd, const char *buf, int len) {
        int sent = 0;
        while (sent < len) {
            fd_set fds;
            FD_ZERO(&fds);
            FD_SET(fd, &fds);
            struct timeval timeout;
            timeout.tv_sec = 10;
            timeout.tv_usec = 0;

            if (select(fd + 1, NULL, &fds, NULL, &timeout) == 1) {
                int n = write(fd, &buf[sent], len - sent);
                if (n < 0) {
                    fprintf(stderr, "Fail to write: %s\n", strerror(errno));
                    return false;
                }
                sent += n;
            } else {
                ROUTER_OUTPUT << "write timeout\n";
                return false;
            }
        }
        ROUTER_OUTPUT << "write: " << len << endl;
        return true;
    }

    bool do_read(int fd, char *buf, int len) {
        int rcvd = 0;
        while (rcvd < len) {
            fd_set fds;
            FD_ZERO(&fds);
            FD_SET(fd, &fds);
            struct timeval timeout;
            timeout.tv_sec = 10;
            timeout.tv_usec = 0;

            if (select(fd + 1, &fds, NULL, NULL, &timeout) == 1) {
                int n = read(fd, &buf[rcvd], len - rcvd);
                if (n < 0) {
                    fprintf(stderr, "Fail to read: %d %s\n", errno,
                            strerror(errno));
                    return false;
                }
                rcvd += n;
            } else {
                ROUTER_OUTPUT << "read timeout\n";
                return false;
            }
        }
        ROUTER_OUTPUT << "read: " << len << endl;
        return true;
    }

    bool do_read_blocking(int fd, char *buf, int len) {
        int rcvd = 0;
        while (rcvd < len) {
            int n = read(fd, &buf[rcvd], len - rcvd);
            if (n < 0) {
                fprintf(stderr, "Fail to read: %d %s\n", errno,
                        strerror(errno));
                return false;
            }
            rcvd += n;
        }
        ROUTER_OUTPUT << "read: " << len << endl;
        return true;
    }

    struct sockaddr_in string_to_struct_addr(string &str) {
        struct sockaddr_in result;
        memset(&result, 0, sizeof(result));
        auto addr_and_port = split(str, ":");
        result.sin_addr.s_addr = inet_addr(addr_and_port[0].c_str());
        result.sin_family = AF_INET;
        result.sin_port = htons(atoi(addr_and_port[1].c_str()));
        return result;
    }

    // -1 indicate errrors
    int connect_to_addr(string addr) {
        struct timeval Timeout;
        Timeout.tv_sec = 1;
        Timeout.tv_usec = 0;
        int fd = socket(PF_INET, SOCK_STREAM, 0);
        struct sockaddr_in sockaddr = string_to_struct_addr(addr);
        int flags = fcntl(fd, F_GETFL, 0);
        if (flags < 0) {
            fprintf(stderr, "Get flags error:%s\n", strerror(errno));
            close(fd);
            return -1;
        }
        if (fcntl(fd, F_SETFL, flags | O_NONBLOCK) < 0) {
            ROUTER_OUTPUT << "get flags failed\n";
            close(fd);
            return -1;
        }
        fd_set wait_set;
        int res = connect(fd, (struct sockaddr *)&sockaddr, sizeof(sockaddr));
        // connected
        if (res == 0) {
            if (fcntl(fd, F_SETFL, flags) < 0) {
                ROUTER_OUTPUT << "connect fcntl failed\n";
                close(fd);
                return -1;
            }
            return fd;
        } else {
            FD_ZERO(&wait_set);
            FD_SET(fd, &wait_set);

            // wait for socket to be writable; return after given timeout
            res = select(fd + 1, NULL, &wait_set, NULL, &Timeout);
        }
        if (fcntl(fd, F_SETFL, flags) < 0) {
            ROUTER_OUTPUT << "connect fcntl failed\n";
            close(fd);
            return -1;
        }

        if (res < 0) {
            ROUTER_OUTPUT << "connect timeout\n";
            close(fd);
            return -1;
        }

        if (FD_ISSET(fd, &wait_set)) {
            return fd;
        } else {
            ROUTER_OUTPUT << "connect timeout\n";
            close(fd);
            return -1;
        }
        assert(0);
        return -1;
    }

    bool recv_response(int fd, string &res) {
        // start receiving response
        uint32_t res_len = 0;
        if (do_read(fd, (char *)&res_len, sizeof(uint32_t)) == false) {
            ROUTER_OUTPUT << "receive header fail\n";
            return false;
        }
        res_len = ntohl(res_len);
        char *tmp = (char *)malloc(sizeof(char) * res_len);
        memset(tmp, 0, res_len);
        if (do_read(fd, tmp, res_len) == false) {
            ROUTER_OUTPUT << "receive response fail\n";
            return false;
        }
        res = string(tmp, res_len);
        free(tmp);
        return true;
    }

    bool recv_response_blocking(int fd, string &res) {
        // start receiving response
        uint32_t res_len = 0;
        if (do_read_blocking(fd, (char *)&res_len, sizeof(uint32_t)) == false) {
            ROUTER_OUTPUT << "receive header fail\n";
            return false;
        }
        res_len = ntohl(res_len);
        char *tmp = (char *)malloc(sizeof(char) * res_len);
        memset(tmp, 0, res_len);
        if (do_read_blocking(fd, tmp, res_len) == false) {
            ROUTER_OUTPUT << "receive response fail\n";
            return false;
        }
        res = string(tmp, res_len);
        free(tmp);
        return true;
    }

    string formatMsg(string input) {
        char len[sizeof(uint32_t)];
        uint32_t str_len = htonl(input.size());
        memcpy(len, &str_len, sizeof(uint32_t));
        string prefix = string(len, sizeof(uint32_t));
        prefix.append(input);
        assert(prefix.size() == input.size() + sizeof(uint32_t));
        return prefix;
    }

    string parseIpFromFd(int fd) {
        struct sockaddr_in sa;
        socklen_t len = sizeof(sa);
        assert(!getpeername(fd, (struct sockaddr *)&sa, &len));
        stringstream ss;
        ss << string(inet_ntoa(sa.sin_addr)) << ":" << ntohs(sa.sin_port);
        return ss.str();
    }

    BIO *out;
    string ip;
    int curr_id;
    int curr_id_place_holder;

    RSA *publicKey;
    RSA* privKey;

    typedef struct idKey {
        string ip;
        int id;

        bool operator < (const idKey b) const {
            if (ip == b.ip) {
                return id < b.id;
            }
            else {
                return ip < b.ip;
            }
        }

        bool operator == (const idKey b) const {
            return ((ip == b.ip) && (id == b.id));
        }

    } idKey;

    typedef struct sessionInfo {
        int fd;
        string sessionKey;
    } sessionInfo;

    // established by handshake invoked by other routers
    map<idKey, sessionInfo> keyInfo;

    // mapping for forwarding msg
    map<idKey, idKey> forward_mapping;

    // mapping for finding out how to go back
    map<idKey, idKey> back_mapping;

    typedef struct establishedInfo {
        int fd;
        int id;
        vector<string> keys;
    } establishedInfo;

    // the session that router explicitly established
    map<vector<string>, establishedInfo> established_session;

    // store info for handshake request this router send out
    map<idKey, establishedInfo> startInfo;

    map<idKey, int> forward_fd_map;

    system_clock::time_point start, end;
    bool timing = false;

    DH *generate_dh_key() {
        DH *dh = DH_new_by_nid(NID_ffdhe2048);
        if (DH_generate_key(dh) != 1) {
            ROUTER_OUTPUT << "generate key failed\n";
            DH_free(dh);
            return NULL;
        }
        return dh;
    }

    int get_curr_id() {
        Router::curr_id++;
        return Router::curr_id;
    }

    int get_curr_id_place_holder() {
        Router::curr_id_place_holder--;
        return Router::curr_id_place_holder;
    }

    string hash(unsigned char* key_str, int size) {
        unsigned char md_value[EVP_MAX_MD_SIZE];
        EVP_MD_CTX* mdctx = EVP_MD_CTX_create();
        unsigned int md_len, i;
        const EVP_MD *md = EVP_get_digestbyname("SHA256");
        EVP_DigestInit_ex(mdctx, md, NULL);
        EVP_DigestUpdate(mdctx, key_str, size);
        EVP_DigestFinal_ex(mdctx, md_value, &md_len);
        EVP_MD_CTX_destroy(mdctx);

        printf("Digest is: ");
        for(i = 0; i < md_len; i++)
            printf("%02x", md_value[i]);
        printf("\n");
        return string((const char*)md_value, md_len);
    }

    void handshake_handler(int fd, string msg, string recv_ip, int id_place_holder) {
        BIGNUM* enc_pk = BN_bin2bn((const unsigned char*) msg.c_str(), msg.size(), NULL);
        BIGNUM* recv_pk = pkDec(enc_pk);
        DH* dh = generate_dh_key();
        const BIGNUM* pk = BN_new();
        DH_get0_key(dh, &pk, NULL);
        unsigned char key_str[DH_size(dh)];
        assert(DH_compute_key(key_str, recv_pk, dh) == DH_size(dh));
        string key = hash(key_str, DH_size(dh));

        unsigned char req_msg_char[BN_num_bytes(pk)];
        assert(BN_bn2bin(pk, req_msg_char) == BN_num_bytes(pk));

        ROUTER_OUTPUT << "handshake handler generate key finished\n";

        // testing purpose, check whether generate the same key
        BIGNUM* tkey = BN_bin2bn(key_str, DH_size(dh), NULL);
        BIO_puts(out, " output key1\n");
        BN_print(out, tkey);
        BIO_puts(out, " \n");
        BIO_puts(out, " output key1 finish\n");

        // format handshake responses
        interface::Request handshake_response;
        handshake_response.set_request_type(HANDSHAKE_REPLY);
        handshake_response.set_msg(string((const char*)req_msg_char, BN_num_bytes(pk)));
        string req_str;
        handshake_response.SerializeToString(&req_str);
        interface::Msg return_msg;
        return_msg.set_msg(req_str);
        return_msg.set_addr(recv_ip);
        int agreed_id = get_curr_id();
        return_msg.set_id(agreed_id);
        return_msg.set_id_place_holder(id_place_holder);
        string return_msg_str;
        return_msg.SerializeToString(&return_msg_str);
        string sendback_msg = formatMsg(return_msg_str);

        ROUTER_OUTPUT << "handshake handler send back response start\n";

        if (!do_write(fd, sendback_msg.c_str(), sendback_msg.size())) {
            ROUTER_OUTPUT << "handshake send back msg failed\n";
        }

        ROUTER_OUTPUT << "handshake handler send back response finished\n";

        idKey ik;
        ik.id = agreed_id;
        ik.ip = recv_ip;
        sessionInfo info;
        info.fd = fd;
        info.sessionKey = key;
        assert(keyInfo.find(ik) == keyInfo.end());
        keyInfo[ik] = info;

    }

    void forward_handshake_handler(int fd, string& forward_ip, string& msg, idKey origin_ik) {
        int forward_fd = connect_to_addr(forward_ip);
        if (forward_fd <= 0) {
            ROUTER_OUTPUT << "connect to forwarded ip failed\n";
            close(forward_fd);
            close(fd);
            return;
        }
        idKey ik;
        ik.ip = parseIpFromFd(forward_fd);
        ik.id = get_curr_id_place_holder();
        assert(keyInfo.find(ik) == keyInfo.end());
        assert(forward_mapping.find(ik) == forward_mapping.end());
        assert(back_mapping.find(ik) == back_mapping.end());
        forward_mapping[origin_ik] = ik;
        back_mapping[ik] = origin_ik;
        ROUTER_OUTPUT << "insert back mapping, id: " << ik.id << ", ip: " << ik.ip << endl;

        // update the id_place_holder
        interface::Msg forward_msg;
        if (!forward_msg.ParseFromString(msg)) {
            ROUTER_OUTPUT << "parse msg failed\n";
            return;
        }
        forward_msg.set_id_place_holder(ik.id);
        assert(forward_msg.has_id() == false);
        string msg_str;
        forward_msg.SerializeToString(&msg_str);
        string sendback_msg = formatMsg(msg_str);
        if (!do_write(forward_fd, sendback_msg.c_str(), sendback_msg.size())) {
            ROUTER_OUTPUT << "sending handshake foward msg failed\n";
        }
        ROUTER_OUTPUT << "finish forward handshake msg to " << forward_ip << endl;
        assert(forward_fd_map.find(origin_ik) == forward_fd_map.end());
        forward_fd_map[origin_ik] = forward_fd;
        thread t(&Router::request_handler_thread, this, forward_fd);
        t.detach();
    }

    void forward_handler(int fd, string& forward_ip, string& msg, idKey origin_ik) {
        assert(forward_mapping.find(origin_ik) != forward_mapping.end());
        idKey forward_ik = forward_mapping[origin_ik];
        assert(forward_fd_map.find(origin_ik) != forward_fd_map.end());
        int forward_fd = forward_fd_map[origin_ik];

        // add id for forward msg
        interface::Msg forward_msg;
        if (!forward_msg.ParseFromString(msg)) {
            ROUTER_OUTPUT << "parse msg failed\n";
            return;
        }
        assert(!forward_msg.has_id());
        assert(!forward_msg.has_id_place_holder());
        forward_msg.set_id(forward_ik.id);
        string msg_str;
        forward_msg.SerializeToString(&msg_str);
        string sendback_msg = formatMsg(msg_str);
        if (!do_write(forward_fd, sendback_msg.c_str(), sendback_msg.size())) {
            ROUTER_OUTPUT << "sending foward msg failed\n";
        }
        ROUTER_OUTPUT << "finish forward msg to " << forward_ip << endl;
    }

    void handshake_reply_handler(int fd, interface::Msg& request, string& origin_ip) {
        ROUTER_OUTPUT << "get to handshake reply handler\n";
        int id_place_holder = request.id_place_holder();
        idKey ik_place_holder;
        ik_place_holder.id = id_place_holder;
        ik_place_holder.ip = origin_ip;
        idKey ik;
        ik.id = request.id();
        ik.ip = origin_ip;

        // update back mapping
        ROUTER_OUTPUT << "find ik place holder, id: " << id_place_holder << ", ip: " << origin_ip << endl;
        auto it = back_mapping.find(ik_place_holder);
        assert(it != back_mapping.end());
        idKey in_ik = back_mapping[ik_place_holder];
        assert(back_mapping.find(ik) == back_mapping.end());
        back_mapping[ik] = in_ik;

        // update forward mapping
        assert(forward_mapping.find(in_ik) != forward_mapping.end());
        forward_mapping[in_ik] = ik;

        // erase back mapping for id_place_holder
        back_mapping.erase(it);

        // format back message
        assert(keyInfo.find(in_ik) != keyInfo.end());
        int back_fd = keyInfo[in_ik].fd;
        string back_ip = in_ik.ip;
        int back_id = in_ik.id;
        string sessionKey = keyInfo[in_ik].sessionKey;

        // clear the id and id_place_holder info
        assert(request.has_id());
        assert(request.has_id_place_holder());
        request.clear_id();
        request.clear_id_place_holder();
        assert(!request.has_id());
        assert(!request.has_id_place_holder());
        string cleared_msg;
        request.SerializeToString(&cleared_msg);

        interface::Request back_req;
        back_req.set_request_type(FORWARD_BACK);
        back_req.set_msg(cleared_msg);
        string back_req_str;
        back_req.SerializeToString(&back_req_str);
        string enc_back_req_str = sessionEnc(sessionKey, back_req_str);

        interface::Msg back_msg;
        back_msg.set_msg(enc_back_req_str);
        back_msg.set_addr(back_ip);
        back_msg.set_id(back_id);
        string back_msg_str;
        back_msg.SerializeToString(&back_msg_str);
        ROUTER_OUTPUT << "\tmsg size: " << back_msg_str.size() << endl;

        string back_str = formatMsg(back_msg_str);

        if (!do_write(back_fd, back_str.c_str(), back_str.size())) {
            ROUTER_OUTPUT << "handshake reply sending back response failed\n";
        }
    }

    void forward_back_handler(int fd, interface::Msg& request, idKey& ik, string& back_ip) {
        idKey in_ik = back_mapping[ik];
        assert(keyInfo.find(in_ik) != keyInfo.end());
        string sessionKey = keyInfo[in_ik].sessionKey;
        int back_fd = keyInfo[in_ik].fd;
        int back_id = in_ik.id;

        // clear the id
        assert(request.has_id());
        assert(!request.has_id_place_holder());
        request.clear_id();
        assert(!request.has_id());
        string cleared_msg;
        request.SerializeToString(&cleared_msg);

        interface::Request back_req;
        back_req.set_request_type(FORWARD_BACK);
        back_req.set_msg(cleared_msg);

        string back_req_str;
        back_req.SerializeToString(&back_req_str);
        string enc_back_req_str = sessionEnc(sessionKey, back_req_str);

        interface::Msg back_msg;
        back_msg.set_msg(enc_back_req_str);
        back_msg.set_addr(back_ip);
        back_msg.set_id(back_id);
        string back_msg_str;
        back_msg.SerializeToString(&back_msg_str);

        string back_str = formatMsg(back_msg_str);

        if (!do_write(back_fd, back_str.c_str(), back_str.size())) {
            ROUTER_OUTPUT << "handshake reply sending back response failed\n";
        }
        ROUTER_OUTPUT << "forward back msg finish\n";
    }

    void recv_back_msg_handler(idKey ik, string& msg) {
        ROUTER_OUTPUT << "enter recv back handler\n";
        vector<string> keys = startInfo[ik].keys;
        string decMsg;
        string encMsg = msg;
        for (int i = 0; i < keys.size(); i++) {
            decMsg = sessionDec(keys[i], encMsg);
            interface::Request parsed_req;
            if (!parsed_req.ParseFromString(decMsg)) {
                ROUTER_OUTPUT << "cannot parse decrypted request msg\n";
                return;
            }
            assert(parsed_req.request_type() == FORWARD_BACK);
            interface::Msg back_msg;
            encMsg = parsed_req.msg();
            if (i != keys.size() - 1) {
                if (!back_msg.ParseFromString(encMsg)) {
                    ROUTER_OUTPUT << "cannot parse Msg type\n";
                    return;
                }
                encMsg = back_msg.msg();
            }
        }
        if (encMsg.size() < 100)
            ROUTER_OUTPUT << "back msg: " << encMsg << endl;

        ROUTER_OUTPUT << "back msg size: " << encMsg.size() << endl;
        end = system_clock::now();
        ROUTER_OUTPUT << "RTT: " << duration_cast<std::chrono::duration<double>>(end - start).count() << endl;
        return;
    }

    void encmsg_handler(int fd, idKey origin_ik, string& msg, string back_ip) {
        ROUTER_OUTPUT << "received msg size: " << msg.size() << endl;
        if (msg.size() < 100)
            ROUTER_OUTPUT << "received msg: " << msg << endl;
    }

    void query_pk_handler(int fd, idKey origin_ik, string& msg, string back_ip, int id, int total_id) {
        interface::Msg query_req;
        if (!query_req.ParseFromString(msg)) {
            ROUTER_OUTPUT << "cannot parse query pk msg\n";
            close(fd);
            return;
        }
        ROUTER_OUTPUT << "recv query pk req, query for ip: " << query_req.msg() << endl;
        int sk_size = 512;
        int proof_size = 32 * 32;
        char* response = (char*) malloc((sk_size + proof_size) * sizeof(char));
        string res_msg = string(response, sk_size + proof_size);

        assert(keyInfo.find(origin_ik) != keyInfo.end());
        string sessionKey = keyInfo[origin_ik].sessionKey;
        int back_fd = fd;
        int back_id = origin_ik.id;

        ROUTER_OUTPUT << "query pk, id: " << id << " total id: " << total_id << endl;
        // send back an ack first!!!
        if (id == total_id - 1) {
            interface::Request ack_req;
            ack_req.set_request_type(ACK);
            ack_req.set_msg("ack");
            string ack_req_str;
            ack_req.SerializeToString(&ack_req_str);
            string enc_ack_req_str = sessionEnc(sessionKey, ack_req_str);

            interface::Msg back_msg;
            back_msg.set_msg(enc_ack_req_str);
            back_msg.set_addr(back_ip);
            back_msg.set_id(back_id);
            string back_msg_str;
            back_msg.SerializeToString(&back_msg_str);
            ROUTER_OUTPUT << "\tmsg size: " << back_msg_str.size() << endl;

            string back_str = formatMsg(back_msg_str);

            if (!do_write(back_fd, back_str.c_str(), back_str.size())) {
                ROUTER_OUTPUT << "ack sending back response failed\n";
            }
            ROUTER_OUTPUT << "send ack back succeed!\n";
        }

        interface::Request back_req;
        back_req.set_request_type(FORWARD_BACK);
        back_req.set_msg(res_msg);
        string back_req_str;
        back_req.SerializeToString(&back_req_str);
        string enc_back_req_str = sessionEnc(sessionKey, back_req_str);

        interface::Msg back_msg;
        back_msg.set_msg(enc_back_req_str);
        back_msg.set_addr(back_ip);
        back_msg.set_id(back_id);
        string back_msg_str;
        back_msg.SerializeToString(&back_msg_str);
        ROUTER_OUTPUT << "\tmsg size: " << back_msg_str.size() << endl;

        string back_str = formatMsg(back_msg_str);

        if (!do_write(back_fd, back_str.c_str(), back_str.size())) {
            ROUTER_OUTPUT << "handshake reply sending back response failed\n";
        }

        ROUTER_OUTPUT << "query pk finish send back query response\n";
        free(response);
    }

    void request_handler_thread(int fd) {
        ROUTER_OUTPUT << fd << " start waiting for request\n";
        system_clock::time_point start, end;
        while(1) {
            string request_str;
            if (recv_response_blocking(fd, request_str) != true) {
                ROUTER_OUTPUT << "[" << fd << "] receive response failed\n";
                continue;
            }
            start = system_clock::now();
            interface::Msg request;
            if (!request.ParseFromString(request_str)) {
                ROUTER_OUTPUT << "cannot parse response correctly\n";
                ROUTER_OUTPUT << "msg size: " << request_str.size() << endl;
                ROUTER_OUTPUT << "msg: " << request_str << endl;
                close(fd);
                return;
            }

            // dec msg here using ip and id, if id is negative, means handshake,
            // no dec required
            string origin_ip = parseIpFromFd(fd);
            ROUTER_OUTPUT << "recv from " << origin_ip << endl;
            // no id given, thus handshake
            if (!request.has_id()) {
                interface::Request recv_req;
                // ROUTER_OUTPUT << "\trecv handshake req size: " << request.msg().size() << endl;
                if(!recv_req.ParseFromString(request.msg())) {
                    ROUTER_OUTPUT << "cannot parse received handshake msg\n";
                    close(fd);
                    return;
                }
                assert(recv_req.request_type() == HANDSHAKE);
                handshake_handler(fd, recv_req.msg(), origin_ip, request.id_place_holder());
                end = system_clock::now();
                ROUTER_OUTPUT << "request time: " << duration_cast<std::chrono::duration<double>>(end - start).count() << endl;
                continue;
            }

            // if (ip, id) appears as root node (this router invokes a
            // handshake), then this means the router receive a message back,
            // store in buffer

            // handshake reply, we need to update the forward/back mapping and
            if (request.has_id_place_holder()) {
                handshake_reply_handler(fd, request, origin_ip);
            }
            // non-handshake reply
            else {
                idKey ik;
                ik.id = request.id();
                ik.ip = origin_ip;
                if (startInfo.find(ik) != startInfo.end()) {
                    string back_msg = request.msg();
                    recv_back_msg_handler(ik, back_msg);
                    end = system_clock::now();
                    ROUTER_OUTPUT << "request time: " << duration_cast<std::chrono::duration<double>>(end - start).count() << endl;
                    continue;
                }
                // if there idKey is stored in back mapping, that means we need
                // to forward back
                if (back_mapping.find(ik) != back_mapping.end()) {
                    string back_ip = request.addr();
                    forward_back_handler(fd, request, ik, back_ip);
                    end = system_clock::now();
                    ROUTER_OUTPUT << "request time: " << duration_cast<std::chrono::duration<double>>(end - start).count() << endl;
                    continue;
                }
                assert(keyInfo.find(ik) != keyInfo.end());
                string sessionKey = keyInfo[ik].sessionKey;
                assert(fd == keyInfo[ik].fd);
                string encMsg = request.msg();
                string decMsg = sessionDec(sessionKey, encMsg);
                interface::Request parsed_req;
                if (!parsed_req.ParseFromString(decMsg)) {
                    ROUTER_OUTPUT << "cannot parse decrypted request msg\n";
                    close(fd);
                    return;
                }
                if (parsed_req.request_type() == FORWARD) {
                    string forward_ip = request.addr();
                    string parsed_msg = parsed_req.msg();
                    forward_handler(fd, forward_ip, parsed_msg, ik);
                } else if (parsed_req.request_type() == FORWARD_HANDSHAKE) {
                    string forward_ip = request.addr();
                    string parsed_msg = parsed_req.msg();
                    forward_handshake_handler(fd, forward_ip, parsed_msg, ik);
                } else if (parsed_req.request_type() == ENCMSG) {
                    string recv_msg = parsed_req.msg();
                    encmsg_handler(fd, ik, recv_msg, origin_ip);
                } else if (parsed_req.request_type() == QUIT) {

                } else if (parsed_req.request_type() == QUERY_PK) {
                    string recv_msg = parsed_req.msg();
                    assert(parsed_req.has_id() && parsed_req.has_total_id());
                    query_pk_handler(fd, ik, recv_msg, origin_ip, parsed_req.id(), parsed_req.total_id());
                } else {
                    assert(0);
                }
                end = system_clock::now();
                ROUTER_OUTPUT << "request time: " << duration_cast<std::chrono::duration<double>>(end - start).count() << endl;
            }
        }
    }

    void listener_thread(string ip_addr) {
        int listen_fd = socket(PF_INET, SOCK_STREAM, 0);
        int opt;
        assert(setsockopt(listen_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt)) >= 0);
        struct sockaddr_in servaddr = string_to_struct_addr(ip_addr);
        assert(bind(listen_fd, (sockaddr *)&servaddr, sizeof(servaddr)) >= 0);
        assert(listen(listen_fd, 100) >= 0);
        ROUTER_OUTPUT << "start listening on " << ip_addr << endl;
        while (1) {
            struct sockaddr_in clientaddr;
            socklen_t clientaddrlen = sizeof(clientaddr);
            int comm_fd = accept(listen_fd, (struct sockaddr *)&clientaddr, &clientaddrlen);
            ROUTER_OUTPUT << ip_addr << " accept a connection.\n";
            thread t(&Router::request_handler_thread, this, comm_fd);
            t.detach();
        }
    }

    const BIGNUM* pkEnc(const BIGNUM* key) {
        int msg_len = BN_num_bytes(key);
        unsigned char* key_str = (unsigned char*) malloc(sizeof(unsigned char) * msg_len);
        assert(BN_bn2bin(key, key_str) == msg_len);
        unsigned char to[RSA_size(publicKey)];
        int len = RSA_public_encrypt(msg_len, key_str, to, publicKey, RSA_PKCS1_PADDING);
        assert(len == RSA_size(publicKey));
        BIGNUM* new_key = BN_bin2bn(to, len, NULL);
        return new_key;
    }

    BIGNUM* pkDec(BIGNUM* key) {
        int msg_len = BN_num_bytes(key);
        assert(msg_len == RSA_size(privKey));
        unsigned char* key_str = (unsigned char*) malloc(sizeof(unsigned char) * msg_len);
        assert(BN_bn2bin(key, key_str) == msg_len);
        unsigned char to[RSA_size(privKey)];
        int len = RSA_private_decrypt(msg_len, key_str, to, privKey, RSA_PKCS1_PADDING);
        BIGNUM* new_key = BN_bin2bn(to, len, NULL);
        assert(len > 0);
        return new_key;
    }

    string sessionEnc(string& sessionKey, string& msg) {
        BIGNUM* iv = BN_new();
        assert(BN_rand(iv, 128, -1, 0) == 1);
        int enc_size = (msg.size() / 16 + 1) * 16;
        unsigned char* ciphertext = (unsigned char*) malloc(enc_size * sizeof(unsigned char));
        unsigned char iv_str[16];
        assert(BN_num_bytes(iv) == 16);
        BN_bn2bin(iv, iv_str);
        unsigned char tag[16];
        int enc_len = AESencrypt((unsigned char*)msg.c_str(), msg.size(), (unsigned char*)sessionKey.c_str(), iv_str, ciphertext, tag);
        if (enc_len > enc_size) {
            ROUTER_OUTPUT << "enc_len: " << enc_len << ", enc_size: " << enc_size << ", msg size: " << msg.size() << endl;
        }
        assert(enc_len <= enc_size);
        interface::EncMsg enc;
        enc.set_iv(string((const char*)iv_str, 16));
        enc.set_enc_msg(string((const char*)ciphertext, enc_len));
        enc.set_tag(string((const char*)tag, 16));
        string enc_msg;
        enc.SerializeToString(&enc_msg);
        BN_free(iv);
        free(ciphertext);
        return enc_msg;
    }

    string sessionDec(string& sessionKey, string& msg) {
        interface::EncMsg enc;
        if (!enc.ParseFromString(msg)) {
            ROUTER_OUTPUT << "decryption cannot parse encrypted msg\n";
            return msg;
        }
        string iv_str = enc.iv();
        string ciphertext = enc.enc_msg();
        string tag = enc.tag();
        unsigned char* dec_msg = (unsigned char*) malloc(msg.size() * sizeof(unsigned char));
        int dec_len = AESdecrypt((unsigned char*)ciphertext.c_str(), ciphertext.size(), (unsigned char*)sessionKey.c_str(), (unsigned char*)iv_str.c_str(), dec_msg, (unsigned char*)tag.c_str());
        assert(dec_len <= msg.size());
        string res = string((const char*)dec_msg, dec_len);
        free(dec_msg);
        return res;
    }

    thread listener;

    void sendQuery(int id, vector<string>& ips, vector<string>& sessions, int fd, int id_with_first_router) {
        interface::Request req;
        req.set_request_type(QUERY_PK);
        req.set_msg(ips[id]);
        req.set_id(id);
        req.set_total_id(ips.size());
        string req_str;
        req.SerializeToString(&req_str);
        interface::Msg query_req;
        query_req.set_addr(ips[id-1]);
        query_req.set_msg(req_str);
        string sendReq;
        query_req.SerializeToString(&sendReq);

        for (int j = id - 1; j >= 0; j--) {
            interface::Request new_req;
            new_req.set_request_type(FORWARD);
            if (j == id - 1) {
                new_req.set_request_type(QUERY_PK);
                new_req.set_id(id);
                new_req.set_total_id(ips.size());
            }
            new_req.set_msg(sendReq);
            string new_req_str;
            new_req.SerializeToString(&new_req_str);
            string encMsg = sessionEnc(sessions[j], new_req_str);
            interface::Msg new_handshake_req;
            new_handshake_req.set_msg(encMsg);
            new_handshake_req.set_addr(ips[j]);
            if (j == 0)
                new_handshake_req.set_id(id_with_first_router);
            string new_handshake_req_str;
            new_handshake_req.SerializeToString(&new_handshake_req_str);
            sendReq = new_handshake_req_str;
        }
        string sendMsg = formatMsg(sendReq);
        if (do_write(fd, sendMsg.c_str(), sendMsg.size()) != true) {
            ROUTER_OUTPUT << "send query req failed\n";
            close(fd);
            return;
        }

        // receive ack
        if (id == ips.size() - 1) {
            string response;
            if (!recv_response(fd, response)) {
                ROUTER_OUTPUT << "recv response for query pk " << id << " failed" << endl;
                close(fd);
                return;
            }

            ROUTER_OUTPUT << "recved response size: " << response.size() << endl;
            interface::Msg request;
            if (!request.ParseFromString(response)) {
                ROUTER_OUTPUT << "query response parse response fail\n";
                return;
            }
            string decMsg;
            string encMsg = request.msg();
            for (int i = 0; i < id; i++) {
                decMsg = sessionDec(sessions[i], encMsg);
                // ROUTER_OUTPUT << "enter recv back handler " << i << " req size: " << encMsg.size() << endl;
                interface::Request parsed_req;
                if (!parsed_req.ParseFromString(decMsg)) {
                    ROUTER_OUTPUT << "cannot parse decrypted request msg\n";
                    return;
                }
                assert(parsed_req.request_type() == FORWARD_BACK || parsed_req.request_type() == ACK);
                interface::Msg back_msg;
                encMsg = parsed_req.msg();
                if (i != id - 1) {
                    if (!back_msg.ParseFromString(encMsg)) {
                        ROUTER_OUTPUT << "cannot parse Msg type\n";
                        return;
                    }
                    encMsg = back_msg.msg();
                }
            }
            ROUTER_OUTPUT << "receive ack finish!\n";
        }

        // recv response
        string response;
        if (!recv_response(fd, response)) {
            ROUTER_OUTPUT << "recv response for query pk " << id << " failed" << endl;
            close(fd);
            return;
        }

        ROUTER_OUTPUT << "recved response size: " << response.size() << endl;
        interface::Msg request;
        if (!request.ParseFromString(response)) {
            ROUTER_OUTPUT << "query response parse response fail\n";
            return;
        }
        string decMsg;
        string encMsg = request.msg();
        for (int i = 0; i < id; i++) {
            decMsg = sessionDec(sessions[i], encMsg);
            // ROUTER_OUTPUT << "enter recv back handler " << i << " req size: " << encMsg.size() << endl;
            interface::Request parsed_req;
            if (!parsed_req.ParseFromString(decMsg)) {
                ROUTER_OUTPUT << "cannot parse decrypted request msg\n";
                return;
            }
            assert(parsed_req.request_type() == FORWARD_BACK);
            interface::Msg back_msg;
            encMsg = parsed_req.msg();
            if (i != id - 1) {
                if (!back_msg.ParseFromString(encMsg)) {
                    ROUTER_OUTPUT << "cannot parse Msg type\n";
                    return;
                }
                encMsg = back_msg.msg();
            }
        }
        ROUTER_OUTPUT << "query response size: " << encMsg.size() << endl;
        return;
    }

public:
    Router(string ip_) {
        out = BIO_new(BIO_s_file());
        BIO_set_fp(out, stdout, BIO_NOCLOSE);
        ip = ip_;
        listener = thread(&Router::listener_thread, this, ip);
        listener.detach();
        curr_id = 1;
        curr_id_place_holder = -1;

        // init pk and sk
        publicKey = RSA_new();
        privKey = RSA_new();

        FILE *PubKeyFile = NULL;
        FILE *PrivKeyFile = NULL;
        if ((PrivKeyFile = fopen("./rsa-keys/private-key", "rb")) == NULL) {
            perror("open");
            assert(0);
        }
        if (PEM_read_RSAPrivateKey(PrivKeyFile, &privKey, NULL, NULL) == NULL) {
            assert(0);
        }
        if ((PubKeyFile = fopen("./rsa-keys/public-key", "rb")) == NULL) {
            assert(0);
        }
        if (PEM_read_RSA_PUBKEY(PubKeyFile, &publicKey, 0, 0) == NULL) {
            assert(0);
        }

    }

    string getip() {
        return ip;
    }

    bool estabilsh_key_exchange(vector<string> ips) {
        if (ips.size() < 1) {
            ROUTER_OUTPUT << "not enough routers provided\n";
            return false;
        }
        int fd = connect_to_addr(ips[0]);
        if (fd <= 0) {
            ROUTER_OUTPUT << "connect to first router failed\n";
            return false;
        }
        system_clock::time_point start, end;
        double wait_time = 0.0;
        ROUTER_OUTPUT << "connect to " << ips[0] << " with fd: " << fd << endl;
        vector<string> sessions;
        int id_with_first_router;
        for (size_t i = 0; i < ips.size(); i++) {
            // query next hop for public key
            if (i >= 1) {
                sendQuery(i, ips, sessions, fd, id_with_first_router);
            }
            DH* dh = generate_dh_key();
            const BIGNUM* pk = BN_new();
            DH_get0_key(dh, &pk, NULL);
            // TODO: public encryption for handshake pk here
            const BIGNUM* enc_pk = pkEnc(pk);
            unsigned char req_msg_char[BN_num_bytes(enc_pk)];
            assert(BN_bn2bin(enc_pk, req_msg_char) == BN_num_bytes(enc_pk));
            interface::Request req;
            req.set_request_type(HANDSHAKE);
            req.set_msg(string((const char*)req_msg_char, BN_num_bytes(enc_pk)));
            string req_str;
            req.SerializeToString(&req_str);
            interface::Msg handshake_req;
            handshake_req.set_addr(ips[i]);
            handshake_req.set_msg(req_str);
            if (i == 0)
                handshake_req.set_id_place_holder(get_curr_id_place_holder());
            string sendReq;
            handshake_req.SerializeToString(&sendReq);

            assert(sessions.size() == i);
            for (int j = i - 1; j >= 0; j--) {
                interface::Request new_req;
                new_req.set_request_type(FORWARD);
                if (j == i - 1)
                    new_req.set_request_type(FORWARD_HANDSHAKE);
                new_req.set_msg(sendReq);
                string new_req_str;
                new_req.SerializeToString(&new_req_str);
                string encMsg = sessionEnc(sessions[j], new_req_str);
                interface::Msg new_handshake_req;
                new_handshake_req.set_msg(encMsg);
                new_handshake_req.set_addr(ips[j + 1]);
                // for the first handshake router, add id
                if (j == 0)
                    new_handshake_req.set_id(id_with_first_router);
                string new_handshake_req_str;
                new_handshake_req.SerializeToString(&new_handshake_req_str);
                sendReq = new_handshake_req_str;
            }
            string sendMsg = formatMsg(sendReq);
            if (do_write(fd, sendMsg.c_str(), sendMsg.size()) != true) {
                ROUTER_OUTPUT << "send handshake req failed\n";
                close(fd);
                return false;
            }

            ROUTER_OUTPUT << "sending out handshake req, waiting for response\n";
            // waiting for responses of handshake
            string response;
            start = system_clock::now();
            if (!recv_response(fd, response)) {
                ROUTER_OUTPUT << "recv response for " << i << " times failed\n";
                close(fd);
                return false;
            }
            end = system_clock::now();
            wait_time += duration_cast<std::chrono::duration<double>>(end - start).count();
            ROUTER_OUTPUT << "receiving handshake responses\n";
            interface::Msg response_msg;
            if (!response_msg.ParseFromString(response)) {
                ROUTER_OUTPUT << "cannot parse response msg correctly\n";
                close(fd);
                return false;
            }
            string handshake_reply_msg = response_msg.msg();
            if (i == 0) {
                id_with_first_router = response_msg.id();
            }
            for (int j = 0; j < i; j++) {
                string decMsg = sessionDec(sessions[j], handshake_reply_msg);
                interface::Request new_response_msg;
                if (!new_response_msg.ParseFromString(decMsg)) {
                    ROUTER_OUTPUT << j << " iter cannot parse response req during onion decryption correctly\n";
                    close(fd);
                    return false;
                }
                handshake_reply_msg = new_response_msg.msg();
                interface::Msg new_msg;
                if (!new_msg.ParseFromString(handshake_reply_msg)) {
                    ROUTER_OUTPUT << j << " iter cannot parse response msg during onion decryption correctly\n";
                    ROUTER_OUTPUT << j << " msg size: " << handshake_reply_msg.size() << endl;
                    ROUTER_OUTPUT << j << " msg content: " << handshake_reply_msg << endl;
                    close(fd);
                    return false;
                }
                handshake_reply_msg = new_msg.msg();
            }
            interface::Request recv_req;
            ROUTER_OUTPUT << "\trecv msg size: " << handshake_reply_msg.size() << endl;
            if (!recv_req.ParseFromString(handshake_reply_msg)) {
                ROUTER_OUTPUT << "cannot parse handshake response msg correctly\n";
                close(fd);
                return false;
            }
            assert(recv_req.request_type() == HANDSHAKE_REPLY);
            string recv_pk_str = recv_req.msg();
            BIGNUM* recv_pk = BN_bin2bn((const unsigned char*) recv_pk_str.c_str(), recv_pk_str.size(), NULL);
            unsigned char key_str[DH_size(dh)];
            assert(DH_compute_key(key_str, recv_pk, dh) == DH_size(dh));
            string key = hash(key_str, DH_size(dh));
            sessions.push_back(key);

            // testing purpose, check whether generate the same key
            BIGNUM* tkey = BN_bin2bn(key_str, DH_size(dh), NULL);
            BIO_puts(out, " output key2\n");
            BN_print(out, tkey);
            BIO_puts(out, " \n");
            BIO_puts(out, " output key2 finish\n");

            DH_free(dh);
            ROUTER_OUTPUT << "wait time: " << wait_time << endl;
        }

        // insert this info into map
        establishedInfo eInfo;
        eInfo.fd = fd;
        eInfo.id = id_with_first_router;
        eInfo.keys = sessions;
        established_session[ips] = eInfo;
        idKey ik;
        ik.id = id_with_first_router;
        ik.ip = parseIpFromFd(fd);
        startInfo[ik] = eInfo;

        // start listening on this fd
        thread t(&Router::request_handler_thread, this, fd);
        t.detach();
        return true;
    }

    bool sendMsg(string& msg, vector<string>& ips) {
        start = system_clock::now();
        string finalMsg = msg;
        assert(established_session.find(ips) != established_session.end());
        establishedInfo eInfo = established_session[ips];
        assert(eInfo.keys.size() == ips.size());
        for (int i = ips.size() - 1; i >= 0; i--) {
            interface::Request req;
            req.set_request_type(FORWARD);
            if (i == ips.size() - 1) {
                req.set_request_type(ENCMSG);
            }
            req.set_msg(finalMsg);
            string tmpReq;
            req.SerializeToString(&tmpReq);
            string encMsg = sessionEnc(eInfo.keys[i], tmpReq);

            interface::Msg m;
            m.set_msg(encMsg);
            m.set_addr(ips[i]);
            if (i == 0) {
                m.set_id(eInfo.id);
            }
            m.SerializeToString(&finalMsg);
        }

        string sendMsg = formatMsg(finalMsg);

        if (!do_write(eInfo.fd, sendMsg.c_str(), sendMsg.size())) {
            ROUTER_OUTPUT << "send msg failed\n";
            return false;
        }
        ROUTER_OUTPUT << "send msg finished\n";
    }

};
