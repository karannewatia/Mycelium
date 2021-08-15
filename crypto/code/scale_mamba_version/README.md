Docker set up instructions: (allocate at least 8 GB of memory for Docker)

After starting the docker application:

inside `Mycelium/crypto/code/scale_mamba_version/`:
- `docker build -t mpc .`
- `docker run -it --rm mpc`

In another shell in `Mycelium/crypto/code/scale_mamba_version/`:
- use `docker ps` to get the id of the docker container running
- `docker cp inputs/decrypt_input.txt id:/root/SCALE-MAMBA/`


Now, in the docker container:
- `cd ~/SCALE-MAMBA/`
- `cp Auto-Test-Data/1/* Data/`
- `bash ./genCertOptions.sh N 1 | ./Setup.x` (N is the number of committee members, we tested with N=10)
- mod value we used for benchmarking MPC costs: 3608870760655701536654448303084521404059979435669688520664454167677047564331360806878098945169255539464747077653151390316596266506041127794233364507011499768902844417
- `./Setup.x` -> 2 -> 2 -> mod -> enter the max possible t (threshold value) (t=4 if N=10)


We first have to set up the shares of the secret key:
- `./benchmark.sh secret_keygen 0 1 2 ...N-1`, where N is the number of committee members

To benchmark MPC decryption (do this after performing the secret key gen):
- `cd Data`
- `./decrypt.sh N`, where N is the number of players
- `cd ..`
- `./benchmark.sh dec_test 0 1 2 ...N-1`, where N is the number of committee members
- Communication cost is in `communication.txt`.

The costs we got are in `scale_mamba_version/MPC_costs.txt`. Note that the costs are much cheaper when the code is run on
Amazon EC2 t2.xlarge instances with 16 GB of RAM.

To test/play around with key gen, encryption, and decryption together in SCALE-MAMBA:
- mod value used in `fhe_test.mpc`: 12413837415352346609
- `./Setup.x` -> 2 -> 2 -> mod -> enter the max possible t (threshold value) (t=4 if N=10)
- `./benchmark.sh fhe_test 0 1 2 ...N-1`, where N is the number of committee members
- Output is in `output_0.txt`
- See the README in `Mycelium/crypto/code/python_version` for instructions on how to generate a different set of FHE parameters.
- Once generated, the `fhe_test.mpc` file in the docker (in `~/SCALE-MAMBA/Programs/fhe_test`) have to be updated appropriately and the mod used in SCALE-MAMBA (which is the ciphertext modulus p) needs to be updated using `./Setup.x` as described above.
