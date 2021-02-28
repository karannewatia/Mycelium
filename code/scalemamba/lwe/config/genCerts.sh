#!/bin/bash

N_PLAYERS=$1

for (( i = 0; i < $N_PLAYERS; i++ ))
do
  cp Player${i}_shareout.txt Player${i}_sharein.txt
  cp ../../../decrypt_Player0_in.txt Player${i}_in.txt
  #openssl genrsa -out Player$i.key 2048
  #openssl req -new -key Player$i.key -out Player$i.csr
  #openssl x509 -req -days 1000 -in Player$i.csr -CA RootCA.crt -CAkey RootCA.key -set_serial 0101 -out Player$i.crt -sha256
done
