#!/bin/bash

N_PLAYERS=$1

for (( i = 0; i < $N_PLAYERS; i++ ))
do
  cp ../../../Player0_in.txt Player${i}_in.txt
  #cp ../../../decrypt_Player0_in.txt Player${i}_in.txt
  #cp Player${i}_shareout.txt Player${i}_sharein.txt 
done
