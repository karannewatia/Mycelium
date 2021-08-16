# Mycelium

This is a partial implementation of Mycelium, a framework for private graph analytics over massive distributed data. This is not a completely distributed end-to-end implementation (we cannot simulate the millions of users required!) - it instead consists of microbenchmarks for user operations, aggregator operations, and elected committee operations.

### Summary map of repository contents:

crypto:
- Python code for user-side/aggregator-side FHE operations (crypto/code/python_version/)
- MPC files for decryption (crypto/code/scale_mamba_version/)
- Amazon EC2 experiment instructions/scripts (crypto/mpc_amazon_ec2_benchmarking/)

zkp
- code for ZK proofs

original_graphs
- the graphs we generated from the data we obtained

graph_scripts
- all scripts used for generating the graphs in the paper

re_sharing:
- Re-sharing (extended VSR protocol) proof-of-concept/rough implementation

onion-routing:
- all onion routing code

onion_routing_costs.xslx:
- costs from running the onion routing code on CloudLab machines


## Instructions for Artifact Reviewers at SOSP 2021:
Our implementation is composed of a series of micro-benchmarks. Please `cd` into each of the above folders for detailed explanations and instructions on evaluating each component separately. We summarize the instructions required to replicate all results below:

## Replication of Graphs and Results in Paper

### Figure 5
### Figure 6
### Committee Costs (Section 6.5)
### Figure 8
### Figure 9

