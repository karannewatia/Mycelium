This is an implementation of the onion routing protocol.
A source node sends a message to a destination node through x intermediate hops,
(where x is 2, 3, or 4 in our experiments).
So, up to 6 CloudLab machines are needed to test the protocol.

#### Environment setup:
- Please use `./install.sh` in the `script` folder to install all required libraries. It will take a while (around an hour) for the installation script to finish. Previously tried on CloudLab m510 machines (8-core 2 GHz Intel Xeon D-1548 processor and 64 GB RAM) running Ubuntu 20.04.

### Requirements:
- python (version v>3.8, we tested with v 3.8.10)

#### Usage:
- `cmake .`
- `make`
- Run `curl ifconfig.me` to get the ip addresses of all nodes, and save these.
- Pick a PORT number to communicate between nodes
- Run `./router 0.0.0.0:PORT | tee out.txt` on all nodes one by one, using the same port number.

#### Steps to run (only from the designated sender node):
- Input `0` to start establishing a path.
- Input total number of nodes in the path (including destination). For example,
   if the sender node wants to establish a path consisting of 2 intermediate nodes/hops between
   itself and the destination, then input 3.
- IPs can be obtained using `curl ifconfig.me` (as mentioned above).
- Input `IP:PORT` of nodes (including destination) sequentially (intermediate hop 1, intermediate hop 2,..., destination). You should be able to see the path established successfully after you input the `IP:PORT` of each intermediate hop and the destination.
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

The costs we got are in `onion_routing_costs.txt`.
The measured costs should be very similar, but there may be some slight discrepancies in the number of bytes communicated --  this is due to the key exchange phase using random shares to establish a secret key. There may also be slight differences in timing based on the hardware used.
