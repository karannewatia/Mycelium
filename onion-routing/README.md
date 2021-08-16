#### Environment setup:
- Please use `./install.sh` in the `script` folder to install all required libraries. Previously tried on
  CloudLab, `ubuntu 20.04`.

#### Usage:
- `cmake .`
- `make`
- Run `./router 0.0.0.0:PORT | tee out.txt` for all nodes one by one.

#### Steps to run (all from the sender node):
- Input `0` to start establishing a path.
- Input total number of nodes in the path (including destination). For example,
   if the sender node wants to establish a path consisting of 2 intermediate nodes/hops between
   itself and the destination, then input 3.
- IPs can be obtained using `curl ifconfig.me`.
- Input `IP:PORT` of nodes (including destination) sequentially. You should be
   able to see the path established successfully after you input all `IPs`.
- Input `1` to start sending message, and then input id of your established
   path (it should be 0 if you only established one path).
- Choose the size of the message you want to send (in MB).
- `Ctrl+C` to exit the program.
- To benchmark the costs from the generated `out.txt` file,
  run `python benchmark.py [node_type]` on each node, where node_type is
  `src` if the node is the original source of the message,
  `dst` if the node is the final destination for the message,
  and `hop` otherwise.

  The costs we got are in `Mycelium/onion_routing_costs.xlsx`.
