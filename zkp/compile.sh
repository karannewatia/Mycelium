#!/bin/bash
PROG=$1

# compile
time ./ZoKrates/target/release/zokrates compile -i $PROG.zok -o $PROG
