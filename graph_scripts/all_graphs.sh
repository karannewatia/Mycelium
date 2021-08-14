#!/bin/bash
python anonymity_set.py
python identification_graph.py
python goodput_graph.py
python duration.py
python mpc_privacy_failure.py
python mpc_liveness.py
python aggregator_computation.py
python aggregator_bandwidth.py
gnuplot bw-user.plot
