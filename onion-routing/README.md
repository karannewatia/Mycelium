# onion-routing

#### Environment setup:
+ Please use `./install.sh` in the `script` folder to install all required libraries. Previously tried on
  Cloudlab, `ubuntu 20.04`.

#### Usage:
+ cmake .
+ make
+ Run `./rounter 0.0.0.0:PORT` for all nodes one by one.

#### Steps to run (all from the sender node):
1. Input `0` to start `establishing a path`.
2. Input total number of nodes (including destination).
3. Input `IP:PORT` of nodes (including destination) sequentially. You should be
   able to see path established successfully after you input all `IPs`.
4. Input `1` to start sending message, and then input id of your established
   path (it should be 0 if you only established one path, and 1 for the second
   path established).
5. Choose the size of the message you want to send (in MB).
