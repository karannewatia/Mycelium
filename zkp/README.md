Follow instructions here to download zokrates:
- `git clone https://github.com/ZoKrates/ZoKrates`
- `cd ZoKrates/`
- `git checkout 0.7.0`
- `git pull origin 0.7.0`
- `cargo +nightly build --release`
- `cd ..`

Requirements:
- python (version v>3)
- cargo (can be installed using `curl https://sh.rustup.rs -sSf | sh`)
- nightly (can be installed using `rustup -v install  nightly`)

Run the following programs using the command:
- `./run.sh [prog_name]`
where [prog_name] can be one of 2 programs (`enc` or `mult`):

This will measure the costs of the two different ZK proofs required for the protocol (one for local encryption, the other for multiplication before the final upload). The times for proof generation and verification are printed out. The size of the proof is the size of the generated `proof.json` file. The costs we got when benchmarking on our machine are in `zkp_costs.txt`.

Compilation takes quite a bit of time (~10 hours), so these programs have all already been pre-compiled.
If for any reason they aren't compiled (or to test the programs in full), before running ./run.sh, run:
`./compile.sh [prog_name]`
