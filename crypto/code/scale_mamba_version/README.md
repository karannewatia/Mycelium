Docker set up instructions: (allocate at least 8 GB of memory for Docker)

After starting the docker application:

inside `Mycelium/crypto/code/scale_mamba_version/`:
- `docker build -t mpc .`
- `docker run -it --rm mpc`

In another terminal `Mycelium/crypto/code/scale_mamba_version/`:
- use `docker ps` to get the id of the docker container running
- `docker cp ../../Cert-Store/ id:/root/SCALE-MAMBA/`
- `docker cp config/decrypt.sh id:/root/SCALE-MAMBA/Data/`
- `docker cp inputs/decrypt_input.txt id:/root/`
Note: decrypt_input.txt assumes polynomial degree = 2^15. Generate a new decrypt_input.txt if the degree is different

in the docker container:
- `cd ~/SCALE-MAMBA/`
- `cp Auto-Test-Data/1/* Data/`
- `bash ./genCertOptions.sh N 1 | ./Setup.x` (N is the number of committee members, we tested with N=10)
- `./Setup.x` -> 2 -> 2 -> mod -> enter the max possible t (threshold value)
mod value we used for benchmarking MPC costs: 3608870760655701536654448303084521404059979435669688520664454167677047564331360806878098945169255539464747077653151390316596266506041127794233364507011499768902844417
t=6 if N=10

We first have to set up the shares of the secret key:
- `./benchmark.sh secret_keygen 0 1 2 ...N-1`, where N is the number of committee members

To benchmark MPC decryption (do this after performing the secret key gen):
- `cd Data`
- `./decrypt.sh N`, where N is the number of players
- `cd ..`
- `./benchmark.sh dec_test 0 1 2 ...N-1`, where N is the number of committee members

Output for Player i is in output_i.txt (or in Data/Playeri_out.txt)
Communication cost is in communication.txt
