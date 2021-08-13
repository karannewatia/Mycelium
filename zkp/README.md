Follow instructions here to download zokrates:
- `git clone https://github.com/ZoKrates/ZoKrates`
- `cd ZoKrates/`
- `git checkout 0.7.0`
- `git pull origin 0.7.0`
- `cargo +nightly build --release`

Requirements:
- python3
- cargo (can be installed using `curl https://sh.rustup.rs -sSf | sh`)
- nightly (can be installed using `rustup -v install  nightly`)

Run the following programs using the command:
- ./run.sh [prog_name]
where [prog_name] can be one of 2 programs:
 - enc
 - mult

This will measure the costs of the two different ZK proofs required for the protocol (one for local encryption, the other for multiplication before upload).

Compilation takes quite a bit of time (~10 hours), so these programs have all already been pre-compiled
If for any reason they aren't compiled (or to test the programs in full), before running ./run.sh, run:
# ./compile.sh [prog_name]
