# onion-routing

#### Environment setup:
+ Please use `./install.sh` in the `script` folder to install all required libraries. Previously tried on
  CloudLab, `ubuntu 20.04`.

#### Usage:
+ `cmake .``
+ `make`
+ Run `./router 0.0.0.0:PORT` for all nodes one by one. (example port number: 10000)

#### Steps to run (all from the sender node):
1. Input `0` to start establishing a path.
2. Input total number of nodes in the path (including destination). For example,
   if the sender node wants to establish a path consisting of 3 intermediate nodes between
   itself and the destination, then input 4.
3. Input `IP:PORT` of nodes (including destination) sequentially. You should be
   able to see path established successfully after you input all `IPs`.
   IPs can be obtained using `curl ifconfig.me`.
4. Input `1` to start sending message, and then input id of your established
   path (it should be 0 if you only established one path, and 1 for the second
   path established).
5. Choose the size of the message you want to send (in MB).
