#!/bin/bash

N_PLAYERS=$1

for (( i = 0; i < $N_PLAYERS; i++ ))
do
  cp ../../../key_gen_input.txt Player${i}_in.txt
done
