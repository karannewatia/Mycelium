# Follow instructions here to download zokrates:
# curl -LSfs get.zokrat.es | sh
# set $ZOKRATES_HOME variable to stdlib

Run the following programs using the command:
# ./run.sh [prog_name]
[prog_name] can be one of 2 programs:
 - enc
 - mult

This will measure the costs of the two different ZK proofs required for the protocol (one for local encryption, the other for multiplication before upload).

Compilation takes quite a bit of time (~10 hours), so these programs have all already been pre-compiled
If for any reason they aren't compiled (or to test the programs in full), before running ./run.sh, run:
# ./compile.sh [prog_name]
