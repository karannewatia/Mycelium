#!/bin/bash
PROG=$1

# compile
time ./zokrates compile -i $PROG.zok -o $PROG
