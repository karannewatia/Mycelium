# Mycelium

This is a partial implementation of Mycelium, a framework for private graph analytics over massive distributed data. This is not a completely distributed end-to-end implementation (we cannot simulate the millions of users required!)
It instead consists of microbenchmarks for user operations, aggregator operations, and elected committee operations.

## Initial installation:
- `git clone https://github.com/karannewatia/Mycelium`
- `cd Mycelium`
- `./install.sh` (requires python version v>3.8 and pip)

## Summary map of repository contents:

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


## Instructions for Artifact Reviewers at SOSP 2021:
Our implementation is composed of a series of micro-benchmarks. Please `cd` into each of the above folders for detailed explanations and instructions on evaluating each component separately. We provide a docker for some of the cryptographic operations, but require access to CloudLab to evaluate our onion-routing costs. The remainder of operations can be evaluated without any specialized hardware or access.

We summarize what is required to replicate all empirical results below:

## Replication of Graphs and Results in Paper

### Figure 5
Follow README in graph_scripts/
### Figure 6
Follow READMEs in zkp/ and onion-routing/ to generate all costs. Then generate graph in graph_scripts/
### User Computation Costs (Section 6.4)
Follow READMEs in crypto/code/python_version/, onion-routing, and zkp/ to generate all costs. The user computation cost includes the costs of encrypting a ciphertext and multiplying 10 ciphertexts (run `encryption_test.py` and `multiplication_test.py` in crypto/code/python_version/), telescoping and sending a message (see onion-routing), and generating the ZK proofs for encryption and multiplication (see zkp/).
### Committee Costs (Section 6.5)
Follow READMEs in crypto/code/scale_mamba_version/ for local simulation and/or single-machine EC2 simulation
### Figure 8
Follow README in graph_scripts/
### Figure 9
Follow READMEs in crypto/code/python_version/, onion-routing and zkp/ to generate all costs. Then generate graph in graph_scripts/

## List of open-source libraries used
- [ZoKrates](https://github.com/Zokrates/ZoKrates)
- [OpenSSL](https://www.openssl.org/)
- [SCALE-MAMBA](https://github.com/KULeuven-COSIC/SCALE-MAMBA)
