#!/bin/bash

# compile
echo "compiling..."
time zokrates compile -i shift.zok
echo "compiled."
# perform the setup phase
zokrates setup
# execute the program
#zokrates compute-witness -a $2 $3 $4
#zokrates compute-witness -a $(seq 500)
#python genInput.py 32768 > witnessInput
python shiftInput.py 32768 > shiftWitnessInput
#time zokrates compute-witness -a $(cat witnessInput)
#cat witnessInput | time zokrates compute-witness --stdin
cat shiftWitnessInput | time zokrates compute-witness --stdin
echo "computed witness."
# generate a proof of computation
time zokrates generate-proof
echo "^ Proof generated"
echo ""
# export a solidity verifier
zokrates export-verifier
# Do verification step
time zokrates verify

