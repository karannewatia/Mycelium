#!/bin/bash
PROG=$1

# compile
#echo "compiling..."
time zokrates compile -i $PROG.zok -o $PROG
#echo "compiled."

