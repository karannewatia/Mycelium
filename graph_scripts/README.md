Requirements:
- python (version v>3, we tested with v 3.8.5)
- matplotlib (can be installed using `pip install matplotlib`)
- numpy (can be installed using `pip install numpy`)
- datetime (can be installed using `pip install datetime`)
- gnuplot (see http://www.gnuplot.info/download.html)

Raw data used for plotting all graphs is in `graph_data.txt`

Graphs will be generated in `Mycelium/new_graphs`:
- `mkdir ../new_graphs`

To generate all graphs:
- `./all_graphs.sh`

To generate the graph for Figure 5(a):
- `python anonymity_set.py`
- equations are in `anonymity_set.py`

To generate the graph for Figure 5(b):
- `python identification_graph.py`
- script used to generate the data is in `identification.py` (the data generated will be slightly different each time because of the randomization involved), and can be run using `python identification.py`.

To generate the graph for Figure 5(c):
- `python goodput_graph.py`
- script used to generate the data is in `goodput.py`, and can be run using `python goodput.py`. Change the value of 'r' (number of messages sent per user) in line 9 of `goodput.py` as needed (we tested with r = 1,2,and 3). Note that the data generated will be slightly different each time because of the randomization involved. It will around 5-10 minutes for each run of `goodput.py` (with r=1,2,3).

To generate the graph for Figure 5(d):
- `python duration.py`
- equations are in `duration.py`

To generate the graph for Figure 6:
- `gnuplot bw-user.plot` (requires data to be in `bw-user.data`)
-  equations are in `user_bandwidth.py`, and can be run with `python user_bandwidth.py`.
- Note that the numbers are slightly lower than the ones in the accepted version of the paper
  since we were able to reduce ZKP costs after the submission. So, the graph generated will have slightly
  lower costs than the corresponding graph in the paper.

To generate the graph for Figure 8(a):
- `python mpc_privacy_failure.py`
- equations are in `mpc_privacy_failure.py`

To generate the graph for Figure 8(b):
- `python mpc_liveness.py`
- equations are in `mpc_liveness.py`

To generate the graph for Figure 9(a):
- `python aggregator_bandwidth.py`
- equations are in `aggregator_bandwidth.py`
- Note that the numbers are slightly lower than the ones in the accepted version of the paper
  since we were able to reduce ZKP costs after the submission. So, the graph generated will have slightly
  lower costs than the corresponding graph in the paper.

To generate the graph for Figure 9(b):
- `python aggregator_computation.py`
- equations are in `aggregator_computation.py`
- Note that the numbers are slightly different from the ones in the accepted version of the paper
  since we were able to reduce ZKP costs after the submission and we included the cost of computing the relinearization operation in this version. The additional number of cores needed for relinearization is a small constant number (around 40), so the ZKP cores still dominate over the aggregation cores as the system scales.
