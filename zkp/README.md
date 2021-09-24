Requirements:
- python (version v>3.8, we tested with v 3.8.5)

Run `./install.sh` to set up ZoKrates (this will take around 5 minutes).


Run the following programs using the command:
- `./run.sh [prog_name]`
where [prog_name] can be one of 2 programs (`enc` or `mult`). It will take around 10 minutes for the mult run.

This will measure the costs of the two different ZK proofs required for the protocol (one for local encryption, the other for multiplication before the final upload). The times for proof generation and verification are printed out. The size of the proof is the size of the generated `proof.json` file. The costs we got when benchmarking on our machine are in `zkp_costs.txt`. Times may vary slightly based on machine resources.


Compilation takes quite a bit of time (~10 hours), so these programs have all already been pre-compiled.
If for any reason they aren't compiled (or to test the programs in full), before running ./run.sh, run:
`./compile.sh [prog_name]`
