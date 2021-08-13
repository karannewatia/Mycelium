#!/bin/bash
PROG=$1
SIZE=${2:-32768}

# perform the setup phase
./zokrates setup -i $PROG

# compute witness
python ${PROG}Input.py $SIZE > ${PROG}Witness
cat ${PROG}Witness | ./zokrates compute-witness --stdin -i $PROG
echo "computed witness."

# generate a proof of computation
time ./zokrates generate-proof -i $PROG
echo "Proof generated."
echo ""

# Do verification step
time ./zokrates verify
echo "Proof verified."
echo ""
