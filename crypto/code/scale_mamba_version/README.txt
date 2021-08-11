Docker set up instructions:

Allocate at least 8 GB of memory for Docker

After starting the docker application:

inside Mycelium:
cd /crypto/code/scale_mamba_version/
docker build -t mpc .    (this will take a while)
docker run -it --rm mpc

In another terminal inside Mycelium:
use docker ps to get the id of the docker container running, and then
copy the following from host to docker:
docker cp crypto/Cert-Store/ id:/root/SCALE-MAMBA/
docker cp crypto/code/scale_mamba_version/config/decrypt.sh id:/root/SCALE-MAMBA/Data/
docker cp crypto/code/scale_mamba_version/config/key_gen.sh id:/root/SCALE-MAMBA/Data/

in the docker:
apt-get install vim
cd ~/SCALE-MAMBA/
cp Auto-Test-Data/1/* Data/

To set up certs for N players: (example N=10)
bash ./genCertOptions.sh N 1 | ./Setup.x

#example mod = 3608870760655701536654448303084521404059979435669688520664454167677047564331360806878098945169255539464747077653151390316596266506041127794233364507011499768902844417
Then set the mod with: ./Setup.x -> 2 -> 2 -> mod -> then enter the max possible t (threshold value)

To perform secret key gen:

In the docker:
./benchmark.sh enc_test 0 1 2 ...N-1


To benchmark MPC decryption (do this after performing the secret key gen):

copy the following from host to docker:
docker cp crypto/code/scale_mamba_version/inputs/decrypt_input.txt id:/root/
Note: decrypt_input.txt assumes polynomial degree = 2^15. Generate a new decrypt_input.txt if the params are different

In the docker:
cd Data
./decrypt.sh N, where N is the number of players
cd ..
./benchmark.sh dec_test 0 1 2 ...N-1

Output for Player i is in output_i.txt (or in Data/Playeri_out.txt)
Error message is in err_i.txt
Communication cost is in communication.txt
