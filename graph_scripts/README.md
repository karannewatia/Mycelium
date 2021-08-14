Requirements:
- python (version v>3)
- matplotlib (can be installed using `pip install matplotlib`)
- numpy (can be installed using `pip install numpy`)

Raw data used for plotting all graphs is in `graph_dara.txt`

To generate all graphs:
- `python `

To generate the graph for Figure 5(a):
- `python anonymity_set.py`
- equations are in `anonymity_set.py`

To generate the graph for Figure 5(b):
- `python identification_graph.py`
- script used to generate the data is in `identification.py`

To generate the graph for Figure 5(c):
- `python goodput_graph.py`
- script used to generate the data is in `goodput.py`

To generate the graph for Figure 5(d):
- `python duration.py`
- equations are in `duration.py`

To generate the graph for Figure 8(a):
- `python mpc_privacy_failure.py`
- equations are in `mpc_privacy_failure.py`

To generate the graph for Figure 8(b):
- `python mpc_liveness.py`
- equations are in `mpc_liveness.py`

To generate the graph for Figure 9(a):
- `python aggregator_bandwidth.py`
- equations are in `aggregator_bandwidth.py`

To generate the graph for Figure 9(b):
- `python aggregator_computation.py`
- equations are in `aggregator_computation.py`
- Note that the numbers are slightly lower than the ones in the accepted version of the paper
  since we were able to reduce ZKP costs after the submission. So, the graph generated will have slightly
  lower costs than the corresponding graph in the paper.
