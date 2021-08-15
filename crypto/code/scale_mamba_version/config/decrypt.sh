#!/bin/bash

N_PLAYERS=$1

for (( i = 0; i < $N_PLAYERS; i++ ))
do
  cp ../decrypt_input.txt Player${i}_in.txt
  cp ~/SCALE-MAMBA/Data/Player${i}_shareout.txt Player${i}_sharein.txt
done
