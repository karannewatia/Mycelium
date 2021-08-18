This is an implementation of the onion routing protocol.
A source node sends a message to a destination node through x intermediate hops,
(where x is 2, 3, or 4 in our experiments).
So, up to 6 CloudLab machines are needed to test the protocol.

#### Environment setup:
- Please use `./install.sh` in the `script` folder to install all required libraries. Previously tried on
  CloudLab, `ubuntu 20.04`. It will take a while (around an hour) for the installation script to finish.

#### Usage:
- `cmake .`
- `make`
- Run `curl ifconfig.me` to get the ip addresses of all nodes, and save these.
- Pick a PORT number to communicate between nodes
- Run `./router 0.0.0.0:PORT | tee out.txt` one all nodes one by one, using the same port number.

#### Steps to run (only from the designated sender node):
- Input `0` to start establishing a path.
- Input total number of nodes in the path (including destination). For example,
   if the sender node wants to establish a path consisting of 2 intermediate nodes/hops between
   itself and the destination, then input 3.
- IPs can be obtained using `curl ifconfig.me`.
- Input `IP:PORT` of nodes (including destination) sequentially. You should be
   able to see the path established successfully after you input all `IPs`.
- Input `1` to start sending message, and then input the id of your established
   path (it is `0` if you only established one path).
- Choose the size of the message you want to send (in MB). We tested with 4.3 MB based on the ciphertext size.

#### Now, steps to benchmark the costs on each node:
- `Ctrl+C` to exit the program.
- To benchmark the costs from the generated `out.txt` file,
  run `python benchmark.py [node_type]` on each node, where node_type is
  `src` if the node is the original source of the message,
  `dst` if the node is the final destination for the message,
  and `hop` otherwise.
- Note that the costs depend on whether the node was the sender, destination, or an intermediate hop.
  Additionally, the costs for the intermediate hops are also different. For example, the first hop has to do more work for telescoping than the other hops.

  The costs we got are in `Mycelium/onion_routing_costs.xlsx`.
