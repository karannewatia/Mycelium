#!/bin/bash
PROG=$1
SIZE=${2:-32768}

# perform the setup phase
./ZoKrates/target/release/zokrates setup -i $PROG

# compute witness
python ${PROG}Input.py $SIZE > ${PROG}Witness
cat ${PROG}Witness | ./ZoKrates/target/release/zokrates compute-witness --stdin -i $PROG
echo "computed witness."

# generate a proof of computation
time ./ZoKrates/target/release/zokrates generate-proof -i $PROG
echo "Proof generated."
echo ""

# Do verification step
time ./ZoKrates/target/release/zokrates verify
echo "Proof verified."
echo ""
